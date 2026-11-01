---
title: Material notes (from my guides)
tags:
  - Materials
  - PLA
  - PETG
  - ABS/ASA
  - TPU
---

# Material notes (from my saved guides)

!!! quote "Source & status"
    Summaries of instructional visuals I saved from **AD3D (@ad3duae)**, added October 25, 2026. These are my **summaries**, not the original images, and the numbers inside the visuals **have not been independently validated**. Use the filament and printer maker's guidance for temperatures, drying, compatibility, and safety. See [Credits & licensing](../contribute/credits.md).

## ASA printing guide
- Check drying requirements and store sealed with desiccant.
- Use the filament maker's ASA profile and confirm the printer, plate, and nozzle suit it.
- Enclosure, glue, and a brim when needed to reduce warping.
- Run a small test print and check adhesion and layer bonding before a long job.
- Ventilate (see [Safety](../safety/index.md)).

## ABS printing guide
- Check dryness and use the maker's ABS profile. Confirm the enclosure and plate are suitable.
- Keep temperatures stable, part cooling low, and use glue and a brim when needed.
- Check a test print for lifted corners and layer cracking before scaling up.

## PLA printing guide
- Choose the **exact** PLA type in the slicer. Silk, wood, CF, glow, and aero PLA all differ.
- Filled or abrasive types (glow, CF) may need a hardened nozzle.
- Use a small test to check flow, surface, and cooling.

## PETG printing guide
- **Check dryness before changing several slicer settings.**
- Start from the profile for your exact PETG product (is it a high-flow variant?).
- Change one variable at a time. The visual's 220 °C and flow values are source-specific suggestions, not universal settings.

## TPU essentials & TPU types
- Confirm the TPU grade, nozzle, and feed path. **Don't assume AMS compatibility from "TPU" alone.**
- The source's Bambu workflow suggests disabling Flow Dynamics Calibration for TPU and using PLA as the support where the printer supports that combination.
- Choose hardness by the job: cushioning and grip (soft), moderate flex, or rigidity and wear resistance (hard). Shore A ≠ Shore D. Conversion charts are approximate.

## OBJ vs. STL in Bambu Studio
- STL = mesh geometry. OBJ can reference colors and materials via its **MTL** file. Keep OBJ, MTL, and textures together.
- Drag the OBJ into Bambu Studio, review the color-matching dialog, assign filaments, and inspect the slice.

## Build stronger prints
- Orient the part so the load doesn't pull layers apart.
- **Walls before infill.** More infill doesn't give proportionally more strength.
- Pick infill pattern and density for the actual use, and test the finished part under its real load.
- More in [Design for printing](../design/index.md).
