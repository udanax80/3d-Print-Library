# Print files

Ready-to-print projects live here, one folder per print. The site gallery is the **Recent prints** page. An external dashboard should start at [`index.json`](index.json), then open each print's `print.json`.

Written notes on the site and these project files are [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/) unless a print's `print.json` names a different license. Credit Jon D, keep the use non-commercial, and share adaptations under the same license.

## Folder layout

```
prints/
  README.md                          this file
  index.json                         catalog of every print
  <print-id>/                        lowercase kebab-case, matches print.json id
    print.json                       machine-readable card
    <project>.3mf                    slicer project, next to print.json
    images/                          previews named from the slicer
      plate1.png
```

`<print-id>` is the folder name and the `id` field. Example: `jollibee-barrel-man`.

Do not put prose pages in a print folder. The only Markdown file under `prints/` is this README. The gallery page is `docs/prints/index.md`, and the build fills it from these JSON files.

## How files are published

Two public URLs serve the same bytes:

| Use this | Base |
|---|---|
| GitHub raw, branch `main` | `https://raw.githubusercontent.com/udanax80/3d-Print-Library/main/prints/` |
| GitHub Pages, after deploy | `https://udanax80.github.io/3d-Print-Library/prints/` |

A file at `prints/<path>` is fetched at `<base><path>`.

- Dashboards on another website should use the **raw** URL. GitHub sends `Access-Control-Allow-Origin: *` on raw files, so a browser page on another origin can read the JSON.
- The **Pages** URL is the direct link for visitors. `mkdocs gh-deploy` publishes it because `hooks/prints.py` copies this folder into the built site. The gallery's download buttons use that copy.

`mkdocs.yml` `site_url` and `repo_url` are the source of those bases. `index.json` must repeat them. The build checks that.

GitHub Pages deploys on push to `main` (`.github/workflows/deploy.yml`). A pull request does not update the Pages URLs. Raw `main` URLs update when the PR is merged.

### Paths for the barrel man

**index.json**

- https://raw.githubusercontent.com/udanax80/3d-Print-Library/main/prints/index.json
- https://udanax80.github.io/3d-Print-Library/prints/index.json

**jollibee-barrel-man/print.json**

- https://raw.githubusercontent.com/udanax80/3d-Print-Library/main/prints/jollibee-barrel-man/print.json
- https://udanax80.github.io/3d-Print-Library/prints/jollibee-barrel-man/print.json

**jollibee-barrel-man/barrelman_complete_65.3mf** (wood barrel with black hoops)

- https://raw.githubusercontent.com/udanax80/3d-Print-Library/main/prints/jollibee-barrel-man/barrelman_complete_65.3mf
- https://udanax80.github.io/3d-Print-Library/prints/jollibee-barrel-man/barrelman_complete_65.3mf

**jollibee-barrel-man/barrelman_complete_65_stripes.3mf** (red/yellow stripe barrel)

- https://raw.githubusercontent.com/udanax80/3d-Print-Library/main/prints/jollibee-barrel-man/barrelman_complete_65_stripes.3mf
- https://udanax80.github.io/3d-Print-Library/prints/jollibee-barrel-man/barrelman_complete_65_stripes.3mf

**jollibee-barrel-man/images/plate1_Bee_body_65.png**

- https://raw.githubusercontent.com/udanax80/3d-Print-Library/main/prints/jollibee-barrel-man/images/plate1_Bee_body_65.png
- https://udanax80.github.io/3d-Print-Library/prints/jollibee-barrel-man/images/plate1_Bee_body_65.png

**jollibee-barrel-man/images/plate2_Barrel_sleeve_65.png**

- https://raw.githubusercontent.com/udanax80/3d-Print-Library/main/prints/jollibee-barrel-man/images/plate2_Barrel_sleeve_65.png
- https://udanax80.github.io/3d-Print-Library/prints/jollibee-barrel-man/images/plate2_Barrel_sleeve_65.png

**jollibee-barrel-man/images/plate2_Barrel_sleeve_stripes_65.png**

- https://raw.githubusercontent.com/udanax80/3d-Print-Library/main/prints/jollibee-barrel-man/images/plate2_Barrel_sleeve_stripes_65.png
- https://udanax80.github.io/3d-Print-Library/prints/jollibee-barrel-man/images/plate2_Barrel_sleeve_stripes_65.png

**jollibee-barrel-man/images/after_barrel_wood_hoops_34.png**

- https://raw.githubusercontent.com/udanax80/3d-Print-Library/main/prints/jollibee-barrel-man/images/after_barrel_wood_hoops_34.png
- https://udanax80.github.io/3d-Print-Library/prints/jollibee-barrel-man/images/after_barrel_wood_hoops_34.png

**jollibee-barrel-man/images/after_barrel_stripes_hoops_34.png**

- https://raw.githubusercontent.com/udanax80/3d-Print-Library/main/prints/jollibee-barrel-man/images/after_barrel_stripes_hoops_34.png
- https://udanax80.github.io/3d-Print-Library/prints/jollibee-barrel-man/images/after_barrel_stripes_hoops_34.png

The Recent prints page repeats this list for every print. When you add a print, add the same pair of URLs here. The build fails if a catalog file is missing from this README.

## Size and git

`.gitignore` ignores the built site, the virtualenv, and caches. It does not ignore `*.3mf`, `*.png`, or `*.json`. Leave it that way: if a print file is ignored, the raw URL and the site both 404.

Commit `.3mf` files as normal Git blobs. `.gitattributes` marks `*.3mf` binary so Git does not treat the zip bytes as text. Do not turn on Git LFS for this folder. LFS would make the raw URL return a pointer file instead of the project.

GitHub rejects a file at 100 MB and warns around 50 MB. These two projects are about 3 MB each. Keep a new file well under 50 MB. The build rejects anything over 95 MB.

## index.json

`schema_version` is `1`. `raw_base_url` and `pages_base_url` are the bases in the table above, including the trailing slash. `prints` is the gallery order, newest first.

Each entry:

| Field | Required | Meaning |
|---|---|---|
| `id` | yes | Same kebab-case id as the folder and `print.json` |
| `title` | yes | Same title as `print.json` |
| `description` | yes | One-line summary for a dashboard list |
| `added` | no | `YYYY-MM-DD` |
| `dir` | yes | Must equal `id` |
| `print_json` | yes | Must equal `<id>/print.json` |
| `thumbnail` | yes, if the print has images | Path relative to `prints/`, and it must be one of that print's images |

The build also requires every `prints/<id>/print.json` folder to appear in this list, and every list entry to exist on disk.

## print.json

`schema_version` is `1`. Paths in `files` and `images` are relative to the print folder. Use letters, numbers, dots, underscores, and hyphens only, so the URLs stay easy to copy. List colors in extruder order.

| Field | Required | Meaning |
|---|---|---|
| `id` | yes | Folder name, lowercase kebab-case |
| `title` | yes | Card heading |
| `description` | yes | One paragraph. What the files are, the scale, and how the variants differ |
| `note` | no | Extra note on the card, such as a trademark |
| `added` | no | `YYYY-MM-DD` |
| `author` | no | Name to credit under CC BY |
| `printer` | yes | Printer the project is for. The barrel man uses `Bambu X1C/X2D` |
| `slicer` | no | App that opens the project, such as `Bambu Studio` |
| `material.type` | yes | Filament family, such as `PLA` |
| `material.colors` | yes | List of `{ "name", "hex" }`. `hex` is `#RRGGBB` |
| `layer_height_mm` | yes | Object of part name to millimeters. The barrel man uses `body` (0.12) and `barrel` (0.16) |
| `scale_percent` | yes | Slicer scale. Use `100` when the file is unscaled |
| `body_height_mm` | yes | Approximate finished height of the main body, in millimeters |
| `license` | yes | Short name. This library uses `CC BY-NC-SA 4.0` |
| `license_url` | no | `https://` link to the license |
| `files` | yes | At least one `{ "filename", "description", "bytes" }`. `bytes` is optional, and if you set it the build checks the size on disk |
| `images` | yes | List of `{ "filename", "alt", "caption" }`. Use `[]` when there is no preview. `caption` is optional. `alt` is required |

`jollibee-barrel-man/print.json` is the worked example.

## Add a print

1. Create `prints/<print-id>/` with the project files and images.
2. Write `print.json` using the fields above. Set `bytes` from `ls -l` if you include it.
3. Add an entry at the top of `prints` in `index.json`.
4. Add both the raw and Pages URL for `print.json`, each project file, and each image to the list in this README.
5. Run `mkdocs build --strict`. The Recent prints page picks the new card up from the JSON. You do not edit the card by hand.
