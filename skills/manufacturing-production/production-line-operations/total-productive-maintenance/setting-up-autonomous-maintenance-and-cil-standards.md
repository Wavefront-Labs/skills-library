---
id: manufacturing-production.production-line-operations.total-productive-maintenance.setting-up-autonomous-maintenance-and-cil-standards
name: setting-up-autonomous-maintenance-and-cil-standards
category: manufacturing-production
field: production-line-operations
product: total-productive-maintenance
tags: [total-productive-maintenance, production-line-operations, tpm, autonomous-maintenance, jishu-hozen, cil, cleaning-inspection-lubrication, initial-clean, defect-tags, red-tag, blue-tag, f-tags, abnormality-tagging, sources-of-contamination, hard-to-access, one-point-lesson, opl, minor-stops, six-big-losses, tpm-pillars, tpm-audit, planned-maintenance, nakajima]
level: practitioner
status: draft
description: "Start TPM autonomous maintenance on a machine: initial clean and defect tagging, fix contamination sources, write a CIL standard operators can do in minutes, and audit it step by step."
sources: ["Nakajima, S. Introduction to TPM (1988)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Setting up autonomous maintenance and CIL standards

**Goal:** operators keep their own machine in basic condition — clean, tight, lubricated,
inspected — so small deterioration is caught before it becomes a breakdown, and
maintenance technicians are freed for planned and skilled work. This is the
**autonomous maintenance** (jishu hozen) pillar of TPM, usually the first one started.

## 1. Know the losses you're attacking
TPM's **six big losses**: breakdowns, setup/adjustment, minor stops and idling, reduced
speed, startup rejects, production rejects. Autonomous maintenance mostly hits
breakdowns and minor stops — the ones caused by dirt, looseness, lack of lubrication
and unnoticed wear. Track them (see
manufacturing-production.production-line-operations.oee-performance-monitoring.calculating-oee-and-building-a-loss-pareto)
before you start so you can show the effect.

## 2. Pick a model machine
Start on **one** machine that matters (the bottleneck or the worst breakdown record),
with a team of its operators across shifts plus one maintenance tech. Make it the
showcase; roll out after it works.

## 3. Step 1: initial clean — "cleaning is inspection"
- Isolate and lock out (every person their own lock). Open guards with maintenance.
- Clean **everything**, down to bare paint, including where nobody normally looks.
- As you clean, **tag every abnormality** with a visible tag and log it: oil leak,
  loose/missing bolt, cracked hose, worn belt, unreadable gauge, missing guard, dirt
  source. Common convention: one colour for operator-fixable, another for maintenance
  (often white/blue vs red — check your site's convention).
- A first clean on a neglected machine routinely finds 50–150 tags. That list is the
  value; work it down and chart open vs closed tags.

## 4. Step 2: sources of contamination and hard-to-access areas
Dirt comes back unless its source is fixed: guard the spray, fix the leak, add a
chip shield or a drip tray. And make cleaning and inspection easy: clear guard panels or
inspection windows, relocated grease points, centralised lubrication, removable covers
with quarter-turn fasteners.

## 5. Step 3: write the CIL standard
For each item: **what, how, tool, standard (what "good" is), frequency, time, who.**
Example line: "Main drive chain — check tension by deflection at marked mid-point —
fingers — 10–15 mm — weekly — 1 min — operator."
- Keep the **daily** CIL to a few minutes (e.g. 5–10 min per shift); longer will be
  skipped under production pressure.
- Use **visual controls** so inspection is a glance: match-marks on bolts (paint
  stripe across bolt and part), green/red bands on gauges, lubricant type and level
  labels, flow-direction arrows, sight glasses.
- Teach each check with a **one-point lesson** (OPL): one page, one topic, mostly
  photo, taught in 5–10 min at the machine.
- Lubrication: right lubricant (label every point with type/colour code), right
  quantity. Over-greasing bearings damages seals and causes heat — the CIL must say
  how many shots.

## 6. Audit and advance
Audit each step formally (team leader then manager) before moving to the next of the
typical seven AM steps (initial clean → contamination sources → CIL standards →
general inspection → autonomous inspection → standardisation → autonomous management).
Pass criteria: tags closed above a set percentage, CIL done on schedule, condition
maintained.

## Gotchas
- An initial clean with no maintenance capacity booked to close red tags kills
  operator trust.
- CIL sheets signed but not done ("pencil-whipping") — audit by physically checking
  a sample of items, not the paperwork.
- Operators must not do work requiring maintenance skill/authorisation (electrical,
  safety devices). The split is defined, not assumed.

## Verify
- [ ] Baseline breakdown/minor-stop data captured before starting.
- [ ] Initial clean done under LOTO; tags logged and trended to closure.
- [ ] Contamination sources fixed, not just cleaned.
- [ ] CIL lists what/how/standard/frequency/time; daily part ≤10 min.
- [ ] Step audits passed before moving on.
