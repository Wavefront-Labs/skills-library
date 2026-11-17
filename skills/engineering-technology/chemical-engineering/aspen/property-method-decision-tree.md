---
id: engineering-technology.chemical-engineering.aspen.property-method-decision-tree
name: property-method-decision-tree
category: engineering-technology
field: chemical-engineering
product: aspen
tags: [chemical-engineering, aspen, aspen-property-method-selection, property-method-decision-tree, property-method, aspen-plus, hysys, thermodynamic-model, nrtl, peng-robinson, decision-tree, fluid-package]
level: practitioner
status: gated
description: "Pick an Aspen Plus or HYSYS property method from chemistry, polarity, pressure and electrolytes using a decision tree, then record the justification."
sources:
  - "Aspen Plus and Aspen HYSYS user guides and help (AspenTech), Seider et al. Product and Process Design Principles"
  - "https://www.aiche.org"
  - "AspenTech Aspen Plus certification study guide AT-05198 (learning objectives, aspentech.com)"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Choosing a property method by chemistry and pressure

**Goal:** a defensible thermodynamic model choice, written down before any flowsheet is built. A wrong method gives confident wrong answers (a missing azeotrope, a wrong relative volatility), and everything downstream inherits it.

## Decision tree (the usual practice, after Carlson's well-known guidance on physical properties)
1. **Electrolytes present** (acids, bases, salts in water)? Use an electrolyte method (ELECNRTL in Aspen Plus (gated: unconfirmed, source is paywalled or blocked)) and the electrolyte wizard. Stop here.
2. **Polar compounds?** (alcohols, ketones, water, acids, amines)
   - Pressure below roughly 10 bar and no near-critical components: an **activity-coefficient method** (NRTL, UNIQUAC, WILSON) with an ideal or Hayden-O'Connell/Redlich-Kwong vapour phase. Use NRTL-RK or WILS-RK style methods when the vapour is not ideal (carboxylic acids need the Hayden-O'Connell dimerisation option; Hayden and O'Connell, Ind. Eng. Chem. Process Des. Dev. 14(3):209-216, 1975, confirmed in Crossref).
   - Higher pressure (the 10 bar boundary is a rule of thumb (gated: unconfirmed, source is paywalled or blocked)): an **EoS with advanced mixing rules** (PSRK, Wong-Sandler-type, SR-POLAR) or an activity model plus Henry's law for light gases.
   - No binary data at all: UNIFAC-type group contribution as a screening estimate only.
3. **Non-polar or slightly polar hydrocarbons and light gases**: Peng-Robinson (Ind. Eng. Chem. Fundam. 15(1):59-64, 1976) or Soave-Redlich-Kwong (Chem. Eng. Sci. 27(6):1197-1203, 1972; both confirmed in Crossref) (PENG-ROB, RK-SOAVE; the -BM variants add the Boston-Mathias alpha function). For heavy oil and refinery fractions, petroleum methods such as BK10, Chao-Seader or Grayson-Streed are in the same family; check the simulator's guidance for your version.
4. **Water/steam service**: a steam-table method (STEAMNBS or STEAM-TA (gated: unconfirmed, source is paywalled or blocked)) for pure water; do not use it for mixtures.
5. **HYSYS**: the same logic applies to the fluid package (Peng-Robinson, SRK, NRTL/UNIQUAC, Acid Gas for amine sweetening). Confirm package names against your installed version.

## Record the decision
Write one paragraph in the simulation basis document: components, temperature and pressure window, polarity, the method chosen, the data used to check it, and a known limit ("not valid above X bar").

## Gotchas
- One method per flowsheet is easiest to defend; use per-block or per-section methods only with a stated reason.
- A cubic EoS with default binaries predicts poor liquid-phase behaviour for polar mixtures even though it converges.
- Method names and defaults vary by version; confirm against the installed help.

## Verify
- [ ] Decision path recorded with the compounds and operating window.
- [ ] Pure-component vapour pressures match literature within a few percent over the window.
- [ ] Binary azeotrope (if any) is reproduced; see `engineering-technology.chemical-engineering.aspen.property-method-validation-against-data`.
