---
id: engineering-technology.biomedical-engineering.medical-device-design.trackability-pushability-testing
name: trackability-pushability-testing
category: engineering-technology
field: biomedical-engineering
product: medical-device-design
tags: [trackability, pushability, catheter-testing, tortuous-path, kink-resistance]
level: advanced
status: gated
description: "Measure catheter trackability, pushability, torque transmission and kink resistance in tortuous vascular models with reproducible fixtures and acceptance limits."
sources: ["ISO 10555-1 Intravascular catheters - General requirements (confirm edition)", "Manufacturer and ASTM technical literature on delivery system testing (no single universal standard; confirm)", "https://www.astm.org"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Trackability and pushability testing

**Goal:** quantify how well a catheter reaches the target and transmits force, with a fixture that represents the clinical anatomy.

## Definitions (ISO 10555-1 scope and any test limits (gated: unconfirmed, source is paywalled or blocked); the metrics below are practice, not a standard)
- **Pushability:** proximal force transmitted to the tip; measured as proximal push force versus distal force or advancement.
- **Trackability:** how easily the device follows a guidewire or path through bends; measured as force to advance through a tortuous model.
- **Torquability:** ratio of tip rotation to input rotation.
- **Kink resistance:** minimum bend radius before the lumen collapses.

## Method
1. Build a fixture from a representative anatomic model (silicone or glass vascular phantom or machined channels), at body temperature in fluid, with defined friction conditions and guidewire.
2. Move the device at a controlled rate with a load cell on the proximal end; record force versus distance; repeat over a defined number of passes.
3. Fix model, lubricant, temperature and speed in the protocol; vary one at a time for sensitivity.
4. Compare against a benchmark device in the same fixture; relative comparison is more robust than absolute numbers.
5. Validate the test method (see tmv-procedure) before using it for acceptance.

## Verify
- [ ] Fixture geometry, friction and speed are documented and repeatable.
- [ ] Acceptance limits tie to clinical need or benchmark data.
- [ ] Gauge repeatability is acceptable.

> Practice guidance, not regulatory or clinical advice. Confirm current standard editions and rules for your jurisdiction, and defer to qualified regulatory, clinical and engineering judgement.
