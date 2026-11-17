---
id: manufacturing-production.production-line-operations.line-changeover-smed.running-a-smed-changeover-study
name: running-a-smed-changeover-study
category: manufacturing-production
field: production-line-operations
product: line-changeover-smed
tags: [line-changeover-smed, production-line-operations, smed, single-minute-exchange-of-die, shingo, changeover, setup-reduction, quick-changeover, internal-external, setup-time, tooling-staging, changeover-checklist, first-off, first-article, spaghetti-diagram, video-analysis, quick-release, standard-work, lean, oee-availability]
level: practitioner
status: draft
description: "Cut changeover time with SMED: film and time a real changeover, split internal vs external work, convert and streamline, then lock it into a checklist with first-off verification."
sources: ["Shingo, S. A Revolution in Manufacturing: The SMED System (1985)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Running a SMED changeover study

**Goal:** take a changeover that costs, say, 90 minutes of a stopped line and make it
reliably shorter *and* right first time, using Shingo's single-minute exchange of die
(SMED) method. "Single minute" means under ten minutes — a direction, not a promise.

**Changeover time is defined as last good part of product A to first good part of
product B at full rate.** Time anything shorter (e.g. "tools swapped") and you hide
the run-up and adjustment, which is usually the biggest chunk.

## 1. Capture the current changeover
- Pick the most frequent or most painful changeover. Agree the start/stop definition
  above with the team.
- **Video it** (with the crew's agreement — tell them it is the process under study,
  not them) and run a stopwatch log. Track the lead operator; if several people work,
  film each or use a wide shot.
- Draw a **spaghetti diagram** of walking. Walking to fetch tools is a classic
  20–30% of a changeover.

## 2. Break it into elements
Watch the video with the operators and list every step with start time and duration:
"fetch die cart 3:40", "loosen 8 bolts 6:10", "trial and adjust 22:00". Their
commentary is where the ideas come from.

## 3. Separate internal from external
- **Internal** = can only be done with the machine stopped.
- **External** = can be done while the machine is still running the previous product.
Mark each element. Typically a lot of "internal" work is really external done at the
wrong time: finding tools, fetching the next tooling, pre-heating, getting paperwork,
reading the spec, waiting for QC.
Move all external work to a **pre-changeover checklist** completed before the last
good part of A. This step alone often cuts the time a lot without any spend.

## 4. Convert internal to external
Ask of each remaining internal step: what would let us do this off the machine?
- Pre-heat dies or moulds on a separate heater.
- Pre-assemble tooling into a subassembly or **standard-height** plate so it locates
  without shimming.
- Pre-set tools off-line on a gauge or presetter.
- Duplicate a cheap change part so the next one is ready.

## 5. Streamline what stays internal
- **Fasteners:** a bolt only needs one turn to clamp; use quarter-turn, cam clamps,
  U-slots, captive or quick-release fixings. Standardise sizes so one tool fits all.
- **Eliminate adjustment:** locating pins, fixed stops, marked scales, recipe
  setpoints — replace "tweak until it looks right" with "set to 42 mm on the scale".
  Trial-and-adjust is usually the biggest single internal block.
- **Parallel work:** two people on opposite sides with a defined split (watch safety:
  never two people with one isolation unless the LOTO procedure covers group lockout).

## 6. Standardise and verify
- Write the new sequence as **changeover standard work**: pre-changeover checklist
  (external), internal steps in order with who does what, post-changeover checklist
  (line clearance of old materials and labels, settings check, first-off).
- **First-off verification:** first good product measured/inspected and signed before
  release at rate. Line clearance matters most where mixed product = recall
  (labels, allergens, pharma).
- Track every changeover time on a run chart; a sudden rise means the checklist is
  being skipped.

## Gotchas
- Speed at the expense of first-off quality just moves the loss into scrap.
- Changeover time falls, then batch sizes must fall too, or the gain sits unused.
- Don't let the "study" become a one-off kaizen: re-film after 3 months.

## Verify
- [ ] Start/stop defined as last good A to first good B at rate.
- [ ] Each element classed internal or external, with times.
- [ ] Pre-changeover checklist done before the line stops.
- [ ] Adjustments replaced by fixed settings where possible; first-off signed.
- [ ] Changeover time trended after the study.

See also engineering-technology.industrial-manufacturing-systems-engineering.lean-six-sigma.value-stream-mapping-and-flow-design.
