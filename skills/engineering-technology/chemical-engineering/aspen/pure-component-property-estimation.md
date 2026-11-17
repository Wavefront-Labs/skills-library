---
id: engineering-technology.chemical-engineering.aspen.pure-component-property-estimation
name: pure-component-property-estimation
category: engineering-technology
field: chemical-engineering
product: aspen
tags: [chemical-engineering, aspen, aspen-binary-parameters-and-regression, pure-component-property-estimation, property-estimation, group-contribution, joback, user-defined-component, missing-properties, aspen-plus, molecular-structure]
level: practitioner
status: gated
description: "Estimate missing pure-component properties in Aspen Plus (Tb, Tc, Pc, vapour pressure) from structure using group contribution, with checks and limits."
sources:
  - "Aspen Plus and Aspen HYSYS user guides and help (AspenTech), Seider et al. Product and Process Design Principles"
  - "https://www.aiche.org"
  - "AspenTech Aspen Plus certification study guide AT-05198 (learning objectives, aspentech.com)"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Estimating missing pure-component properties

**Goal:** make a usable component definition for a compound that is not in the databank, and know how accurate it is.

## Steps
1. Create the component as **User defined** (or Conventional with missing fields) and enter the molecular formula and, ideally, the **molecular structure** (draw it or enter the connectivity) so group methods can run.
2. Enter any measured values you have first: molecular weight, normal boiling point, density, critical properties, vapour pressure data.
3. Under **Properties > Estimation** (menu name (gated: unconfirmed, source is paywalled or blocked)), run estimation for the missing items (the simulator offers several group-contribution methods for boiling point, critical properties, heat of formation and so on; choose and note the method).
4. Review the estimated values with the **Retrieve/Estimate** results and compare against any measured point (a single measured Tb is enough to reduce a lot of risk).
5. Check derived curves: vapour pressure versus T from the estimated parameters must pass through the measured normal boiling point.

## Accuracy guidance
Group methods typically give boiling points within a few percent (gated: unconfirmed, source is paywalled or blocked) but critical properties and heats of formation can be much further off for large or polyfunctional molecules; treat results as screening-grade.

## Gotchas
- Estimating many properties from one structure compounds errors; measure the ones that drive the design.
- Salts, polymers and ionic liquids need dedicated methods, not these.

## Verify
- [ ] The estimated vapour pressure curve matches a known data point.
- [ ] Estimation methods and values documented as estimates.
