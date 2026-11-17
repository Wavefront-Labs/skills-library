---
id: creative-arts.design-for-form-and-experience.concept-design.placing-parting-lines-on-moulded-products
name: placing-parting-lines-on-moulded-products
category: creative-arts
field: design-for-form-and-experience
product: concept-design
tags: [design-for-manufacture, dfm, parting-line, split-line, injection-moulding, witness-line, product-design, cmf]
level: practitioner
status: draft
description: "Decide where the mould parting line falls on a product so it is hidden or deliberate: silhouette edges, step features, and its effect on draft, flash and finish."
sources:
  - "Protolabs Design Guide - Parting lines in injection molding (protolabs.com/resources/design-tips)"
  - "SOLIDWORKS Help - Parting Lines and Mold Tools (help.solidworks.com)"
  - "NASAD Handbook, industrial design materials and processes competency"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Parting line placement

**Goal:** the line where mould halves meet ends up where it does not spoil the form, or becomes
a designed feature.

## Facts to design with
- The parting line leaves a fine witness line and sometimes flash; on gloss or light colours it
  is visible.
- It usually runs along the part's **largest silhouette** in the pull direction (the widest
  outline seen from the pull axis), because draft goes away from it in both directions.
- Changing the parting line changes draft directions above and below it.

## Placement options
1. **On a sharp silhouette edge:** hides inside an edge highlight; the cleanest default.
2. **On a step or shut line:** add a small step (0.3-0.5 mm) or a groove so the line hides in the shadow.
3. **On a radius:** worst case; the line cuts the highlight. Avoid on large visible radii.
4. **Under a secondary part** (label, trim, overmould) that covers it.
5. **Designed in:** a deliberate break line between two colour or texture zones.

## Process
- Mark the pull direction on the first CAD blockout; sketch the largest silhouette in that view.
- Review the parting line with the toolmaker early; their preferred line may differ for gating
  and ejection.
- In SOLIDWORKS: Mold Tools > Parting Lines finds the line for a pull direction and draft angle.

## Gotchas
- Organic forms may need a 3D (stepped or curved) parting line, which raises tool cost.
- Side actions add their own witness lines; show them on the CMF sheet too.

## Verify
Renders and the first appearance model show the parting line where it was planned; the
toolmaker signs off the same line.
