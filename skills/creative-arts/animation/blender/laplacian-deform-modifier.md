---
id: creative-arts.animation.blender.laplacian-deform-modifier
name: laplacian-deform-modifier
category: creative-arts
field: animation
product: blender
tags: [blender, laplacian-deform, laplacian-smooth, modifiers, deform, anchors, scans]
level: practitioner
status: docs-checked
description: "Pose a dense mesh while keeping surface detail with Blender's Laplacian Deform (anchor group, Repeat, Bind), and denoise scans with Smooth Laplacian (Repeat, Lambda Factor/Border)."
sources:
  - https://docs.blender.org/manual/en/latest/modeling/modifiers/deform/laplacian_deform.html
  - https://docs.blender.org/manual/en/latest/modeling/modifiers/deform/laplacian_smooth.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# laplacian-deform-modifier

Goal: reposition part of a dense mesh while preserving surface detail, non-destructively.

## Laplacian Deform

You define "anchor" vertices and move some of them. The modifier keeps the other anchors fixed and computes the best positions for all remaining vertices to preserve the original detail, using differential coordinates (curvature and direction relative to neighbours).

1. Create a vertex group holding the anchors (the vertices you will move and the ones to hold fixed). **An anchors vertex group is required; without it the modifier does nothing.** The weight of each vertex does not matter: only vertices with weight greater than 0 count.
2. Add *Laplacian Deform*, choose the group (the field is labelled *Anchor Weights*; Invert is available) and press **Bind**, which captures the geometric detail.
3. Move the anchors (for example with Hook modifiers placed before it, so they act on the original vertices).
4. To change the anchor group later, press **Unbind** first, then Bind again.
- **Repeat**: iterations to improve the solution; more iterations retain detail better but take longer.

Error messages: invalid/renamed vertex group, vertices or edges added or deleted since bind, or "The system did not find a solution". The manual notes that on dense meshes above 100,000 vertices the nonlinear optimisation may fail.

## Smooth Laplacian (separate modifier)

Reduces noise (for example in real-world reconstructions) with minimal shape change; a negative factor exaggerates shape.
- **Repeat**: repetitions; 0 means no smoothing. Each repetition recalculates the flow curvature, removing more noise with a small Factor under 1.0.
- **Axis**: X, Y, Z toggles.
- **Lambda Factor**: small removes noise, large smooths away fine detail, negative enhances shape (multiple iterations can magnify noise when negative).
- **Lambda Border**: border edges are controlled separately; positive smooths, negative enhances.
- **Preserve Volume**: reduces the shrinkage that smoothing causes.
- **Normalized**: results depend on face size; when disabled, spikes may occur.
- **Vertex Group** (+ Invert).
- The manual warns that meshes over about 10,000 vertices may take minutes; test on a small portion first.

## Verify

Move an anchor: unanchored areas follow with detail intact. Smooth Laplacian: compare against the original at Repeat 0.

## Checked

Date: 2026-10-27. Documentation release: Blender manual, 5.2 release branch (Laplacian Deform and Smooth Laplacian pages). Confirmed: anchor group requirement, Bind/Unbind, Repeat, Smooth Laplacian options and size warning. Corrected the earlier claim of a separate Iterations field and weight-1 anchors, and removed unconfirmed typical values, volume figures and cross-skill workflow advice.
Method: documentation only; no commands were run.
