---
id: manufacturing-production.production-line-operations.oee-performance-monitoring.calculating-oee-and-building-a-loss-pareto
name: calculating-oee-and-building-a-loss-pareto
category: manufacturing-production
field: production-line-operations
product: oee-performance-monitoring
tags: [oee-performance-monitoring, production-line-operations, oee, overall-equipment-effectiveness, availability, performance, quality, ideal-cycle-time, planned-production-time, teep, loss-tree, six-big-losses, downtime-logging, downtime-codes, pareto, micro-stops, minor-stops, shift-report, shift-handover, kpi, line-performance]
level: practitioner
status: draft
description: "Calculate OEE correctly (availability x performance x quality), avoid the common inflation tricks, log downtime with usable codes, and turn it into a loss Pareto and a shift report."
sources: ["Nakajima, S. Introduction to TPM (1988)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Calculating OEE and building a loss Pareto

**Goal:** a number for how much of a line's possible good output you actually got, plus
a ranked list of where the rest went, so the shift and the improvement team work on the
biggest loss rather than the loudest one.

## 1. The calculation
Over **planned production time** (shift time minus planned breaks/meetings, and
minus no-orders time if your site excludes it — decide and write it down):

- **Availability** = run time ÷ planned production time
  (run time = planned time − all stops: breakdowns, changeovers, material waits).
- **Performance** = (ideal cycle time × total count) ÷ run time
  (equivalently total count ÷ (run time × ideal rate)).
- **Quality** = good count ÷ total count (first-pass good; reworked units are *not* good).
- **OEE = A × P × Q** — or directly: (good count × ideal cycle time) ÷ planned time.

Worked example: 480 min shift, 30 min breaks → 450 min planned. Stops 60 min → run
390 min → A = 86.7%. Ideal rate 100/min (0.6 s cycle); count 34,000 → P = 34,000 ÷
(390 × 100) = 87.2%. Rejects 700 → Q = 33,300 ÷ 34,000 = 97.9%. OEE = 74.0%.
Check: 33,300 ÷ (450 × 100) = 74.0%. Always do the direct check — it catches errors.

## 2. Keep the number honest
- **Ideal cycle time** = the machine's design/nameplate or proven best sustainable rate
  — not "what we normally run". Setting it to the usual speed hides speed loss and gives
  performance near 100%.
- Don't exclude changeovers or "small stops" from planned time to look better. If you
  must report a variant, label it.
- Performance > 100% means the ideal rate is wrong.
- Benchmarks like "85% world class" are rough and process-dependent; compare a line to
  its own trend, not to another plant.

## 3. Logging downtime so you can use it
- **Automatic capture** of stop start/end from the PLC where possible; operator assigns
  the reason. Manual logs miss most short stops.
- Short **minor stops** (under a threshold, e.g. 2–5 min) often appear only as
  performance loss. Count their frequency even if you don't code each one — 200 stops
  of 30 s is 100 minutes.
- A reason-code tree two or three levels deep: *Breakdown → Filler → Capper head*.
  Keep the top level to ~8–12 options. "Other" over ~10% of downtime means the codes
  are wrong or not enforced.
- Record the **machine that caused it**, not the one that stopped (a starved filler is
  not a filler fault).

## 4. Loss tree and Pareto
1. Convert every loss to the same unit — **minutes of lost time** (or lost units):
   speed loss minutes = run time − (count × ideal cycle time); quality loss minutes =
   rejects × ideal cycle time.
2. Build the tree: planned time → availability losses (by category/machine), performance
   losses (minor stops, slow running), quality losses (startup rejects, running rejects).
3. **Pareto** the bottom level over at least a few weeks: sorted bars plus cumulative
   line. The top 2–3 bars typically hold most of the loss; that's where the kaizen or
   TPM effort goes.

## 5. The shift report and handover
On one page: OEE and A/P/Q vs target, good output vs plan, top 3 losses with minutes and
actions taken, open issues for the next shift, safety and quality events. Review it at
a short start-of-shift meeting at the line board.

## Gotchas
- Averaging OEE across lines of different speeds by simple mean is wrong — weight by
  planned time (or sum good-output × ideal-time over sum planned time).
- An OEE gain from slowing the ideal rate is fake.
- Don't use OEE to compare operators; it drives under-reporting of stops.

## Verify
- [ ] A × P × Q equals the direct (good × ideal ÷ planned) figure.
- [ ] Ideal cycle time is design/best rate; P never exceeds 100%.
- [ ] "Other" is a small share of downtime.
- [ ] Pareto built on weeks of data, in minutes, and drives the action list.
