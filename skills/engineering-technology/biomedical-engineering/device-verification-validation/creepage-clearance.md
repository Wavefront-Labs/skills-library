---
id: engineering-technology.biomedical-engineering.device-verification-validation.creepage-clearance
name: creepage-clearance
category: engineering-technology
field: biomedical-engineering
product: device-verification-validation
tags: [creepage-clearance, iec-60601-testing, hipot, electrical-safety-testing, mopp, moop, pollution-degree, comparative-tracking-index]
level: advanced
status: gated
description: "Determine creepage and clearance for IEC 60601-1: working voltage, pollution degree, material group, MOPP and MOOP values at 250 V, PCB slots, coatings and measurement."
sources: ["IEC 60601-1:2005+AMD1:2012+AMD2:2020 clause 8.9 Creepage distances air clearances and distances through insulation (confirm edition and tables)", "IEC 60664-1 Insulation coordination for equipment within low-voltage supply systems (confirm edition)", "PCB design guides from isolation component manufacturers"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Creepage and clearance

**Goal:** physical distances between conductive parts that prevent tracking and flashover at the working voltage, for each means of protection.

Distances below are the commonly quoted values at about 250 V rms mains for IEC 60601-1 3rd edition at pollution degree 2 (all table values and material-group limits here: (gated: unconfirmed, source is paywalled or blocked)); use the standard's tables for the actual working voltage, pollution degree, altitude and material group.

## Definitions
- **Clearance:** shortest distance through air between two conductive parts.
- **Creepage:** shortest path along an insulating surface; depends on pollution degree and the material's comparative tracking index (CTI).
- Distances through insulation (solid) need minimum thickness or multi-layer insulation tests.

## Typical values (about 250 V rms working voltage)
| Means of protection | Creepage | Clearance | Dielectric test |
|---|---|---|---|
| 1 MOPP | 4 mm | 2.5 mm | 1500 V ac |
| 2 MOPP | 8 mm | 5 mm | 4000 V ac |
| 1 MOOP | 2.5 mm | 2 mm | 1500 V ac |
| 2 MOOP | 5 mm | 4 mm | about 3000 V ac (reinforced) |

## Factors
- **Working voltage:** the highest rms (and peak) voltage across the insulation in normal use; consider switching and transient voltages in isolated converters.
- **Pollution degree:** PD1 (sealed), PD2 (normal indoor, non-conductive), PD3 (conductive pollution); coatings can allow PD1 only if they are adhesive and meet coating test requirements.
- **Material group** from CTI: group I (CTI at least 600), II (400-599), IIIa (175-399), IIIb (100-174); higher CTI allows shorter creepage.
- **Altitude:** correction factors for use above 2000 m.
- **Slots and ribs:** a slot in the PCB at least 1 mm wide can add creepage path; narrower slots do not count. Ribs raise creepage if tall enough.

## Design and verification
1. Define each isolation barrier and its means of protection from the risk analysis (see means-of-protection).
2. Map barrier locations on the schematic and PCB layout; use design-rule checks with the required distances.
3. Measure on the assembled product (gauges, microscope); remember component tolerances, solder fillets and potting.
4. Verify with dielectric strength tests (see dielectric-strength-test) and component certificates (isolated converters, optocouplers, transformers).

## Verify
- [ ] Table of barriers, working voltages, required and measured distances.
- [ ] Layout includes slots or keepout around isolation barriers.
- [ ] Re-check after any layout or enclosure change.
