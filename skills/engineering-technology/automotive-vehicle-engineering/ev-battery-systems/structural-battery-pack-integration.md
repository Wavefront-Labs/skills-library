---
id: engineering-technology.automotive-vehicle-engineering.ev-battery-systems.structural-battery-pack-integration
name: structural-battery-pack-integration
category: engineering-technology
field: automotive-vehicle-engineering
product: ev-battery-systems
tags: [structural-battery-pack, pack-mechanical, cell-to-body, structural-pack, floor-stiffness, pack-integration, battery-enclosure, load-path, adhesive-bonding]
level: practitioner
status: draft
description: "Integrate the battery pack as a vehicle structural member: load paths, stiffness contribution, joint design, service access, and trade-offs against crash and thermal needs."
sources:
  - "Warner, Lithium-Ion Battery Chemistries and Pack Design (chapter list)"
  - "Kramer, Passive Safety of Vehicles (chapter list)"
  - "UN Regulation 100 (REESS safety; confirm current revision at https://unece.org)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# Structural battery pack integration

## 1. Idea
Instead of a pack carried by the body, the pack enclosure (and sometimes the cells) carries body loads: floor bending and torsion stiffness, side-impact paths, seat anchorage. Benefits are stiffness, packaging height and mass. Costs are complexity in service, repair, thermal and crash design.

## 2. Levels of integration (pick deliberately)
1. **Bolted underfloor pack:** a separate unit attached at many points; modest stiffness contribution.
2. **Pack as floor structure (pack-to-body, cell-to-body):** the pack top or tray forms the passenger floor; cell-to-pack removes modules.
3. **Cells as structure (structural adhesives or foam around cells):** early production and research; needs deep CAE and cell-level mechanical data.

## 3. Design steps
1. Define pack load cases: body torsion, bending, seat and belt anchorage, side-impact path, jacking, towing, underbody strike.
2. Set a stiffness contribution target (share of body torsional stiffness) by CAE; compare with a non-structural baseline.
3. Design attachments: bolt pattern, adhesive plus bolt, sealed joints; check joint stiffness (see body joint stiffness). Include thermal expansion mismatch between an aluminium tray and a steel body.
4. Protect cells: allowable cell deformation, and cell swelling pressure on enclosure walls over life.
5. Keep thermal-runaway venting paths separate from structural paths.
6. Plan service and repair: how to remove or repair after a crash or cell failure; bonded structures usually limit this.

## 4. Verification
Pack stiffness tests (torsion and bending), vehicle torsional stiffness test, vibration and shock (see pack vibration test), crash CAE and tests with post-crash electrical safety evaluation under the applicable regulations (see UN R100 and local crash standards; confirm current versions).

## Failure modes
- Stiffness counted twice (pack and body optimised independently).
- Adhesive degraded by thermal cycling or creep under sustained load.
- Seals compromised by structural deflection (see pack sealing).

## Verify
- [ ] Structural contribution computed and measured.
- [ ] Joints analysed including thermal expansion.
- [ ] Crash and post-crash safety path agreed with the crash-safety team.
- [ ] Service strategy documented.
