---
id: engineering-technology.chemical-engineering.process-design.pfd-and-stream-table-development
name: pfd-and-stream-table-development
category: engineering-technology
field: chemical-engineering
product: process-design
tags: [chemical-engineering, process-design, pd-design-basis-and-pfd, pfd-and-stream-table-development, pfd, process-flow-diagram, stream-table, stream-numbering, flowsheet-drawing, equipment-numbering, heat-and-material-balance]
level: practitioner
status: draft
description: "Develop a process flow diagram and its stream table: what to show, numbering, stream properties, and consistency checks with the heat and material balance."
sources:
  - "Towler and Sinnott Chemical Engineering Design, Turton et al. Analysis Synthesis and Design of Chemical Processes, Peters Timmerhaus and West Plant Design and Economics, Douglas Conceptual Design of Chemical Processes, NCEES FE and PE Chemical exam specifications"
  - "https://www.aiche.org"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# PFD and stream table development

**Goal:** a PFD that a new engineer can read in minutes, tied line-by-line to the stream table.

## What the PFD shows
- Major equipment (vessels, columns, exchangers, pumps, compressors, reactors) with tag numbers and a short name.
- Main process lines with flow arrows, stream numbers in diamonds or boxes, major bypasses and recycles.
- Key control loops that fix the operating concept (not every instrument; that is the P&ID).
- Utilities connections, shown as lines to equipment with utility names.
- Basic equipment data in a box below or beside: duty, area, volume, power.

## Stream table
For every numbered stream list: phase, temperature, pressure, mass flow, molar flow, component flows (or fractions), enthalpy flow or specific enthalpy, density or volumetric flow, and the molecular weight. Add a footnote of the basis (kg/h, hours per year, design case).

## Numbering
Use a consistent scheme: equipment tags as type letter plus unit plus sequence (for example E-101 for a heat exchanger in unit 100). Stream numbers sequential through the flowsheet; never reuse after deletion.

## Consistency checks
1. Mass balance closes on every unit and on the overall plant.
2. Streams on the PFD are exactly those in the table.
3. Simulation output copied by script, not typed, to prevent transcription errors.
4. Operating temperatures and pressures stay consistent with equipment ratings added later.

## Gotchas
- A PFD is a snapshot of one case; label normal, maximum and turndown cases separately if they differ.
- Do not clutter with spare equipment or drains; those go on the P&ID.

## Verify
- [ ] Overall mass closes in kg/h; every unit closes.
- [ ] Each stream appears once with unique number.
