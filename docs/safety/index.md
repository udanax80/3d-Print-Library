---
title: Ventilation & VOCs
tags:
  - Safety
  - ABS/ASA
  - PC
  - PA / PA-CF
---

# Safety: ventilation & VOCs

FDM printers release **ultrafine particles (UFPs)** and **volatile organic compounds (VOCs)** while printing. Research from UL's Chemical Insights found emissions vary by filament, printer, and temperature. Higher-temperature materials such as **ABS** and **nylon** generally emit more, and the measured VOCs include **styrene** (ABS/ASA), **caprolactam** (nylon), formaldehyde, and acetaldehyde. ([UL Chemical Insights: 3D printing emissions](https://chemicalinsights.ul.org/3d-printing/))

## Practical rules

| Situation | Do this |
|---|---|
| PLA / PETG, occasional | Ventilated room. Don't sit next to the printer for hours |
| **ABS / ASA / PC / PA** | Enclosed printer **with filtration (carbon + HEPA) or ducted exhaust**. Don't print these in a bedroom or poorly ventilated space |
| Opening the enclosure after a hot print | Let the filter run a few minutes after the print ends, then open |
| Long or frequent jobs | Put printers in a separate, ventilated room. Consider an air-quality monitor (PM2.5 / VOC) |
| Acetone smoothing, solvents, resin (future) | Outdoors or under extraction. Nitrile gloves and eye protection. Keep away from ignition sources |

- **Filters wear out.** Replace carbon filters on the maker's schedule.
- Don't create drafts across the print (warping) when ventilating. Exhaust the enclosure, not the build plate.

## Fire and electricity

A printer is a heater that moves. Treat it like a kettle you do not walk away from until you trust it.

- Don't leave a printer running in an empty house until it has finished many boring prints without a fault. Use the camera and failure detection when the machine has them.
- A smoke detector in the room, and an ABC or CO₂ extinguisher you can reach without stepping over the printer.
- Thermal-runaway protection should stay enabled. It cuts the heater if the temperature does not rise. Check it again after any firmware change.
- Keep the spool and loose filament off the heated bed. A scrap on a 100 °C plate is how a small fire starts.
- Do not stack a printer on a carpet or inside a cupboard with no air. The power supply needs the ventilation the maker designed.

## Enclosure

Close the box for ABS, ASA, nylon, and PC. Open the door or lid for PLA if the chamber has no "keep it cool" mode. The point of the box is still air, not a hotter room around the whole printer.

If the machine has a carbon or HEPA filter, leave the fan running for a few minutes after a hot job, then open the door. Filters fill up. Replace them on the maker's schedule, not when they look dirty.

An enclosure is also a guard. A CoreXY head at the speeds in the [printer table](../buy/printers.md) is not something to reach into.

## Kids and pets

- The nozzle is hot enough to burn after the fans have stopped. The bed stays hot too.
- Moving belts and a tool changer will pinch fingers. The rule is: if it is printing, the door stays shut and hands stay out.
- Pets will eat filament scraps and chew a dangling spool. Cut waste goes in a bin with a lid, not on the floor.
- Resin, isopropyl alcohol, and acetone do not live on a low shelf. Filament printers are the ones this page is about. A resin vat is a separate setup with gloves.
- Show a child the stopped printer, not the running one. The interesting part is the finished object.

!!! warning "Not medical or industrial-hygiene advice"
    This is a hobbyist summary. Follow your printer and filament makers' safety data sheets (SDS) and local regulations.
