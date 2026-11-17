---
id: manufacturing-production.industrial-automation-plc-programming.siemens-tia-portal.s7-1500-project-structure-scl-and-online-changes
name: s7-1500-project-structure-scl-and-online-changes
category: manufacturing-production
field: industrial-automation-plc-programming
product: siemens-tia-portal
tags: [siemens-tia-portal, tia-portal, siemens, step-7, s7-1500, s7-1200, simatic, plc, scl, structured-text, ladder, lad, fbd, ob1, ob35, cyclic-interrupt, function-block, instance-db, optimized-block-access, data-block, udt, plc-data-type, download, download-without-reinitialization, snapshot, online-offline-compare, profinet, device-name, plcsim, wincc, industrial-automation-plc-programming]
level: practitioner
status: draft
description: "Structure an S7-1500/1200 project in TIA Portal: OBs, FBs with instance DBs, PLC data types, SCL vs LAD choice, and downloading changes without stopping or reinitialising the line."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# S7-1500 project structure, SCL and safe online changes in TIA Portal

**Goal:** lay out a Siemens S7-1500 (or S7-1200) program so it is readable, reusable
and can be changed while the line runs, without losing retained data or tripping the CPU.

*Draft: written from general TIA Portal V16–V19 practice; menu names shift between
versions and the reinitialisation rules depend on firmware. Confirm on PLCSIM first.*

## 1. Block architecture
- **OB1 (Program cycle)** only *calls* things — no logic in it. One call per machine
  module (`Infeed`, `Press`, `Outfeed`), each an FB with its own instance DB.
- **Cyclic interrupt OB (OB30–OB38, e.g. OB35 at 100 ms)** for anything time-sensitive:
  PID (`PID_Compact`), totalisers, filtered analog scaling. Do not put PID in OB1 —
  its scan time wanders.
- **OB100 (Startup)** sets known initial states. **OB82/OB86/OB121/OB122** exist for
  diagnostics; on S7-1500 a missing error OB does *not* stop the CPU the way it did on
  S7-300, so do not rely on "CPU went to STOP" to tell you something failed.
- **FB vs FC:** FB when the block has memory (timers, states, edge bits); FC for pure
  calculation. An FC with a static-looking variable is a bug factory.
- **PLC data types (UDTs)** for every repeated structure (a motor, a valve, a recipe).
  Change the UDT once; every instance updates.

## 2. Language choice
- **LAD/FBD** for interlocks and permissives maintenance electricians will read online.
- **SCL** for maths, loops over arrays, string handling, state machines (`CASE #state OF`).
  Keep SCL blocks short; online monitoring of SCL is harder for a night-shift tech.
- Use symbolic names everywhere. With **optimized block access** (default on new
  blocks) absolute addresses like `DB10.DBX2.0` don't exist — HMI and third-party
  drivers must use symbolic access. Untick "Optimized" only for legacy S7 comms
  (e.g. some older SCADA drivers), and say so in the block comment.

## 3. Downloading changes to a running PLC
1. **Go online, Compare** (right-click CPU › Compare › Offline/online). Know exactly what
   differs before downloading. If someone changed the PLC from another laptop, upload
   or merge first — never blind-overwrite.
2. Take a **snapshot of actual values** of important DBs (DB › Snapshot), so you can
   restore setpoints/counters if a DB gets reinitialised.
3. Enable **"Download without reinitialization"** (block property, *Memory reserve*):
   set a memory reserve on FBs/DBs you expect to extend, and then *add* tags only into
   the reserve area. Changing a tag's type, deleting a tag or reordering usually forces
   reinitialisation of that DB — the dialog will say "reinitialize" — read it.
4. In the download preview, the default for a running CPU may be **"Stop modules"**.
   Choose "No action" where offered; if the change requires STOP, schedule it.
5. Changes to **hardware configuration** (module, IP, PROFINET topology) generally need
   a STOP. Plan them for a stop window.

## 4. PROFINET gotchas
- Devices are found by **device name**, not IP. A replacement drive or I/O head with a
  blank name won't come up until named (Online › Assign device name), unless topology
  is configured so the CPU can auto-name the replacement ("support device replacement
  without exchangeable medium").
- Firmware mismatch between project and real module gives a "compatible" warning or a
  red module; match the configured version or use the newest the hardware accepts.

## 5. Gotchas that bite
- **Retentive memory:** only tags marked *Retain* survive power loss; counters for
  production totals must be retentive.
- **Know-how protection** on library blocks hides logic — keep the password in the
  plant's credential store, not with one integrator.
- **Edge detection in FCs** (`R_TRIG` needs an instance) — use it in FBs, or the edge
  memory is shared/lost.
- Archive with **Project › Archive (.zap)** before every site change; version the
  archives with date and TIA version (projects upgrade one way only).

## Verify
- [ ] OB1 contains only FB calls; time-critical logic lives in a cyclic OB.
- [ ] Offline/online compare shows identical after download.
- [ ] The download dialog did not reinitialise any DB holding counters or recipes
      (or you restored them from a snapshot).
- [ ] CPU stayed in RUN; diagnostics buffer shows no new errors.
- [ ] A .zap archive of the as-left project exists with the TIA version in its name.
