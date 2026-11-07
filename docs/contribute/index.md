---
title: Contribute
tags:
  - Contributing
---

# Contribute

This site is a Git repo. Every page is a Markdown file in `docs/`. Friends can suggest fixes the same way open-source docs work, through a **pull request (PR)**.

## The quick way (no install)

1. Open the page on the site and click the **✏️ edit** icon at the top right.
2. GitHub opens the Markdown file. Make your change and describe it.
3. Choose **"Create a new branch and start a pull request"**.
4. I'll review and merge. The site rebuilds automatically through GitHub Actions.

New to PRs? See [GitHub Docs: Creating a pull request](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/creating-a-pull-request).

## The local way

```bash
git clone https://github.com/udanax80/3d-Print-Library.git
cd 3d-Print-Library
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
mkdocs serve          # live preview at http://127.0.0.1:8000
```

## What makes a good contribution

- **Cite a source** for every number (manufacturer wiki, data sheet, Prusa KB, or "my test, printer X, date").
- **Label ranges as starting points.** Don't present your printer's tuned value as universal.
- Add **photos** of failures and fixes to `docs/assets/img/` (JPG/WebP, ≤ 300 KB, your own photos only).
- Add **tags** in the page front matter (material, printer, problem type) so search and the [tag index](../tags.md) pick it up.
- One topic per PR is easiest to review.
- Use the [page template](page-template.md) for new pages.

## Adding a printer to the fleet table
Add a row to `docs/fleet/index.md` with a **manufacturer spec link and the date you checked it** in the *Source / last checked* column. Mark anything unverified as **not verified**.

## Adding a print

Print-ready files do not go in `docs/`. Add a folder under [`prints/`](https://github.com/udanax80/3d-Print-Library/tree/main/prints) with a `print.json`, the project files, and preview images, then list it in `prints/index.json`. The folder layout and the schema are in [`prints/README.md`](https://github.com/udanax80/3d-Print-Library/blob/main/prints/README.md). The [Recent prints](../prints/index.md) page builds its cards from those JSON files.

## Structured data

`data/*.json` is the catalog other tools fetch. The schema notes are in [`data/README.md`](https://github.com/udanax80/3d-Print-Library/blob/main/data/README.md). Change the JSON, not a copied table: the printer comparison, glossary, materials tables, and troubleshooting index are filled in at build time.

See also: [Credits & licensing](credits.md).
