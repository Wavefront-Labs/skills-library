---
id: computing-software.it-support-helpdesk.desktop-support.laptop-battery-replacement-and-swelling
name: laptop-battery-replacement-and-swelling
category: computing-software
field: it-support-helpdesk
product: desktop-support
tags: [it-support-helpdesk, desktop-support, laptop-hardware, hardware-replacement, battery-replacement, swollen-battery, powercfg-batteryreport, battery-wear, lithium-ion, battery-disposal, comptia-a-plus]
level: practitioner
status: draft
description: "Assess and replace laptop batteries: powercfg /batteryreport wear figures, vendor diagnostics, swollen battery handling and storage, safe replacement and lithium disposal."
sources:
  - "https://learn.microsoft.com/en-us/windows-hardware/design/component-guidelines/powercfg-command-line-options"
  - "https://www.comptia.org/certifications/a"
  - "https://www.epa.gov/recycle/used-lithium-ion-batteries"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# laptop-battery-replacement-and-swelling

Goal: replace worn batteries on evidence, and handle swollen ones as the
fire hazard they are.

## Measure wear
```cmd
powercfg /batteryreport /output "%USERPROFILE%\Desktop\battery.html"
```
Report shows **Design capacity** vs **Full charge capacity** (wear = 1 −
full/design), cycle count, and recent usage. Replace when full charge
< ~60–70 % of design, or vendor diagnostics (Dell SupportAssist, HP Battery
Check, Lenovo Vantage) flag "Replace". Many vendor warranties cover
batteries 1 year only, separate from the 3-year system warranty.

## Swollen battery
Signs: trackpad raised or not clicking, case gaps, keyboard bulge, laptop
rocking on a flat surface.
1. Stop charging; power off; don't press the case closed.
2. Remove only if it can be done without bending/puncturing; otherwise send
   whole unit to vendor/repairer.
3. Store in a fire-safe container (metal box, sand or a LiPo bag) away from
   combustibles until collection.
4. Never ship by normal post — damaged lithium cells are dangerous goods;
   use the vendor's/recycler's process.

## Replacement
- Order the exact part number from the service manual (wattage-hour and
  connector differ across sub-models).
- Shut down fully, unplug, ESD strap; disconnect battery connector before
  anything else.
- Internal batteries: screws plus sometimes adhesive pull-tabs; never pry
  with metal tools into cells.
- After fitting: boot, let it charge to 100 % uninterrupted once, update BIOS
  (battery firmware/charging logic ships in BIOS).

## Battery longevity settings
Vendor charge limits (Dell "Primarily AC use", Lenovo "Conservation mode",
HP "Battery Care") cap charge at ~80 % for docked laptops — reduces
swelling on always-plugged machines. Push via vendor management tools.

## Disposal
Lithium-ion batteries go to an approved battery recycler/WEEE collection,
terminals taped. Never household waste or general e-waste skips.

## Verify
New battery report shows full charge ≈ design capacity, Windows shows
"plugged in, charging" then 100 %, and the old battery is logged to the
recycling/disposal record.
