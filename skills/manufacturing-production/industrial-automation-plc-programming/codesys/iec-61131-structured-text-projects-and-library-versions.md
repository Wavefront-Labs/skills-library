---
id: manufacturing-production.industrial-automation-plc-programming.codesys.iec-61131-structured-text-projects-and-library-versions
name: iec-61131-structured-text-projects-and-library-versions
category: manufacturing-production
field: industrial-automation-plc-programming
product: codesys
tags: [codesys, codesys-v3, iec-61131-3, structured-text, st, twincat, twincat-3, beckhoff, schneider-machine-expert, wago, ifm, plc, function-block, method, property, interface, oop, task-configuration, library-manager, library-versions, placeholder-libraries, persistent, retain, online-change, login, boot-application, ethercat, canopen, gvl, dut, industrial-automation-plc-programming]
level: practitioner
status: draft
description: "Build maintainable CODESYS/TwinCAT projects in structured text: POU and DUT layout, task configuration, library version pinning, persistent data, and online change versus full download."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# IEC 61131-3 structured text projects and library versions in CODESYS

**Goal:** a CODESYS V3 project (or a derivative: Beckhoff TwinCAT 3, Schneider Machine
Expert, WAGO e!COCKPIT/CODESYS, ifm, etc.) that builds the same next year, survives
an online change, and keeps its retained data.

*Draft: generic CODESYS V3.5 SP1x behaviour. Derivatives rename menus and differ in
targets (TwinCAT runs on Windows/TwinCAT/BSD real-time); check your vendor's notes.*

## 1. Project layout
- **POUs:** Programs (one per machine module), Function Blocks (devices, sequences),
  Functions (stateless maths). Group in folders: `Devices/`, `Modules/`, `Utils/`.
- **DUTs:** `STRUCT` for data records, `ENUM` (with `{attribute 'qualified_only'}` and
  `{attribute 'strict'}`) for states, so `E_State.Running` can't collide or be
  assigned a raw integer.
- **GVLs** only for I/O mapping and genuinely global config. Pass everything else
  through FB inputs/outputs or `VAR_IN_OUT`.
- **OOP extensions** (methods, properties, `INTERFACE`, `EXTENDS`) are useful for
  device families, but keep inheritance one level deep — maintenance staff must still
  follow it online.

## 2. Task configuration
- Default: one cyclic `MainTask`. Add a faster task only for what needs it (e.g. 1–2 ms
  for EtherCAT motion via SoftMotion/NC, 10 ms for control loops).
- Each task calls programs explicitly; a program not in any task **does not run** — a
  common "why is nothing happening" cause.
- Watch **Task monitoring** (cycle time, jitter, max). If the watchdog is enabled and
  exceeded, the runtime stops the application — set it sensibly, don't disable it.
- Data shared between tasks of different priority can tear mid-write; copy into the
  task at its start, or use the vendor's synchronisation (e.g. `SysSem`, mutexes) for
  multi-word structures.

## 3. Libraries: pin versions
- Library Manager › each library shows a version or `*` (newest installed). **Never
  ship with `*`.** Set the exact version so another PC builds the same code.
- **Placeholder libraries** resolve via the device description; a new device
  description can silently change the resolved version. Check after updating a device.
- Export a **project archive** (File › Project Archive › Save/Send) including
  libraries and device descriptions — the `.project` file alone won't build elsewhere.

## 4. Retained data
- `VAR RETAIN` survives warm reset/power cycle; `VAR PERSISTENT` (declared in a
  **Persistent Variables** list) also survives a new download. Recipes, counters and
  calibrations belong there.
- After adding a variable to the persistent list, the layout changes — on many runtimes
  persistent values are re-initialised if the list structure no longer matches. Add new
  entries at the end; never reorder.

## 5. Login: online change vs download
- On login with changes, CODESYS offers **Login with online change**, **Login with
  download** (stops the application, reinitialises non-retained data) or no change.
- Online change is refused or risky when: FB instance layout changes heavily, task
  config changes, or library versions change. It also can't safely move a running
  state machine — handle states that disappear.
- Afterwards create the **boot application** (Online › Create boot application, or
  enable implicit creation) — otherwise a power cycle runs the *old* code.

## Gotchas
- ST `:=` vs `=`: `IF x = 5` compares; `x := 5;` assigns. An `IF x := 5` won't compile,
  but `bDone = TRUE;` alone compiles in some versions as a pointless expression
  (warning only) — read warnings.
- Integer overflow wraps silently (`INT` 32767 + 1 = −32768). Use `DINT`/`LREAL` for
  accumulators.
- Timers (`TON`) must be called every cycle; calling inside an `IF` freezes them.
- EtherCAT/CANopen slave ESI/EDS files must match the actual device revision.

## Verify
- [ ] No library shows `*` in the Library Manager.
- [ ] Every program appears under a task; task max cycle < watchdog with margin.
- [ ] After online change, boot application updated (power-cycle test on a stop).
- [ ] Persistent data survived a test download on the bench.
- [ ] Project archive opens and builds on a clean PC.
