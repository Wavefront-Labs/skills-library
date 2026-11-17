---
id: engineering-technology.chemical-engineering.aspen.binary-interaction-parameter-retrieval
name: binary-interaction-parameter-retrieval
category: engineering-technology
field: chemical-engineering
product: aspen
tags: [chemical-engineering, aspen, aspen-binary-parameters-and-regression, binary-interaction-parameter-retrieval, binary-parameters, interaction-parameters, aspen-plus, databank, apv, nrtl, uniquac, unifac, missing-parameters]
level: practitioner
status: gated
description: "Retrieve, inspect and sanity-check binary interaction parameters in Aspen Plus databanks, and flag pairs that fall back to defaults or estimates."
sources:
  - "Aspen Plus and Aspen HYSYS user guides and help (AspenTech), Seider et al. Product and Process Design Principles"
  - "https://www.aiche.org"
  - "AspenTech Aspen Plus certification study guide AT-05198 (learning objectives, aspentech.com)"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Retrieving and checking binary interaction parameters

**Goal:** know exactly which binary pairs are backed by data and which are estimates or zero.

## Steps
1. After setting components and the property method, open **Properties > Parameters > Binary Interaction** and select the parameter set for your model (NRTL-1, WILSON-1, UNIQ-1, or the k_ij set for the cubic EoS).
2. Ensure **Retrieve parameters** is active for the databanks (the built-in VLE and LLE binary databanks); run the Properties step (gated: unconfirmed, source is paywalled or blocked). Exact databank names vary by version; read the Retrieve Parameters help text for yours.
3. Inspect each pair: where the values come from (the data source column), the temperature range, and the data type (VLE vs LLE vs infinite dilution).
4. List pairs with no retrieved data: these default to zero (ideal) or are absent. Mark them as risks.
5. For high-risk pairs (azeotropes, close boiling) plan regression or a UNIFAC estimate.

## Reading the numbers
NRTL has aij, aji, bij, bji and a non-randomness parameter cij (alpha). Renon and Prausnitz (AIChE J. 14(1):135-144, 1968, citation confirmed in Crossref) tied alpha to the type of mixture; the commonly quoted values run from 0.2 to 0.47 depending on pair class (gated: unconfirmed, source is paywalled or blocked). Do not assume one value suits every pair; check that alpha is in a sensible range. Large asymmetry (huge opposite-sign terms) suggests a fit over a narrow data range.

## Gotchas
- Database parameters are valid only for the stated T range and for the pair as given; do not reuse a set fitted to LLE for VLE without checking.
- The same pair may have several sets from different sources; the order of precedence can change between versions.
- (Databank names such as VLE-IG are Aspen-specific (gated: unconfirmed, source is paywalled or blocked).) A pair listed in VLE-IG assumes an ideal gas vapour; do not combine with a vapour model of Hayden-O'Connell without checking.

## Verify
- [ ] A table of every pair with source and range exists.
- [ ] Missing pairs identified and mitigation chosen.
- [ ] Binary Txy check for the highest-risk pair done.
