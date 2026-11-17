---
id: engineering-technology.biomedical-engineering.medical-device-design.symbols-and-udi-labelling
name: symbols-and-udi-labelling
category: engineering-technology
field: biomedical-engineering
product: medical-device-design
tags: [udi-labelling, udi, device-identification, iso-15223-1, gs1]
level: practitioner
status: gated
description: "Plan device labelling: ISO 15223-1 symbols, unique device identification (UDI) with DI and PI, data carriers, and database submissions per jurisdiction."
sources: ["ISO 15223-1 Medical devices - Symbols to be used with information to be supplied by the manufacturer (confirm edition)", "FDA UDI rule, 21 CFR Part 830, https://www.ecfr.gov/current/title-21/part-830", "EU MDR Regulation 2017/745 UDI provisions (confirm current text)", "European Commission, EUDAMED mandatory use from 28 May 2026, https://health.ec.europa.eu/latest-updates/eudamed-four-first-modules-will-be-mandatory-use-28-may-2026-2025-11-27_en", "https://www.fda.gov/medical-devices/unique-device-identification-system-udi-system/contact-fda-accredited-issuing-agency"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Symbols and UDI labelling

**Goal:** labels carry correct symbols and a machine-readable unique device identifier that meets each market's rules.

## UDI
- A UDI has a **device identifier (DI)** fixed to the model and a **production identifier (PI)** for lot, serial, expiry or manufacture date as applicable.
- Issued under a regulator-accredited issuing agency system; FDA lists three accredited agencies: GS1, HIBCC and ICCBBA (fda.gov, Contact an FDA-Accredited Issuing Agency). Use the issuer's formats.
- Provide both human-readable form and an automatic identification data carrier (barcode or 2D symbol) per the rules; carriers must be readable at the packaging levels the rules require.
- Submit device data to the regulator databases (GUDID in the US; EUDAMED in the EU, where the European Commission notice of 27 Nov 2025 states the first four modules, including UDI/device registration, are mandatory from 28 May 2026; later modules are still pending, so confirm current status).
- Plan the identification structure (each packaging level and any kits) early, with change control for when a DI must change.

## Symbols
- Use standard symbols from ISO 15223-1 (edition and symbol list (gated: unconfirmed, source is paywalled or blocked)) with their defined meaning; explain them in the IFU if they might not be understood, as the rules allow.
- Do not use a standard symbol for a different meaning.
- Language and text requirements vary by country.

## Verify
- [ ] DI and PI assignment documented per product and packaging level.
- [ ] Barcodes verified (grade and decode) on production samples.
- [ ] Database submission and label content reviewed with regulatory affairs for each market.

> Practice guidance, not regulatory or clinical advice. Confirm current standard editions and rules for your jurisdiction, and defer to qualified regulatory, clinical and engineering judgement.
