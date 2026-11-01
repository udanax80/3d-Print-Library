---
title: Design for printing
tags:
  - Design
  - Strength
  - Tolerances
---

# Design for printing

Rules of thumb for parts you model yourself. All values are <span class="badge-start">starting points</span> for a 0.4 mm nozzle. Print a [tolerance test](https://www.orcaslicer.com/wiki/calibration/tolerance_calib) on your own printer and adjust. Reference: [Prusa KB: Modeling with 3D printing in mind](https://help.prusa3d.com/article/modeling-with-3d-printing-in-mind_164135).

## Tolerances & clearances

| Fit | Gap per side (typical start) | Example |
|---|---|---|
| Press / interference fit | 0.0–0.1 mm | Pins meant to stay put |
| Snug / slip fit | 0.15–0.2 mm | Lids, sliding parts |
| Loose / free fit | 0.3–0.4 mm | Hinges and print-in-place moving parts |
| Print-in-place gaps | ≥ 0.3–0.5 mm | Articulated toys, captive joints |

Account for material shrink (ABS/PA more than PLA) and **elephant's foot** on mating bottom edges (add a 0.3–0.5 mm chamfer).

## Holes

- **Vertical holes print undersized**, often by 0.1–0.3 mm. Add clearance, use slicer **hole compensation** (X-Y hole compensation), or drill or ream to final size.
- **Horizontal holes:** make the top a **teardrop or diamond** so it's self-supporting, or use support. Otherwise the top sags.
- For accurate bearing or shaft fits, print slightly undersize and ream.

## Orientation for strength

- Layers are the weak direction. **Loads should run along the layers, not pull them apart.** A hook printed upright snaps at a layer line. Printed lying flat, it doesn't.
- Overhangs up to ~45° usually print without support. Bridges up to ~10–20 mm depending on material and cooling.
- Put cosmetic faces up or on the side, not on supports. Add a flat base or split the model if it can't sit flat.

## Walls vs infill

- **Walls (perimeters) carry most of the load** for bending and torsion. Going from 2 to 4 walls often helps more than doubling infill.
- Typical functional starting point: **3–4 walls, 4–5 top/bottom layers, 15–30 % gyroid or cubic infill.**
- Around bolt holes and inserts, add wall thickness locally (modifiers) rather than raising global infill.
- More infill ≠ proportionally more strength, and it costs time, weight, and filament. (Also covered in my *Build stronger prints* guide.)
- Myths to avoid: see [Ellis: Misconceptions & bad advice](https://ellis3dp.com/Print-Tuning-Guide/articles/misconceptions.html).

## Threads, inserts & fasteners

| Method | Best for | Design notes |
|---|---|---|
| **Heat-set inserts** (brass) | Repeated assembly, strong threads | Hole per the insert maker's spec (usually slightly smaller than the insert OD, with a tapered lead-in). ≥ 3 walls around it. Install with a soldering iron about 10–20 °C above the filament's print temp. See [Prusa: heat-set inserts & tools](https://www.prusa3d.com/category/heat-set-inserts-and-tools/) |
| **Self-tapping screws** into plastic | Quick, low-cycle joints | Pilot hole ≈ 80–85 % of screw OD. Extra walls |
| **Captive nuts** (hex pocket) | Cheap, strong | Hex pocket +0.2–0.3 mm across flats. Slot from the side or insert with a pause-at-layer |
| **Printed threads** | ≥ M8 / large threads | Use a modeled thread with ~0.2–0.4 mm clearance. Print vertically. Small printed threads are weak |

## Other tips

- **Minimum wall** ≈ 2 × nozzle width (0.8 mm for 0.4 mm nozzle). **Minimum feature** ≈ nozzle width.
- **Fillets** at stress points. **Chamfers** on bottom edges (not fillets, which overhang).
- Text: embossed ≥ 0.6 mm tall and ≥ 1 mm wide strokes print best on vertical faces.
- Design multi-color parts as separate bodies (or 3MF parts) so the slicer can assign filaments.
