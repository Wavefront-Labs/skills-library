---
id: engineering-technology.agricultural-and-biosystems-engineering.irrigation-design.fertigation-injection-and-backflow-prevention
name: fertigation-injection-and-backflow-prevention
category: engineering-technology
field: agricultural-and-biosystems-engineering
product: irrigation-design
tags: [agricultural-and-biosystems-engineering, irrigation-design, fertigation-injection, drip-design, micro-irrigation, chemigation, venturi-injector, injection-pump, backflow-prevention, check-valve]
level: practitioner
status: gated
description: "Design drip fertigation: injector types, injection-rate calculation, compatibility and acid precautions, and the backflow-prevention hardware and interlocks regulators require."
sources:
  - "Keller & Bliesner, Sprinkle and Trickle Irrigation"
  - "Hoffman et al., Design and Operation of Farm Irrigation Systems (ASABE)"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Fertigation injection and backflow prevention

**Goal:** apply nutrients through the system evenly, safely and without contaminating the water source.

## Injection devices
- **Venturi**: simple, uses pressure drop; flow varies with pressure.
- **Positive displacement pumps** (piston, diaphragm): fixed rate; proportional (water-driven) injectors keep ratio constant.
- **Pump-to-tank with metering valve** for gravity systems.

## Injection rate
`injection rate (L/h) = nutrient dose (kg/ha) x area (ha) / (concentration of nutrient in stock (kg/L) x injection time (h))`. Run for the middle part of the irrigation set, with flushing at start (to charge the pipe) and at the end (to clear the lines); the water-only flush time equals the transit time to the farthest emitter.

## Compatibility and precautions
1. Run a jar test of mixed fertiliser: calcium with sulphate or phosphate precipitates; do not mix incompatible stocks in one tank.
2. Acid (to control pH or clean) and chlorine must be handled per safety data sheets; add acid to water, never water to acid; do not mix acid and chlorine (toxic gas).
3. Use corrosion-resistant materials for injectors and pipes.
4. Fertiliser injection upstream of filters lets filters catch precipitates; check the maker's advice per product.

## Backflow prevention
Chemigation systems require protection of the water source: an irrigation pipeline check valve, vacuum relief, low-pressure drain, and an injection check valve, plus interlocks so the injector stops if the irrigation pump stops. Exact devices and certification are set by local or national regulation and the water authority; follow them and use a qualified, licensed installer.

## Verify
- [ ] Uniformity of EC (or tracer) along the lateral is within about 10 percent (gated: unconfirmed, source is paywalled or blocked).
- [ ] Interlock and backflow devices tested and recorded.
