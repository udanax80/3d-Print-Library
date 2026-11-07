"""Publish prints/ with the MkDocs site and fill the Recent prints page.

The catalog lives at the repository root so raw.githubusercontent.com can
serve each file. MkDocs only copies docs/ on its own, so this hook registers
those same files as site assets under prints/. Links on docs/prints/index.md
use paths like ``jollibee-barrel-man/file.3mf``; MkDocs resolves them because
each asset's src URI is ``prints/<id>/...``.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

from mkdocs.exceptions import PluginError
from mkdocs.plugins import get_plugin_logger
from mkdocs.structure.files import File

log = get_plugin_logger("prints")

MARKER = "<!-- PRINTS-GALLERY -->"
PAGE = "prints/index.md"
RAW_BRANCH = "main"
# Stay under GitHub's 100 MB hard limit. GitHub also warns around 50 MB;
# prints/README.md tells contributors to keep files well below that.
MAX_BYTES = 95 * 1024 * 1024
ID_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
NAME_RE = re.compile(r"^(?:[A-Za-z0-9._-]+/)*[A-Za-z0-9._-]+$")
HEX_RE = re.compile(r"^#[0-9A-Fa-f]{6}$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
IMAGE_EXT = {".png", ".jpg", ".jpeg", ".webp", ".gif"}

_CATALOG: dict | None = None


def _fail(message: str) -> None:
    raise PluginError(f"prints: {message}")


def _repo_root(config) -> Path:
    return Path(config.config_file_path).parent


def _yaml_scalar(text: str, key: str) -> str:
    match = re.search(rf"^{re.escape(key)}:\s*(\S+)\s*$", text, re.MULTILINE)
    if not match:
        _fail(f"mkdocs.yml is missing {key}.")
    return match.group(1).strip("'\"")


def _url_bases(config) -> tuple[str, str]:
    # Read mkdocs.yml from disk. `mkdocs serve` replaces config.site_url with
    # the local address before the build events run.
    text = Path(config.config_file_path).read_text(encoding="utf-8")
    site = _yaml_scalar(text, "site_url").rstrip("/")
    repo = _yaml_scalar(text, "repo_url").rstrip("/")
    if not repo.startswith("https://github.com/"):
        _fail("mkdocs.yml repo_url must be a GitHub repository URL.")
    pages = f"{site}/prints/"
    raw = repo.replace("https://github.com/", "https://raw.githubusercontent.com/", 1)
    raw = f"{raw}/{RAW_BRANCH}/prints/"
    return raw, pages


def _load_json(path: Path):
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        _fail(f"{path} is not valid JSON ({exc}).")
    if not isinstance(data, dict):
        _fail(f"{path} must be a JSON object.")
    return data


def _req_str(data: dict, key: str, where: str) -> str:
    value = data.get(key)
    if not isinstance(value, str) or not value.strip() or "\n" in value:
        _fail(f"{where} field {key} must be a single-line non-empty string.")
    return value


def _opt_str(data: dict, key: str, where: str) -> str | None:
    if key not in data or data[key] is None:
        return None
    return _req_str(data, key, where)


def _number(value, where: str) -> int | float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        _fail(f"{where} must be a number.")
    return value


def _rel_name(value: str, where: str) -> str:
    if not isinstance(value, str) or not NAME_RE.fullmatch(value) or ".." in value.split("/"):
        _fail(
            f"{where} must be a relative path using letters, numbers, dots, underscores, "
            "and hyphens (no spaces)."
        )
    return value


def _validate_print(data: dict, folder: Path) -> None:
    where = str(folder / "print.json")
    if data.get("schema_version") != 1:
        _fail(f"{where} schema_version must be 1.")
    pid = _req_str(data, "id", where)
    if pid != folder.name or not ID_RE.fullmatch(pid):
        _fail(f"{where} id must be the folder name in lowercase kebab-case.")
    _req_str(data, "title", where)
    _req_str(data, "description", where)
    note = _opt_str(data, "note", where)
    if note is not None and ("]" in note or "<" in note):
        _fail(f"{where} note cannot contain ']' or '<'.")
    added = _opt_str(data, "added", where)
    if added is not None and not DATE_RE.fullmatch(added):
        _fail(f"{where} added must be YYYY-MM-DD.")
    _opt_str(data, "author", where)
    _req_str(data, "printer", where)
    _opt_str(data, "slicer", where)

    material = data.get("material")
    if not isinstance(material, dict):
        _fail(f"{where} material must be an object with type and colors.")
    _req_str(material, "type", f"{where} material")
    colors = material.get("colors")
    if not isinstance(colors, list) or not colors:
        _fail(f"{where} material.colors must be a non-empty list.")
    for i, color in enumerate(colors):
        if not isinstance(color, dict):
            _fail(f"{where} material.colors[{i}] must be an object.")
        _req_str(color, "name", f"{where} material.colors[{i}]")
        hex_color = _req_str(color, "hex", f"{where} material.colors[{i}]")
        if not HEX_RE.fullmatch(hex_color):
            _fail(f"{where} material.colors[{i}].hex must be #RRGGBB.")

    heights = data.get("layer_height_mm")
    if not isinstance(heights, dict) or not heights:
        _fail(f"{where} layer_height_mm must be an object of part name to millimeters.")
    for part, height in heights.items():
        if not isinstance(part, str) or not part.strip() or "|" in part or "\n" in part:
            _fail(f"{where} layer_height_mm keys must be short part names.")
        number = _number(height, f"{where} layer_height_mm.{part}")
        if not 0 < number <= 1.2:
            _fail(f"{where} layer_height_mm.{part} must be between 0 and 1.2 mm.")

    scale = _number(data.get("scale_percent"), f"{where} scale_percent")
    if not 0 < scale <= 1000:
        _fail(f"{where} scale_percent must be greater than 0.")
    height = _number(data.get("body_height_mm"), f"{where} body_height_mm")
    if not 0 < height < 10000:
        _fail(f"{where} body_height_mm must be the approximate height in millimeters.")

    _req_str(data, "license", where)
    license_url = _opt_str(data, "license_url", where)
    if license_url is not None and not license_url.startswith("https://"):
        _fail(f"{where} license_url must be an https URL.")

    seen: set[str] = set()
    files = data.get("files")
    if not isinstance(files, list) or not files:
        _fail(f"{where} files must list at least one print file.")
    for i, item in enumerate(files):
        if not isinstance(item, dict):
            _fail(f"{where} files[{i}] must be an object.")
        name = _rel_name(item.get("filename"), f"{where} files[{i}].filename")
        _req_str(item, "description", f"{where} files[{i}]")
        path = folder / name
        if not path.is_file():
            _fail(f"{where} files[{i}] points at missing file {name}.")
        actual = path.stat().st_size
        if actual > MAX_BYTES:
            _fail(f"{name} is {actual} bytes, over the {MAX_BYTES} byte GitHub limit.")
        if "bytes" in item:
            claimed = item["bytes"]
            if isinstance(claimed, bool) or not isinstance(claimed, int) or claimed != actual:
                _fail(f"{where} files[{i}].bytes is {claimed}; the file is {actual} bytes.")
        if name in seen:
            _fail(f"{where} lists {name} more than once.")
        seen.add(name)

    images = data.get("images")
    if not isinstance(images, list):
        _fail(f"{where} images must be a list (use [] if there are none).")
    for i, item in enumerate(images):
        if not isinstance(item, dict):
            _fail(f"{where} images[{i}] must be an object.")
        name = _rel_name(item.get("filename"), f"{where} images[{i}].filename")
        if Path(name).suffix.lower() not in IMAGE_EXT:
            _fail(f"{where} images[{i}] must be a png, jpg, webp, or gif.")
        alt = _req_str(item, "alt", f"{where} images[{i}]")
        if "]" in alt:
            _fail(f"{where} images[{i}].alt cannot contain ']'.")
        caption = _opt_str(item, "caption", f"{where} images[{i}]")
        if caption is not None and "]" in caption:
            _fail(f"{where} images[{i}].caption cannot contain ']'.")
        path = folder / name
        if not path.is_file():
            _fail(f"{where} images[{i}] points at missing file {name}.")
        if path.stat().st_size > MAX_BYTES:
            _fail(f"{name} is over the {MAX_BYTES} byte GitHub limit.")
        if name in seen:
            _fail(f"{where} lists {name} more than once.")
        seen.add(name)


def load_catalog(config) -> dict:
    root = _repo_root(config) / "prints"
    index_path = root / "index.json"
    if not index_path.is_file():
        _fail("prints/index.json is missing.")
    raw_base, pages_base = _url_bases(config)
    index = _load_json(index_path)
    if index.get("schema_version") != 1:
        _fail("prints/index.json schema_version must be 1.")
    if index.get("raw_base_url") != raw_base or index.get("pages_base_url") != pages_base:
        _fail(
            "prints/index.json raw_base_url and pages_base_url must match mkdocs.yml "
            f"({raw_base} and {pages_base})."
        )
    entries = index.get("prints")
    if not isinstance(entries, list):
        _fail("prints/index.json prints must be a list.")

    discovered = {path.parent.name for path in root.glob("*/print.json")}
    listed_ids: list[str] = []
    prints = []
    for i, entry in enumerate(entries):
        where = f"prints/index.json prints[{i}]"
        if not isinstance(entry, dict):
            _fail(f"{where} must be an object.")
        pid = _req_str(entry, "id", where)
        if not ID_RE.fullmatch(pid):
            _fail(f"{where} id must be lowercase kebab-case.")
        if entry.get("dir") != pid or entry.get("print_json") != f"{pid}/print.json":
            _fail(f"{where} dir and print_json must point at {pid}/print.json.")
        folder = root / pid
        print_path = folder / "print.json"
        if not print_path.is_file():
            _fail(f"{where} has no {pid}/print.json.")
        data = _load_json(print_path)
        _validate_print(data, folder)
        if entry.get("title") != data["title"]:
            _fail(f"{where} title must match {pid}/print.json.")
        summary = _req_str(entry, "description", where)
        added = _opt_str(entry, "added", where)
        if added is not None and not DATE_RE.fullmatch(added):
            _fail(f"{where} added must be YYYY-MM-DD.")
        thumb = _opt_str(entry, "thumbnail", where)
        if data["images"] and not thumb:
            _fail(f"{where} thumbnail is required when the print has images.")
        if thumb is not None:
            _rel_name(thumb, f"{where} thumbnail")
            if not (root / thumb).is_file():
                _fail(f"{where} thumbnail does not exist.")
            if not any(thumb == f"{pid}/{image['filename']}" for image in data["images"]):
                _fail(f"{where} thumbnail must be one of the print images.")
        listed_ids.append(pid)
        prints.append({"entry": entry, "data": data, "summary": summary})

    if len(listed_ids) != len(set(listed_ids)):
        _fail("prints/index.json lists the same id more than once.")
    missing = discovered - set(listed_ids)
    extra = set(listed_ids) - discovered
    if missing or extra:
        _fail(
            "prints/index.json must list every prints/<id>/print.json folder. "
            f"Missing {sorted(missing) or 'none'}; unknown {sorted(extra) or 'none'}."
        )

    readme = (root / "README.md").read_text(encoding="utf-8") if (root / "README.md").is_file() else ""
    if raw_base not in readme or pages_base not in readme:
        _fail("prints/README.md must document the raw and Pages base URLs.")
    page = _repo_root(config) / "docs" / "prints" / "index.md"
    page_text = page.read_text(encoding="utf-8") if page.is_file() else ""
    if raw_base not in page_text or pages_base not in page_text:
        _fail("docs/prints/index.md must document the raw and Pages base URLs.")
    for rel in _catalog_rels(prints):
        raw_url = raw_base + rel
        pages_url = pages_base + rel
        if raw_url not in readme or pages_url not in readme:
            _fail(f"prints/README.md must list both public URLs for {rel}.")

    return {
        "raw_base": raw_base,
        "pages_base": pages_base,
        "prints": prints,
        "root": root,
    }


def _catalog_rels(prints: list[dict]) -> list[str]:
    rels = ["index.json"]
    for item in prints:
        pid = item["data"]["id"]
        rels.append(f"{pid}/print.json")
        for group in ("files", "images"):
            for entry in item["data"][group]:
                rels.append(f"{pid}/{entry['filename']}")
    return rels


def _human_size(num_bytes: int) -> str:
    return f"{num_bytes / (1024 * 1024):.1f} MB"


def _cell(value: str) -> str:
    return " ".join(value.split()).replace("|", "\\|")


def _render_print(item: dict, raw_base: str, pages_base: str) -> str:
    data = item["data"]
    pid = data["id"]
    lines = [f"## {_cell(data['title'])} {{ #{pid} }}", "", f"<p>{_html(data['description'])}</p>", ""]
    if data.get("note"):
        lines.extend(["!!! note", f"    {_cell(data['note'])}", ""])

    lines.extend(['<div class="grid cards print-shots" markdown>', ""])
    for image in data["images"]:
        alt = image["alt"]
        src = f"{pid}/{image['filename']}"
        lines.append(f"-   ![{alt}]({src})")
        lines.append("")
        if image.get("caption"):
            lines.append(f"    {_cell(image['caption'])}")
            lines.append("")
    lines.extend(["</div>", ""])

    rows = [
        ("Printer", _html(data["printer"])),
        ("Material", _html(_material_label(data))),
        ("Layer height", _html(_height_label(data["layer_height_mm"]))),
        ("Scale", f"{_trim(data['scale_percent'])}%"),
        ("Body height", f"about {_trim(data['body_height_mm'])} mm"),
        ("License", _license_html(data)),
    ]
    if data.get("slicer"):
        rows.insert(1, ("Slicer", _html(data["slicer"])))
    if data.get("author"):
        rows.append(("Author", _html(data["author"])))
    if data.get("added"):
        rows.append(("Added", _html(data["added"])))
    lines.append('<table class="print-meta"><tbody>')
    for label, value in rows:
        lines.append(f"<tr><th>{_html(label)}</th><td>{value}</td></tr>")
    lines.append("</tbody></table>")
    lines.append("")

    if data["material"]["colors"]:
        lines.append("**Colors**")
        lines.append("")
        lines.append('<div class="print-swatches">')
        for color in data["material"]["colors"]:
            name = _html(color["name"][:1].upper() + color["name"][1:])
            hex_color = color["hex"]
            lines.append(
                '<span class="print-swatch-item">'
                f'<span class="print-swatch" style="background:{hex_color}"></span> '
                f"{name} <code>{hex_color}</code></span>"
            )
        lines.append("</div>")
        lines.append("")

    lines.extend(['<div class="print-actions" markdown>', ""])
    for item_file in data["files"]:
        name = item_file["filename"]
        size = _human_size(item_file.get("bytes") or ( _repo_file_size(pid, name)))
        label = _cell(item_file["description"])
        href = f"{pid}/{name}"
        lines.append(
            f'[{label} ({size}) :material-download:]({href})'
            f'{{ .md-button .md-button--primary download="{Path(name).name}" }}'
        )
        lines.append("")
    lines.append(f'[View print.json]({pid}/print.json){{ .md-button }}')
    lines.extend(["", "</div>", ""])

    lines.extend(['??? info "Direct URLs"', ""])
    lines.append("    Pages links are served with this site. Raw links read the file from git branch `main`.")
    lines.append("")
    url_items = [("print.json", f"{pid}/print.json")]
    for group in ("files", "images"):
        for entry in data[group]:
            url_items.append((entry["filename"], f"{pid}/{entry['filename']}"))
    for label, rel in url_items:
        lines.append(f"    **{label}**")
        lines.append("")
        for kind, base in (("Pages", pages_base), ("raw", raw_base)):
            url = base + rel
            lines.append(f"    - [{url}]({url}) ({kind})")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def _repo_file_size(pid: str, name: str) -> int:
    # Used only if a file omits bytes. The catalog root is filled before render.
    assert _CATALOG is not None
    return (_CATALOG["root"] / pid / name).stat().st_size


def _html(value: str) -> str:
    return (
        value.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def _trim(value: int | float) -> str:
    if isinstance(value, float) and value.is_integer():
        return str(int(value))
    return str(value)


def _material_label(data: dict) -> str:
    material = data["material"]
    count = len(material["colors"])
    noun = "color" if count == 1 else "colors"
    return f"{_cell(material['type'])} · {count} {noun}"


def _height_label(heights: dict) -> str:
    return " · ".join(f"{_trim(height)} mm {_cell(part)}" for part, height in heights.items())


def _license_html(data: dict) -> str:
    name = _html(data["license"])
    url = data.get("license_url")
    if url:
        return f'<a href="{_html(url)}">{name}</a>'
    return name


def _render_gallery() -> str:
    assert _CATALOG is not None
    if not _CATALOG["prints"]:
        return "No prints are listed in `prints/index.json` yet.\n"
    parts = [
        _render_print(item, _CATALOG["raw_base"], _CATALOG["pages_base"])
        for item in _CATALOG["prints"]
    ]
    return "\n---\n\n".join(parts)


def _publishable(root: Path) -> list[Path]:
    files = []
    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        rel = path.relative_to(root).as_posix()
        if rel == "README.md" or rel.endswith(".md") or path.name.startswith("."):
            continue
        files.append(path)
    return files


def on_pre_build(config, **kwargs):
    global _CATALOG
    _CATALOG = load_catalog(config)


def on_files(files, config, **kwargs):
    if _CATALOG is None:
        _fail("print catalog was not loaded.")
    root = _CATALOG["root"]
    for path in _publishable(root):
        size = path.stat().st_size
        if size > MAX_BYTES:
            _fail(f"{path.name} is {size} bytes, over the {MAX_BYTES} byte GitHub limit.")
        src_uri = path.relative_to(root.parent).as_posix()
        if files.get_file_from_path(src_uri) is None:
            files.append(File.generated(config, src_uri, abs_src_path=str(path.resolve())))
    log.info(f"Publishing {len(_publishable(root))} files from prints/")
    return files


def on_page_markdown(markdown, page, config, files, **kwargs):
    if page.file.src_uri != PAGE:
        return markdown
    if markdown.count(MARKER) != 1:
        _fail(f"docs/{PAGE} must contain {MARKER} exactly once.")
    return markdown.replace(MARKER, _render_gallery())


def on_post_build(config, **kwargs):
    if _CATALOG is None:
        _fail("print catalog was not loaded.")
    site = Path(config.site_dir)
    missing = [
        rel
        for rel in _catalog_rels(_CATALOG["prints"])
        if not (site / "prints" / rel).is_file()
    ]
    if missing:
        _fail("these print files were not copied into the site: " + ", ".join(missing))


def on_serve(server, config, builder, **kwargs):
    server.watch(str(_repo_root(config) / "prints"), builder)
    return server
