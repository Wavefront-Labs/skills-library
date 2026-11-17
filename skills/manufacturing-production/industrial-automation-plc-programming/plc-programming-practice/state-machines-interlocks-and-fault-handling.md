---
id: manufacturing-production.industrial-automation-plc-programming.plc-programming-practice.state-machines-interlocks-and-fault-handling
name: state-machines-interlocks-and-fault-handling
category: manufacturing-production
field: industrial-automation-plc-programming
product: plc-programming-practice
tags: [plc-programming-practice, plc, plc-programming, iec-61131-3, ladder-logic, structured-text, sfc, state-machine, sequence, step-sequencer, case-statement, interlocks, permissives, fault-handling, first-out, alarm-latching, reset, isa-88, packml, omac, module-states, code-structure, naming-convention, double-coil, scan-cycle, one-shot, edge-detection, watchdog-timer, industrial-automation-plc-programming]
level: practitioner
status: draft
description: "Write PLC logic maintenance can read: one state machine per module, separate permissives and interlocks, latched first-out faults with timeouts, and a structure that survives the 2am breakdown."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# State machines, interlocks and fault handling (vendor-agnostic)

**Goal:** control logic where the current step of every module is visible, every
output has one obvious place it's written, and every stall produces a named fault —
on any IEC 61131-3 platform (Siemens, Rockwell, CODESYS, etc.).

*Draft: distilled from common practice and PackML/ISA-88 ideas; adapt names to
your site standard if one exists — consistency beats elegance.*

## 1. Structure per module
For each machine module (infeed, press, robot cell) keep the same four sections, in order:
1. **Inputs** — map raw I/O to named, debounced, conditioned signals.
2. **Permissives/interlocks** — compute `OK_to_X` booleans.
3. **Sequence** — the state machine deciding what to do.
4. **Outputs** — write each physical output **once**, from sequence requests AND
   interlocks: `Motor_Run := Seq_Req_Run AND Run_Interlocks_OK;`

Writing an output in two places (the "double coil") means the last write wins and
nobody can follow it online. Search for it; eliminate it.

## 2. The state machine
- An integer/enum **step number** per module; in ST a `CASE` statement, in ladder one
  rung group per step with `EQU Step 30`. SFC is fine where the team reads SFC.
- Number steps in tens (`10, 20, 30…`) so you can insert `25` later.
- Each step: **action** (requests set while in this step), **transition condition**,
  **step timeout**. Transitions move the step number; actions are derived from it —
  don't latch outputs inside steps.
- Standard states around the sequence (PackML-like): `Idle → Starting → Execute →
  Completing → Complete`, plus `Stopping/Stopped`, `Aborting/Aborted`, `Held`.
  Even if you don't implement full PackML, have explicit **Stopped**, **Running** and
  **Faulted** and a defined way back to Home.
- Display the step number *and a text description* on the HMI. "Press waiting in step
  40: clamp closed sensor" saves a callout.

## 3. Interlocks vs permissives
- **Permissive:** must be true to *start* (guard closed, upstream ready).
- **Interlock:** must stay true to *keep running*; dropping it stops the action
  (overtravel, low lube pressure).
- **Safety functions don't live here.** E-stops and guard interlocking are in the safety
  PLC/relay; standard logic only *reads* their status. See
  `manufacturing-production.industrial-automation-plc-programming.machine-safety-systems.risk-assessment-to-performance-level-and-safety-validation`.

## 4. Fault handling
- **Every wait has a timeout.** Step timer starts on step entry; if the transition
  hasn't happened by T, raise a specific fault ("Clamp did not close in 2.0 s") and go
  to Faulted.
- **Feedback faults** on every actuated device: commanded but no feedback within T,
  or feedback without command.
- **Latch faults**, and clear them only with a reset *after* the condition is gone.
  Auto-clearing faults hide intermittent problems.
- **First-out capture:** freeze the first fault in a cascade so the HMI shows the cause,
  not the 14 consequences.
- On reset: return to a known state (usually Home or Stopped), never resume mid-step
  unless the step is designed for it.

## 5. Readability rules
- Names say what it is and its sense: `Clamp_Closed_PS` not `I_3_4`; avoid negatives
  like `Not_Stop`.
- Rung/line comments explain **why**, not what the instruction does.
- Use one-shots (rising edges) for counts and events; a level-triggered counter counts
  every scan.
- No magic numbers — timeouts and setpoints are named parameters, ideally HMI-adjustable
  within limits.
- Remember the **scan**: inputs read, logic solves top-down, outputs write. A bit set
  late in the scan is not seen by earlier logic until next scan.

## Gotchas
- Forcing I/O to "get it running" and forgetting the force. Check forces before leaving.
- Sequences that rely on a sensor never failing — always ask "what if it stays on?"
- Copy-pasted modules with one address not changed. Prefer FBs/AOIs + UDTs.

## Verify
- [ ] Every physical output is written in exactly one place.
- [ ] Every sequence step has a timeout and a named fault.
- [ ] HMI shows current step text for each module.
- [ ] Faults latch and need reset after the condition clears.
- [ ] No forces active at handover.
