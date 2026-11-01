---
title: Multi-material planning
tags:
  - Multi-material
  - Supports
  - Snapmaker U1
  - Flashforge Creator 5 Pro
  - Bambu X1C
  - Bambu X2D
  - Creality K2 Plus
---

# Multi-material planning

My fleet has three different approaches: **single nozzle + switcher** (X1C + AMS, K2 Plus + CFS, Hi + optional CFS), **dual nozzle** (X2D), and **independent tool changers** (Snapmaker U1, Creator 5 Pro). Choosing the right one saves a lot of waste and time.

## Tool changer vs AMS/CFS

| | Tool changer (U1, Creator 5 Pro) | Dual nozzle (X2D) | Single nozzle + AMS/CFS (X1C, K2 Plus, Hi) |
|---|---|---|---|
| Materials per job | 4 (one per tool) | 2 hotends, with AMS feeding them | Up to 16 slots (more units) |
| Waste per swap | Small: prime/wipe only | Small between nozzles; purge within one nozzle's slots | **Full purge** of the previous color each swap |
| Time per swap | Seconds (tool park/pick) | Fast between nozzles | Slow: cut, retract, load, purge |
| Mixed materials (PLA + PETG, PLA + TPU) | Excellent, each tool tuned separately | Good: body on one nozzle, support/interface on the other | Possible, but each swap purges and temps change |
| Best for | 2–4 colors with many swaps per layer, support interfaces, mixed materials | Support-heavy parts with a dedicated interface material | Many colors with few swaps (e.g. color-by-height, signs) |

**Rules of thumb**

- **Swaps per layer × layers = waste.** A 4-color model with color changes on every layer belongs on a tool changer.
- Few colors that change by height (stacked bands) → AMS/CFS is fine.
- Want a support-interface material? → X2D, U1, or Creator 5 Pro first.

## Purge & prime

- **Flushing volume** (single-nozzle) depends on the color pair. Dark → light needs the most. Bambu Studio sets it per from/to pair, with a multiplier. Lower it carefully and test for color bleed. ([Bambu Wiki: Reduce waste during filament change](https://wiki.bambulab.com/en/software/bambu-studio/reduce-wasting-during-filament-change))
- **Prime tower** stabilizes pressure after a swap. Tool changers can still need one. ([Bambu Wiki: Prime tower](https://wiki.bambulab.com/en/software/bambu-studio/parameter/prime-tower))
- Waste reducers: **flush into infill / flush into objects**, group color changes, order filaments light → dark, print several copies per plate so one tower serves them all.

## Support-interface pairs

The idea: a material that **doesn't bond well** to the body is used only for the interface layers, so supports pop off cleanly with a smooth underside. Then top Z distance can be **0** ([Bambu Wiki: Support](https://wiki.bambulab.com/en/software/bambu-studio/support)).

| Body material | Interface material | Notes |
|---|---|---|
| PLA | **PETG** | Classic pair: they barely bond. Cheap and easy |
| PETG | **PLA** | Works the other way too |
| PLA | Bambu *Support for PLA* (Support W) / *Support for PLA/PETG* | Purpose-made breakaway |
| PLA / PETG | **PVA** or **BVOH** | Water-soluble for internal cavities. Very moisture-sensitive, keep dry |
| ABS / ASA | **HIPS** | HIPS dissolves in d-limonene. Also breakaway |
| PA / PA-CF / PET-CF | Bambu *Support for PA/PET* | Remove promptly. It absorbs moisture |
| TPU | **PLA** | Suggested in my TPU guide where the printer supports the combo |

!!! tip "Interface-only saves material"
    Print the **support base** in the body material and only the **interface layers** in the special material. That's fewer swaps and less purge (or no purge on a tool changer).

!!! warning "Verify per printer"
    Material pairing and temperatures must be in range for both tools/nozzles. Use each maker's guidance (the X2D listing says *"use manufacturer guidance for support pairing"*).
