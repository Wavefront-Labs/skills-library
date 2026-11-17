---
id: engineering-technology.aerospace-engineering.ansys-fluent.fluent-force-and-moment-reports
name: fluent-force-and-moment-reports
category: engineering-technology
field: aerospace-engineering
product: ansys-fluent
tags: [fluent, ansys, fluent-postprocessing, force-reports, drag-lift-moment, report-definitions, convergence-monitor, coefficients]
level: practitioner
status: draft
description: "Define drag, lift and moment report definitions in Fluent with correct axes and moment centre, plot them as convergence monitors, and export results."
sources:
  - "Ansys Fluent user guide (force reports and report definitions)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# Fluent: force and moment reports

**Goal:** monitored, correct aerodynamic coefficients.

## Steps
1. **Solution > Report Definitions > New > Force:** Drag, Lift or Moment; select the wall zones making up the vehicle (not the symmetry plane or farfield), and give the force vector direction.
2. Check **Report Type**: coefficient (using reference values), force, or moment; and plot options (Print to Console, Plot, Write).
3. Moment definition: select moment centre and axis.
4. Add convergence conditions on each definition (for example stop when the standard deviation over 100 iterations is below a threshold).
5. After the run, use **Reports > Forces** for the pressure and viscous split, per-zone breakdown, and write to a file.

## Practice
- Report pressure and viscous components separately for drag audits.
- For component loads, report per zone (wing, fuselage, tail).

## Gotchas
- Forces on a half model are half; check the reference area.
- Wrong force direction vector at nonzero alpha swaps lift and drag.

## Verify
- [ ] Sum of zone forces equals total; sign and magnitude agree with a hand estimate.
