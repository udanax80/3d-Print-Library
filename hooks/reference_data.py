"""Publish data/*.json with the site and fill the pages that mirror it.

Dashboards fetch the JSON from raw.githubusercontent.com. The same files are
registered here so GitHub Pages serves a copy. Printer, glossary, material,
and troubleshooting tables are rendered from the JSON so the page cannot drift.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

from mkdocs.exceptions import PluginError
from mkdocs.plugins import get_plugin_logger
from mkdocs.structure.files import File

log = get_plugin_logger("reference-data")

RAW_BRANCH = "main"
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
MARKERS = {
    "buy/printers.md": "<!-- PRINTER-TABLE -->",
    "glossary.md": "<!-- GLOSSARY -->",
    "materials/beginner.md": "<!-- MATERIALS-TABLES -->",
    "fix/index.md": "<!-- TROUBLE-INDEX -->",
}

_DATA: dict | None = None


def _fail(message: str) -> None:
    raise PluginError(f"data: {message}")


def _repo(config) -> Path:
    return Path(config.config_file_path).parent


def _yaml_scalar(text: str, key: str) -> str:
    match = re.search(rf"^{re.escape(key)}:\s*(\S+)\s*$", text, re.MULTILINE)
    if not match:
        _fail(f"mkdocs.yml is missing {key}.")
    return match.group(1).strip("'\"")


def _bases(config) -> tuple[str, str]:
    # mkdocs serve rewrites config.site_url before build events. Read the file.
    text = (_repo(config) / "mkdocs.yml").read_text(encoding="utf-8")
    site = _yaml_scalar(text, "site_url").rstrip("/")
    repo = _yaml_scalar(text, "repo_url").rstrip("/")
    if not repo.startswith("https://github.com/"):
        _fail("mkdocs.yml repo_url must be a GitHub repository URL.")
    raw = repo.replace("https://github.com/", "https://raw.githubusercontent.com/", 1)
    return f"{raw}/{RAW_BRANCH}/data/", f"{site}/data/"


def _load(path: Path):
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        _fail(f"{path.name} is not valid JSON ({exc}).")
    if not isinstance(data, dict):
        _fail(f"{path.name} must be a JSON object.")
    return data


def _html(value: str) -> str:
    return (
        value.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def _num(value, where: str):
    if value is None:
        return None
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        _fail(f"{where} must be a number or null.")
    return value


def _validate(root: Path, raw_base: str, pages_base: str) -> dict:
    index = _load(root / "index.json")
    if index.get("schema_version") != 1:
        _fail("index.json schema_version must be 1.")
    if index.get("raw_base_url") != raw_base or index.get("pages_base_url") != pages_base:
        _fail(f"index.json base URLs must be {raw_base} and {pages_base}.")
    files = index.get("files")
    if not isinstance(files, list) or not files:
        _fail("index.json files must be a non-empty list.")
    listed = []
    for item in files:
        path = item.get("path")
        if not isinstance(path, str) or not path.endswith(".json"):
            _fail("each index files[] entry needs a .json path.")
        for key in ("title", "description", "schema_notes"):
            if not isinstance(item.get(key), str) or not item[key].strip():
                _fail(f"index.json {path} is missing {key}.")
        listed.append(path)
        if path != "index.json" and not (root / path).is_file():
            _fail(f"index.json lists {path}, which is not in data/.")
    on_disk = sorted(p.name for p in root.glob("*.json"))
    if sorted(listed) != on_disk:
        _fail(f"index.json files must match data/*.json. Listed {sorted(listed)}, disk {on_disk}.")
    readme = (root / "README.md").read_text(encoding="utf-8")
    for name in on_disk:
        if raw_base + name not in readme or pages_base + name not in readme:
            _fail(f"data/README.md must list the raw and Pages URL for {name}.")

    printers = _load(root / "printers.json")
    glossary = _load(root / "glossary.json")
    materials = _load(root / "materials.json")
    trouble = _load(root / "troubleshooting.json")
    _validate_printers(printers)
    _validate_glossary(glossary)
    _validate_materials(materials)
    _validate_trouble(trouble, _repo_from_data(root))
    return {
        "root": root,
        "raw_base": raw_base,
        "pages_base": pages_base,
        "printers": printers,
        "glossary": glossary,
        "materials": materials,
        "trouble": trouble,
    }


def _repo_from_data(data_dir: Path) -> Path:
    return data_dir.parent


def _validate_printers(data: dict) -> None:
    if data.get("schema_version") != 1:
        _fail("printers.json schema_version must be 1.")
    rows = data.get("printers")
    if not isinstance(rows, list) or len(rows) < 15:
        _fail("printers.json needs the researched printer list.")
    ids = [row.get("id") for row in rows]
    if len(ids) != len(set(ids)):
        _fail("printer ids must be unique.")
    picks = data.get("picks") or {}
    for key in ("beginners", "multicolor", "engineering", "big_prints"):
        chosen = picks.get(key)
        if not isinstance(chosen, list) or not chosen:
            _fail(f"printers.json picks.{key} must be a non-empty list of ids.")
        for pid in chosen:
            if pid not in ids:
                _fail(f"picks.{key} references unknown id {pid}.")
    for row in rows:
        pid = row.get("id")
        for key in ("brand", "model", "best_for", "skill_level", "last_checked"):
            if not isinstance(row.get(key), str) or not row[key].strip():
                _fail(f"{pid} is missing {key}.")
        if row["skill_level"] not in {"beginner", "intermediate", "advanced"}:
            _fail(f"{pid} skill_level must be beginner, intermediate, or advanced.")
        if not DATE_RE.fullmatch(row["last_checked"]):
            _fail(f"{pid} last_checked must be YYYY-MM-DD.")
        _num(row.get("price_usd"), f"{pid} price_usd")
        _num(row.get("max_nozzle_c"), f"{pid} max_nozzle_c")
        _num(row.get("max_bed_c"), f"{pid} max_bed_c")
        _num(row.get("chamber_max_c"), f"{pid} chamber_max_c")
        _num(row.get("top_speed_mm_s"), f"{pid} top_speed_mm_s")
        for flag in ("enclosed", "heated_chamber"):
            if row.get(flag) not in (True, False, None):
                _fail(f"{pid} {flag} must be true, false, or null.")
        volume = row.get("build_volume_mm")
        if volume is not None:
            if not isinstance(volume, dict):
                _fail(f"{pid} build_volume_mm must be an object or null.")
            for axis in ("x", "y", "z"):
                _num(volume.get(axis), f"{pid} build_volume_mm.{axis}")
        multi = row.get("multi_material")
        if not isinstance(multi, dict):
            _fail(f"{pid} multi_material must be an object.")
        _num(multi.get("slots"), f"{pid} slots")
        urls = row.get("source_urls")
        if not isinstance(urls, list) or not urls or not all(isinstance(u, str) and u.startswith("https://") for u in urls):
            _fail(f"{pid} needs at least one https source_urls entry.")


def _validate_glossary(data: dict) -> None:
    terms = data.get("terms")
    if not isinstance(terms, list) or len(terms) < 60:
        _fail(f"glossary.json needs at least 60 terms, found {0 if not isinstance(terms, list) else len(terms)}.")
    seen = set()
    for term in terms:
        tid = term.get("id")
        if tid in seen:
            _fail(f"duplicate glossary id {tid}.")
        seen.add(tid)
        if not term.get("term") or not term.get("definition"):
            _fail(f"glossary term {tid} needs term and definition.")


def _validate_materials(data: dict) -> None:
    rows = data.get("materials")
    if not isinstance(rows, list):
        _fail("materials.json materials must be a list.")
    ids = {row.get("id") for row in rows}
    for needed in ("pla", "petg", "tpu", "abs", "asa", "pa", "pc"):
        if needed not in ids:
            _fail(f"materials.json is missing {needed}.")
    for row in rows:
        if row.get("level") not in {"beginner", "advanced"}:
            _fail(f"{row.get('id')} level must be beginner or advanced.")
        if row.get("enclosure") not in {"no", "optional", "yes"}:
            _fail(f"{row.get('id')} enclosure must be no, optional, or yes.")
        for key in ("nozzle_c", "bed_c", "dry_c"):
            span = row.get(key)
            if not isinstance(span, dict) or span.get("min") is None or span.get("max") is None:
                _fail(f"{row.get('id')} {key} needs min and max.")


def _validate_trouble(data: dict, repo: Path) -> None:
    rows = data.get("defects")
    if not isinstance(rows, list) or len(rows) < 8:
        _fail("troubleshooting.json needs a defect list.")
    page = (repo / "docs" / "fix" / "index.md").read_text(encoding="utf-8")
    for row in rows:
        if row.get("difficulty") not in {"easy", "medium", "hard"}:
            _fail(f"{row.get('id')} difficulty must be easy, medium, or hard.")
        if not row.get("symptom") or not row.get("causes"):
            _fail(f"{row.get('id')} needs a symptom and causes.")
        if row["title"] not in page:
            _fail(f"docs/fix/index.md must mention {row['title']}.")
        image = repo / row["image"]
        if not image.is_file():
            _fail(f"{row['id']} image does not exist: {row['image']}.")


def _fmt_num(value, suffix: str = "") -> str:
    if value is None:
        return "—"
    number = int(value) if isinstance(value, float) and value.is_integer() else value
    return f"{number}{suffix}"


def _money(row: dict) -> str:
    price = row.get("price_usd")
    if price is None:
        return "—"
    if isinstance(price, float) and not price.is_integer():
        return f"${price:,.2f}"
    return f"${int(price):,}"


def _volume(row: dict) -> str:
    # Long notes stay in the details block. The cell stays one line.
    volume = row.get("build_volume_mm")
    if not volume:
        return "Varies" if row.get("build_volume_note") else "—"
    return f"{_fmt_num(volume.get('x'))} × {_fmt_num(volume.get('y'))} × {_fmt_num(volume.get('z'))}"


def _yes_no(value) -> str:
    if value is True:
        return "Yes"
    if value is False:
        return "No"
    return "—"


def _chamber(row: dict) -> str:
    if row.get("chamber_max_c") is not None:
        return f"{_fmt_num(row['chamber_max_c'])} °C"
    if row.get("heated_chamber") is True:
        return "Heated, max not stated"
    if row.get("heated_chamber") is False:
        return "No"
    return "—"


def _multi(row: dict) -> str:
    multi = row.get("multi_material") or {}
    system = multi.get("system")
    if not system and multi.get("slots") is None:
        return "—"
    bits = []
    if system:
        bits.append(_html(system))
    if multi.get("slots") is not None:
        slots = _fmt_num(multi["slots"])
        if multi.get("max_slots") not in (None, multi.get("slots")):
            slots += f"–{_fmt_num(multi['max_slots'])}"
        bits.append(f"{slots} slots")
    return ", ".join(bits) if bits else "—"


def _sort(value) -> str:
    if value is None:
        return "~"
    return str(value)


def _printer_table(data: dict) -> str:
    by_id = {row["id"]: row for row in data["printers"]}
    labels = {
        "beginners": "Best for beginners",
        "multicolor": "Best for multicolor",
        "engineering": "Best for engineering filament",
        "big_prints": "Best for big prints",
    }
    lines = [
        "These four short lists are judgments from the specs below, not a lab test and not the manufacturer's ranking.",
        "",
        '<div class="grid cards" markdown>',
        "",
    ]
    blurbs = {
        "beginners": "Open machines with a low from-price, or a multicolor printer that already includes the color unit.",
        "multicolor": "A built-in color system, a filament changer, or several toolheads.",
        "engineering": "A published heated chamber, or a high nozzle temperature on an enclosed machine.",
        "big_prints": "The largest build volumes in this table.",
    }
    for key, title in labels.items():
        names = ", ".join(f"{by_id[pid]['brand']} {by_id[pid]['model']}" for pid in data["picks"][key])
        lines.extend([f"-   **{title}**", "", f"    {names}. {blurbs[key]}", ""])
    lines.extend(["</div>", "", "Dashes mean the source page did not state that value. Prices are the from-price or sale price in the note, in USD, and they move.", ""])
    lines.append('<div class="print-table-wrap">')
    lines.append('<table class="sortable" id="printer-compare">')
    lines.append("<thead><tr>")
    for label in (
        "Printer",
        "Price",
        "Volume (mm)",
        "Enclosed",
        "Chamber",
        "Nozzle",
        "Multi-material",
        "Top speed",
        "Best for",
        "Skill",
        "Checked",
    ):
        lines.append(f"<th>{label}</th>")
    lines.append("</tr></thead><tbody>")
    for row in data["printers"]:
        source = row["source_urls"][0]
        name = f'<a href="{_html(source)}">{_html(row["brand"])} {_html(row["model"])}</a>'
        speed = _fmt_num(row.get("top_speed_mm_s"), " mm/s")
        lines.append("<tr>")
        cells = [
            (_sort(row["model"]), name),
            (_sort(row.get("price_usd")), _money(row)),
            (_sort((row.get("build_volume_mm") or {}).get("x")), _volume(row)),
            (_sort(row.get("enclosed")), _yes_no(row.get("enclosed"))),
            (_sort(row.get("chamber_max_c") if row.get("chamber_max_c") is not None else row.get("heated_chamber")), _chamber(row)),
            (_sort(row.get("max_nozzle_c")), _fmt_num(row.get("max_nozzle_c"), " °C")),
            (_sort((row.get("multi_material") or {}).get("slots")), _multi(row)),
            (_sort(row.get("top_speed_mm_s")), speed),
            (_sort(row["best_for"]), _html(row["best_for"])),
            (_sort(row["skill_level"]), _html(row["skill_level"])),
            (_sort(row["last_checked"]), _html(row["last_checked"])),
        ]
        for sort_key, html in cells:
            lines.append(f'<td data-sort="{_html(sort_key)}">{html}</td>')
        lines.append("</tr>")
    lines.append("</tbody></table></div>")
    lines.append("")
    lines.append("Click a column heading to sort. The printer name links to the spec source.")
    lines.append("")
    lines.append("??? note \"Price notes and conflicts\"")
    lines.append("")
    for row in data["printers"]:
        bits = [f"**{row['brand']} {row['model']}.**"]
        if row.get("price_note"):
            bits.append(row["price_note"])
        if row.get("notes"):
            bits.append(row["notes"])
        if row.get("speed_note"):
            bits.append(row["speed_note"])
        lines.append("    " + " ".join(bits))
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def _glossary(data: dict) -> str:
    terms = sorted(data["terms"], key=lambda item: item["term"].lower())
    lines = []
    for term in terms:
        lines.append(f"### {term['term']}")
        lines.append("")
        lines.append(term["definition"])
        lines.append("")
    return "\n".join(lines)


def _materials(data: dict) -> str:
    def table(level: str) -> str:
        rows = [row for row in data["materials"] if row["level"] == level]
        lines = [
            "| Material | Nozzle °C | Bed °C | Enclosure | Dry | Good for | Watch out |",
            "|---|---|---|---|---|---|---|",
        ]
        for row in rows:
            nozzle = f"{row['nozzle_c']['min']}–{row['nozzle_c']['max']}"
            bed = f"{row['bed_c']['min']}–{row['bed_c']['max']}"
            dry = f"{row['dry_c']['min']}–{row['dry_c']['max']} °C, {row['dry_hours']} h"
            lines.append(
                f"| **{row['name']}** | {nozzle} | {bed} | {row['enclosure']} | {dry} | {row['good_for']} | {row['watch_outs']} |"
            )
        # Tab bodies have to be indented or pymdownx treats each title as an empty tab.
        return "\n".join("    " + line for line in lines)

    return "\n".join(
        [
            '=== "Start here"',
            "",
            table("beginner"),
            "",
            '=== "Later"',
            "",
            table("advanced"),
            "",
        ]
    )


def _trouble(data: dict) -> str:
    lines = [
        "| Defect | What you see | Difficulty | Start here |",
        "|---|---|---|---|",
    ]
    for row in data["defects"]:
        anchor = row["page"].split("#", 1)[-1]
        lines.append(
            f"| **[{row['title']}](#{anchor})** | {row['symptom']} | {row['difficulty']} | {row['causes'][0]['fix']} |"
        )
    return "\n".join(lines) + "\n"


def on_pre_build(config, **kwargs):
    global _DATA
    root = _repo(config) / "data"
    raw_base, pages_base = _bases(config)
    _DATA = _validate(root, raw_base, pages_base)


def on_files(files, config, **kwargs):
    if _DATA is None:
        _fail("reference data was not loaded.")
    root = _DATA["root"]
    for path in sorted(root.glob("*.json")):
        src_uri = path.relative_to(root.parent).as_posix()
        if files.get_file_from_path(src_uri) is None:
            files.append(File.generated(config, src_uri, abs_src_path=str(path.resolve())))
    log.info(f"Publishing {len(list(root.glob('*.json')))} JSON files from data/")
    return files


def on_page_markdown(markdown, page, config, files, **kwargs):
    marker = MARKERS.get(page.file.src_uri)
    if not marker:
        return markdown
    if _DATA is None:
        _fail("reference data was not loaded.")
    if markdown.count(marker) != 1:
        _fail(f"docs/{page.file.src_uri} must contain {marker} once.")
    if page.file.src_uri == "buy/printers.md":
        block = _printer_table(_DATA["printers"])
    elif page.file.src_uri == "glossary.md":
        block = _glossary(_DATA["glossary"])
    elif page.file.src_uri == "materials/beginner.md":
        block = _materials(_DATA["materials"])
    else:
        block = _trouble(_DATA["trouble"])
    return markdown.replace(marker, block)


def on_post_build(config, **kwargs):
    if _DATA is None:
        _fail("reference data was not loaded.")
    site = Path(config.site_dir) / "data"
    missing = [name for name in ("index.json", "printers.json", "glossary.json", "materials.json", "troubleshooting.json") if not (site / name).is_file()]
    if missing:
        _fail("JSON files missing from the built site: " + ", ".join(missing))
