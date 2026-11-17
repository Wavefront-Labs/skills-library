---
id: engineering-technology.chemical-engineering.piping-instrumentation.pid-equipment-and-nozzle-information
name: pid-equipment-and-nozzle-information
category: engineering-technology
field: chemical-engineering
product: piping-instrumentation
tags: [chemical-engineering, piping-instrumentation, pi-pid-development, pid-equipment-and-nozzle-information, equipment-tags, nozzle-schedule, pid-data]
level: practitioner
status: draft
description: "Record equipment tags and nozzle information on a P&ID: sizes, ratings, design data blocks and connection details."
sources:
  - "Crane Technical Paper 410, Perry Chemical Engineers Handbook, ASME B31.3, ISA-5.1, Darby Chemical Engineering Fluid Mechanics, Karassik Pump Handbook"
  - "https://www.isa.org"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Pid equipment and nozzle information

**Goal:** Record equipment tags and nozzle information on a P&ID: sizes, ratings, design data blocks and connection details.

## Steps
1. Show equipment tag and name, with a data block of design pressure, temperature and the capacity or volume as the company standard requires.
2. Show nozzle sizes and ratings for the key nozzles, and the facing, with a nozzle schedule kept in a controlled document.
3. Indicate the elevation-critical items (for example NPSH height, barometric legs, drain by gravity) in notes.
4. Show internals relevant to the process (trays, demisters, distributors) and their reference numbers.
5. Keep the P&ID, the datasheets and the nozzle list consistent by a controlled change process.

## Gotchas
- Mismatch between datasheet and P&ID is a common source of errors.
- Do not put detailed vessel mechanical data on the P&ID.

## Verify
- [ ] Nozzles on the P&ID match the datasheet.
- [ ] Design pressures and temperatures agree with the process data.
