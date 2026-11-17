---
id: creative-arts.design-for-form-and-experience.concept-design.drawing-exploded-views-for-presentation
name: drawing-exploded-views-for-presentation
category: creative-arts
field: design-for-form-and-experience
product: concept-design
tags: [presentation-board, concept-presentation, exploded-view, assembly-view, technical-illustration, keyshot, fusion-360, solidworks]
level: practitioner
status: draft
description: "Produce clear exploded views for concept presentations: explode axes and order, spacing, leader callouts, and making them from CAD in Fusion or SOLIDWORKS."
sources:
  - "SOLIDWORKS Help - Exploded Views, Explode Line Sketch (help.solidworks.com)"
  - "Autodesk Fusion help - Animation workspace - Transform components, Auto Explode (help.autodesk.com/view/fusion360/ENU)"
  - "Koos Eissen and Roselien Steur, Sketching - The Basics, ch Exploded views"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Exploded views

**Goal:** show how a product is built (parts, order, key internal features) so stakeholders
understand the architecture and the cost story at a glance.

## Composition rules
1. **Explode along real assembly axes:** parts move the way they would come apart, usually one
   main axis. Do not scatter parts in random directions.
2. **Order = assembly order:** outer parts furthest out, internal parts in their stack order.
3. **Spacing:** gaps large enough to see each part's main face, small enough that they still read
   as one product. Overlap is acceptable if contours stay clear.
4. **Viewpoint:** a three-quarter view from the side that shows the most parts; slightly elevated.
5. **Explode lines** (thin dashed centrelines) show which part goes where when the travel is long.
6. **Callouts:** numbers or short labels with leader lines, aligned on a grid at the side, not
   scattered across the image.

## From CAD
- SOLIDWORKS: Insert > Exploded View; drag parts along the triad axis in steps; Insert > Explode
  Line Sketch for the travel lines. Steps can be animated (Animate Collapse/Explode).
- Fusion: Animation workspace > Transform Components or Auto Explode (one level / all levels),
  then adjust; publish a still or video from the storyboard.
- Render in KeyShot with the same lighting as the hero shots for a consistent board.

## Sketch version
Draw the main body first in perspective, then extend the explode axis to its vanishing point and
place parts along it; ellipses and screw axes stay on the axis.

## Verify
A colleague can name every part and say how many fasteners or steps assemble it; no part sits
off its axis.
