# Data files

These JSON files are the structured copy of the beginner reference. Jon's dashboards should fetch them from git, not scrape the HTML.

License: [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/).

## URLs

| Use this | Base |
|---|---|
| GitHub raw, branch `main` | `https://raw.githubusercontent.com/udanax80/3d-Print-Library/main/data/` |
| GitHub Pages, after deploy | `https://udanax80.github.io/3d-Print-Library/data/` |

A file at `data/<name>.json` is `<base><name>.json`.

Dashboards on another website should use the **raw** URL. GitHub sends `Access-Control-Allow-Origin: *` on raw files. The Pages copy is the same bytes, published because `hooks/reference_data.py` adds the JSON to the MkDocs build.

`data/index.json` lists every file and a short schema note. `raw_base_url` and `pages_base_url` in that file must match `mkdocs.yml`. The build checks.

The raw and Pages URLs update when this lands on `main` and the Pages workflow runs. A pull request does not publish them.

### Files

- https://raw.githubusercontent.com/udanax80/3d-Print-Library/main/data/index.json
- https://udanax80.github.io/3d-Print-Library/data/index.json
- https://raw.githubusercontent.com/udanax80/3d-Print-Library/main/data/printers.json
- https://udanax80.github.io/3d-Print-Library/data/printers.json
- https://raw.githubusercontent.com/udanax80/3d-Print-Library/main/data/glossary.json
- https://udanax80.github.io/3d-Print-Library/data/glossary.json
- https://raw.githubusercontent.com/udanax80/3d-Print-Library/main/data/materials.json
- https://udanax80.github.io/3d-Print-Library/data/materials.json
- https://raw.githubusercontent.com/udanax80/3d-Print-Library/main/data/troubleshooting.json
- https://udanax80.github.io/3d-Print-Library/data/troubleshooting.json

## What null means

In `printers.json`, `null` means the manufacturer page did not state that value. Do not treat it as zero or as false. `best_for` and `skill_level` are this site's judgments, called out in the file's `disclaimer`.

## Add or change a record

1. Edit the JSON. Keep `schema_version` at 1 unless you change the shape and update `index.json` plus this README.
2. If you add a file, list it in `index.json` and add both URLs above.
3. Run `mkdocs build --strict`. The printer table, glossary, materials tables, and troubleshooting index are filled from these files at build time.
