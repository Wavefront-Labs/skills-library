---
id: manufacturing-production.production-line-operations.conveyor-batching-systems.balancing-conveyor-flow-buffers-and-batch-dosing
name: balancing-conveyor-flow-buffers-and-batch-dosing
category: manufacturing-production
field: production-line-operations
product: conveyor-batching-systems
tags: [conveyor-batching-systems, production-line-operations, conveyor, accumulation, accumulation-table, buffer, line-balancing, v-curve, bottleneck, starved, blocked, back-pressure, photo-eye, batching, dosing, weigh-batching, loss-in-weight, in-flight, preact, blockage, bridging, rat-holing, hopper, conveyor-safety, nip-points]
level: practitioner
status: draft
description: "Keep material flowing on conveyor and batching systems: set speeds around the bottleneck, manage accumulation buffers, tune dosing preact/in-flight, and clear blockages without injury."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Balancing conveyor flow, buffers and batch dosing

**Goal:** keep the bottleneck machine running 100% of the time it can, by running the
conveyors and buffers around it correctly, and meter batches to weight without
overshoot. Applies to packaging/bottling lines, bulk-solids plants and mixing rooms.

## 1. Find and protect the bottleneck
- The **bottleneck** (the constraint) is the machine with the lowest effective rate —
  on filling/packing lines it is normally designed to be the filler. An hour lost there
  is an hour lost for the line; an hour lost elsewhere may be absorbed by buffers.
- Classic line design runs machines in a **V-curve**: upstream and downstream machines
  are rated faster than the constraint (often by roughly 10–25% per step outward;
  check your line's design figures) so they can refill and empty buffers after a stop.
- So: if your speed settings make the upstream run slower than the filler, you have
  moved the constraint. Don't "balance" everything to the same speed.

## 2. Read the line state
Each machine is either **running, starved** (no input), **blocked** (output full) or
**down** (own fault). Look at the HMI states or simply walk the line:
- Filler starved → the problem is upstream. Filler blocked → downstream.
- Only fix the machine that is *down*; the others are symptoms.

## 3. Accumulation and buffers
- Accumulation tables, tray stackers and buffer conveyors absorb short stops. Their
  photo-eyes typically signal **low / normal / high / full** to the machine controls
  (e.g. full → slow or stop upstream; low → slow the downstream to save the buffer).
- Run buffers **half full** in steady state for a stop on either side. A buffer that is
  always full upstream of the constraint means the upstream is fine; one that is always
  empty means it is a hidden constraint.
- Back-pressure damages product (glass chipping, cans denting, labels scuffing).
  Zero-pressure accumulation or lower conveyor speed fixes this; increasing speed
  doesn't.
- Don't move or "adjust" photo-eye positions to clear a nuisance stop — they set the
  logic. Report it.

## 4. Batch dosing to target
For weigh batching (ingredient into a hopper or mixer on load cells):
- **Coarse/fine feed:** fast feed until ~90–95% of target, then dribble feed to cut-off.
- **In-flight / preact:** material still falling when the valve closes. The controller
  closes early by the preact amount. If batches consistently overshoot, preact is too
  small; undershoot, too large. Most controllers adapt it automatically — make sure
  auto-preact is on and has a sensible limit.
- Tare before each dose; check the scale with a test weight at the frequency your
  quality plan sets.
- **Loss-in-weight feeders** (continuous dosing) refill periodically; during refill
  they run volumetrically, so too-frequent refills hurt accuracy.

## 5. Blockages in bulk material
- Hoppers: **bridging** (an arch over the outlet) and **rat-holing** (a channel through
  the middle) come from moisture, fines or compaction. Vibrators/air pads help;
  hammering the hopper wall dents it and makes it worse.
- **Never** rod or reach into a hopper, chute, screw or conveyor without isolation and
  lockout. Moving conveyors and screws cause entanglement and amputation; a
  bridged hopper can release suddenly. Confined-space rules apply to entering bins.
- Find the cause: wet feedstock, wrong grade, worn liner, failed vibrator.

## 6. Conveyor basics to check on rounds
Belt tracking (belt drifting toward one edge), spillage under transfer points, noisy
or seized rollers, guards on nip points and tail pulleys, pull-cord e-stops working.

## Verify
- [ ] You know which machine is the constraint and its rated speed.
- [ ] Upstream/downstream speeds sit above the constraint, not equal to it.
- [ ] Buffers are around half full in steady running.
- [ ] Batch weights within tolerance with auto-preact on; scale checked.
- [ ] No one entered a hopper/conveyor without lockout.

*Uncertain: V-curve percentages and buffer sensor behaviour differ by line design
— use the OEM's line specification.*
