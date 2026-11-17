---
id: engineering-technology.agricultural-and-biosystems-engineering.irrigation-design.drip-filtration-design-and-backflush
name: drip-filtration-design-and-backflush
category: engineering-technology
field: agricultural-and-biosystems-engineering
product: irrigation-design
tags: [agricultural-and-biosystems-engineering, irrigation-design, filtration-design, drip-design, micro-irrigation, media-filter, disc-filter, screen-filter, hydrocyclone, backflush]
level: practitioner
status: gated
description: "Specify drip filtration: screen, disc, media and hydrocyclone selection by water source, mesh size from emitter passage, flow rate, pressure-loss alarms and automatic backflush."
sources:
  - "Keller & Bliesner, Sprinkle and Trickle Irrigation"
  - "Hoffman et al., Design and Operation of Farm Irrigation Systems (ASABE)"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Drip filtration design and backflush

**Goal:** protect emitters from physical clogging at an acceptable cost and maintenance burden.

## Selection by source
- **Well water, low solids**: screen or disc filters; hydrocyclone (sand separator) in front if the well pumps sand.
- **Surface water (canal, pond), organics**: media (sand/gravel) filters, often followed by a screen or disc safety filter.
- **High-algae water**: media filtration plus chlorination ahead of filters; shade and cover ponds.

## Sizing
1. **Filtration degree**: the opening should be about one-tenth to one-fifth of the smallest emitter passage (gated: unconfirmed, source is paywalled or blocked); the maker gives the required mesh (typical 120-200 mesh for many emitters (gated: unconfirmed, source is paywalled or blocked)).
2. **Flow**: do not exceed the filter's rated flow per unit area; for media filters use the maker's flow per tank (often about 40-60 m3/h per m2 of media bed (gated: unconfirmed, source is paywalled or blocked), check the data sheet).
3. **Pressure loss**: clean loss usually 0.1-0.5 bar; backflush at a pressure differential of about 0.5 bar above the clean value (gated: unconfirmed, source is paywalled or blocked) (manufacturer specific). Use differential pressure switches.
4. **Backflush flow**: media tanks need enough flow from other tanks; use two or more tanks so the others supply the backwash; design the pump for the extra flow while backwashing.
5. Provide a safety screen/disc downstream of media filters.

## Gotchas
- Dirty filters reduce flow and emitter pressure; the pump's duty point shifts.
- Disposal of backwash water into a pond or field must respect local rules.
- Media loses effect if channels form; replace per maker's schedule.

## Verify
- [ ] Differential pressure logged; backflush events are as designed.
- [ ] Downstream sample shows no particles above the emitter limits.
