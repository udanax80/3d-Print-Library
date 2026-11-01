---
title: Calibration sequence
tags:
  - Calibration
  - Stringing
  - Under-extrusion
---

# Calibration sequence

Calibrate **per printer × per filament × per nozzle**. Save the result as a named filament profile, such as `PETG-Brand-X1C-0.4`.

!!! tip "Order matters"
    The [OrcaSlicer Calibration Guide](https://www.orcaslicer.com/wiki/guides/calibration_guide) recommends **temperature → max volumetric speed → pressure advance → flow ratio → retraction**, because each step depends on the one before. Shrinkage/tolerance comes last. Bambu printers with auto-calibration (X1C/X2D Flow Dynamics) can cover PA automatically. Run the manual tests when the auto result looks wrong.

| # | Test | What you're finding | How to read it | Reference |
|---|---|---|---|---|
| 1 | **Temperature tower** | Best nozzle temp for this spool | Pick the block with the best balance of layer bonding, bridges/overhangs, surface, and stringing. Lean higher for fast or high-flow printing | [Orca: Temp calibration](https://www.orcaslicer.com/wiki/calibration/temp_calib) |
| 2 | **Max volumetric speed** | Flow ceiling before under-extrusion | Note where gaps or rough walls start, then set ~10–20 % below that | [Orca: Max volumetric speed](https://www.orcaslicer.com/wiki/calibration/volumetric_speed_calib) |
| 3 | **Pressure advance** (Bambu: *Flow Dynamics*) | Corner sharpness and even lines at speed changes | Choose the line or corner with no bulge or gap at speed transitions | [Orca: Pressure advance](https://www.orcaslicer.com/wiki/calibration/pressure_advance_calib) · [Bambu Wiki: Flow Dynamics](https://wiki.bambulab.com/en/software/bambu-studio/calibration_pa) · [Ellis: PA/LA](https://ellis3dp.com/Print-Tuning-Guide/articles/pressure_linear_advance/introduction.html) |
| 4 | **Flow ratio** (extrusion multiplier) | Correct amount of plastic | Smoothest top surface without ridges (over) or gaps (under) | [Orca: Flow ratio](https://www.orcaslicer.com/wiki/calibration/flow_ratio_calib) · [Bambu Wiki: Flow rate](https://wiki.bambulab.com/en/software/bambu-studio/calibration_flow_rate) · [Ellis: Extrusion multiplier](https://ellis3dp.com/Print-Tuning-Guide/articles/extrusion_multiplier.html) |
| 5 | **Retraction** | Shortest retraction with clean travel | Lowest section without strings. Direct drive is usually ~0.4–1.5 mm. **Dry the filament first** | [Orca: Retraction test](https://www.orcaslicer.com/wiki/calibration/retraction_calib) |
| 6 | **Shrinkage / tolerance** | Dimensional accuracy and fit | Print a 50–100 mm XY test and measure with calipers. Set the filament's shrinkage %. Use a tolerance test for peg/hole fits | [Orca: Tolerance test](https://www.orcaslicer.com/wiki/calibration/tolerance_calib) |

!!! note "Shrinkage quick math"
    `shrinkage % = measured ÷ designed × 100`. A 100 mm design that measures 99.4 mm gives **99.4 %**. PLA/PETG are usually 99.6–100 %. ABS/ASA/PC/PA typically shrink more. Measure, don't guess.

## My results

Fill in as you go. PRs from friends with their own results are welcome (add your printer name).

| Printer | Filament (brand / type) | Nozzle | Temp °C | Max vol. speed mm³/s | PA / K | Flow ratio | Retraction mm | Shrinkage % | Date |
|---|---|---|---|---|---|---|---|---|---|
| X1C | _e.g._ PLA Basic | 0.4 hardened | | | auto | | | | |
| X2D | | | | | | | | | |
| K2 Plus | | | | | | | | | |
| Hi | | | | | | | | | |
| U1 (T0–T3) | | | | | | | | | |
| Creator 5 Pro (T0–T3) | | | | | | | | | |

!!! tip "Tool changers"
    On the **U1** and **Creator 5 Pro**, each toolhead is its own hotend, so check **per-tool XY offsets** (the printer's own tool-alignment calibration) and calibrate flow/PA per tool if results differ.
