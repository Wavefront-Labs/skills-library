---
id: engineering-technology.chemical-engineering.piping-instrumentation.pipe-schedule-and-wall-thickness
name: pipe-schedule-and-wall-thickness
category: engineering-technology
field: chemical-engineering
product: piping-instrumentation
tags: [chemical-engineering, piping-instrumentation, pi-line-sizing, pipe-schedule-and-wall-thickness, pipe-schedule, wall-thickness, asme-b31-3, pressure-design-thickness, corrosion-allowance, mill-tolerance, nominal-pipe-size, piping-class]
level: practitioner
status: gated
description: "Select pipe schedule and wall thickness with the ASME B31.3 pressure design equation, corrosion allowance and mill tolerance, as an engineering estimate for the piping designer."
sources:
  - "Crane Technical Paper 410, Perry Handbook fluid transport section, ASME B31.3 Process Piping, ISA-5.1, ISO 10628, ISA-75.01.01 / IEC 60534-2-1, Darby Chemical Engineering Fluid Mechanics, Karassik Pump Handbook"
  - "https://www.aiche.org"
  - "https://www.asme.org/codes-standards/find-codes-standards/b36-10-welded-seamless-wrought-steel-pipe"
  - "https://www.asme.org/codes-standards/find-codes-standards/b31-3-process-piping (B31.3-2024 current)"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Pipe schedule and wall thickness selection

**Goal:** a preliminary wall thickness and schedule for estimating and line lists. Final design is by qualified piping engineers to the applicable code and edition (for process piping commonly ASME B31.3; confirm the edition and jurisdiction).

## Pressure design thickness (straight pipe, internal pressure, B31.3 form)
t = P D / [2 (S E W + P Y)] (B31.3 form; confirm the equation and terms in the current edition (gated: unconfirmed, source is paywalled or blocked))
with P the internal design gauge pressure, D the outside diameter, S the allowable stress at the design temperature from the code tables, E the quality factor, W the weld joint strength reduction factor (1 below the creep range), and Y a coefficient (0.4 for ferritic steels at moderate temperature (gated: unconfirmed, source is paywalled or blocked)). Check the code for the conditions of use.

## Minimum required thickness
t_m = t + c, where c is the sum of corrosion, erosion and thread or groove allowances (corrosion allowance is set by corrosion data, not a default). Since mill tolerance on seamless pipe is commonly 12.5% under (gated: unconfirmed, source is paywalled or blocked), the nominal thickness must be at least t_m/0.875 (1/0.875 = 1.143).

## Selecting the schedule
1. Compute the nominal thickness required.
2. Select the next standard wall (NPS and schedule from ASME B36.10M "Welded and Seamless Wrought Steel Pipe", 2018 edition on stabilized maintenance, and B36.19M "Stainless Steel Pipe", 2018, per asme.org) with nominal thickness not less than required.
3. Record the piping class (material, rating, corrosion allowance, flange class) that covers the line.
4. Consider other loads (external pressure and vacuum, weight, thermal expansion, wind) which often govern large or thin pipes.

## Practice
For many lines the minimum practical schedule is set by handling (small bore: Sch 80 or XS for threaded or vibration-prone connections).

## Gotchas
- Allowable stresses depend on temperature and material grade: use the code table for the actual design temperature.
- Flange rating (Class 150, 300, ...) must also suit the design pressure and temperature.

## Verify
- [ ] The calculation cites the code edition and the stress table used.
- [ ] A qualified piping engineer has reviewed any line used for safety-critical service.
