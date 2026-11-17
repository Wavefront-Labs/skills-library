---
id: creative-arts.design-for-form-and-experience.concept-design.designing-surface-transitions-and-fillet-character
name: designing-surface-transitions-and-fillet-character
category: creative-arts
field: design-for-form-and-experience
product: concept-design
tags: [form-language, form-development, surface-transitions, fillet-transitions, g1-continuity, g2-continuity, curvature-continuous, highlights, product-design]
level: advanced
status: draft
description: "Choose and communicate how surfaces meet: radius size and variation, G1 versus G2 transitions, softened versus crisp edges, and how highlights reveal them."
sources:
  - "Autodesk Fusion help, Inspect - Zebra Analysis and Curvature Comb Analysis (help.autodesk.com/view/fusion360/ENU)"
  - "SOLIDWORKS Help, Fillets - Curvature continuous and conic fillets (help.solidworks.com)"
  - "NASAD Handbook, industrial design 3D form competencies"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Surface transitions and fillet character

**Goal:** decide deliberately how every edge on the product turns, because edge character
carries more of the design language than the main surfaces.

## Vocabulary
| Transition | What you see | Use |
|---|---|---|
| Sharp edge | Hard line, crisp shadow | Precision, tools, technical |
| Constant radius (G1, tangent) | Highlight jumps at the tangent line | Cheap, quick; looks "CAD" at large radii |
| Curvature-continuous (G2) | Highlight flows smoothly round the edge | Premium consumer products |
| Variable radius | Radius grows/shrinks along the edge | Dynamic forms, sporty language |
| Chamfer / conic | Flat or tight band of light | Catching a highlight line on purpose |

## Deciding the hierarchy
1. Rank edges: primary (silhouette-defining), secondary (feature edges), tertiary (small
   details). Give primary edges the largest and most consistent treatment.
2. Keep a small set of radii (for example 0.5, 2, 6 mm) rather than a different value per
   edge. Consistency reads as quality.
3. Where three edges meet at a corner, decide the blend order early; a corner where radii of
   very different sizes meet produces pinched patches.
4. Decide sharp versus soft by the light: a soft edge gives a highlight, a sharp one gives a
   line. Sketch the highlight you want, then pick the transition that produces it.

## Communicating
- In sketches: indicate radius size with the highlight width; a crisp edge with a thin
  bright line, a soft edge with a broad gradient.
- In CAD: G2 fillets (SOLIDWORKS: Fillet > Curvature continuous profile; Fusion: the Fillet dialog's
  continuity option set to G2 where your version offers it) and check with zebra analysis: stripes must flow without
  kinks across the edge for G2; they align but kink for G1.

## Gotchas
- Large constant radii on boxy forms look inflated; reduce or go variable.
- Fillets under 0.3 mm on moulded plastic do not survive tooling polish; coordinate with
  engineering on minimum radii.
- Draft angle changes how a fillet reads from the side; review with draft applied.

## Verify
Render or photograph the model under a striped or softbox light: highlights should behave
exactly as sketched with no breaks at the transitions you meant to be smooth.
