---
title: Speed, top surface & wall order
description: Which speeds to slow down, how to get a smoother top, and which wall order to pick, checked against Bambu Studio's stock profile.
tags:
  - Slicer
  - Speed
  - Top surface
  - Walls
  - Bambu Studio
---

# Speed, top surface & wall order

Three slicer topics that change how a part **looks** more than how strong it is. Each section gives the short answer first, then what was checked.

!!! quote "Source and what was checked"
    Topics prompted by **AD3D (@ad3duae)** guide visuals. The text and tables here are my own. On November 20, 2026 the claims were checked against Bambu Studio's stock `0.20mm Standard @BBL X1C` process profile, the `Bambu PLA Basic @BBL X1C` filament profile ([BambuStudio profiles on GitHub](https://github.com/bambulab/BambuStudio/tree/master/resources/profiles/BBL)), the [Bambu Wiki: advanced quality settings](https://wiki.bambulab.com/en/software/bambu-studio/parameter/quality-advance-settings), the [Bambu Wiki: ironing](https://wiki.bambulab.com/en/software/bambu-studio/parameter/ironing), and the [OrcaSlicer wiki: walls and surfaces](https://www.orcaslicer.com/wiki/print_settings/quality/quality_settings_wall_and_surfaces). **None of it was print-tested on my machines yet.**

## Speed by feature

**Short answer:** slow the two surfaces you can see (outer wall, top surface) and the first layer. Leave inner walls and infill fast. The stock Bambu profile is already tuned, so slow down only when a surface is not good enough.

All numbers are for **PLA, 0.4 mm nozzle, 0.20 mm layers**.

| Feature | Quality-first range (guide) | Bambu stock, X1C / P1S | What slowing down buys |
|---|---|---|---|
| Initial layer | 20–30 mm/s | 50 mm/s (first-layer infill 105) | Bed adhesion. Try it when corners lift or small features do not stick |
| Outer wall | 40–80 mm/s | 200 mm/s | Smoother, glossier walls. Biggest visual change, biggest time cost |
| Inner wall | 80–150 mm/s | 300 mm/s | Little. Inner walls are hidden |
| Top surface | 30–60 mm/s | 200 mm/s | Flatter top with fewer visible lines |
| Sparse infill | 100–200 mm/s | 270 mm/s | Nothing visible. Flow limit decides the real speed |

!!! warning "The guide range is a quality preset, not a high-speed one"
    Every row in the guide column is **well under** the stock Bambu profile, in places by a factor of three or more. Treat it as "what to try when the surface matters," not as a baseline for a fast printer. Print time goes up. Check the slicer's estimate before committing a long job. The slicer rarely reaches 200 mm/s on small parts anyway, because acceleration limits it, so the time penalty is smaller than the ratio suggests.

### The flow limit is the real speed limit

`flow (mm³/s) ≈ speed × line width × layer height`

Bambu PLA Basic is capped at **21 mm³/s** on the standard X1C hotend. With stock widths (0.42 mm outer wall, 0.45 mm infill) and 0.20 mm layers:

| Setting | Flow asked for | Result |
|---|---|---|
| Outer wall 200 mm/s | 200 × 0.42 × 0.20 ≈ 16.8 mm³/s | Under the cap. Prints as set |
| Outer wall 60 mm/s | ≈ 5.0 mm³/s | Far under the cap |
| Sparse infill 270 mm/s | 270 × 0.45 × 0.20 ≈ 24.3 mm³/s | **Over the cap.** The slicer slows it to about 233 mm/s |
| Sparse infill 200 mm/s | ≈ 18.0 mm³/s | Under the cap |

This is a rectangle estimate. It overstates flow by roughly 10%, because the slicer models a rounded bead. The point holds: typing a bigger infill number does nothing once the filament's volumetric limit is reached. Raise the limit only after the [max volumetric speed test](calibration.md).

**Where to set it (Bambu Studio):** *Process → Speed*. First-layer speeds are under *Initial layer speed*. The flow cap is in the **filament** settings, *Volumetric speed limitation → Max volumetric speed*.

## Smoother top surfaces

**Short answer:** in order of effect: calibrate flow, turn on ironing for flat tops, slow the top surface, add a top layer. Change one setting per test.

| Setting | Bambu stock (0.20 mm Standard) | Try | Cost | Checked |
|---|---|---|---|---|
| **Flow ratio and temperature** | Per filament | Run the [calibration sequence](calibration.md) first | One test print | Over-extrusion leaves ridges, under-extrusion leaves gaps. No top-surface setting hides either |
| **Ironing** | Off | *All top surfaces* or *Topmost surface only* | Slow extra pass on every ironed area | Bambu Wiki: works on **flat** tops only, adds time, and a badly tuned flow makes the surface worse |
| **Top surface speed** | 200 mm/s | 100, then 60 mm/s | Time on top layers only | Sources disagree, see below |
| **Top shell layers** | 5 (shell thickness 1.0 mm) | 6 (6 × 0.20 = 1.20 mm) | One more solid layer per top surface | The slicer uses whichever is thicker: layer count or shell thickness |
| **Top surface pattern** | Monotonic line | Leave it | None | Already the stock setting. Nothing to change on a Bambu profile |
| **Top surface line width** | 0.42 mm | 0.40 mm | None | A 0.02 mm change. No source shows a measured benefit. Lowest priority |

!!! warning "Two guides, two top-speed ranges"
    One guide says **30–60 mm/s**, another says **60–100 mm/s**, and the stock profile is **200 mm/s**. Neither range has a primary source. Use them as test points: print the same flat part at 200, 100, and 60 and keep the slowest one that still shows a difference.

!!! info "Ironing cautions from the Bambu Wiki"
    Ironing runs at very low flow, which the wiki says can lead to heat creep and clogs with low-softening filaments such as PLA, PETG, and TPU. The nozzle also drags on the part, so it can knock loose a model that is not stuck down well. Curved tops gain little. Use it for flat, visible tops such as lids, signs, and coasters.

**Where to set it (Bambu Studio):** ironing is under *Process → Quality → Ironing*. Top shell layers, pattern, and thickness are under *Process → Strength → Top/bottom shells*. Top surface line width is under *Process → Quality → Line width* (turn on **Advanced**). Top surface speed is under *Process → Speed*.

## Wall printing order

**Short answer:** keep **Inner/Outer** (the default) for anything with overhangs. Try **Inner/Outer/Inner** on parts with 3 or more walls and no steep overhangs when you want the cleanest outer surface.

| Order | What it does | Good for | Gives up |
|---|---|---|---|
| **Inner/Outer** (default) | Inner walls first, outer wall last | **Overhangs.** The outer wall has an inner wall beside it to stick to | Inner walls can push on the outer wall, which can show as faint lines |
| **Outer/Inner** | Outer wall first | Cleaner surface, since the outer wall sets before anything presses on it | Worse overhangs. Seams can be more visible |
| **Inner/Outer/Inner** | Innermost walls, then the outer wall, then the wall next to it | Least shrink marking on the outer surface | Worse overhangs, same reason as Outer/Inner |

All three rows match the Bambu Wiki. Two notes from the OrcaSlicer wiki, which matter on the K2 Plus, U1, and Creator 5 Pro because their slicers are Orca-based:

- Orca recommends **Inner/Outer/Inner over Outer/Inner** in most cases when the goal is surface finish and dimensional accuracy.
- Inner/Outer/Inner needs a spare inner wall to print first. With too few walls there is nothing to print ahead of the outer wall, so use **3 or more walls**.

**Rule of thumb:** check the model for overhangs past about 45°. If it has them, stay on Inner/Outer. If it is a box, a lid, or a sign, test Inner/Outer/Inner.

**Where to set it (Bambu Studio):** *Process → Quality → Advanced → Order of walls* (turn on **Advanced**).

## Test log

Fill in after a real test. One change per print.

| Date | Printer | Filament | Setting changed | From → to | Result |
|---|---|---|---|---|---|
| | | | | | |

Related: [Slicer basics](slicer-basics.md) · [Slicer tips](slicer-tips.md) · [Calibration sequence](calibration.md)
