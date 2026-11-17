---
id: manufacturing-production.chemical-process-manufacturing.emerson-deltav.control-module-changes-and-alarm-handling
name: control-module-changes-and-alarm-handling
category: manufacturing-production
field: chemical-process-manufacturing
product: emerson-deltav
tags: [emerson-deltav, deltav, dcs, distributed-control-system, control-studio, deltav-explorer, deltav-operate, live, control-module, function-block, pid-block, ai-block, ao-block, download, online-edit, mode, auto, man, cas, alarm-management, alarm-suppression, alarm-shelving, deltav-batch, phase-logic, isa-88, isa-18-2, moc, chemical-plant, process-control]
level: practitioner
status: draft
description: "Change a DeltaV control module safely on running plant (Control Studio edit, download, mode handling) and handle alarms properly from the operator station without hiding real problems."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# DeltaV: changing a control module on live plant and handling alarms

**Goal:** make a small configuration change (a tuning value, an alarm limit, a block
parameter) to a running DeltaV control module without bumping the process, and work
the alarm list from the operator station in a way that keeps alarms meaningful.

*Draft note:* menu names below reflect DeltaV v13–v15 and DeltaV Live/Operate as
generally documented; your site's version, security keys and procedures win. Never
change running control without your site's MOC and permission rules.

## 1. Know the tools
- **DeltaV Explorer** — the configuration tree (areas, nodes, modules, I/O).
- **Control Studio** — opens a module's function-block diagram (AI → PID → AO, plus
  calc, logic, SFC blocks) for editing and **on-line** viewing.
- **DeltaV Operate / DeltaV Live** — operator graphics, faceplates, alarm banner and
  alarm list.
- **Diagnostics** — node/controller/I/O health; check it before blaming the logic.
- **DeltaV Batch** — recipes, phases (phase logic modules) and the batch executive.

## 2. Change vs download: the core distinction
- Many parameters (setpoint, mode, tuning gains, alarm limits on some blocks) can be
  **written on-line** from the faceplate or Control Studio on-line view. These are
  runtime values: they are **not** in the database and a later download can overwrite
  them with the configured value. Record the change and update the configuration too,
  or upload the live value if your site permits.
- Structural edits (adding a block, rewiring, changing block options) need a
  **download** of the module (or the controller). A module download re-initialises
  that module's blocks; depending on version and edit type, PID blocks may reset or
  jump mode.

**Before any download on live plant:**
1. Read the **download preview / differences** report — it lists exactly what will
   change. Unexpected items mean someone else has pending edits; stop and find out.
2. Put the loop in a safe state with the board operator: usually **MAN** at the
   current output, so a re-initialised PID cannot move the valve.
3. Download the **module**, not the whole controller, unless the change demands it.
4. Check the module on-line: no bad status (BAD/UNCERTAIN), no "config error", outputs
   where they were. Return to AUTO/CAS with the operator watching the trend.

## 3. Modes you must read correctly
`MODE.TARGET` is what was asked; `MODE.ACTUAL` is what the block is doing. Target AUTO
with actual IMAN or LO means something upstream/downstream (an interlock, a bad
input, a shed from CAS) is holding it — fix the cause, don't just re-request AUTO.
**CAS** means setpoint comes from another block; **RCAS/ROUT** means from a remote
application. A loop that keeps shedding from CAS to AUTO usually has a bad primary.

## 4. Handling alarms at the console
1. **Acknowledge** means "I have seen it" — not "it is fixed". Ack, then act.
2. Work highest priority first; the banner shows the newest, the alarm list sorts by
   priority/time — use the list during a flood.
3. Read the **faceplate and trend** before responding: is the PV real (compare a
   redundant transmitter or a field check) or an instrument fault?
4. **Suppress/shelve** only under your site's alarm philosophy (ISA-18.2 style): with
   a reason, an expiry, and a log entry. A shelved alarm forgotten across a shift
   change is a classic incident precursor — hand over every shelved/suppressed alarm.
5. Chattering or standing alarms are a configuration problem: raise them for
   rationalisation (deadband, on/off delay, limit review) rather than living with them.

## 5. Gotchas
- An on-line tuning change that was never put in the database vanishes on the next
  download, months later, with a different engineer.
- Downloading a module that is referenced by a running batch phase can abort or hold
  the phase; coordinate with batch operations.
- Alarm limits changed in the faceplate may need the alarm-limit security key and are
  still a change under MOC.
- "Bad PV" propagates: a failed transmitter can drive the PID to its configured
  fault-state action. Know what each loop does on bad input.

## Verify
- [ ] Download differences reviewed and matched the intended change only.
- [ ] Loop placed in a safe mode before the download, returned after, trend checked.
- [ ] On-line value changes also captured in the configuration (or documented).
- [ ] MODE.TARGET equals MODE.ACTUAL for touched loops.
- [ ] Every shelved/suppressed alarm has a reason, an expiry and a handover entry.

Related: manufacturing-production.chemical-process-manufacturing.control-room-operation.alarm-floods-trends-and-shift-handover
