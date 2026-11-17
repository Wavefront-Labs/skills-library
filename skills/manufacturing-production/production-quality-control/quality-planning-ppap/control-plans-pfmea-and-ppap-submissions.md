---
id: manufacturing-production.production-quality-control.quality-planning-ppap.control-plans-pfmea-and-ppap-submissions
name: control-plans-pfmea-and-ppap-submissions
category: manufacturing-production
field: production-quality-control
product: quality-planning-ppap
tags: [quality-planning-ppap, ppap, production-part-approval-process, apqp, aiag, iatf-16949, psw, part-submission-warrant, submission-level-3, process-flow-diagram, pfmea, process-fmea, aiag-vda-fmea, action-priority, rpn, control-plan, special-characteristics, cc, sc, dimensional-results, ballooned-drawing, msa, initial-process-studies, ppk, run-at-rate, capacity-verification, appearance-approval-report, aar, imds, safe-launch, gp12, production-quality-control]
level: practitioner
status: draft
description: "Get a part approved for volume: build the process flow, PFMEA and control plan as a linked set, run the studies, assemble a PPAP Level 3 package with PSW, and pass run-at-rate."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Control plans, PFMEA and PPAP submissions

**Goal:** prove to the customer, before volume production, that your process makes good
parts consistently at the quoted rate — and leave behind a control plan the floor
actually follows. Based on AIAG PPAP 4th edition, AIAG-VDA FMEA (2019) and IATF 16949;
customer-specific requirements (CSRs) override the generic manuals — read them first.

## 1. The linked set: flow → PFMEA → control plan
Every process step should appear with the same number in all three documents.
1. **Process flow diagram**: receiving to shipping, including inspection, rework loops,
   storage and transport steps (rework and handling are where many failures start).
2. **PFMEA**: for each step, functions/requirements → failure modes → effects (with severity) →
   causes → current prevention and detection controls → occurrence/detection ratings →
   **Action Priority (H/M/L)** in AIAG-VDA (replacing RPN-only ranking in the old AIAG 4th edition).
   High severity (9–10, safety/regulatory) needs strong prevention regardless of other scores.
3. **Control plan**: for each step, characteristic (product and process), **special
   characteristic symbol** (customer-defined: e.g. critical/significant), spec/tolerance,
   evaluation method (gauge), sample size and frequency, control method (SPC, poka-yoke,
   100% check), **reaction plan**. Control plan phases: prototype, pre-launch, production.
Detection controls listed in the PFMEA must match what's in the control plan.

## 2. Studies you need before submission
- **Dimensional results**: all characteristics on the ballooned drawing, typically on a
  set number of parts per cavity/process stream (often 5 or per CSR) — see
  manufacturing-production.production-quality-control.dimensional-inspection-metrology.first-article-inspection-with-hand-tools-and-surface-plate.
- **MSA** for gauges in the control plan (gage R&R, attribute agreement).
- **Initial process studies**: Ppk on special characteristics from a significant production
  run (PPAP manual references ≥ 100 readings / 25 subgroups); typical acceptance **Ppk ≥ 1.67**
  (1.33–1.67 conditional, < 1.33 not acceptable without customer agreement).
- **Material/performance test results**, lab scope/accreditation evidence.
- **Appearance Approval Report** if appearance items exist.
- **IMDS** material data submission where required (automotive).

## 3. PPAP package (18 elements; Level 3 default)
Design records, engineering change docs, customer engineering approval (if required),
DFMEA (if design responsible), process flow, PFMEA, control plan, MSA, dimensional results,
material/performance results, initial process studies, qualified lab documentation, AAR,
sample product, master sample, checking aids, CSR compliance records, and the **Part Submission
Warrant (PSW)** summarising and declaring it. **Level 3** = PSW + samples + complete supporting data
submitted; other levels vary what's submitted vs retained.

## 4. Run-at-rate (capacity verification)
- Run production at quoted rate with production tooling, people, gauges and materials, for
  the agreed period (e.g. a shift or 300 parts — customer-specific; GM, Ford and Stellantis each define it).
- Record output, downtime, scrap, and compare against quoted daily/weekly capacity
  including OEE assumptions.
- Shortfalls need an action plan before PPAP approval.

## 5. After approval
- **Safe launch / early production containment** (e.g. GP-12 style additional inspection)
  for the initial period.
- Any change to process, location, sub-supplier, material or tooling needs customer
  notification and usually re-PPAP. Changes without notification are a serious breach.
- PFMEA and control plan are **living**: update them after every NCR/8D.

## Gotchas
- Copying a PFMEA from another part without walking the actual line.
- Control plan frequencies that the floor can't physically do.
- Capability studies from a hand-picked short run.
- Special characteristics on the drawing missing from the control plan.
- Submitting PSW with open items not declared.

## Verify
- [ ] Process steps numbered identically across flow, PFMEA and control plan.
- [ ] Every special characteristic has a control method, gauge with acceptable MSA, and reaction plan.
- [ ] Ppk ≥ CSR target on special characteristics from a representative run.
- [ ] All 18 elements present/retained per required level; PSW signed.
- [ ] Run-at-rate met quoted capacity or has an approved plan.
