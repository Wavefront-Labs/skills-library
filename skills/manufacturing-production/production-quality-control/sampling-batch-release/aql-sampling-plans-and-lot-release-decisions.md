---
id: manufacturing-production.production-quality-control.sampling-batch-release.aql-sampling-plans-and-lot-release-decisions
name: aql-sampling-plans-and-lot-release-decisions
category: manufacturing-production
field: production-quality-control
product: sampling-batch-release
tags: [sampling-batch-release, acceptance-sampling, aql, acceptable-quality-limit, iso-2859-1, ansi-asq-z1-4, mil-std-105e, z1-9, iso-3951, sample-size-code-letter, inspection-level, general-inspection-level-ii, normal-tightened-reduced, switching-rules, ac-re, accept-reject-numbers, c-equals-zero, squeglia, oc-curve, lot-release, quarantine, hold-tag, incoming-inspection, receiving-inspection, in-process-inspection, final-inspection, certificate-of-analysis, coa, coc, skip-lot, production-quality-control]
level: practitioner
status: draft
description: "Decide whether a lot ships: read ISO 2859-1/Z1.4 tables (code letter, sample size, Ac/Re), apply switching rules, place inspection points, coordinate lab tests, and run hold/release properly."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# AQL sampling plans and lot release decisions

**Goal:** make accept/reject decisions on lots that are statistically defensible,
consistent between inspectors, and traceable — and never let an unreleased lot move.

## 1. Reading the AQL tables (ISO 2859-1 / ANSI/ASQ Z1.4, attributes)
1. **Lot size** → with the **inspection level** (General II unless specified; I is
   smaller samples, III larger; S-1 to S-4 for destructive/expensive tests) → **code letter**
   (Table I). Example: lot 3,000 at Level II → code **K**.
2. Code letter + **AQL** + **severity** (normal/tightened/reduced) → **sample size** and
   **Ac/Re** (Table II-A for normal single sampling). Code K → n = 125; at AQL 1.0 → **Ac 3, Re 4**.
3. Arrows in the table mean "use the first plan above/below the arrow" — **including its
   sample size**, not the code letter's.
4. Draw the sample **randomly** across the whole lot (all pallets/cartons, start/middle/end), not from the top layer.
5. Count nonconforming units (or nonconformities, if the plan is per 100 units). ≤ Ac → accept; ≥ Re → reject.

Different AQLs per defect class are normal, e.g. critical 0 (any = reject, often 100% check),
major 1.0, minor 2.5–4.0 — agree with customer/spec.

## 2. What AQL does and doesn't mean
- AQL is the quality level the plan **usually accepts** (high probability, often ~90–95%+ at the AQL).
  Lots much worse can still pass sometimes — look at the plan's **OC curve** for LTPL/LQ.
- Accepting a lot doesn't make the defective units in the sample OK: they're still removed/dispositioned.
- **c = 0 plans** (Squeglia's zero-acceptance tables) are common in automotive/medical
  device — any defect rejects the lot with smaller sample sizes.

## 3. Switching rules (part of the standard — often skipped)
- **Normal → tightened**: 2 of 5 consecutive lots rejected.
- **Tightened → normal**: 5 consecutive lots accepted.
- **Normal → reduced**: e.g. 10 consecutive lots accepted (with switching score conditions
  in the 1999 ISO edition), steady production, and approval by the responsible authority.
- **Discontinue** if 5 consecutive lots remain on tightened. Track the state per supplier/part.

## 4. Where to inspect
- **Incoming**: supplier lots, often with skip-lot or CoA/CoC reliance for proven suppliers.
- **In-process**: first-off, patrol inspections, SPC (prevents bad lots rather than finding them).
- **Final**: before release, matching customer requirements and labelling.
Put inspection where it prevents value being added to bad parts.

## 5. Lab tests and release
- Submit samples with full identification (part/product, lot, sample point, time); track
  results against the spec and the lot.
- **Status control**: every lot is **Quarantine/Hold**, **Released**, or **Rejected**, by
  physical tag and by system status (ERP/WMS block). System status must match the tag.
- Release only when all required checks are complete and in spec, records reviewed,
  deviations closed or assessed; the release signature belongs to an authorised person.
- **Rejected lot**: NCR, segregate, disposition (rework, sort 100%, use-as-is with
  concession, return, scrap) — see
  manufacturing-production.production-quality-control.nonconformance-root-cause.containment-and-8d-problem-solving.
- **Resampling** a rejected lot hoping for a pass is not allowed unless the procedure
  defines it (e.g. after a full sort).

## Gotchas
- Taking the sample size from the code letter when the table arrow pointed to another plan.
- Sampling only what's accessible on the pallet surface.
- Lot made of mixed production days/machines — define lots so they're homogeneous.
- Hold tag on the pallet but lot still available in the ERP → shipped by the warehouse.
- Using reduced inspection without meeting the switching conditions.

## Verify
- [ ] Code letter, sample size and Ac/Re checked against the current table edition.
- [ ] Sample random across the lot; locations recorded.
- [ ] Switching state known and recorded per part/supplier.
- [ ] Physical and system lot status agree; nothing unreleased has moved.
- [ ] Rejections have NCRs and dispositions authorised.
