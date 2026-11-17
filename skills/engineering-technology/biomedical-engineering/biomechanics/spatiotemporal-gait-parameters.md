---
id: engineering-technology.biomedical-engineering.biomechanics.spatiotemporal-gait-parameters
name: spatiotemporal-gait-parameters
category: engineering-technology
field: biomedical-engineering
product: biomechanics
tags: [spatiotemporal-gait, gait-analysis, gait-cycle, cadence, stride-length, step-width, double-support, froude-number]
level: practitioner
status: gated
description: "Compute gait spatiotemporal parameters from events: stride and step length and time, cadence, speed, stance and double support percentages, width and normalisation."
sources: ["Perry and Burnfield, Gait Analysis: Normal and Pathological Function", "Winter, Biomechanics and Motor Control of Human Movement", "Zeni, Richards and Higginson, Two simple methods for determining gait events during treadmill and overground walking (Gait Posture 2008)"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Spatiotemporal gait parameters

**Goal:** standard, comparable gait measures derived from foot contact and toe-off events.

## Events and definitions
- **Heel strike (initial contact)** and **toe-off** from force plates (threshold) or kinematic algorithms (for example Zeni: heel and toe positions relative to the pelvis).
- **Stride** = from one heel strike to the next heel strike of the same foot; **step** = from heel strike of one foot to the other foot's heel strike.
- Stride time, step time, stance time, swing time, single and double support times.

## Calculations
- Cadence (steps/min) = 60 / mean step time.
- Stride length = distance between successive heel positions of the same foot in the walking direction; step length similarly for opposite feet.
- Speed = stride length / stride time (or pelvis marker displacement over time).
- Stance %, swing %, double support % of the gait cycle.
- Step width = mediolateral distance between heel positions of consecutive steps.
- Symmetry indices (left/right ratio or difference).

## Typical healthy adult values (indicative; textbook figures (gated: unconfirmed, source is paywalled or blocked))
Comfortable speed about 1.2-1.4 m/s, cadence about 100-120 steps/min, stride length about 1.3-1.5 m, stance about 60% and swing 40%, double support about 20% (two intervals of about 10%). Values change with age, height and speed.

## Normalisation
Divide lengths by leg length (or height) and speeds by sqrt(g L) (Froude number) for comparing people of different size; compare at similar speeds because many parameters depend on speed.

## Verify
- [ ] Stance + swing equals 100% of the cycle for each limb.
- [ ] Event detection checked against force plate events (differences within a frame or two).
- [ ] At least 6-10 strides per condition; report variability (coefficient of variation).
