---
id: manufacturing-production.chemical-process-manufacturing.honeywell-experion.console-operation-and-control-strategy-edits
name: console-operation-and-control-strategy-edits
category: manufacturing-production
field: chemical-process-manufacturing
product: honeywell-experion
tags: [honeywell-experion, experion-pks, experion, honeywell, dcs, distributed-control-system, control-builder, control-module, cm, sequential-control-module, scm, c300, pid-block, regcalc, station, hmiweb, hmiweb-display-builder, faceplate, point-detail, alarm-summary, alarm-shelving, operator-console, load, checkpoint, mode, man, auto, cas, process-control, chemical-plant]
level: practitioner
status: draft
description: "Run continuous plant from an Experion PKS Station (alarm summary, point detail, modes, shelving) and make a safe Control Builder edit and load to a C300 control module."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Experion PKS: console operation and safe control strategy edits

**Goal:** operate a continuous unit from an Experion Station competently, and make a
small Control Builder change to a running control module (CM) without upsetting the
process.

*Draft note:* names reflect Experion PKS R5xx as generally documented (Station,
Control Builder, C300, HMIWeb Display Builder). Release, licensing and your site's
security levels change what you see; follow site procedures and MOC.

## 1. The pieces
- **Station** — operator interface: custom HMIWeb displays, **Alarm Summary**, point
  **detail displays** and faceplates, trends, event summary.
- **Control Builder** — builds **Control Modules (CMs)** of function blocks
  (DATAACQ, PIDA, AUXCALC, REGCALC, logic) and **Sequential Control Modules (SCMs)**
  for step logic. Has a *Project* view (configured, offline) and a *Monitoring* view
  (what is loaded and running in the controller).
- **C300 / ACE / C200E** — the controllers that execute CMs.
- **HMIWeb Display Builder** — edits operator graphics (.htm-based displays).

## 2. Console operation essentials
1. **Start of shift:** walk the overview displays, then the Alarm Summary (sort by
   priority), then any **shelved/disabled** alarms list and the handover log. Know
   what is in MAN and why.
2. **Point detail** shows PV, SP, OP, MODE, MODEATTR (operator vs program) and alarm
   limits. Before acting on an alarm, check the PV against a related measurement and
   the trend — instrument fault or real process?
3. **Modes:** MAN (operator sets OP), AUTO (operator sets SP), CAS (SP from a
   primary). **MODEATTR = PROGRAM** means an application or SCM owns the loop —
   changing it from the console fights the program; find out first.
4. **Shelving:** use the Station's shelving with a reason and duration if your alarm
   philosophy allows it; review shelved alarms at every handover.
5. **Alarm flood:** stop acknowledging line-by-line; identify the initiating event
   (first-out or earliest alarm in the event summary) and stabilise that.

## 3. Making a CM change (Control Builder)
1. Open the CM in the **Project** tree; compare against the **Monitoring** tree. If
   they differ before you start, someone has unloaded edits or on-line changes —
   resolve that before adding yours.
2. Make the edit (parameter, wiring, block) in Project. Keep it minimal.
3. With the board operator, put affected loops in a safe state (usually MAN, holding
   output) — a CM load can re-initialise blocks.
4. **Load** the CM (right-click → Load, or Load with Contents as your site requires)
   to the controller. Read the load dialog: it says whether the CM will be
   inactivated during load. Most CM loads require the CM to go INACTIVE briefly.
5. Re-activate the CM, check in Monitoring view: block states, no bad PV, OP where it
   was. Return loops to AUTO/CAS with the trend on screen.
6. **Upload / update to project** any on-line parameter changes (e.g. tuning set from
   the faceplate) so the project matches the controller, and take a **checkpoint**
   per site practice so a controller restore does not bring back old values.

## 4. Gotchas
- A load from a stale Project overwrites tuning that operators changed on-line. Always
  reconcile Monitoring → Project before loading.
- Inactivating a CM that feeds others can shed their modes (CAS → AUTO/MAN).
- SCMs mid-step behave differently on reload; never load an SCM that is running a
  sequence without the procedure for it.
- Display edits are also changes: a mislabelled tag on an HMIWeb display has caused
  operators to move the wrong valve. Peer-check display changes.

## Verify
- [ ] Project and Monitoring reconciled before and after the change.
- [ ] Load dialog read; affected loops in safe mode during load and restored after.
- [ ] No bad PV / inactive blocks after activation; trend steady.
- [ ] Checkpoint saved; MOC/change record updated.
- [ ] Shelved alarms reviewed at handover with reasons and expiry.

Related: manufacturing-production.chemical-process-manufacturing.emerson-deltav.control-module-changes-and-alarm-handling
