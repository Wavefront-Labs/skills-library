---
id: business-finance.general-management.business-process-improvement.process-mapping-and-bottleneck-analysis
name: process-mapping-and-bottleneck-analysis
category: business-finance
field: general-management
product: business-process-improvement
tags: [general-management, business-process-improvement, process-mapping, swimlane, value-stream-mapping, vsm, lean, lean-office, bottleneck, theory-of-constraints, flow-efficiency, lead-time, touch-time, rework, percent-complete-accurate, gemba, sop, continuous-improvement, kaizen]
level: practitioner
status: draft
description: "Map an office process as it really runs with swimlanes, measure touch vs wait time and flow efficiency, locate the bottleneck, and redesign and pilot the fix."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Process mapping and bottleneck analysis — find where office work actually waits

**Goal:** draw how a process really runs today, measure where time goes, and fix the
constraint rather than polishing steps that don't matter.

## 1. Scope the process
Write one line each: **trigger** (what starts it), **output** (what "done" means for
the customer), **customer**, and **boundaries** (first and last step in scope).
Pick a process with volume and pain: invoice approval, onboarding, quote-to-order.

## 2. Map the current state — with the people who do it
- Walk the process ("gemba walk") or follow one real item end to end. Documentation
  and managers describe the intended process; staff describe the real one.
- Use a **swimlane map**: one lane per role/team, boxes for steps, diamonds for
  decisions, arrows for hand-offs. Sticky notes on a wall or a whiteboard tool beat
  a diagramming tool at this stage.
- Capture loops explicitly: rework, "send back for correction", approvals that
  bounce. These are usually where the time goes.
- Map the common path first, then the top 2–3 exceptions by volume.

## 3. Add the data
For each step record:
- **Process (touch) time** — hands-on minutes.
- **Wait time** before the step (queue, inbox, awaiting approval).
- **% complete and accurate** — share of items arriving at the next step needing no
  correction.
- Volume and who does it.
Then compute **flow efficiency = total touch time ÷ total lead time**. Office
processes are often under 10–15%: most lead time is waiting, so speeding up people
achieves little. *(Typical-range claim from lean literature; measure your own.)*

## 4. Find the bottleneck
The bottleneck is the step with the **largest queue in front of it** or the lowest
throughput capacity. Signs: work piles up before it, downstream steps wait idle, and
it is often a single approver or specialist. Improving any other step does not
improve end-to-end throughput.

## 5. Redesign (future state)
Apply in this order:
1. **Eliminate** steps that add no value for the customer (duplicate checks,
   re-keying, approvals nobody refuses — check approval rejection rates; under ~1%
   suggests a rubber stamp).
2. **Reduce hand-offs**; each hand-off adds a queue.
3. **Fix quality at source** — a checklist or validated form at intake removes
   downstream rework.
4. **Relieve the bottleneck**: protect its time, give it only clean work, add
   capacity or delegate thresholds (e.g. approvals under a limit go to a deputy).
5. **Standardise** the new way in an SOP, then automate stable steps last.

## 6. Pilot and measure
Run the new process on a subset for 2–4 weeks; compare lead time, touch time, %C&A
and volume against the baseline. Then roll out and update the SOP.

## Gotchas
- Mapping the ideal instead of reality — always validate with an actual item.
- Automating a broken process: you get the same rework faster.
- Ignoring exceptions: 20% of cases may take 80% of the effort.
- Measuring averages only; track the 85th–90th percentile lead time too.

## Verify
- [ ] Map was validated by walking at least one real item through every step.
- [ ] Each step has touch time, wait time and %C&A; flow efficiency is calculated.
- [ ] The bottleneck is identified by queue/throughput evidence, not opinion.
- [ ] The future state removes steps or hand-offs, not just renames them.
- [ ] A pilot compared before/after lead time and the SOP was updated.
