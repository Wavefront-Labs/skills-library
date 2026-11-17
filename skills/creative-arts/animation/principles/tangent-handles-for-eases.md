---
id: creative-arts.animation.principles.tangent-handles-for-eases
name: tangent-handles-for-eases
category: creative-arts
field: animation
product: principles
tags: [animation, slow-in-slow-out, tangent-handles, graph-editor, bezier, ease-in, ease-out, broken-tangents, weighted-tangents, maya, blender, cg]
level: practitioner
status: draft
description: "Shape ease-ins, ease-outs, snaps and hits with tangent types and handle weights in the graph editor, and read curve shapes as spacing."
sources:
  - https://docs.blender.org/manual/en/latest/editors/graph_editor/fcurves/properties.html
  - https://docs.blender.org/manual/en/latest/editors/graph_editor/fcurves/editing.html
  - https://books.google.com/books?vid=ISBN9780865478978
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Tangent handles for eases

Goal: control slow-in/slow-out precisely in CG curves. The slope of a curve is speed; a flat
section is slow, a steep section is fast. Tangent handles set that slope at each key.

## Reading curves as spacing
- Flat tangent at a key = ease (slow in/out).
- Steep straight segment = constant speed.
- Sharp corner (broken tangent) = instant change of direction - an impact or a hit.
- Curve overshooting past the key value = unwanted overshoot from auto tangents.

## Tangent types
| Need | Blender handle type | Maya tangent |
|---|---|---|
| Smooth ease in/out | Auto Clamped / Aligned flat | Auto / Spline / Flat |
| No overshoot between keys | Auto Clamped | Auto / Clamped |
| Impact, bounce contact | Vector or broken Free handles | Linear in, broken |
| Mechanical constant speed | Vector or Linear interpolation | Linear |
| Hold until snap | Constant interpolation | Stepped |

Set in Blender: Graph Editor, select keys, V for handle type, T for interpolation. Maya: Graph
Editor tangent buttons; break tangents with Break Tangents; enable Weighted Tangents and
unlock weights to lengthen handles.

## Shaping eases
- **Longer handle** on the side of the ease = longer slow section (stronger ease).
- **Asymmetric eases**: slow out of a pose, fast into the next - shorten the incoming handle
  at the second key.
- **Hits**: break the tangent at the contact so velocity flips instantly.
- **Accent then settle**: steep in, slight overshoot key, flat settle.

## Failure modes
- Leaving all tangents on default Auto: every move eases both ends - floaty.
- Weighted handles so long the curve overshoots between keys.
- Editing tangents on rotation channels in Euler with gimbal flips - check curves for
  360-degree jumps first (Blender: Discontinuity (Euler) Filter).

## Verify
- [ ] Motion trail spacing matches the intended ease.
- [ ] No curve exceeds its key values unintentionally.
- [ ] Impacts have broken tangents (a corner in the curve).

Related: `creative-arts.animation.principles.favouring-inbetweens`,
`creative-arts.animation.principles.stepped-blocking-to-spline`.
