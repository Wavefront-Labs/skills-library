---
id: engineering-technology.chemical-engineering.piping-instrumentation.compressor-selection-and-staging
name: compressor-selection-and-staging
category: engineering-technology
field: chemical-engineering
product: piping-instrumentation
tags: [chemical-engineering, piping-instrumentation, pi-compressors-and-vacuum, compressor-selection-and-staging, compressor-selection, compressor-staging, centrifugal-compressor]
level: practitioner
status: gated
description: "Select a compressor type (centrifugal, reciprocating, screw) and number of stages from flow, pressure ratio and gas properties."
sources:
  - "Crane Technical Paper 410, Perry Chemical Engineers Handbook, ASME B31.3, ISA-5.1, Darby Chemical Engineering Fluid Mechanics, Karassik Pump Handbook"
  - "https://www.isa.org"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Compressor selection and staging

**Goal:** Select a compressor type (centrifugal, reciprocating, screw) and number of stages from flow, pressure ratio and gas properties.

## Steps
1. Use the flow and head: centrifugal for large flows at moderate ratios, reciprocating for high ratios and low flow, screw for medium flows and dirty gases.
2. Divide the overall ratio over stages, commonly equal ratios with intercooling to limit discharge temperature (for reciprocating machines, ratio per stage is often limited to about 3 to 4 (gated: unconfirmed, source is paywalled or blocked); confirm with the vendor).
3. Check the molecular weight sensitivity for centrifugal machines, which change head capability.
4. Plan the driver (motor, steam turbine, gas turbine), the spare, and the capacity control (speed, inlet guide vanes, recycle, unloaders).
5. Collect vendor options and compare lifecycle cost, availability and maintenance.

## Gotchas
- Variable gas composition is difficult for centrifugal compressors.
- Pulsation studies are needed for reciprocating machines.

## Verify
- [ ] Stage ratios give acceptable discharge temperatures.
- [ ] Capacity control range covers the operating cases.
