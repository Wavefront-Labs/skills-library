---
id: creative-arts.animation.art-direction.cross-department-approval-tracking
name: cross-department-approval-tracking
category: creative-arts
field: animation
product: art-direction
tags: [art-direction, art-review, approval-tracking, status, sign-off]
level: advanced
status: draft
description: "Track art approvals across design, modeling, surfacing, lighting and BG: one status vocabulary, who signs off what, dependencies, and reports showing what is blocked."
sources:
  - https://help.autodesk.com/view/SGSUB/ENU/
  - https://animationguild.org/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Approval status tracking across departments

Goal: everyone can see what is approved, by whom, and what is waiting on art direction.

## 1. One status vocabulary
Use the same small set on every task: `not started`, `in progress`, `pending review`, `revise`,
`approved with notes`, `approved (final)`, `on hold`, `omit`. Avoid department-specific dialects.

## 2. Sign-off matrix
| Asset stage | Approver |
|---|---|
| Design / concept | art director (production designer for world assets) |
| Model / turntable | art director + CG supervisor |
| Surfacing / lookdev | art director |
| Colour model | colour stylist, then art director |
| Lighting master shot | art director + director |
| BG paintings | art director |
Keep the matrix in the bible and let the tracker enforce it (only approvers can set approved).

## 3. Dependencies
- Link tasks: a model cannot go final until its design is approved; lighting not until lookdev is.
- When an approved upstream asset changes, downstream tasks are flagged for re-review.

## 4. Reports
- Weekly: items pending art review older than N days, items in revise for more than two rounds,
  approvals blocking downstream work.
- Keep the review backlog under a week; if it grows, add review slots rather than artists.

## Verify
- [ ] Single status list used in all departments.
- [ ] Approver per stage defined and enforced.
- [ ] Upstream changes flag downstream tasks.

Related: `creative-arts.animation.pipeline.production-tracking`,
`creative-arts.animation.art-direction.running-art-dailies`.
