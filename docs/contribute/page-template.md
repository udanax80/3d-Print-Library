---
title: Page template
tags:
  - Contributing
---

# Page template

Copy this into a new `.md` file under the right section in `docs/`, then add it to `nav:` in `mkdocs.yml`.

````markdown
---
title: Short page title
tags:
  - PETG          # material(s)
  - Bambu X1C     # printer(s), if specific
  - Stringing     # problem type, if any
---

# Short page title

One-sentence summary of what this page helps with.

!!! warning "Starting points"
    Values below are starting points. Check your filament label and printer profile.

## Steps / table

| Thing | Value | Source |
|---|---|---|
| … | … | [Link](https://…) · checked YYYY-MM-DD |

## Sources
- [Manufacturer page](https://…), checked YYYY-MM-DD
````
