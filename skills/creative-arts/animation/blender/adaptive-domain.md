---
id: creative-arts.animation.blender.adaptive-domain
name: adaptive-domain
category: creative-arts
field: animation
product: blender
tags: [blender, smoke, gas-sim, adaptive-domain, mantaflow]
level: practitioner
status: docs-checked
description: "Use Mantaflow Adaptive Domain for gas sims: margin, threshold, add resolution, and when it saves time versus when it clips smoke."
sources:
  - https://docs.blender.org/manual/en/latest/physics/fluid/type/domain/gas/adaptive_domain.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# adaptive-domain

## What it does

Gas domains only. When enabled, the domain adaptively shrinks to best fit the gas, saving computation by leaving voxels without gas out of the simulation. Unless Add Resolution is used, the adaptive domain does not exceed the bounds of the original domain.

## Settings (Domain > Adaptive Domain panel)

- **Add Resolution**: number of voxels to add around the outside of the domain.
- **Margin**: extra space left around the gas, in voxels. Very fast-moving gas may need larger margins so it is not cut off, at the cost of more voxels.
- **Threshold**: smallest amount of gas a voxel can contain before it counts as empty and may be cut out.

## When to use

- Plumes, explosions expanding from a point, smoke trails following a moving object: the gas occupies a small part of a large domain.
- Avoid it when thin wispy gas sits near the threshold, since it can be clipped.

## Gotchas

- Smoke is cut off by an invisible edge: raise Margin or lower Threshold.
- The original domain must still contain the whole effect.
- Liquid domains have no Adaptive Domain panel.

## Verify

Compare a few frames against a non-adaptive bake for clipping.

## Checked

Checked 2026-10-27 against the Blender 5.2 manual (physics/fluid/type/domain/gas/adaptive_domain; branch blender-v5.2-release) and the 5.2 source (rna_fluid.cc). Confirmed: what Adaptive Domain does and its bound rule, Add Resolution, Margin, Threshold, and that it lives in the Gas settings.

Method: documentation only; no commands were run.
