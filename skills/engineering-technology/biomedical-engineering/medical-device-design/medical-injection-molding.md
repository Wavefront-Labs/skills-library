---
id: engineering-technology.biomedical-engineering.medical-device-design.medical-injection-molding
name: medical-injection-molding
category: engineering-technology
field: biomedical-engineering
product: medical-device-design
tags: [injection-molding, medical-dfm, design-for-manufacture, scientific-molding, medical-grade-resin, cavity-validation, tooling]
level: advanced
status: gated
description: "Specify and validate injection moulding for medical parts: resin choice, tooling, scientific moulding window, cavity validation, and what the process validation must prove."
sources: ["https://www.iso.org/standard/10993-1"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Medical injection moulding

**Goal:** make a part from a qualified resin and mould that passes dimensional and function specs lot after lot, with a validated, documented process.

Practice guidance; process validation is expected under ISO 13485 (confirm edition) and the applicable regulation for your market.

## Choices
- **Resin:** medical-grade supplier with change-notification agreements and a master file or declaration; biocompatibility is evaluated on the finished, sterilised part (ISO 10993-1; the 2018 edition is withdrawn and ISO 10993-1:2025 is current per iso.org), not inherited from the resin data sheet. Lock supplier, grade and colourant.
- **Tool:** steel hardness and finish to the part life and resin; draft and wall thickness for uniform fill (keep wall changes gradual); gates and vents placed to avoid weld lines in critical zones; multi-cavity tools need balanced fill and cavity-to-cavity capability.
- **Process development (scientific moulding):** viscosity curve, gate-seal study, pressure drop, cooling time and packing window; record the process window and set nominal in the middle.
- **Sensors:** cavity pressure and temperature sensors support monitoring and shorten investigations.

## Validation (IQ/OQ/PQ)
- IQ: machine, tool, dryer, chiller, sensors installed and calibrated.
- OQ: worst-case process corners (low and high settings) still make conforming parts.
- PQ: three or more production-like lots at nominal with defined sample sizes (gated: unconfirmed, source is paywalled or blocked); see process-validation-iq-oq-pq.
- Control: monitor critical parameters, re-validate on tool repair, resin or machine change.

## Gotchas
- Regrind, moisture in hygroscopic resins and cooling imbalance cause drift and warpage.
- Post-mould annealing and sterilisation can change dimensions; measure after both.

## Verify
- [ ] Critical-to-quality dimensions capable (see process-capability).
- [ ] Resin, tool and process changes under change control.
- [ ] Cavity-to-cavity data on multi-cavity tools.
