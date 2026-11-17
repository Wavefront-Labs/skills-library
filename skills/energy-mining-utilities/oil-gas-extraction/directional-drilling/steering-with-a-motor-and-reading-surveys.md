---
id: energy-mining-utilities.oil-gas-extraction.directional-drilling.steering-with-a-motor-and-reading-surveys
name: steering-with-a-motor-and-reading-surveys
category: energy-mining-utilities
field: oil-gas-extraction
product: directional-drilling
tags: [directional-drilling, directional-driller, dd, mwd, survey, inclination, azimuth, minimum-curvature, dogleg-severity, dls, toolface, gravity-toolface, magnetic-toolface, mud-motor, bent-housing, sliding, rotating, slide-rotate, rotary-steerable, rss, build-rate, turn-rate, projection-to-bit, well-plan, anti-collision, separation-factor, geosteering, horizontal-well, reactive-torque]
level: advanced
status: draft
description: "Steer a directional well: survey QC and minimum curvature, projecting to plan, setting toolface with a bent motor, slide-rotate sequencing, RSS basics and anti-collision checks."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Steering with a motor and reading surveys

**Goal:** keep the wellbore on (or acceptably near) the plan, with smooth curvature, and
never too close to another well.

> Status: draft. Industry-general method; exact survey QC criteria, tolerances and
> anti-collision rules come from the operator's directional standards and survey
> management programme.

## 1. Surveys
- MWD sends **inclination, azimuth** and measured depth (MD) at each survey station
  (usually after connections). The directional software computes position with the
  **minimum curvature** method.
- **QC each survey:** check total gravity, total magnetic field and dip angle against
  the reference model within tolerances; flag magnetic interference near casing or
  other wells. A survey that fails QC is not used to steer without a reason.
- **Dogleg severity (DLS)** — curvature, in °/100 ft or °/30 m. High local DLS creates
  casing wear, stuck pipe and completion problems even if the overall well hits target.
- **Projection to bit:** the survey sensor is tens of feet behind the bit. Project
  ahead using the motor yield or last-sliding behaviour to know where the bit really is.

## 2. Steering with a bent-housing motor
- The motor's bend points the bit in the **toolface** direction. **Sliding** (no string
  rotation, mud powers the bit) drills in the toolface direction and curves the hole.
  **Rotating** the string averages the bend out and drills roughly straight.
- **Toolface:** **gravity toolface (GTF)** relative to the high side of the hole when
  inclination is above a few degrees; **magnetic toolface (MTF)** relative to north
  at near-vertical inclinations. 0° GTF = build, 180° = drop, 90° right/270° left = turn.
- Set toolface by rotating the string a little, then **watching it settle**: reactive
  torque from the motor twists the string to the left (anticlockwise) as weight goes on,
  so you set the surface orientation to the right of the desired toolface.
- **Slide-rotate ratio:** to achieve, say, 3°/100 ft with a motor that yields 6°/100 ft
  when sliding, slide about half of each stand and rotate the rest (simplified — real
  yields vary with formation and BHA).
- Slide early and in shorter bursts rather than one big correction; smaller doglegs.

## 3. Rotary steerable systems (RSS)
- RSS steer while rotating (push-the-bit or point-the-bit), giving smoother holes and
  better hole cleaning. The DD sends downlinks (pump flow or RPM patterns) to change
  steering settings. Learn the vendor's downlink protocol and confirm acknowledgement
  on the MWD before assuming the tool changed mode.

## 4. Staying on plan
- Compare actual vs plan each survey: distance and direction from plan (e.g. ahead/
  behind, high/low, left/right) and the DLS needed to get back. Don't overcorrect.
- **Geosteering** (horizontal wells) changes the target in real time from LWD
  (gamma, resistivity) to stay in the reservoir; agree who calls changes.

## 5. Anti-collision
- Plan scans compute **separation factor** between your uncertainty ellipse and nearby
  wells. Below the operator's thresholds, special procedures apply (e.g. stop drilling,
  extra surveys, shut in the offset well).
- Signs of approaching another well: magnetic interference, cement or steel in the
  returns, sudden torque/vibration changes. Stop and assess.

## Gotchas
- Bad weight transfer while sliding (stick-slip, hanging up) gives unpredictable toolface.
- A wrong magnetic declination or grid convergence setting rotates the whole well.
- Don't trust a single survey taken right after a long slide; confirm the trend.

## Verify
- [ ] Each survey QC'd and accepted before use.
- [ ] Bit position projected; deviation from plan and required DLS known.
- [ ] Toolface held steady during slides; reactive torque accounted for.
- [ ] DLS kept within plan limits.
- [ ] Anti-collision scan current; thresholds known.
