---
id: engineering-technology.aerospace-engineering.aircraft-structures.bolted-joint-bearing-bypass
name: bolted-joint-bearing-bypass
category: engineering-technology
field: aerospace-engineering
product: aircraft-structures
tags: [aircraft-structures, joints, fasteners, bolted-joints, bearing-stress, net-section, shear-out, bypass-load, edge-distance]
level: practitioner
status: verified
description: "Check metallic bolted joints for bearing, shear-out, net-section and bypass interaction, with edge distance and pitch rules of thumb."
sources:
  - "MMPDS Handbook (joint chapter)"
  - "Niu, Airframe Structural Design"
  - "Bruhn, Analysis and Design of Flight Vehicle Structures"
  - "https://www.law.cornell.edu/cfr/text/14/25.625"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Bolted joint bearing and bypass

**Goal:** margins of safety for fastened joints.

## Checks
- **Bearing:** `sigma_br = P / (D t)` vs bearing allowable (MMPDS values depend on edge distance ratio `e/D`: allowable at `e/D = 1.5` and `2.0`).
- **Shear-out and net tension:** edge distance `e` typically at least 2D (pitch at least 4D) for good efficiency (gated: unconfirmed, source is paywalled or blocked); check net-section stress with stress concentration.
- **Bolt shear and bending:** fastener shear allowable from the fastener standard; bending in thick or long grip joints.
- **Bypass:** load not transferred at the fastener passes by it; interaction of bearing and bypass governs in multi-row joints.
- **Fitting factor:** 25.625(a) requires a fitting factor of at least 1.15 on the fitting, its attachment and the bearing on the joined members unless the fitting is proven by limit and ultimate load tests simulating actual stress conditions; 25.625(b) lists exceptions. Confirm in the current text.

## Procedure
1. Get fastener loads from FE or load distribution (see fastener skill).
2. Compute bearing and bypass at each hole, with the stress concentration factor.
3. Apply fitting factor and compare with allowables (basis and temperature).
4. Check fatigue at the hole with Kt and the fastener-induced preload.

## Gotchas
- Countersunk holes reduce bearing capacity (reduce for knife-edge depth).
- Interference-fit fasteners and cold working change fatigue behaviour.

## Verify
- [ ] Margins use basis allowables for the right temperature, thickness and grain direction.
