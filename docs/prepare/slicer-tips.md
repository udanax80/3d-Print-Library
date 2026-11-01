---
title: Slicer tips (seams, supports, strength)
tags:
  - Slicer
  - Supports
  - Seams
  - Strength
---

# Slicer tips

!!! quote "Source"
    Seam and support sections are organized from my saved **AD3D (@ad3duae)** guides, whose visuals cite the Bambu Lab Wiki. Settings were **not independently verified**. Cross-checked against [Bambu Wiki: Seam settings](https://wiki.bambulab.com/en/software/bambu-studio/seam), [Bambu Wiki: Support](https://wiki.bambulab.com/en/software/bambu-studio/support), and [Prusa KB: Seam position](https://help.prusa3d.com/article/seam-position_151069).

## Seam position

The seam is where each layer's perimeter starts and stops. You can move it, but you can't make it disappear.

| Mode | What it does | When to use it |
|---|---|---|
| **Nearest** | Picks a nearby, less-visible spot (concave corners), avoiding overhangs. May move between layers | Models with hidden corners. Check in preview |
| **Aligned** | Tries to line the seam up vertically across layers | One consistent line is easier to hide or sand |
| **Back** | Puts the seam toward the back of the plate (Y+), whatever the model orientation | Rotate the model so the hidden face points to the back |
| **Random** | Scatters seam points around the surface | When scattered marks look better than a line (may leave small zits) |

**Workflow (Bambu Studio):** *Quality → Seam* → pick a mode → use **Seam Painting** for exact placement on a hidden edge → on curved surfaces consider **Scarf joint seam** (profile-dependent) → slice, preview, and test small before a long job.

## Support tuning

Three controls balance **underside finish** against **easy removal**. There's no single universal profile.

| Setting | Lower / fewer | Higher / more |
|---|---|---|
| **Top Z distance** (vertical gap) | Better underside, harder removal, more scarring risk | Easier removal, rougher underside |
| **Top interface layers** | Faster, less material, pattern may show through | Smoother, flatter underside. Removal may get easier or harder |
| **Top interface spacing** | Denser contact, smoother, harder removal | Easier removal, rougher underside |

**Test one change at a time:**

1. Save a copy of your working profile and use a small supported test model.
2. Rough underside → smaller top Z distance or tighter interface spacing. Too hard to remove → increase the gap or spacing.
3. Change top Z distance **one layer height at a time**, since rounding can change the real gap, especially with tree supports or when *Independent support layer height* is off.
4. Adjust interface spacing in **0.05–0.1 mm** steps.
5. Interface layers = 0 disables the interface. The source suggests this *may* help PLA-on-PLA removal. Treat it as a test, not a default.
6. Record material, layer height, the three settings, underside appearance, and removal effort.

!!! info "Dedicated support material changes the rules"
    Bambu's wiki: with a dedicated support/interface filament (e.g. Bambu *Support for PLA*), **top Z distance can be 0**. With the same filament as the body, use about **0.2 mm**, or removal gets very hard. **3 interface layers** gives a stable, flat platform. ([Bambu Wiki: Support](https://wiki.bambulab.com/en/software/bambu-studio/support)) See [Multi-material planning](multi-material.md) for interface pairs.

## Strength settings (quick version)

- **Walls (perimeters) add strength faster than infill.** Try 3–4 walls before raising infill above ~25 %.
- Orient so loads run **along** layers, not across them.
- Hotter (within range) and slower = better layer bonding. More cooling = better overhangs but weaker bonds.
- Full details: [Design for printing](../design/index.md).
