---
id: business-finance.project-and-program-management.program-management.benefits-realisation-and-dependencies
name: benefits-realisation-and-dependencies
category: business-finance
field: project-and-program-management
product: program-management
tags: [project-and-program-management, program-management, programme-management, benefits-realisation, benefits-realization, benefits-map, benefits-register, benefits-dependency-network, dependency-management, dependency-register, program-governance, steering-committee, sro, tranches, msp, business-case, outcomes, change-management, roadmap]
level: practitioner
status: draft
description: "Run a program for outcomes: benefits maps and register with business owners, cross-project dependency registers, tranche governance and post-closure benefits tracking."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Benefits realisation and cross-project dependency management

**Goal:** run a program so that its projects together deliver the business benefits
that justified it — not just outputs on time — and so the dependencies between
projects don't silently derail them.

## 1. Programs vs projects
A **project** delivers outputs (a system, a building, a process). A **program**
coordinates related projects and change activities to achieve **outcomes and
benefits** (lower cost-to-serve, more revenue, compliance) that no single project
delivers alone. The program manager owns the joins between projects and the path
from outputs to benefits.

## 2. Map outputs → outcomes → benefits
Build a **benefits map** (or benefits dependency network), working right to left:
```
strategic objective ← benefits ← business changes/outcomes ← enablers/outputs (projects)
```
Example: "Reduce cost-to-serve by 15%" ← "30% fewer calls per customer" ← "customers
self-serve address changes" ← "new portal (Project A) + process redesign (Project B)
+ call-centre retraining (change activity)".
Business changes (people doing things differently) are where benefits are usually
lost; they need owners just like projects do.

## 3. Define each benefit properly
For each benefit: description, **measure**, **baseline**, **target**, timing (benefits
often arrive months after go-live), **benefit owner** (a business manager who will
own it after the program closes — not the program manager), dependencies, and
dis-benefits (things that get worse, e.g. temporary productivity dip).
Record in a **benefits register**; agree with finance how cash benefits are counted
and whether they'll come out of budgets.

## 4. Dependency management
- Build a **dependency register**: from (project/deliverable) → to, what's needed,
  need-by date, promised date, owner on each side, status.
- Types: technical/data, resource (shared specialists), decision (policy sign-off),
  external (vendor, regulator).
- Visualise as a dependency map or program roadmap with linked milestones; review
  weekly at the program level. Any slip in a "from" date triggers impact analysis on
  the "to" project immediately.
- Reduce dependencies where you can (re-scope, decouple interfaces, stub/mocks) — the
  cheapest dependency is the one you remove.

## 5. Governance and cadence
- **Program board/steering committee** (sponsor/SRO, benefit owners, key suppliers):
  monthly; decisions on priorities, tranches, funding, cross-project trade-offs.
- **Program team** (project managers, change lead, PMO): weekly; dependencies,
  risks, integrated plan.
- Organise delivery into **tranches** that each release a usable capability and some
  benefits; review the business case at each tranche end — continue, change or stop.

## 6. Realisation and handover
Track benefit measures from go-live; report realised vs planned. Before program
closure, transfer remaining benefit tracking to benefit owners with a review date.
Post-closure benefits reviews (e.g. 6–12 months on) close the loop.

## Gotchas
- **Benefits written to justify funding** and never measured afterwards.
- Program manager as benefit owner — accountability leaves when the program closes.
- Double counting the same saving in two projects' business cases.
- Dependencies tracked only inside each project's plan; nobody owns the joins.
- Status "green" on every project while the program outcome is at risk.

## Verify
- [ ] Benefits map links each project output to outcomes and benefits.
- [ ] Each benefit has measure, baseline, target, timing and a business owner.
- [ ] Dependency register has both-side owners and need-by vs promised dates.
- [ ] Tranche reviews revisit the business case.
- [ ] Benefits tracking continues past closure with a scheduled review.
