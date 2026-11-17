---
id: creative-arts.design-for-form-and-experience.concept-design.applying-draft-angles-and-running-draft-analysis
name: applying-draft-angles-and-running-draft-analysis
category: creative-arts
field: design-for-form-and-experience
product: concept-design
tags: [design-for-manufacture, dfm, draft-angle, draft-analysis, pull-direction, injection-moulding, solidworks, fusion-360, product-design]
level: practitioner
status: draft
description: "Apply draft to moulded parts early: pull direction, typical draft angles, where draft changes the look, and checking it with draft analysis in SOLIDWORKS or Fusion."
sources:
  - "SOLIDWORKS Help - Draft feature and Draft Analysis (help.solidworks.com)"
  - "Autodesk Fusion help - Draft command and Draft Analysis (help.autodesk.com/view/fusion360/ENU)"
  - "Protolabs Design Guide - Injection molding draft (protolabs.com/resources/design-tips)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Draft angles and draft analysis

**Goal:** a moulded part that can eject from the tool, designed so the draft is part of the form
instead of a surprise that changes the look late.

## Basics
- **Pull direction:** the axis the tool halves separate along. Every face parallel to it needs draft.
- **Typical draft:** 1-2 degrees as a default for smooth surfaces; 0.5 degrees is a practical
  minimum on polished faces; add more for textures (roughly 1 degree per 0.025 mm texture depth)
  and for deep features. Core side (inside) often needs more because the part shrinks onto it.
- **Draft direction:** surfaces taper so the part gets smaller toward the moving half.

## Design implications
- A 2 degree draft on a 60 mm tall wall shifts the top edge about 2 mm in; boxy forms become
  slightly tapered. Sketch with draft from the start for tall parts.
- Draft creates a visible change in highlight angle; on premium parts, place the parting line
  where the draft change is hidden or reads as a deliberate line.

## In CAD
- SOLIDWORKS: Insert > Features > **Draft** (Neutral plane, Parting line or Step draft);
  View > Display > **Draft Analysis** with the pull direction and minimum angle; faces show
  positive, negative and "requires draft" colours.
- Fusion: Modify > **Draft** (pull direction, faces, angle); Inspect > **Draft Analysis** with
  the angle threshold.
- Apply draft before fillets so fillets follow drafted faces.

## Gotchas
- Undercuts (negative draft) need side actions or lifters, adding cost; check snap fits and
  logos on side walls.
- Straight-pull texture on side walls without enough draft scuffs the texture.

## Verify
Draft analysis in the actual pull direction shows no faces below the minimum angle except
those deliberately assigned to side actions, and the toolmaker confirms the pull direction.
