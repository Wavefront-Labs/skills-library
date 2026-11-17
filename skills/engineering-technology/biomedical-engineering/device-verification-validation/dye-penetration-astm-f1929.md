---
id: engineering-technology.biomedical-engineering.device-verification-validation.dye-penetration-astm-f1929
name: dye-penetration-astm-f1929
category: engineering-technology
field: biomedical-engineering
product: device-verification-validation
tags: [dye-penetration, packaging-validation, shelf-life, packaging-shelf-life, astm-f1929, seal-integrity, channel-leak, astm-f1886]
level: practitioner
status: gated
description: "Detect seal leaks in porous medical packaging with dye penetration per ASTM F1929: dye selection, application, inspection, sensitivity, interpretation and alternatives."
sources: ["ASTM F1929 Standard test method for detecting seal leaks in porous medical packaging by dye penetration (confirm current edition)", "ASTM F3039 Detecting leaks in non-porous packaging or flexible barrier materials by dye penetration (confirm)", "ISO 11607-1 and -2 Packaging for terminally sterilized medical devices"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Dye penetration test (ASTM F1929)

**Goal:** show that seals of porous packaging (for example pouches with a paper or spunbonded polyethylene side) have no channels allowing leakage.

## Principle
A low-surface-tension dye solution is applied along the inside edge of a seal; capillary action pulls the dye through any channel. Dye visible on the outside of the seal after a short time indicates a leak.

## Procedure outline
1. **Select dye:** typically a toluidine blue or methylene blue solution with a surfactant so the surface tension is low (the standard specifies a limit on surface tension); the dye must not stain the porous material before the test.
2. **Prepare samples:** use pouches after sealing, sterilisation and ageing as required; cut a small opening in the non-porous side or inject through the film.
3. **Apply dye:** inject a small volume of dye into the pouch and tilt so the dye wets the whole seal edge for a defined time, commonly at least 5 seconds (gated: unconfirmed, source is paywalled or blocked).
4. **Inspect:** within a short time (for example 20 seconds (gated: unconfirmed, source is paywalled or blocked)) view the seal for dye penetrating the seal width; observe the whole seal length and measure channels with a loupe.
5. **Record:** pass if no dye passes the seal; document location and width of any leak.

## Sensitivity and limits
- The method detects channels of the order of 50 micrometres wide (gated: unconfirmed, source is paywalled or blocked); smaller channels may escape.
- It is a **destructive** test, operator-dependent, and not suitable for fully non-porous packages (where dye penetration under ASTM F3039, bubble leak or vacuum decay is used).
- Use with seal strength (see seal-strength-astm-f88) and visual inspection (ASTM F1886) to evaluate seal quality.

## Alternatives
- **Bubble emission test** (ASTM F2096) for gross leaks of porous packages by internal pressurisation under water.
- **Vacuum decay**, **helium leak**, **microbial challenge** (ISO 11607-1 annex on microbial barrier tests).

## Verify
- [ ] Dye surface tension and concentration verified per batch.
- [ ] Positive controls (intentional channels) detected.
- [ ] Results recorded for each seal side, in OQ and PQ and shelf life studies.
