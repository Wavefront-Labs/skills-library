---
id: creative-arts.animation.blender.smoke-dissolve
name: smoke-dissolve
category: creative-arts
field: animation
product: blender
tags: [blender, smoke, gas-sim, smoke-dissolve, dissolve-smoke, lifetime]
level: practitioner
status: docs-checked
description: "Make Mantaflow smoke fade with Dissolve: time in frames, slow (logarithmic) dissolve, and when to use it for wispy trails."
sources:
  - https://docs.blender.org/manual/en/latest/physics/fluid/type/domain/settings.html
  - https://docs.blender.org/manual/en/latest/physics/fluid/type/flow.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# smoke-dissolve

## Settings (Domain > Gas > Dissolve)

- **Dissolve** checkbox: allows gas to dissipate over time.
- **Time**: speed of gas dissipation, in frames.
- **Slow**: dissolves the gas in a logarithmic fashion: quickly at first, but it lingers longer.

## Uses

- Steam from a cup or breath: short Time, Slow on.
- Smoke trail behind a moving object: a moderate Time so the trail fades instead of filling the domain.
- Keeps the domain from saturating with smoke in long shots.

## Alternatives

- Outflow flow objects remove fluid that enters their bounding box.

## Gotchas

- Time is in frames, so the look changes with the scene frame rate.

## Verify

Emit a single puff and step through frames: the density fades over roughly the Time you set.

## Checked

Checked 2026-10-27 against the Blender 5.2 manual (physics/fluid/type/domain/settings (Gas > Dissolve) and physics/fluid/type/flow (Outflow); branch blender-v5.2-release) and the 5.2 source (rna_fluid.cc). Confirmed: Dissolve checkbox, Time in frames, Slow logarithmic behaviour, Outflow behaviour.

Method: documentation only; no commands were run.
