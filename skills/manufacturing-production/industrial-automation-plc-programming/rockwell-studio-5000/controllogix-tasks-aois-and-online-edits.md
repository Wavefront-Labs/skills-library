---
id: manufacturing-production.industrial-automation-plc-programming.rockwell-studio-5000.controllogix-tasks-aois-and-online-edits
name: controllogix-tasks-aois-and-online-edits
category: manufacturing-production
field: industrial-automation-plc-programming
product: rockwell-studio-5000
tags: [rockwell-studio-5000, studio-5000, rslogix-5000, logix-designer, rockwell, allen-bradley, controllogix, compactlogix, plc, ladder-logic, structured-text, add-on-instruction, aoi, udt, user-defined-type, continuous-task, periodic-task, event-task, rpi, ethernet-ip, produced-consumed-tags, online-edit, test-edits, assemble-edits, factorytalk-view, alias-tags, major-fault, minor-fault, industrial-automation-plc-programming]
level: practitioner
status: draft
description: "Organise a ControlLogix/CompactLogix project in Studio 5000: tasks and RPIs, UDTs and Add-On Instructions, safe online edits (test/assemble), and the faults that stop a line."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# ControlLogix tasks, AOIs and online edits in Studio 5000

**Goal:** build an Allen-Bradley Logix project that is predictable in timing, reusable
through UDTs/AOIs, and safe to edit while production runs.

*Draft: based on Studio 5000 Logix Designer v30–v36 practice; check the exact
behaviour of your firmware revision (major revision must match the project).*

## 1. Tasks and timing
- One **continuous task** at most (the default MainTask). It runs as fast as it can and
  is pre-empted by everything else.
- Put control that needs a fixed rate (PID via `PIDE`, analog filtering, motion
  planning helpers) in a **periodic task** (e.g. 10–100 ms). Check the task's
  *Max scan* in Task Properties › Monitor; if max scan approaches the period you get
  overlaps (a minor fault and lost executions).
- **Priorities:** lower number = higher priority (1–15). Don't make everything priority 1.
- **I/O RPI** (Requested Packet Interval) on each EtherNet/IP module sets how often data
  updates — independent of scan. An input read in a 5 ms task off a 20 ms RPI module
  only changes every 20 ms. Lower RPIs cost network bandwidth/CIP connections.

## 2. Data design
- **UDTs** for every repeated object (motor, valve, station). Note: editing a UDT that's
  in use is **not possible online** on most versions — plan UDT changes for downtime.
- **Add-On Instructions (AOIs)** package a UDT-like interface plus logic: inputs,
  outputs, InOut parameters, local tags. Use them for device templates (motor control,
  valve with feedback timeout). AOIs **cannot be edited online** either; changing one
  means a download. Version them (Revision field + note) and keep a library.
- **Alias tags** map I/O (`Local:3:I.Data.4`) to names (`Conv1_PE_Infeed`). Program
  against aliases; then swapping a card only means re-pointing aliases.
- **Program-scoped vs controller-scoped:** keep tags program-scoped unless genuinely
  shared; use **Program Parameters** (v24+) for clean interfaces between programs.
- **Produced/consumed tags** for PLC-to-PLC data; size them < 500 bytes per connection
  and use a UDT so both ends match.

## 3. Online edits without stopping the line
1. Go online, confirm the project is **matched** (no "offline file differs"). Upload if
   unsure — never download someone else's stale file to a running plant.
2. Right-click the rung › **Start pending rung edits**. Edit. **Accept** (verifies,
   sends to controller but old logic still runs).
3. **Test Accepted Program Edits** — new logic now executes; old logic is kept. Watch
   the machine. **Untest** returns instantly to the old logic if it misbehaves.
4. **Assemble** to make it permanent; then **save** (and save to the controller image
   if your site uses SD card storage, e.g. "Load image: On power-up" settings).
5. New tags can be created online; changing a tag's data type cannot.

Structured text and function block routines support online edits too, but the
test/untest step is per-program, not per-rung — read the dialog.

## 4. Faults that stop a line
- **Major fault** (controller faults to Program mode): array index out of range
  (Type 4 Code 20), unhandled divide etc. Defend with bounds checks, or a
  **Controller Fault Handler** program that logs and (only if deliberately decided)
  clears specific codes.
- **Module connection faults**: an I/O module set to "Major fault on controller if
  connection fails in Run mode" will stop the whole PLC when one remote rack drops.
  Decide per module.
- **Keyswitch:** REM position allows remote mode changes; RUN locks them. Know which
  your site requires.

## Gotchas
- Firmware major revision in project ≠ controller → can't go online until you change
  the project revision or flash (ControlFLASH). Flashing clears the program.
- **FactoryTalk View** tags read by name — renaming a tag silently breaks the HMI. Use
  the cross-reference before renaming.
- Disabled rungs (`AFI`) left in production confuse the next engineer; comment why.

## Verify
- [ ] Periodic task max scan < ~50% of its period.
- [ ] After edits: assembled, saved, project file matches controller.
- [ ] No unexplained minor faults in Controller Properties › Minor Faults.
- [ ] I/O module fault behaviour chosen deliberately for each remote rack.
- [ ] HMI screens still resolve every tag (no "?" / error indicators).
