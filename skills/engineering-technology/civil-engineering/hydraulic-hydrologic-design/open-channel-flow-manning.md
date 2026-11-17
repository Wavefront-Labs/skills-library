---
id: engineering-technology.civil-engineering.hydraulic-hydrologic-design.open-channel-flow-manning
name: open-channel-flow-manning
category: engineering-technology
field: civil-engineering
product: hydraulic-hydrologic-design
tags: [open-channel-flow, manning, normal-depth, critical-depth, froude-number, hydraulic-radius, channel-design, hydraulic-jump, specific-energy, roughness]
level: practitioner
status: draft
description: "Compute normal and critical depth in open channels with Manning's equation: SI/US constants, hydraulic radius, Froude regime, roughness choice, hydraulic jump check."
sources: ["Chow, Open-Channel Hydraulics", "Chaudhry, Open-Channel Flow", "FHWA HDS-3 Design of Roadside Channels with Flexible Linings", "Arcement and Schneider, USGS WSP 2339 Guide for Selecting Manning's Roughness Coefficients"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# Open-channel flow with Manning's equation

Q = (k/n) A R^(2/3) S^(1/2). k = 1.0 in SI (m, m3/s) and 1.486 in US customary (ft, cfs). A area, R = A/P hydraulic radius, S bed slope (equals energy slope at normal depth).

## Normal depth
Solve for y by iteration because A and R depend on y. Rectangular: A = b y, P = b + 2y. Trapezoid with side slope z (horizontal per 1 vertical): A = (b + z y) y, P = b + 2 y sqrt(1 + z^2).

## Critical depth and regime
- Froude number Fr = V / sqrt(g D), D = A/T hydraulic depth. Fr < 1 subcritical (downstream control), Fr > 1 supercritical (upstream control).
- Critical flow condition: Q^2 T / (g A^3) = 1. Rectangular: yc = (q^2/g)^(1/3), q = Q/b.
- Slope steeper than critical gives supercritical flow; where it meets a subcritical reach a hydraulic jump forms, so check energy dissipation and freeboard.

## Roughness n
Concrete about 0.012 to 0.015; grass-lined 0.03 to 0.05 or more (depends on depth and retardance); natural streams about 0.03 to 0.1 or more. Choose from photo guides (USGS) and calibrate where possible. Vegetation roughness falls as depth rises.

## Design
Check velocity limits (erosion; use tractive shear for riprap or linings), freeboard, bends, and subcritical operation where possible.

## Verify
Recompute Q from the solved y; cross-check against HEC-RAS or a spreadsheet.

> Professional guidance only. Design, sign-off and site decisions belong to a licensed/chartered engineer applying the codes adopted in the project jurisdiction; check edition and local amendments.
