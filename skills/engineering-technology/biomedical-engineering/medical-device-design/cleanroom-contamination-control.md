---
id: engineering-technology.biomedical-engineering.medical-device-design.cleanroom-contamination-control
name: cleanroom-contamination-control
category: engineering-technology
field: biomedical-engineering
product: medical-device-design
tags: [cleanroom, contamination-control, iso-14644, environmental-monitoring, gowning]
level: practitioner
status: gated
description: "Specify and operate cleanrooms for device manufacture: ISO 14644 classes, particle and bioburden monitoring, gowning, material flow and cleaning."
sources: ["https://www.iso.org/standard/53393.html","https://www.iso.org/obp/ui/#iso:std:iso:14644:-1:ed-2:v1:en"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Cleanroom and contamination control

**Goal:** control particles and microbes in the manufacturing environment according to the product risk.

## Method
1. Decide cleanliness need from product risk: implant or sterile-barrier-exposed processes need controlled environments; ISO 13485 requires controls where environment affects quality (confirm clause in the text (gated: unconfirmed, source is paywalled or blocked)).
2. Choose an ISO 14644-1:2015 class (ISO 5 to ISO 8 are common for devices (gated: unconfirmed, source is paywalled or blocked)) with at-rest and operational states; the standard classifies by particle concentration for sizes 0.1 to 5 micrometre (ISO Class 5 limit 3,520 per cubic metre at 0.5 micrometre and larger).
3. Design: HEPA filtration, air change rate, pressure cascades between rooms, smooth cleanable surfaces, material and personnel airlocks.
4. Monitoring: particle counts per ISO 14644-2:2015 (monitoring plan) on a defined schedule, differential pressure, temperature and humidity; viable (bioburden) air and surface sampling with alert and action levels.
5. Gowning and behaviour procedures; cleaning agents and rotation; training and qualification.
6. Qualify (installation, operation, performance); requalify at defined intervals and after changes.

## Traps
- Class stated without state (at rest versus in operation).
- Treating monitoring data as records only; trend it and act on excursions with CAPA.

## Verify
- [ ] Room classification report and ongoing monitoring data available.
- [ ] Excursion procedure and trend review exist.
- [ ] Product bioburden or cleanliness testing corroborates the environment.

> Practice guidance, not regulatory or clinical advice. Confirm current standard editions and rules for your jurisdiction, and defer to qualified regulatory, clinical and engineering judgement.
