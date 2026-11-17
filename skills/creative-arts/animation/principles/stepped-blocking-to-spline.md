---
id: creative-arts.animation.principles.stepped-blocking-to-spline
name: stepped-blocking-to-spline
category: creative-arts
field: animation
product: principles
tags: [animation, pose-to-pose-method, stepped-blocking, blocking, blocking-plus, spline, polish, cg, graph-editor, dailies]
level: practitioner
status: draft
description: "Run the CG pose-to-pose pipeline: stepped blocking, blocking-plus with breakdowns, the spline switch, and polish, with what each review stage must show."
sources:
  - https://books.google.com/books?vid=ISBN9780865478978
  - https://docs.blender.org/manual/en/latest/editors/graph_editor/fcurves/properties.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Stepped blocking to spline

Goal: the standard feature/TV CG workflow that keeps notes cheap: approve poses and timing in
stepped mode, then convert to curves, then polish.

## Stages
1. **Blocking (stepped)** - keys and extremes only, interpolation set to stepped/constant.
   Shows: story poses, timing, staging, camera. Review: "do the poses and timing work?"
2. **Blocking plus** - add breakdowns and major overlap keys, still stepped, roughly every
   2-4 frames on fast action. Review: arcs and spacing readable in steps.
3. **Spline switch** - change all keys to spline/Bezier (Maya: Default tangents to Auto/Spline;
   Blender: Graph Editor > Key > Interpolation Mode > Bezier, T menu). Expect floatiness.
4. **Spline fix** - remove floaty eases, fix overshoot from auto tangents, add moving holds
   (keep 2-6 frames of drift on holds), clean arcs.
5. **Polish** - overlap, fingers, face, eye darts, blinks, contact sticking, foot slip.

## Rules that make the switch painless
- Key **all controls on the same frames** during blocking (key the whole character), so splines
  do not interpolate from distant unrelated keys.
- Add **copied holds**: a key at the start and end of every hold so splines do not drift.
- Block on the frame the pose should be fully reached; breakdowns hold the path.
- Keep a saved stepped version before switching.

## Common spline problems
| Problem | Fix |
|---|---|
| Floaty, everything eases | Flatten fewer tangents; linear or broken tangents into hits |
| Overshoot past a pose | Clamped/auto-clamped tangents (Blender: Auto Clamped handles) |
| Dead holds | Moving hold: 2-6 % drift and slight settle |
| Feet sliding | Lock IK feet with constant interpolation on planted frames |

## Verify
- [ ] Stepped blocking approved before splining.
- [ ] After the switch, every hold drifts, no limb overshoots unintentionally.
- [ ] Arcs traced and clean in the spline pass.

Related: `creative-arts.animation.principles.keys-extremes-breakdowns`,
`creative-arts.animation.principles.tangent-handles-for-eases`.
