---
id: engineering-technology.chemical-engineering.piping-instrumentation.pump-and-system-curve-matching
name: pump-and-system-curve-matching
category: engineering-technology
field: chemical-engineering
product: piping-instrumentation
tags: [chemical-engineering, piping-instrumentation, pi-pump-hydraulics, pump-and-system-curve-matching, pump-curve, system-curve, operating-point, affinity-laws, best-efficiency-point, parallel-pumps, pump-selection, total-dynamic-head]
level: practitioner
status: gated
description: "Plot system and pump curves to find the operating point, apply affinity laws, check position relative to best efficiency point and the effect of parallel and series pumps."
sources:
  - "Crane Technical Paper 410, Perry Handbook fluid transport section, ASME B31.3 Process Piping, ISA-5.1, ISO 10628, ISA-75.01.01 / IEC 60534-2-1, Darby Chemical Engineering Fluid Mechanics, Karassik Pump Handbook"
  - "https://www.aiche.org"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Pump and system curve matching

**Goal:** a pump that operates near its best efficiency point (BEP) across the real flow range.

## System curve
H_sys(Q) = (static head + delta P/(rho g) between end points) + K_sys Q^2, where K_sys comes from the friction in pipes, fittings and equipment at design flow. For a control valve, add its pressure drop at the flow.

## Procedure
1. Compute the head required at minimum, normal and maximum flow, adding margin (margins set by company practice; do not stack margins).
2. Plot the system curve for the clean and fouled cases.
3. Overlay the vendor pump curves (head, efficiency, power, NPSHr versus flow).
4. The operating point is the intersection. Check: normal flow lies within the preferred operating region, often quoted as about 70 to 110% of BEP flow (gated: unconfirmed, source is paywalled or blocked), minimum stable flow is respected, and the maximum flow is below the end of the curve with NPSHr margin.
5. Check the shutoff head against the downstream design pressure (a pump can reach it on blocked discharge).
6. Power: P_shaft = rho g Q H/eta; choose the motor with a margin (margin per company practice or API 610 (gated: unconfirmed, source is paywalled or blocked); the motor must cover the end of the curve).

## Affinity laws (for speed change N or impeller trim D)
Q2/Q1 = N2/N1, H2/H1 = (N2/N1)^2, P2/P1 = (N2/N1)^3 (and similar for trimming, approximately).

## Parallel and series
Parallel pumps add flow at the same head; the combined operating point is lower than twice one pump flow because the system curve rises; check each pump stays above minimum flow. Series pumps add head.

## Gotchas
- Oversized pumps throttled by control valves waste energy and run far left of BEP.
- Curves are for water; viscous liquids need correction factors.

## Verify
- [ ] Operating point for each case marked on the curve with percent of BEP.
- [ ] Shutoff head and motor power checked.
