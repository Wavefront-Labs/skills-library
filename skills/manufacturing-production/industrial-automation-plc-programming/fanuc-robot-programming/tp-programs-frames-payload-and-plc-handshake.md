---
id: manufacturing-production.industrial-automation-plc-programming.fanuc-robot-programming.tp-programs-frames-payload-and-plc-handshake
name: tp-programs-frames-payload-and-plc-handshake
category: manufacturing-production
field: industrial-automation-plc-programming
product: fanuc-robot-programming
tags: [fanuc-robot-programming, fanuc, fanuc-robot, r-30ib, r-30ib-plus, teach-pendant, tp-program, karel, user-frame, tool-frame, utool, uframe, tcp, three-point-method, six-point-method, payload, payload-identification, motion-instructions, fine, cnt, position-registers, pr, uop, ui-uo, di-do, gi-go, ethernet-ip, profinet, plc-handshake, style-select, pns, rsr, dcs, dual-check-safety, irvision, roboguide, industrial-automation-plc-programming]
level: practitioner
status: draft
description: "Program FANUC robots that run reliably in a cell: tool and user frames, payload setup, TP motion with FINE/CNT, position registers, and a clean PLC handshake over UOP and group I/O."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# FANUC TP programs, frames, payload and the PLC handshake

**Goal:** a FANUC robot (R-30iB/iB Plus/iD class) that runs a cell under PLC
control, survives re-teaching and tool crashes, and never moves unexpectedly.

*Draft: from general FANUC practice; menu paths and UOP defaults vary by controller
and software options. Always confirm on the pendant and in your safety risk
assessment — this skill does not replace FANUC training.*

## 1. Frames before points
- **Tool frame (UTOOL):** teach the TCP with the **six-point method** (three
  approaches to a fixed pin for XYZ, plus orientation points) on a rigid pointer.
  Record the result; enter it numerically for spare tools of the same design.
- **User frame (UFRAME):** teach with the **three-point** (origin, +X, +Y) method on
  the fixture's datum features. Teach all points *in* the user frame.
- Payoff: if the fixture moves or is replaced, re-teach three points of the frame and
  every program point follows. Points taught in UFRAME 0 (world) have to be re-taught
  one by one.
- Every program should select its frames explicitly at the top:
  `UFRAME_NUM=1 ;` `UTOOL_NUM=2 ;` — don't rely on whatever was active.

## 2. Payload
- Set mass, centre of gravity and inertia per tool/part combination
  (**PAYLOAD[n]** schedules; switch with `PAYLOAD[2]` after gripping a part).
- Wrong payload → collision detection false trips, poor path accuracy, reducer wear.
  Use **payload identification** (where licensed) to measure it.

## 3. Motion instructions
- `J P[1] 100% FINE` — joint move, stop exactly. `L P[2] 500mm/sec CNT50` — linear,
  blend through the point.
- **FINE** where the robot must actually arrive (pick, place, before I/O). **CNT** for
  approach/via points to save cycle time.
- I/O after a CNT point fires *before* the robot reaches it — a gripper opening early
  is the classic bug. Use FINE, or a TIME BEFORE/AFTER instruction if timing matters.
- Use **position registers** (PR[n]) for approach offsets: `L P[3] 200mm/sec FINE
  Offset,PR[5]` keeps one taught point plus a computed approach.

## 4. PLC handshake (pattern)
Use **UOP** signals (UI/UO) for robot state and **group I/O** (GI/GO) for data,
mapped onto the EtherNet/IP or PROFINET adapter.
1. PLC checks robot **CMDENBL** / ready, no fault, in AUTO.
2. PLC writes the **program/job number** to a GI, then pulses **start** (style/PNS
   selection or a custom handshake via DI). Robot echoes the job number on a GO.
3. Robot sets *In Cycle*, does the work, raises **job complete** (DO) and holds it.
4. PLC sees complete, drops the request; robot drops complete. Both sides time out
   if the other side doesn't respond within N seconds and raise a named fault.
5. For zones the robot and another machine share, use **interference zone**
   handshakes: robot requests entry, waits for the permit, releases when clear.
Keep the handshake identical across robots on the line — maintenance learns it once.

## 5. Safety
- Teach mode at reduced speed (T1 ≤ 250 mm/s), deadman held. AUTO only when the cell is
  clear and guarded.
- **DCS** (Dual Check Safety) position/speed limits are part of the safety function;
  changes need sign-off and re-validation. See
  `manufacturing-production.industrial-automation-plc-programming.machine-safety-systems.risk-assessment-to-performance-level-and-safety-validation`.

## Gotchas
- Backups: do an **All of above** backup to USB (or via FTP) before any change;
  include image backups for recovery.
- Singularity near wrist alignment (J5 ≈ 0°) on linear moves → slow or fault; reorient.
- Override % left at 30% after testing halves throughput — check before handover.
- **ROBOGUIDE** offline programs need touch-up on the real cell; frames rarely match.

## Verify
- [ ] Every program sets UFRAME/UTOOL explicitly; points taught in a user frame.
- [ ] Payload schedules match the actual tool with and without a part.
- [ ] No I/O action on a CNT point unless intentional.
- [ ] Handshake times out on both sides with a readable fault.
- [ ] Full backup on file from after the final change.
