---
id: engineering-technology.chemical-engineering.process-design.carbon-footprint-of-utilities
name: carbon-footprint-of-utilities
category: engineering-technology
field: chemical-engineering
product: process-design
tags: [chemical-engineering, process-design, pd-sustainability-and-lca, carbon-footprint-of-utilities, carbon-footprint, emission-factor, utilities]
level: practitioner
status: verified
description: "Estimate the carbon footprint of process utilities (steam, electricity, fuel, cooling) with documented emission factors."
sources:
  - "GHG Protocol, A Corporate Accounting and Reporting Standard (Revised Edition), https://www.ghgprotocol.org/sites/default/files/standards/ghg-protocol-revised.pdf"
  - "US EPA, GHG Emission Factors Hub, https://www.epa.gov/climateleadership/ghg-emission-factors-hub"
  - "Towler and Sinnott, Chemical Engineering Design; Turton et al., Analysis, Synthesis and Design of Chemical Processes; Peters, Timmerhaus and West, Plant Design and Economics (textbooks, method only)"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Carbon footprint of utilities

**Goal:** Estimate the carbon footprint of process utilities (steam, electricity, fuel, cooling) with documented emission factors.

## Steps
1. Convert each utility duty into fuel or electricity use with efficiencies (boiler efficiency, compressor power).
2. Multiply by emission factors: fuel combustion factors from the fuel composition and grid electricity factors from the local grid and year.
3. Allocate steam and power from combined heat and power consistently, and state the method.
4. Sum scope 1 (direct) and scope 2 (purchased electricity; check the current GHG Protocol Scope 2 Guidance for purchased steam, heat and cooling) emissions for the unit and report per tonne of product.
5. Cite the source and year of every factor; grid factors are revised regularly (the US EPA GHG Emission Factors Hub publishes annual updates including eGRID electricity factors).

## Gotchas
- Emission factors are location and year specific (US EPA Hub or your national inventory); use the published factor for your jurisdiction and year and confirm it.
- Do not mix gross and net heating values.

## Verify
- [ ] Total reconciles with the fuel purchased.
- [ ] Factors are cited with source and year.
