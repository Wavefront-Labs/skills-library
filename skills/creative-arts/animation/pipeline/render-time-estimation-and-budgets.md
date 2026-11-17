---
id: creative-arts.animation.pipeline.render-time-estimation-and-budgets
name: render-time-estimation-and-budgets
category: creative-arts
field: animation
product: pipeline
tags: [render-estimate, render-time, core-hours, render-budget, farm-capacity, cloud-rendering, production-management]
level: advanced
status: draft
description: "Estimate render time and cost: test frames, core-hours, passes and re-renders, farm capacity, cloud pricing, schedule planning and tracking actuals."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Render time estimation and budgets

Render time is a production constraint with a cost. Estimate it early, then refine with real numbers.

## Estimate
1. **Sample frames** from each shot type (simple, average, heaviest), rendered at final resolution and quality settings on representative farm hardware.
2. Record **wall time per frame** and the **cores** used, giving **core-hours per frame** (time x cores / 3600).
3. Total = sum over shots of frames x core-hours per frame x passes or layers.
4. Multiply for **re-renders**: lighting iterations, fixes and final re-renders commonly multiply the total several times; use history for the factor, or start with 2-3x and update.
5. Add **comp and encoding** time, and cache/simulation costs.
6. Convert to cost: core-hours x cost per core-hour (owned hardware amortisation, power and staff, or cloud instance rates).

## Capacity and schedule
- **Farm capacity** = cores x available hours (account for downtime and artist use).
- Compare capacity with demand per week to find peaks (final lighting weeks) and decide whether to burst to the cloud (`render-preflight.md`, `render-licensing-management.md`).
- Convert to **calendar time** for the delivery schedule (`producing-scheduling.md`).

## Reduce
- Test lower sample counts and denoising (`wedging-and-test-renders.md`).
- Reduce resolution for preview, optimise geometry and textures, and cache simulations.
- Render only what changed (layer, region or frame range).

## Track
- Log actual render time and size per frame in the tracker or farm statistics, and compare with the estimate each week.
- Feed the real averages back into the next budget (`building-an-animation-budget.md`).

## Gotchas
- Memory limits can force fewer jobs per host and reduce throughput.
- Variance between frames is large; use percentile estimates (for example the 90th) for planning, not only averages.
- Licence limits can cap parallelism regardless of core count.

## Verify
- [ ] Estimates are built from rendered samples at final settings.
- [ ] The re-render factor is explicit.
- [ ] Actuals are compared weekly.
