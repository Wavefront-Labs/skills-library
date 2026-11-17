---
id: manufacturing-production.electronics-semiconductor-manufacturing.ict-functional-test.test-failure-triage-to-repair
name: test-failure-triage-to-repair
category: manufacturing-production
field: electronics-semiconductor-manufacturing
product: ict-functional-test
tags: [ict-functional-test, ict, in-circuit-test, bed-of-nails, fixture, flying-probe, functional-test, fct, boundary-scan, jtag, keysight-3070, teradyne, takaya, spea, test-yield, first-pass-yield, fpy, false-failure, retest, nff, no-fault-found, repair-ticket, failure-analysis, pcba, debug, pareto, test-coverage]
level: practitioner
status: draft
description: "Triage ICT, flying-probe and functional test failures: separate fixture and contact faults from real defects, write a repair ticket that points at the part, and stop retest-until-pass."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Test failure triage to repair

**Goal:** every failing board leaves the test station with a **specific, correct
repair instruction** — and test-station problems (fixtures, probes, programs) are
fixed at the station instead of being shipped to the repair bench as "board faults".

## 1. The first question: board or tester?
Before blaming the board:
- **Same failure on several consecutive boards** at the same node → suspect fixture
  (worn/bent pogo pin, dirty probe, broken wire) or a program/limit issue, or a
  systemic process defect (wrong reel). Check a known-good board.
- **Failure moves** between runs on the same board → contact problem. Clean the probes,
  check vacuum/pneumatic hold-down, inspect for flux residue on test pads.
- **Opens test failing** across many pins of one connector → fixture alignment.
- Run the station's **self-test/fixture verification** at shift start; many ICT
  platforms have a fixture diagnostic.

## 2. Retest policy — the rule that protects yield numbers
"Retest until it passes" hides fixture faults and intermittent defects. Set a rule:
- One retest allowed after reseating the board; a second failure goes to repair/debug.
- Log **first-pass yield** (first attempt only), not final yield. A gap between FPY
  and final yield is the size of your hidden contact problem.

## 3. Reading the failure
- **ICT** reports by component and node: shorts, opens, wrong value (R/C/L out of
  limits), diode/transistor orientation, powered digital/analog tests. A short report
  names nodes — map them to the layout to find the bridge (often an adjacent fine-pitch
  pin pair).
- A **wrong value** on a passive is often a measurement artefact from a parallel path;
  check whether the test is "guarded" and whether the limit was set on a real board
  population. Only send to repair if the value is genuinely off.
- **Flying probe**: slower, no fixture, good for NPI and low volume; probe-mark and
  contact issues on small pads are common.
- **Boundary scan (JTAG)**: chain integrity fails first — if the chain is broken, the
  "fails" downstream mean nothing. Fix the chain (TCK/TMS/TDI/TDO path, device power).
- **Functional test**: fails are symptoms ("no boot", "current too high"). Check power
  rails and current draw first, then clocks, then programming/firmware, then the
  failing subsystem.

## 4. The repair ticket
A good ticket says: board serial, station, test step, measured vs limit, **suspected
component reference designator(s)** and suspected defect type (bridge, missing,
reversed, wrong value), plus a picture if available. "Failed FCT" is not a ticket.
After repair, the board goes back through the **same test**, not a later one.

## 5. Close the loop
Pareto failures weekly by refdes and defect type. Recurring failures at the same
location are a process issue (print, placement, a supplier lot) — send them to process
engineering, not to the repair bench forever. Track **NFF (no fault found)** returns
from repair: a high NFF rate means test is producing false failures.

## Gotchas
- Electrostatic damage during debug is a real cause of new failures — ESD discipline
  at the repair bench too.
- Programming a board twice (firmware) can mask a flash fault; log every attempt.
- Limits loosened to "get boards out" during a crisis are rarely tightened again —
  record them as temporary deviations with an expiry.

## Verify
- [ ] Known-good board passes the station at shift start.
- [ ] FPY reported alongside final yield; retest rule followed.
- [ ] Every repair ticket names refdes and defect type.
- [ ] Repaired boards retested on the failing station.
- [ ] Top-5 failure Pareto reviewed weekly with process engineering.

*Draft: platform-specific tools (Keysight i3070, Teradyne, Takaya, SPEA) differ in
report formats; this is the general method.*
