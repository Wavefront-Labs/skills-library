---
id: engineering-technology.chemical-engineering.aspen.henry-components-and-supercritical-species
name: henry-components-and-supercritical-species
category: engineering-technology
field: chemical-engineering
product: aspen
tags: [chemical-engineering, aspen, aspen-property-method-selection, henry-components-and-supercritical-species, henrys-law, henry-comps, dissolved-gas, supercritical, noncondensable, aspen-plus, solubility, activity-coefficient]
level: practitioner
status: gated
description: "Handle dissolved gases and supercritical components with Henry's law in Aspen Plus (Henry-Comps, parameter retrieval) when using activity-coefficient methods."
sources:
  - "Aspen Plus and Aspen HYSYS user guides and help (AspenTech), Seider et al. Product and Process Design Principles"
  - "https://www.aiche.org"
  - "AspenTech Aspen Plus certification study guide AT-05198 (learning objectives, aspentech.com)"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Henry components and supercritical species

**Goal:** model gases such as N2, O2, CO2, H2, CH4 dissolved in a liquid when the property method is an activity model that has no vapour pressure for them above their critical temperature.

## Why
Activity-coefficient methods need P_i^sat. Above a component's critical temperature it does not exist, so Aspen Plus uses Henry's constant instead: y_i phi_i P = x_i H_i (solute i in solvent), with H_i a function of temperature.

## Steps in Aspen Plus
(AspenTech's study guide confirms Henry's components are a standard topic; the menu names and parameter names below are unconfirmed (gated: unconfirmed, source is paywalled or blocked).)
1. Identify the supercritical or very light species in the mixture (H2, N2, CO, CO2, light hydrocarbons in water at moderate temperature).
2. Create a **Henry Components** list under Components > Henry Comps (a set named like HC-1) containing those components.
3. In the property method form (Methods > Specifications) enter that list as the Henry components ID.
4. Under Parameters, check that Henry's constants for each gas/solvent pair are retrieved (HENRY-1 style parameters); view them with Retrieve Parameters, and regress your own from data if missing.
5. Run Property Analysis and plot solubility versus pressure for a binary gas/solvent pair; compare with literature solubility.

## When to use an EoS instead
Above roughly 10 to 20 bar (gated: unconfirmed, source is paywalled or blocked), or when gas solubility matters a lot, Henry's law (valid at low solute concentration) loses accuracy; consider an EoS with suitable binaries.

## Gotchas
- A component in the Henry list is excluded from the usual vapour-pressure treatment; do not list condensable species there.
- Check solvent and solute order for the constants; they are not symmetric.
- Mixed solvent systems need Henry constants for each solvent pair; Aspen Plus mixes them with a stated rule, confirm in the help for your version.

## Verify
- [ ] Gas solubility at one T and P matches a literature value within the expected accuracy.
- [ ] No warnings about missing Henry parameters in the run report.
