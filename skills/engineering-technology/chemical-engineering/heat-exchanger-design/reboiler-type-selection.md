---
id: engineering-technology.chemical-engineering.heat-exchanger-design.reboiler-type-selection
name: reboiler-type-selection
category: engineering-technology
field: chemical-engineering
product: heat-exchanger-design
tags: [chemical-engineering, heat-exchanger-design, hx-condensers-reboilers, reboiler-type-selection, reboiler, kettle-reboiler, thermosiphon-reboiler, forced-circulation, reboiler-selection, column-bottoms, vaporizer, heat-duty]
level: practitioner
status: draft
description: "Select a reboiler type (kettle, vertical or horizontal thermosiphon, forced circulation, internal) from fouling, vacuum, viscosity, duty and plot constraints."
sources:
  - "Kern Process Heat Transfer, Perry Handbook heat transfer section, TEMA Standards, Heat Exchanger Design Handbook (HEDH), Kemp Pinch Analysis and Process Integration, Smith Chemical Process Design and Integration"
  - "https://www.aiche.org"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Reboiler type selection

**Goal:** the right vaporiser for a column or process duty.

## Options
| Type | Strengths | Limits |
|---|---|---|
| **Kettle** (K shell) | Simple, separate disengagement space, good for high vaporisation, vacuum and wide-boiling mixtures | Large shell and holdup (bad for heat-sensitive materials), poor with fouling and solids, relatively costly |
| **Vertical thermosiphon** | Compact, low fouling, no pump, short residence time | Needs elevation difference and low pressure drop, instability with viscous or vacuum service, limited to moderate vaporisation per pass |
| **Horizontal thermosiphon** | Lower elevation, better for large duties | Piping complexity, stability with wide boiling range |
| **Forced circulation** | Handles viscous, fouling and high solids services, high velocity | Pump cost, operation and maintenance, low circulation failure risk |
| **Internal (in-column) reboiler** | Cheap, small | Small duties, hard to maintain |

## Selection steps
1. Define duty, bottoms composition range, operating pressure, vaporisation fraction, fouling tendency and viscosity.
2. For clean, low-to-moderate-viscosity service at moderate pressure the vertical thermosiphon is the default.
3. For vacuum columns or heat-sensitive products think of kettles or forced circulation with careful holdup control.
4. For wide-boiling mixtures prefer once-through or kettle to avoid heavy accumulation at the exchanger.
5. Choose heating medium: steam (pressure level sets temperature; condensing steam gives high duty control) or hot oil; limit wall temperature to avoid fouling or decomposition.
6. Keep the heat flux below about 70% of the critical (see the boiling skill).

## Gotchas
- Control: thermosiphon flow cannot be throttled on the process side; control the heating medium.
- Reboiler instability (flow oscillations) is a common startup problem; check the hydraulics at turndown.
- Steam trap and condensate drainage to avoid flooding the tubes.

## Verify
- [ ] Selection table with chosen type and the rejected alternatives and reasons.
- [ ] Wall temperature and heat flux within limits.
