---
id: engineering-technology.agricultural-and-biosystems-engineering.irrigation-design.emitter-selection-and-flow-exponent
name: emitter-selection-and-flow-exponent
category: engineering-technology
field: agricultural-and-biosystems-engineering
product: irrigation-design
tags: [agricultural-and-biosystems-engineering, irrigation-design, emitter-selection, drip-design, micro-irrigation, emitter-flow-exponent, pressure-compensating-emitter, drip-tape, inline-emitter]
level: practitioner
status: gated
description: "Select drip emitters: online or inline, pressure-compensating or turbulent, flow exponent x, coefficient of variation, spacing, flow rate and manufacturer data checks."
sources:
  - "Keller & Bliesner, Sprinkle and Trickle Irrigation"
  - "Hoffman et al., Design and Operation of Farm Irrigation Systems (ASABE)"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Emitter selection and flow exponent

**Goal:** an emitter whose flow variation over the design head range keeps uniformity high and which resists clogging in your water.

## Characteristics
- **Flow law**: `q = k H^x`. x of 0.5 for orifice/turbulent, about 0.7-1.0 for long laminar-path emitters, near 0 to 0.2 for pressure-compensating (PC) designs (gated: unconfirmed, source is paywalled or blocked). Flow variation for a head variation: `dq/q = x dH/H`.
- **Manufacturer's coefficient of variation Cv** of emitter flow from a batch (lower is better; values for good products are low single-digit percentages). Use the maker's data, and measure in field.
- **Types**: online (inserted in a pipe), inline (built into tube, thin-wall tape or thick-wall dripline), micro-sprinklers and jets for tree crops.
- **Flow rates and spacings**: row crops with thin-wall tape often 0.5-1.5 L/h at 20-60 cm; orchards 2-8 L/h at several per tree (gated: unconfirmed, source is paywalled or blocked). Set emitter flow and spacing for soil wetting pattern (sand: closer; clay: wider, lower flow).

## Selection steps
1. Choose by soil, crop and slope: PC emitters for long runs or slopes, turbulent non-PC for flat short runs.
2. Check the clogging resistance: larger flow-path dimension, flushing features, and self-cleaning PC diaphragms.
3. Work out the required pressure range from the maker's chart.
4. Confirm hydraulic variation at design (see lateral skill).

## Gotchas
- PC emitters have a minimum pressure to start regulating (often about 0.5-1.0 bar (gated: unconfirmed, source is paywalled or blocked)); check.
- Cheap thin-wall tape lasts a season or few; plan lifecycle.
- Emitter-to-emitter variation increases with wear.

## Verify
- [ ] Catch test of flows along a lateral matches the design EU.
