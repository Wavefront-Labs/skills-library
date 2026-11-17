---
id: manufacturing-production.assembly-line-hand-work.torque-controlled-fastening.dc-tool-torque-sequences-and-fastener-error-proofing
name: dc-tool-torque-sequences-and-fastener-error-proofing
category: manufacturing-production
field: assembly-line-hand-work
product: torque-controlled-fastening
tags: [torque-controlled-fastening, assembly-line-hand-work, torque, fastening, dc-tool, dc-nutrunner, transducerised-tool, clutch-screwdriver, shut-off-tool, pulse-tool, torque-angle, angle-monitoring, tightening-strategy, torque-sequence, cross-pattern, hard-joint, soft-joint, joint-rate, rundown, nok, ok-nok, bolt-count, socket-tray, position-control, torque-arm, audit-torque, residual-torque, torque-wrench, iso-5393, iso-6789]
level: practitioner
status: draft
description: "Fasten at a line station with controlled tools: choose clutch vs DC tools, follow the tightening sequence, read OK/NOK results, handle rejects, and audit residual torque with a wrench."
sources: ["ISO 5393 (rotary tools for threaded fasteners - performance test)", "ISO 6789 (hand torque tools)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# DC tool torque sequences and fastener error-proofing

**Goal:** every fastener at the station is present, run down and tightened to spec, in
the right order, with a record — and a missed or bad one stops the unit before it moves
on. Torque is only a proxy for **clamp load** (most of the torque goes into friction), so
the method and consistency matter as much as the number.

## 1. Know the tools
- **Click/clutch screwdrivers (air or electric):** a clutch slips at a set torque.
  Simple, cheap, no data unless fitted with a signal output. Accuracy depends on
  setting and the joint.
- **Shut-off air nutrunners:** stop at torque; better than stall tools.
- **DC electric (transducerised) tools:** measure torque and angle each rundown and
  report **OK/NOK** to a controller; can run multi-step strategies and feed the MES.
  The standard for safety-critical and traceable joints.
- **Pulse tools:** fast and low reaction, but torque control is less precise unless
  transducerised.
- **Torque arm / reaction bar:** use one on high torque — reaction kicks injure wrists.

## 2. Joint behaviour
- **Hard joint** (metal-to-metal): torque rises steeply over a few degrees.
- **Soft joint** (gasket, plastic, springs): torque rises over many turns.
Tools are tested to both (ISO 5393 uses ~30° and ~360°+ joints); a tool set on a
hard joint can **overshoot or undershoot** on a soft one. Set and verify on the real
joint.

## 3. The tightening strategy and sequence
- Typical DC strategy: fast rundown → slow down near seating → final step to target
  torque, with **angle monitoring** (an acceptance window of degrees after a snug
  threshold). Torque OK but angle low = cross-thread or already tightened; torque OK
  but angle high = stripped, missing washer, soft joint.
- For multi-bolt joints (flanges, covers, wheels), follow the **sequence** in the
  instruction — usually a **cross/star pattern**, often in two or more passes
  (e.g. snug all, then final all). Tightening round the circle distorts the part and
  leaves the first bolts loose.
- **Position control:** some stations use an articulated arm with encoders, or the
  controller's bolt counter, so the tool only enables at the next bolt in the sequence.

## 4. Error-proofing at the station
- **Bolt count:** the controller expects N OK rundowns on this unit; it won't release
  the unit (or the next station) until it has them.
- **Socket tray / selector:** lifting the wrong socket disables the tool or selects the
  matching program.
- **Parts presence:** pick-to-light or fastener counting feeders show a missed screw.
- **Re-hit protection:** a second rundown on an already-tight fastener gives a
  "double hit" NOK rather than counting it again.
Never re-zero the counter or move the unit on by override unless you have the
authority and record why.

## 5. Handling NOK
1. Stop; read the result (torque low/high, angle low/high).
2. Follow the station's NOK procedure: typically back off and re-run once if allowed,
   or replace the fastener (some — torque-to-yield bolts, thread-locked, plastic
   threads — must never be reused).
3. A second NOK = send to repair/quarantine with a tag, and call the team leader.
4. Repeated NOKs at one position = check fastener lot, part threads, tool, socket wear.

## 6. Audits and calibration
- **Residual (audit) torque:** at intervals, a quality tech checks fasteners with a
  calibrated click or digital wrench, measuring **breakaway** or the **"crack-on"**
  torque to further tighten. Residual torque reads differently from dynamic torque,
  so use the plant's audit method and limits.
- Tools and wrenches calibrated on schedule (wrenches per ISO 6789); DC tools checked
  with a transducer on a joint simulator.

## Verify
- [ ] Tool program/socket matches the fastener on the instruction.
- [ ] Sequence and passes followed; bolt count complete before release.
- [ ] Every NOK handled by procedure and recorded.
- [ ] Residual torque audit within limits; tools in calibration.

*Uncertain: angle windows, re-run rules and audit limits are specific to each joint
and plant — none are universal.*
