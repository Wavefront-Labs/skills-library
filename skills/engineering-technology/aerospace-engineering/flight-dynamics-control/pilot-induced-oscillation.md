---
id: engineering-technology.aerospace-engineering.flight-dynamics-control.pilot-induced-oscillation
name: pilot-induced-oscillation
category: engineering-technology
field: aerospace-engineering
product: flight-dynamics-control
tags: [pilot-induced-oscillation, pio, pio-categories, bandwidth-criterion, neal-smith, handling-qualities]
level: practitioner
status: draft
description: "Recognise and screen for pilot-induced oscillation with category definitions, bandwidth and phase-delay criteria, and design changes that cut PIO tendency."
sources:
  - "National Research Council, Aviation Safety and Pilot Control"
  - "Hoh and Mitchell et al., handling qualities criteria reports"
  - "Nelson, Flight Stability and Automatic Control"
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# Pilot-induced oscillation

**Goal:** find PIO-prone configurations early and remove the cause.

## What PIO is
An unintended sustained oscillation caused by the pilot's attempt to control the aircraft; the closed loop of pilot plus vehicle goes unstable or near unstable.

## Categories
- **Category I**: essentially linear pilot-vehicle dynamics, caused by excess phase lag or low damping.
- **Category II**: quasi-linear, where rate or position limits cut effective gain and add lag.
- **Category III**: nonlinear transitions, such as mode switching or abrupt changes in effective dynamics (a recognised classification in the National Research Council study of PIO).

## Screening
1. Compute the frequency response from stick to controlled attitude, including actuators, filters, delays and computation lag.
2. Apply the bandwidth criterion (pitch attitude bandwidth against phase delay) and the Neal-Smith criterion, and compare with the boundary plots in the criteria documents.
3. Check the open-loop onset point and the amplitude-dependence: gain reduction at large amplitude from rate limiters.
4. Ground-based simulation with a task of high gain tracking, then flight test with a PIO rating scale.

## Design remedies
- Reduce delay in the loop (higher update rate, lighter filtering).
- Prevent actuator rate saturation or use rate-limiter compensation.
- Reduce control-system lag; add lead; limit pilot gain through force gradients.
- Avoid abrupt mode changes in the control law.

## Gotchas
- A configuration that passes linear criteria can still exhibit Category II PIO under saturation.
- Simulator motion cues change pilot gain; do not rely on fixed-base results alone.

## Verify
- [ ] Rate-limit and saturation cases were simulated with a high-gain pilot task and show no divergence.
