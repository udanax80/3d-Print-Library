# 3d-Print-Library

Jon's Print Lab: a shared 3D printing reference, built with [MkDocs Material](https://squidfunk.github.io/mkdocs-material/) and organized by print lifecycle:
**Choose → Fleet → Materials → Prepare → Fix → Design → Finish → Maintain → Safety → Contribute.**

Written content and the print files in [`prints/`](prints/README.md) are licensed under [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/). See [LICENSE](LICENSE).

## Print files

Ready-to-print projects live in [`prints/`](prints/README.md), one folder per print, starting with `prints/jollibee-barrel-man/`. The site shows them on **Recent prints**. A dashboard can fetch [`prints/index.json`](prints/index.json).

Each file is committed in git (these `.3mf` projects are about 3 MB, under GitHub's limits) and copied into the GitHub Pages site on deploy:

- Raw, branch `main`: `https://raw.githubusercontent.com/udanax80/3d-Print-Library/main/prints/`
- Pages, after deploy: `https://udanax80.github.io/3d-Print-Library/prints/`

The exact URL for every file, and the `print.json` schema, are in [`prints/README.md`](prints/README.md).

Structured catalogs for dashboards live in [`data/`](data/README.md). Fetch [`data/index.json`](https://raw.githubusercontent.com/udanax80/3d-Print-Library/main/data/index.json) from git `main`. The same files are copied into the GitHub Pages site at `https://udanax80.github.io/3d-Print-Library/data/`.

## Run locally
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
mkdocs serve   # http://127.0.0.1:8000
mkdocs build --strict   # outputs ./site
```

## Publish on GitHub Pages
1. `mkdocs.yml` is set for this repo: `site_url` `https://udanax80.github.io/3d-Print-Library/`, `repo_url` `https://github.com/udanax80/3d-Print-Library`, `repo_name` `udanax80/3d-Print-Library`, and `edit_uri` `edit/main/docs/`.
2. The workflow `.github/workflows/deploy.yml` builds the site and pushes it to the `gh-pages` branch on every push to `main` (`mkdocs gh-deploy --force`). It needs `permissions: contents: write`.
3. After the workflow runs, set **Settings → Pages → Source: Deploy from a branch → `gh-pages` / root**.
4. PRs are build-checked by `.github/workflows/check.yml`.

## Before going public
- [ ] Get permission from AD3D (@ad3duae) for the summarized guides, or rewrite from primary sources (see `docs/contribute/credits.md`)
- [ ] Verify the "AMS Pro" naming (likely AMS 2 Pro) and the open questions on the Fleet page
- [x] Content license is [CC BY-NC-SA 4.0](LICENSE)
- [ ] Replace placeholder failure images in `docs/assets/img/` with real photos

See `docs/contribute/index.md` for how friends can contribute.
