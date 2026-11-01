---
hide:
  - toc
title: Material matrix
tags:
  - PLA
  - PETG
  - ABS/ASA
  - TPU
  - PA / PA-CF
  - PC
  - Materials
---

# Material matrix

!!! warning "Starting points, not settings"
    These are **typical, widely used ranges** for standard grades, cross-checked against the [Prusa Material Guide](https://help.prusa3d.com/materials) and [Bambu Lab Filament Guide](https://wiki.bambulab.com/en/general/filament-guide-material-table). **The temperature printed on your spool and your printer's own filament profile come first.** Specialty blends (silk, high-flow, CF/GF, "HF", "Pro") can be well outside these ranges. Check each against the [fleet's max temps](../fleet/index.md).

## At a glance

| Material | Nozzle °C | Bed °C | Chamber | Dry (°C / h) | Enclosure | Common failures |
|---|---|---|---|---|---|---|
| **PLA** | 190–230 | 45–65 | Keep it cool: lid/door open, ideally < ~35 °C | 45–55 / 4–8 | **No** (cooling matters more) | Heat creep and clogs in a hot enclosure, stringing, soft overhangs if under-cooled |
| **PETG** | 220–260 | 70–90 | Ambient | 55–65 / 4–8 | No | Stringing and blobs, over-sticking to smooth PEI (glue or release agent), wet-filament bubbles |
| **ABS / ASA** | 240–270 | 90–110 | Warm, ~40–60 °C passive or heated | 60–80 / 4–8 | **Yes** | Warping/lifted corners, layer splitting on tall parts, fumes (styrene) |
| **TPU** (95A typical) | 210–240 | 30–60 | Ambient | 50–60 / 4–8 | No | Buckling in the extruder, stringing, feeder/AMS incompatibility, slow print speeds required |
| **PA / PA-CF** | 260–300 | 80–110 | Warm–hot, ~40–60 °C+ | 70–90 / 8–12 | **Yes** | **Very hygroscopic** (dry before *every* print), warping, stringing, abrasive CF wears soft nozzles |
| **PC** (and PC blends) | 260–300 | 100–120 | Hot, ~50–60 °C+ | 70–90 / 6–8 | **Yes** | Severe warping, layer cracking, adhesion loss without glue/brim |

<small>Chamber values are typical targets for enclosed printers. Active chamber heating on my fleet: K2 Plus up to 60 °C; X2D and Creator 5 Pro up to 65 °C; X1C via the aftermarket Panda Breath (not verified).</small>

## Per-material notes

=== "PLA"
    - Easiest material. Needs **strong part cooling**. Print with the lid open or door ajar on enclosed machines.
    - Specialty PLAs: **silk** prints slower and hotter, **wood/glow/CF** fills are abrasive or clog-prone, so use 0.4 mm hardened or larger nozzles.
    - Softens around 55–60 °C, so it's not for car interiors or hot rooms.
    - Source: [Prusa KB: PLA](https://help.prusa3d.com/article/pla_2062)

=== "PETG"
    - Tougher and more heat-tolerant than PLA. Moderate cooling.
    - Bonds *very* strongly to smooth PEI, so use glue stick or a textured plate as a **release layer**.
    - Stringing is usually wet filament or too-high temperature. Dry it before you change retraction.
    - PETG and PLA barely bond to each other, which makes them a classic support-interface pair (see [Multi-material](../prepare/multi-material.md)).
    - Source: [Prusa KB: PETG](https://help.prusa3d.com/article/petg_2059)

=== "ABS / ASA"
    - Needs an enclosure, low or no part cooling, glue, and a brim on large footprints.
    - ASA is UV-stable for outdoor parts; ABS is cheaper and easy to acetone-smooth (so is ASA).
    - **Ventilate**: both emit styrene. See [Safety](../safety/index.md).
    - Sources: [Prusa KB: ABS](https://help.prusa3d.com/article/abs_2058) · [Prusa KB: ASA](https://help.prusa3d.com/article/asa_1809)

=== "TPU"
    - Print slowly (low volumetric flow), with minimal retraction.
    - **Check that your exact TPU grade is approved for your AMS/CFS/feeder.** Softer grades usually aren't. Use an external spool when in doubt.
    - Shore A and Shore D are different scales, so compare the maker's data sheet rather than a chart.
    - Source: [Prusa KB: Flexible materials](https://help.prusa3d.com/article/flexible-materials_2057)

=== "PA / PA-CF"
    - Strong, tough, heat-resistant, and extremely moisture-sensitive. Print straight from a dryer or dry box.
    - **CF/GF fills are abrasive.** Use a hardened steel nozzle and extruder gears rated for them.
    - Bambu notes that supports on PA should be removed **within ~2 hours**, before the part absorbs moisture ([Bambu Wiki: Support](https://wiki.bambulab.com/en/software/bambu-studio/support)).
    - Source: [Prusa KB: Polyamide (Nylon)](https://help.prusa3d.com/article/polyamide-nylon_167188)

=== "PC"
    - Very high heat resistance and toughness. The hardest of these to keep flat.
    - Hot chamber, glue, a brim, slow first layers, and no drafts.
    - Source: [Prusa KB: Polycarbonate](https://help.prusa3d.com/article/polycarbonate-pc_165812)

## Choosing by requirement

| Need | Try first | Then |
|---|---|---|
| Easy, detailed, indoor | PLA | PETG |
| Outdoors / UV | ASA | PETG (short-term) |
| Heat near engines, cars, lamps | ASA, PC | PA-CF |
| Tough + slightly flexible (clips, hinges) | PETG | PA |
| Rubbery grip, dampers | TPU | — |
| Stiff, strong, engineering | PA-CF | PC |

See also: [Drying & storage](drying-storage.md) · [Material notes from my guides](material-notes.md)
