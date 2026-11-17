---
id: repair-maintenance.consumer-electronics-repair.laptop-pc-repair.no-power-triage-and-thermal-service
name: no-power-triage-and-thermal-service
category: repair-maintenance
field: consumer-electronics-repair
product: laptop-pc-repair
tags: [laptop-pc-repair, laptop-repair, pc-repair, desktop-repair, no-power, no-post, no-display, beep-codes, post-codes, debug-led, cmos-battery, ec-reset, psu-tester, atx-psu, paperclip-test, thermal-paste, repaste, thermal-pads, liquid-metal, fan-cleaning, overheating, throttling, hinge-repair, ram-upgrade, ssd-upgrade, nvme, memtest86, hwinfo]
level: practitioner
status: draft
description: "Triage laptops and desktops that won't power, POST or stay cool: charger, EC reset, minimal-config boot, PSU and RAM tests, then repaste, pads, fan cleaning and hinge fixes."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# No-power triage and thermal service for laptops and PCs

**Goal:** split "dead" machines into charger, power, board, RAM, or display faults in
under 30 minutes, and do a thermal service that actually lowers temperatures.

## 1. Define "dead"
Note exactly: any LED? fan spin? caps-lock blink pattern or beeps? display backlight?
Each narrows the fault:
- **No LED, no fan:** power input (charger, DC jack, battery, board input stage).
- **Fans spin, black screen:** no POST (RAM, CPU/board, BIOS) or no display (panel,
  cable, backlight). Shine a torch at the screen — a faint image means backlight.
- **Blink or beep pattern:** a POST code; look it up in the maker's service manual.
  Desktops: a debug LED or a 2-digit POST card says where it stopped.

## 2. Laptop power triage
1. Measure the charger at the plug under no load (19–20 V barrel) or on a USB-C
   meter (should negotiate 15/20 V). A meter reading 5 V only means no PD negotiation.
2. Remove battery (or unplug it internally) and try charger only, and vice versa.
3. **EC / power drain reset:** unplug everything, hold power 30–60 s. Many Lenovo,
   Dell and HP models have a pinhole or internal reset; it clears latched protections.
4. Minimal config: one RAM stick, no SSD, no peripherals. Try each RAM slot.
5. Still no life: board-level — see
   repair-maintenance.consumer-electronics-repair.electronics-fault-diagnosis.power-rail-tracing-and-short-finding.

## 3. Desktop power triage
1. PSU: swap with a known-good unit, or use a PSU tester. The paperclip test (green
   PS_ON to black) only proves the fan spins, not the rails under load.
2. Check 24-pin and the 4/8-pin CPU connector are both fully seated — the most common
   "no POST" after a build.
3. Breadboard outside the case on the motherboard box: CPU, one RAM stick, PSU,
   speaker. Rules out case shorts and standoffs.
4. Clear CMOS (jumper or remove coin cell for 5 minutes) after RAM/CPU changes; some
   boards take several minutes of memory training on first boot — wait before calling it.
5. **Never open an ATX PSU** to repair unless trained: the primary capacitor holds
   mains-level voltage after unplugging.

## 4. Thermal service
1. Baseline: log CPU/GPU temperature and clocks with HWiNFO (Windows) or
   `sensors`/`s-tui` (Linux) under 10 minutes of load.
2. Disconnect battery. Remove the heatsink by its numbered screw order, loosening in
   reverse.
3. Clean old paste with IPA and lint-free wipes. Note thermal pad thickness with
   calipers before removing (common 0.5, 1.0, 1.5 mm). Wrong thickness = no contact
   on the die.
4. Paste: a pea-sized dot or thin spread on bare laptop dies; good non-conductive
   paste only. Liquid metal is electrically conductive and eats aluminium — only on
   copper coolers with insulated surrounds, and only if you know the risks.
5. Fans: hold the rotor still while blowing dust out (spinning a fan with air can
   generate back-voltage and wreck bearings). Clean the fin stack; it is usually the
   real blockage.
6. Retighten in the numbered order, evenly. Re-run the baseline load test.

## 5. Hinges and upgrades
- Hinges: cracked lid mounts or broken brass inserts cause the "lid peeling open".
  Re-glue inserts with epoxy or use repair brackets; tight, seized hinges break the
  case — lubricate or replace the hinge pair.
- RAM: check if soldered first. Run MemTest86 for at least one full pass after any
  RAM change.
- SSD: confirm M.2 key and length (2242/2280), NVMe vs SATA, and clone or reinstall.

## Gotchas
- Swollen laptop batteries lift trackpads: replace, do not compress them back.
- A charger that "works on another laptop" may still lack the ID pin signal for
  this one (Dell/HP barrel ID pins) and charge slowly or not at all.
- Repaste does nothing if the fan or heatpipe is failed; if temperatures don't move,
  check fan RPM and replace the heatsink assembly.
- (Draft note: reset procedures differ by model; the service manual wins.)

## Verify
- [ ] Machine POSTs and boots repeatedly from cold, on battery and on charger.
- [ ] Battery charges and the OS reports the charger correctly (wattage).
- [ ] Load test temperatures lower than baseline with no throttling.
- [ ] MemTest86 pass with no errors after RAM work.
- [ ] Hinges open and close smoothly with no flex at the lid mounts.
