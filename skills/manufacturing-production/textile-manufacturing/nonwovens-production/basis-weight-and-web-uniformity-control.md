---
id: manufacturing-production.textile-manufacturing.nonwovens-production.basis-weight-and-web-uniformity-control
name: basis-weight-and-web-uniformity-control
category: manufacturing-production
field: textile-manufacturing
product: nonwovens-production
tags: [nonwovens-production, nonwovens, spunbond, meltblown, sms, spunmelt, carded-web, carding, cross-lapper, needlepunch, needle-punching, hydroentangling, spunlace, thermal-bonding, calender-bonding, through-air-bonding, basis-weight, gsm, cd-profile, md-profile, beta-gauge, online-scanner, web-uniformity, formation, polypropylene, pp, pet, filtration, hygiene, reicofil, andritz, oerlikon, dilo, edana, inda, tensile-strength]
level: practitioner
status: draft
description: "Hold basis weight and uniformity on spunmelt and carded nonwoven lines: reading online scanner CD/MD profiles, the main levers per process, bonding checks and common web defects."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Basis weight and web uniformity control

**Goal:** nonwoven rolls at the specified **basis weight** (g/m²) with an even
**cross-direction (CD) profile** and the required strength — every metre. Customers
(hygiene, medical, filtration) test basis weight and tensile per roll; light spots also
fail barrier and filtration properties.

## 1. Read the profile, not just the average
- **Online scanners** (beta/X-ray/IR gauges traversing the web) report:
  - **MD** (machine-direction) variation over time — trends, cycling.
  - **CD profile** — weight across the width, often as a colour map over time.
  - **Short-term/formation** variation (cloudiness) — within-sample uniformity.
- Confirm against **lab cut-and-weigh**: die-cut samples (e.g. 100 cm²) across the
  width, weighed and reported per standard test methods (EDANA/INDA NWSP methods are
  typical). Recalibrate the scanner if they disagree.

## 2. Spunbond / meltblown (spunmelt) levers
- **Basis weight = polymer throughput ÷ (belt speed × width)**. Throughput from spin
  pump speed; the gross lever is pump speed vs belt speed.
- **CD profile**: die/spinneret temperature zones, polymer distribution in the die
  (coat-hanger), blocked capillaries (light streaks), quench/process air uniformity
  across the width, suction under the belt.
- **Meltblown**: air temperature and flow (fibre diameter), die-to-collector distance
  (DCD), polymer MFI. Shot (polymer beads) comes from too-low air or too-hot polymer.
- Polymer: melt flow index (MFI) changes with resin lot; check incoming material data.
- Spinneret/die cleaning schedule — blocked holes grow over time.

## 3. Carded lines (needlepunch, spunlace, thermal bonded)
- **Fibre feed**: opening/blending consistent, chute/volumetric feed and weigh-pan
  feeders for card feed weight; card settings (cylinder, worker/stripper clearances).
- **Cross-lapper** builds the batt: its traverse profiling controls CD profile
  (edges often heavier — use the lapper's profiling function).
- **Drafting/stretching** downstream changes weight and fibre orientation (MD:CD
  strength ratio).
- Card clothing wear → neps and thin spots; maintain on schedule.

## 4. Bonding checks
- **Thermal calender**: roll temperature (both rolls, across width), nip pressure,
  bond-point pattern. Under-bonded → fuzz, low tensile; over-bonded → stiff, pinholes.
- **Needlepunch**: needle density (punches/cm²), penetration depth, needle wear/breakage
  (broken needles leave lines and can contaminate product — log and remove).
- **Hydroentangling**: water jet pressure per manifold, nozzle strip condition (blocked
  jets → streaks), water filtration, drying.
- **Through-air**: air temperature uniformity across the oven for bicomponent fibres.
Test **tensile strength and elongation** MD and CD per roll/lot, plus thickness and
application tests (air permeability, hydrohead, absorbency) per spec.

## 5. Web defects
| Defect | Cause |
|---|---|
| MD streaks (light/heavy lines) | Blocked spinneret holes, die zone, blocked hydro jets, card wire damage |
| Holes/thin spots | Drips, shot, vacuum problems, web breaks |
| Drips/polymer lumps | Die leaks, degraded polymer |
| Edge heavy/light | Lapper profile, edge suction/trim settings |
| Cloudy formation | Air turbulence, fibre opening, card settings |
| Wrinkles | Winder tension, uneven bonding |

## 6. Winding and roll quality
Winder tension and slitter settings; roll labels with lot, position across the width
(slit position), and length. Keep **lane** identity — a defect in one CD position
affects specific slit rolls.

## Verify
- [ ] Scanner verified against lab cut-and-weigh.
- [ ] Basis weight mean on target; CD profile within spread limit.
- [ ] Tensile MD/CD and application tests pass per roll/lot.
- [ ] Defect inspection (camera system) alarms reviewed; affected lanes held.

*Draft: test methods and limits depend on customer and NWSP/ISO standard versions;
line-specific control loops (auto die-bolt or profile control) vary by OEM.*
