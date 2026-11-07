---
title: Slicer basics
description: The ten slicer settings that change a print, in the order a beginner should meet them.
tags:
  - Beginner
  - Slicer
---

# Slicer basics

A slicer cuts the model into layers and writes the file your printer runs. You can ignore most of the menus. These ten settings are the ones that change the result. Leave the rest on the printer's default profile until one of these is not enough.

Use the profile for **your printer and your nozzle**. A 0.4 mm nozzle is the usual one in the box. The deeper notes on seams and supports are [Slicer tips](slicer-tips.md). Tuning a new spool is the [calibration sequence](calibration.md).

## 1. Layer height

How thick each slice is. **0.20 mm** is a normal everyday height on a 0.4 mm nozzle. **0.12–0.16 mm** looks smoother and takes longer. **0.28 mm** is a draft. Stay under about 75% of the nozzle width so the lines still squash together. The printer profile already knows a safe list. Pick from that list.

## 2. Walls (perimeters)

The solid outlines. Two walls is a display model. Three or four walls is the first thing to add when a part snaps. Walls do more for strength than stuffing the inside with infill.

## 3. Infill

The lattice inside. **10–15%** gyroid or grid is enough for most models and stands. **20–40%** is for parts you will stand on or bolt down, and only after you have added walls. 100% infill is rarely the right answer. It is slow, and the part can still split between layers.

## 4. Nozzle and bed temperature

Use the **spool label**, then the slicer's generic preset for that plastic if the label gives a range. [Materials 101](../materials/beginner.md) has the usual bands. Change temperature in 5 °C steps. Hotter sticks layers together and strings more. Cooler looks cleaner and can go brittle.

## 5. Speed, really volumetric flow

The big "500 mm/s" number is a maximum, not a promise. The hotend can only melt so much plastic per second. If walls look thin at high speed, you are past that limit. Slow the outer wall for looks. Leave the infill faster. The calibration page shows how to find a volumetric limit instead of guessing.

## 6. Part cooling

The fan on the side of the nozzle. **PLA wants it on**, or bridges sag. **ABS, ASA, and PC want it off or nearly off**, or the part splits and lifts. PETG is in between. The material preset usually sets this. Do not "improve" it on the first print.

## 7. Supports

Plastic scaffolding under overhangs. Turn them on when a slope is steeper than about 45 degrees from vertical, or when a bridge is long. Paint them on just the spots that need them if the slicer allows it. They scar the surface. A second material that does not bond (PLA supporting PETG, or a dedicated support filament) lets you set the gap to zero. Same-plastic supports need a gap or they become part of the model. Details: [Slicer tips](slicer-tips.md).

## 8. Brim, skirt, raft

A **skirt** is a throwaway loop that primes the nozzle. Leave it on. A **brim** is a lip stuck to the first layer so corners do not lift. Use it on small feet and on ABS. A **raft** is a whole disposable platform. Use it when nothing else will stick, not as a habit.

## 9. Retraction

A short pull of filament before the nozzle jumps, so it does not draw a hair. The printer profile's number is the right start. If you still see strings, [dry the filament](../materials/drying-storage.md) before you chase retraction. Direct-drive machines often land around 0.4–1.5 mm. That range is a test window from the [stringing notes](../fix/index.md#stringing), not a value to type in blindly.

## 10. Seam

Every layer has to start somewhere. That start leaves a mark. Hide it on a corner or on the back of the part. You cannot turn it off. How the modes differ: [Slicer tips](slicer-tips.md#seam-position).

---

**A ten-minute practice:** import a 20 mm cube or a simple clip, select your printer and PLA, set 0.20 mm layers and 3 walls, leave everything else, slice, and look at the preview. If the first layer in the preview is a solid sheet and the travels are not a bird's nest, print it.
