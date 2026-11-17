---
id: architecture-construction.site-supervision-trade-coordination.rfi-submittal-management.managing-submittal-registers-rfis-and-document-control
name: managing-submittal-registers-rfis-and-document-control
category: architecture-construction
field: site-supervision-trade-coordination
product: rfi-submittal-management
tags: [site-supervision-trade-coordination, rfi-submittal-management, submittals, submittal-register, submittal-schedule, shop-drawings, product-data, samples, mock-ups, approval-status, approved-as-noted, revise-and-resubmit, rfi, rfi-log, document-control, transmittals, revision-control, superseded-drawings, lead-times, procurement, design-team, aconex, procore, spreadsheet-register]
level: practitioner
status: draft
description: "Run the site-designer information flow in any tool: a submittal register tied to lead times, reviewing shop drawings before sending, RFI discipline and revision control."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Managing submittal registers, RFIs and document control

**Goal:** every product and shop drawing is approved before it's needed, every design
question gets answered before it stops work, and nobody builds from a superseded drawing.
Tool-agnostic: works in Procore/Aconex/ACC or a disciplined spreadsheet.

## 1. Build the submittal register at the start
- Go through the specification section by section and list every required submittal:
  shop drawings, product data, samples, mock-ups, test reports, warranties, O&M.
- For each: spec reference, description, responsible subcontractor, reviewer
  (architect/engineer), **required-on-site date** (from the programme), **lead time**
  (fabrication + delivery), and review time (from the contract, e.g., 10 working days).
- Work backwards: **submit-by date = required-on-site − lead time − review time −
  resubmission allowance.** Long-lead items (lifts, façade, switchboards, structural
  steel) surface in week one, not month four.

## 2. Review before you send
The contractor's review is not a mailbox:
- Does it match the spec (product, grade, finish, fire rating, performance)?
- Dimensions and interfaces coordinated with other trades (openings, fixings,
  services)?
- Complete (all sheets, calcs, certificates)? Deviations from spec clearly flagged
  as deviations?
Stamp/sign your review, then transmit. Unreviewed submittals that bounce cost weeks.

## 3. Track status
- Status categories (common): **Approved**, **Approved as noted** (proceed and incorporate
  the notes — read them!), **Revise and resubmit**, **Rejected**, **For information**.
- Weekly register review: overdue with reviewer, overdue with sub, items whose submit-by
  date has passed without submission. Escalate in meeting minutes.
- Only approved (or approved-as-noted) submittals released to fabrication/installation.

## 4. RFI discipline
- One question per RFI, specific location, reference documents, and a **proposed answer**.
- Number sequentially; log date raised, required-by date (with reason: "needed for slab
  pour 12 Nov"), ball-in-court, date answered, cost/time impact flag.
- Don't use RFIs to request changes — that's a variation/change request. Don't let
  designers use RFI answers to issue changes without the change process.
- Distribute answers to every affected trade and record the answer on the drawing set.

## 5. Document control
- A single source of truth for current drawings (the platform or a controlled set).
- On every new revision: issue via transmittal, record receipt, **mark superseded
  sheets "SUPERSEDED"** and remove them from the field (or void them in the app).
- Check revision letters/numbers in the title block against the drawing register before
  any trade starts a package.
- Keep as-built markups current as work proceeds, not at the end.

## Gotchas
- Lead time ignored → approved product arriving months late.
- "Approved as noted" treated as "approved" — notes never incorporated.
- Old revision on a foreman's clipboard → rework.
- RFIs answered by email to one person and lost.

## Verify
- [ ] Register lists every spec-required submittal with submit-by dates from lead times.
- [ ] Contractor review recorded on each submittal before transmittal.
- [ ] No fabrication released without approved status.
- [ ] RFI log current with ball-in-court and required-by reasons.
- [ ] Spot-check three field drawings against the current register revision.

*Status: draft — common US/AU/UK contract practice; review periods and status names vary
by contract.*
