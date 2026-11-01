---
title: Drying & storage
tags:
  - Materials
  - Wet filament
  - PLA
  - PETG
  - TPU
  - PA / PA-CF
  - PC
---

# Filament drying & storage

Most FDM filaments are **hygroscopic**: they absorb moisture from the air. Wet filament shows up as stringing, popping or hissing at the nozzle, bubbles, rough or fuzzy surfaces, and weak layers. **Dry before you re-tune.**

## Drying starting points

| Material | Temp (°C) | Time (h) | Prusa reference (Prusament) | How sensitive |
|---|---|---|---|---|
| PLA | 45–55 | 4–8 | 45 °C / 6 h | Low–moderate |
| PETG | 55–65 | 4–8 | 55 °C / 6 h | Moderate |
| ABS | 60–80 | 4–6 | — | Moderate |
| ASA | 70–80 | 4–6 | 80 °C / 4 h | Moderate |
| TPU | 50–60 | 4–8 | 60 °C / 4–6 h | High |
| PA / PA-CF | 70–90 | 8–12 | PA11-CF: 90 °C / 6 h | **Very high** |
| PC / PC blend | 70–90 | 6–8 | PC Blend: 85 °C / 5 h | High |
| PVA / BVOH (supports) | 45–55 | 8+ | — | **Very high** |

Sources: [Prusa KB: Drying filament](https://help.prusa3d.com/article/drying-filament_332086) · [Bambu Lab Wiki: Filament Drying Recommendations](https://wiki.bambulab.com/en/filament-acc/filament/dry-filament). Always check the filament maker's data sheet. **Don't exceed the spool's rated temperature.** Many cardboard and cheap plastic spools deform above ~60–70 °C.

!!! info "What my gear can do (verify against current docs)"
    - **Bambu AMS 2 Pro / AMS HT** can dry in place. Bambu notes that AMS 2 Pro tops out around 65 °C, so it may not fully dry high-temp materials, and that **AMS HT** handles all filaments. Static drying mode isn't suitable for PLA, PVA, Support for PLA/PETG, or TPU (spools can stick). On an **X1**, each AMS 2 Pro needs its own power adapter to dry. The **X2D** can power one from the printer. ([Bambu Wiki](https://wiki.bambulab.com/en/filament-acc/filament/dry-filament))
    - Bambu also documents **heated-bed drying** on enclosed X-series printers, with the filament covered on the bed.
    - **Creality CFS / Snapmaker U1 / Creator 5 Pro**: add your dryer or dry-box notes here (PRs welcome).

## Storage

- **Target < 20 % RH** in storage for sensitive materials (PA, PC, TPU, PVA). Keep everything else below ~30–40 %.
- Airtight boxes or vacuum bags with **silica gel** desiccant plus a cheap hygrometer. Recharge the desiccant when it changes color.
- Return spools to storage right after printing. **Print PA and PVA straight from a dry box.**
- Label each spool with its open/dry date.

## Is it wet? Quick checks

1. Listen for crackling or popping at the nozzle during a purge or extrusion.
2. Look for steam, bubbles, or a rough, matte, fuzzy surface where it should be glossy.
3. Watch for a sudden increase in stringing on a profile that used to be clean.
4. Snap test (PLA/PETG): wet filament often becomes brittle and snaps when bent.

See also: [Fix → Wet filament](../fix/index.md#wet-filament)
