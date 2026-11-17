---
id: architecture-construction.architecture.building-codes-compliance.egress-and-occupancy-code-analysis
name: egress-and-occupancy-code-analysis
category: architecture-construction
field: architecture
product: building-codes-compliance
tags: [building-codes-compliance, building-code, code-analysis, code-review, ibc, international-building-code, nfpa-101, life-safety-code, approved-document-b, building-regulations, ncc, bca, occupancy-classification, use-group, occupant-load, occupant-load-factor, means-of-egress, exit-width, travel-distance, common-path-of-travel, dead-end-corridor, exit-separation, number-of-exits, fire-separation, fire-resistance-rating, construction-type, life-safety-plan, sprinklers, accessibility, ada, permit-set]
level: practitioner
status: draft
description: "Run an egress/life-safety code analysis: classify occupancy, compute occupant loads, size and count exits, check travel distance, common path, dead ends and separation, and draw a life-safety plan."
sources: ["International Building Code (ICC) chapters 3, 5, 6, 10", "NFPA 101 Life Safety Code", "UK Approved Document B; Australian NCC Volume One (for equivalent concepts)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Egress and occupancy code analysis

**Goal:** a written, repeatable code analysis that proves people can get out — done at
schematic design, when moving a stair is cheap, not at permit when it isn't.

> **Jurisdiction warning.** The *method* below is common to most codes; the *numbers*
> are not. Examples cite the IBC style of thinking only to illustrate. Always use the
> edition adopted by your jurisdiction plus local amendments, and confirm with the
> building official or a fire engineer. Figures here are illustrative, not authoritative.

## 1. Set up the analysis sheet
Record: governing code and edition, local amendments, sprinklered (yes/no — it changes
almost every limit), construction type, building height and storeys, area per floor.

## 2. Occupancy classification
Classify each space by **use**, not by name: assembly, business, educational,
mercantile, residential, storage, institutional, etc. (IBC Chapter 3 groups A, B, E, M,
R, S, I…). Mixed use: decide whether occupancies are **separated** (fire barriers
between, each judged on its own) or **non-separated** (most restrictive rules apply
throughout). Small accessory areas may be allowed under a percentage threshold — check.

## 3. Occupant load
`Occupant load = floor area ÷ occupant load factor` for each function.
- Use **gross** or **net** area as the table specifies per use (IBC uses gross for
  offices, net for classrooms/assembly — verify).
- Illustrative factors from IBC-style tables: business ≈ 150 sf gross/person
  (older editions 100), assembly unconcentrated (tables and chairs) 15 sf net,
  standing space 5 sf net. *Look up the adopted table.*
- Fixed seating: count seats.
- Sum per room → per floor → per exit stair.

## 4. Number of exits
Driven by occupant load per room/storey (and sometimes by travel distance or use).
Commonly: 1–500 occupants → 2 exits; 501–1,000 → 3; >1,000 → 4 (IBC-type). Single-exit
spaces are allowed only below specific occupant and travel limits.

## 5. Exit capacity (width)
`Required width = occupant load × width factor` (e.g. inch-per-occupant factors, lower
for sprinklered buildings, different for stairs vs level components). Then:
- Respect **minimum** widths (corridors, doors' *clear* width, stair width) even when
  the calculation says less.
- **Balanced exits:** losing any one exit must not reduce capacity below a set fraction
  (IBC: no more than 50% of the required capacity through one exit).

## 6. Arrangement
- **Exit separation:** two exits at least ½ the overall diagonal of the area served
  apart (⅓ if fully sprinklered, IBC-type).
- **Travel distance** to an exit, measured along the actual path around furniture and
  walls, within the table limit for the occupancy and sprinkler status.
- **Common path of travel** (before occupants have a choice of two routes) and
  **dead-end corridors** within their limits.
- Doors swing in the direction of egress above an occupant threshold; no egress through
  kitchens, storerooms or lockable spaces.

## 7. Fire separation and construction type
Check allowable height/area for the occupancy and construction type (with sprinkler
and frontage increases); identify rated assemblies: exit stairs/shafts, corridors where
required, occupancy separations, fire walls. Rated walls continue to the deck above and
openings need rated doors/dampers.

## 8. Life-safety plan
Per floor: occupancy per room, occupant loads, exit locations and capacities, travel
paths with distances, rated walls (colour/linetype by rating), sprinkler note,
fire-extinguisher and alarm locations if required. Reviewers read this sheet first.

## Gotchas
- The occupant load from the *code*, not the client's headcount, sizes egress.
- Accessible means of egress (areas of refuge, evacuation lifts) is a separate check.
- Stairs discharging into a lobby must meet specific conditions — confirm.

## Verify
- [ ] Code edition, amendments and sprinkler status stated on the analysis.
- [ ] Every room has an occupancy, area basis and occupant load.
- [ ] Exits counted and sized; balanced-capacity check passes.
- [ ] Separation, travel distance, common path and dead-end measured on plan.
- [ ] Life-safety plan issued with the permit set; uncertainties raised with the official.
