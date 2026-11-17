---
id: engineering-technology.chemical-engineering.separation-processes.extractor-equipment-selection
name: extractor-equipment-selection
category: engineering-technology
field: chemical-engineering
product: separation-processes
tags: [chemical-engineering, separation-processes, sep-liquid-extraction, extractor-equipment-selection, extractor-selection, mixer-settler, rotating-disc-contactor, pulsed-column, centrifugal-extractor, extraction-column, kuhni, karr-column]
level: practitioner
status: draft
description: "Choose liquid-liquid extraction equipment (mixer-settler, packed, pulsed, rotating-disc, centrifugal) from stage count, density difference, interfacial tension and fouling."
sources:
  - "Seader Henley and Roper Separation Process Principles, Perry Chemical Engineers Handbook separations sections, Kister Distillation Design, Treybal Mass-Transfer Operations, McCabe Smith and Harriott Unit Operations"
  - "https://www.aiche.org"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Extractor equipment selection

**Goal:** a justified choice of contactor.

## Selection factors
1. **Stages needed**: a few stages (1 to 5) suit mixer-settlers; 5 to 10 favour agitated or pulsed columns; more can need multiple columns.
2. **Density difference and interfacial tension**: a low density difference (below about 0.05 to 0.1 g/cm3) or low interfacial tension favours centrifugal contactors (very short residence time), high-density-difference systems work in simple columns.
3. **Throughput**: large flows favour columns; small flows and many products favour mixer-settlers or centrifugal units.
4. **Residence time**: sensitive products (unstable compounds) need centrifugal contactors; slow-reaction systems tolerate mixer-settlers.
5. **Fouling and solids**: avoid packed columns; open-agitated column or mixer-settler is easier to clean.
6. **Footprint and head room**, inventory (flammable solvents lower inventory in centrifugal units), operability and turndown.

## Types
- **Mixer-settler**: stages in series, flexible, large footprint and inventory.
- **Spray, packed and sieve-tray columns**: cheap, few effective stages.
- **Agitated columns** (rotating disc, Scheibel, Kuhni) and **pulsed or reciprocating plate (Karr)** columns: more stages per height, moderate cost.
- **Centrifugal contactors**: compact and fast, higher capital and maintenance.

## Procedure
1. Compile properties: densities, viscosities, interfacial tension, solids.
2. Screen against the above factors; use vendor guidance and pilot tests.
3. Size from HETS and flooding data from the vendor.
4. Plan phase separation (coalescers) and entrainment control.

## Gotchas
- Emulsions and rag layers; surface-active impurities change interfacial behaviour.
- Mass transfer direction (dispersed to continuous or reverse) changes drop behaviour (Marangoni effects).

## Verify
- [ ] Pilot-scale test or vendor reference for similar chemistry.
- [ ] Flooding and phase separation margins stated.
