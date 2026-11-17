---
id: manufacturing-production.production-quality-control.nonconformance-root-cause.containment-and-8d-problem-solving
name: containment-and-8d-problem-solving
category: manufacturing-production
field: production-quality-control
product: nonconformance-root-cause
tags: [nonconformance-root-cause, nonconformance, ncr, nonconformance-report, mrb, material-review-board, disposition, use-as-is, rework, repair, scrap, concession, deviation-permit, containment, quarantine, 8d, eight-disciplines, a3, 5-why, five-whys, fishbone, ishikawa, is-is-not, root-cause-analysis, rca, occurrence-and-escape, corrective-action, capa, preventive-action, effectiveness-check, poka-yoke, customer-complaint, scar, supplier-corrective-action, production-quality-control]
level: practitioner
status: draft
description: "Handle defective output end to end: write the NCR, contain fast, disposition properly, run an 8D with is/is-not, fishbone and 5-why for occurrence and escape, then prove the fix worked."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Containment and 8D problem solving

**Goal:** stop defective product reaching the customer today, then make sure the same
problem can't happen again — with evidence. The 8D (Eight Disciplines, Ford origin)
structure is the common automotive/industrial format; A3 and DMAIC cover the same logic.
Workplace-safety RCA is a different domain (law-government occupational health skills).

## 1. Write the NCR (minutes, not days)
- **What**: part/product, revision, lot/serials, quantity, characteristic, requirement vs actual.
- **Where/when found**: station, process step, date/time, by whom, how (gauge, inspection).
- Photos, measurement data, and the physical parts tagged and segregated.
A good NCR is factual: "Ø12.05 measured, spec Ø12.00 ±0.02, 7 of 40 parts", not "holes oversize again".

## 2. Contain (D3) — within 24 h is a common customer expectation
Think about every place suspect product can be:
- At the machine and in WIP, finished goods stock, in transit, at the customer (and their customers' lines), at sub-tier suppliers.
- Define **suspect range** by time/lot since the last known good evidence.
- Quarantine + **100% sort** (or 200% for critical, two separate inspections) with a
  verified method. Mark sorted good parts so they're identifiable (e.g. a dot, a label "sorted").
- Record quantities: sorted, good, rejected. Track containment until the permanent fix is proven.

## 3. Disposition (MRB)
Options: **use-as-is** (needs engineering/customer concession if it deviates from spec),
**rework** (bring back to spec by approved method, re-inspect), **repair** (usable but
not to original spec — needs approval), **return to supplier**, **scrap**. Disposition
is by authorised people, documented on the NCR.

## 4. The 8D
| D | What to do |
|---|---|
| D0 | Emergency response, decide an 8D is warranted |
| D1 | Cross-functional team (production, quality, engineering, maintenance; the operator who knows the job) |
| D2 | Problem description: **is / is-not** (what, where, when, how many — and what's *not* affected) |
| D3 | Interim containment (above) |
| D4 | Root cause for **occurrence** *and* **escape** (why made, why not detected) — verify it |
| D5 | Choose permanent corrective actions; prove they address the root causes |
| D6 | Implement, remove containment once effectiveness shown |
| D7 | Prevent recurrence: update PFMEA, control plan, work instructions, similar parts/lines |
| D8 | Close and recognise the team |

## 5. Root cause tools
- **Is/is-not** narrows the search: "only cavity 3, only night shift, started 12 March, not on the sister machine" points somewhere.
- **Fishbone (Ishikawa)**: brainstorm under Man, Machine, Method, Material, Measurement, Environment — then test candidates with data.
- **5-why**: ask why from the defect until you reach a cause you can control and that
  explains all the is/is-not facts. Branch when there are several causes.
- **Verify** the root cause: turn the problem **on and off** (reproduce it with the cause,
  eliminate it without), or show data correlation strongly — otherwise it's a hypothesis.
- "Operator error" and "retrain operator" are almost never accepted as the root cause/fix;
  ask why the process allowed the error, and prefer **error-proofing (poka-yoke)**.

## 6. Effectiveness check
- Define upfront what proves the fix: e.g. zero recurrences over N lots/weeks, Cpk ≥ target, gauge R&R after fixture change.
- Close only when evidence is in. Reopen if it recurs.

## Gotchas
- Containing only the parts on the machine, not stock and in transit.
- 5-why that jumps to a convenient answer ("because of bad material") without data.
- Fixing occurrence but not escape — the next different defect also escapes.
- Many 8Ds stuck at D5 forever: assign owners and dates.

## Verify
- [ ] NCR has facts, quantities, evidence and tagged parts.
- [ ] Containment covers every location of suspect product, with counts.
- [ ] Disposition approved by authorised people; concessions documented.
- [ ] Root causes for occurrence and escape verified (on/off or data).
- [ ] PFMEA/control plan updated; effectiveness criteria met before closure.
