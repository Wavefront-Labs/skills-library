---
id: engineering-technology.automotive-vehicle-engineering.chassis-suspension-design.pedal-ratio-booster-and-master-cylinder
name: pedal-ratio-booster-and-master-cylinder
category: engineering-technology
field: automotive-vehicle-engineering
product: chassis-suspension-design
tags: [pedal-ratio, master-cylinder, brake-booster, brake-line-pressure, pedal-effort, caliper-clamp-force]
level: practitioner
status: gated
description: "Size the brake hydraulic chain: pedal ratio, booster, master cylinder bore, line pressure, caliper force and brake torque, with pedal travel checks."
sources:
  - "Limpert, Brake Design and Safety"
  - "Newcomb and Spurr, Braking of Road Vehicles"
  - "https://www.mlit.go.jp/jidosha/un/UN_R013H.pdf"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Pedal ratio, booster and master cylinder

1. Brake torque per wheel: `T = 2*mu_pad*p*A_piston*r_eff` for a disc brake (two pads, pad friction mu_pad, line pressure p, total caliper piston area, effective pad radius). Required T from the deceleration and axle load.
2. Line pressure: `p = (F_pedal*i_pedal*boost_ratio_or_added_force)/A_master`. Pedal ratio typically 3-5:1 (gated: unconfirmed, source is paywalled or blocked); booster adds force up to a limit (run-out) after which only pedal force adds.
3. Choose master cylinder bore: smaller bore gives higher pressure per pedal force but more pedal travel for the same fluid volume; check required fluid volume (caliper pistons, flexing hoses, pad wear) plus fade/compliance margin.
4. Pedal effort for 0.5 g stop target, and force at maximum deceleration: set by ergonomics and standards. UN R13-H (Annex 3) tests service braking with a foot force of 6.5 to 50 daN (65 to 500 N), requires at least 6.43 m/s2 mean fully developed deceleration from 100 km/h with the engine disconnected, and at least 5.76 m/s2 with the engine connected; confirm the current text.
5. Failure modes: loss of vacuum or booster means pedal forces must still reach the legislated deceleration; split circuits (diagonal or front/rear) required.
6. Check pedal travel and feel: jump-in, travel to bite, linearity.
7. Test: pedal force versus deceleration, travel, boosted and unboosted performance.

**Gotchas:** pedal feel suffering from compliance; hose expansion.

## Verify
- [ ] Unboosted deceleration meets the legal minimum at the permitted pedal force.
- [ ] Pedal travel at 1 g leaves a safety margin before the floor.
