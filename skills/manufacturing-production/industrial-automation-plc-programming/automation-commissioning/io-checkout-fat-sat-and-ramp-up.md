---
id: manufacturing-production.industrial-automation-plc-programming.automation-commissioning.io-checkout-fat-sat-and-ramp-up
name: io-checkout-fat-sat-and-ramp-up
category: manufacturing-production
field: industrial-automation-plc-programming
product: automation-commissioning
tags: [automation-commissioning, commissioning, line-commissioning, io-checkout, point-to-point, loop-check, loop-test, fat, factory-acceptance-test, sat, site-acceptance-test, iec-62381, dry-run, wet-run, cold-commissioning, hot-commissioning, punch-list, ramp-up, oee, rate-run, performance-test, handover, as-built, redlines, mechanical-completion, pre-start-safety-review, loto, industrial-automation-plc-programming]
level: practitioner
status: draft
description: "Take a line from installed to production rate: mechanical completion, I/O checkout and loop tests, FAT/SAT protocols, dry and wet runs, punch-list control and a measured ramp-up to handover."
sources: ["IEC 62381 (FAT, FIT, SAT and SIT for automation systems)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# I/O checkout, FAT/SAT and ramp-up

**Goal:** an orderly path from "installed" to "handed over at rate", where every I/O
point is proven, every test has evidence, and nobody discovers a swapped wire at
3 a.m. on launch week.

*Draft: generic sequence; contract terms (what counts as acceptance) and regulated
industries (pharma CQV, GAMP) add requirements not covered here.*

## 1. Before power: mechanical completion
- Walk-down against drawings: every device installed, labelled, terminated, guarded.
- Insulation resistance (megger) of motor and field cables *with drives/electronics
  disconnected*; continuity of earthing.
- Pre-start safety review: guarding, E-stops, LOTO points identified, energy sources
  documented. Commissioning is when equipment is most dangerous — half-finished guards,
  people inside the cell, untested logic.

## 2. FAT (at the builder's site)
- Agreed **test protocol** written in advance: each function, how tested, expected
  result, signature box. Include safety functions, recipes, alarms, HMI navigation,
  fault recovery and comms with upstream/downstream (simulated if needed).
- Run with real product where possible; record cycle time and reject rates.
- Everything that fails goes on the **punch list** with owner and category
  (A = must fix before shipping, B = before SAT, C = before handover).
- FAT is cheaper than site fixes by a large factor — resist "we'll sort it on site".

## 3. I/O checkout on site (point-to-point)
Work from an exported I/O list (spreadsheet: tag, address, description, device, panel,
terminal, result, date, initials).
- **Digital inputs:** actuate the real device (block the photo-eye, make the prox),
  see the right tag change in the PLC/HMI. Don't jumper at the terminal — that proves
  the card, not the field wiring.
- **Digital outputs:** with the device mechanically safe, force/command the output, see
  the right valve/contactor act. Forcing is controlled: one person on the PLC, one at
  the device, radio contact, cleared after.
- **Analog loop check:** inject 4, 12, 20 mA (or simulate with the transmitter's test
  function) and check scaling at the HMI: 0%, 50%, 100% of range. Check the sign/units.
- **Motors:** bump for rotation direction before coupling where possible.
- **Networked devices:** confirm device name/IP, firmware, parameter set loaded.
Mark every row; anything not done is visible.

## 4. Dry run, then wet run
- **Dry run:** sequences without product (or with air/water instead of product).
  Prove each step, each timeout fault, each interlock, E-stop and restart behaviour.
- **Wet/product run:** first at reduced speed, single cycles, then continuous. Expect
  product-related issues: sensors tuned for the dummy part, jams on real tolerances.

## 5. SAT and ramp-up
- **SAT** repeats the critical FAT tests on site with the real utilities and
  interfaces; plus integrated tests with neighbouring machines.
- **Ramp-up:** define the curve up front (e.g. 50% of rate in week 1, 80% in week 3,
  100% at handover — numbers depend on the contract). Track **OEE** (availability ×
  performance × quality) per shift and a downtime Pareto; attack the top reason daily.
- **Rate run/performance test:** a continuous run of agreed length at rated speed with
  agreed availability and quality targets — the acceptance evidence.

## 6. Handover
- As-built drawings (redlines incorporated), final PLC/HMI/drive/robot backups,
  spare parts list, manuals, training records, closed punch list (or signed exceptions).

## Gotchas
- Changes during commissioning without version control → nobody knows which program
  is final. Back up at the end of every day with the date in the name.
- Temporary bypasses and forces left in at handover. Do a formal "forces and bypasses"
  check.
- Operators trained on a machine that isn't finished learn workarounds; train again at handover.

## Verify
- [ ] Every I/O row signed, with field device actuated (not jumpered).
- [ ] FAT and SAT protocols signed, punch list categorised and A items closed.
- [ ] Rate run meets agreed speed, availability and quality.
- [ ] No forces/bypasses active; final backups stored off the machine.
- [ ] As-builts and spares list delivered.
