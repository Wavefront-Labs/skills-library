---
id: engineering-technology.chemical-engineering.aspen.rstoic-ryield-rgibbs-selection
name: rstoic-ryield-rgibbs-selection
category: engineering-technology
field: chemical-engineering
product: aspen
tags: [chemical-engineering, aspen, aspen-reactor-blocks, rstoic-ryield-rgibbs-selection, rstoic, ryield, rgibbs, requil, reactor-block, aspen-plus, chemical-equilibrium, gibbs-minimization]
level: practitioner
status: gated
description: "Choose between RStoic, RYield, REquil and RGibbs reactor blocks in Aspen Plus from what you know: stoichiometry, yields or only thermodynamics."
sources:
  - "Aspen Plus and Aspen HYSYS user guides and help (AspenTech), Seider et al. Product and Process Design Principles"
  - "https://www.aiche.org"
  - "AspenTech Aspen Plus certification study guide AT-05198 (learning objectives, aspentech.com)"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Choosing RStoic, RYield or RGibbs

**Goal:** the right reactor model for the information available, avoiding precision you do not have.

## Selection by knowledge
(Block names and behaviours are Aspen-specific (gated: unconfirmed, source is paywalled or blocked); the study guide confirms an RGibbs option to include both vapor and liquid phases and balance-based reactor models.)
| You know | Use |
|---|---|
| Reaction stoichiometry and conversion (or extent) | RStoic |
| Product yields only (no stoichiometry; includes non-conventional, pseudo-components) | RYield |
| Reaction stoichiometry and temperature, equilibrium reached | REquil (reaction-by-reaction equilibrium) |
| Only the species list; equilibrium by minimising Gibbs energy | RGibbs |
| Kinetics and volume | RCSTR or RPlug (see the kinetic-models skill) |

## RStoic
Enter each reaction, then specify fractional conversion of a key component or extent; set the reactor T, P or duty. Sub-stream solids can be handled; heat of reaction comes from formation enthalpies.

## RYield
Enter yields per unit mass of feed (or by component); the block does not enforce atom balance, so check element balances yourself; the heat of reaction comes from formation enthalpies of the products.

## RGibbs
List the possible product species; the block minimises Gibbs free energy at the given T and P (or T and duty). Use **restricted equilibrium** options (temperature approach or specified extents) for systems that do not reach full equilibrium (for example, methane steam reforming at lower temperatures, where a temperature approach to equilibrium is typical).
If solids can form (carbon), include them and set phase equilibrium appropriately.

## Gotchas
- RGibbs finds the global minimum only for the species you list; omitted species change the answer.
- An RStoic set with conversion specs inconsistent with thermodynamics can produce impossible results (conversion above equilibrium).
- Always check the block's heat duty sign and magnitude against a hand calculation (see `engineering-technology.chemical-engineering.process-design.mass-and-energy-balances`).

## Verify
- [ ] Element balances close.
- [ ] Outlet composition is at or below the thermodynamic equilibrium conversion for your T and P.
