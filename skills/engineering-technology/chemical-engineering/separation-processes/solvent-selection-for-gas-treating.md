---
id: engineering-technology.chemical-engineering.separation-processes.solvent-selection-for-gas-treating
name: solvent-selection-for-gas-treating
category: engineering-technology
field: chemical-engineering
product: separation-processes
tags: [chemical-engineering, separation-processes, sep-absorption-and-stripping, solvent-selection-for-gas-treating, solvent-selection, gas-treating, acid-gas-removal, amine, physical-solvent, absorption-solvent, selectivity, co2-capture, h2s]
level: practitioner
status: draft
description: "Select an absorption solvent for gas treating (water, amines, physical solvents) from solubility, selectivity, vapour pressure, regeneration and corrosion criteria."
sources:
  - "Seader Henley and Roper Separation Process Principles, Perry Chemical Engineers Handbook separations sections, Kister Distillation Design, Treybal Mass-Transfer Operations, McCabe Smith and Harriott Unit Operations"
  - "https://www.aiche.org"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Solvent selection for gas treating

**Goal:** a short list of solvents with an economic and safety rationale.

## Criteria
1. **Solubility and capacity**: high solute loading per unit solvent; low m (Henry's constant).
2. **Selectivity**: for example H2S over CO2 (tertiary amines such as MDEA have kinetic selectivity), CO2 over hydrocarbons.
3. **Vapour pressure**: low volatility reduces solvent losses to the treated gas.
4. **Viscosity and foaming tendency**; surface tension.
5. **Regeneration**: heat duty (chemical solvents bind strongly and need steam), flash-regenerable physical solvents, thermal stability, degradation products.
6. **Corrosion and materials**, toxicity, flammability, environmental fate, cost and availability.

## Families
- **Water**: for very soluble gases (NH3, HCl); cheap.
- **Chemical (amine) solvents**: MEA, DEA, MDEA, blends; good at low partial pressure of acid gas; high regeneration heat.
- **Physical solvents** (glycol ethers, methanol, N-methylpyrrolidone and others): capacity grows with partial pressure (Henry's law); good for high-pressure acid gas with low regeneration energy; may also absorb hydrocarbons.
- **Hybrid** solvents and **alkaline solutions** (potassium carbonate), and **solid sorbents** as alternatives.

## Procedure
1. State feed gas pressure, composition, product specs.
2. Rank solvent options by partial pressure of solute: low favours chemical, high favours physical.
3. Compute indicative circulation rate and regeneration duty from equilibrium data.
4. Do a safety and environmental screen (toxicity, handling, waste).
5. Use licensor or vendor data for the final choice; proprietary solvent performance is licensor-specific.

## Gotchas
- Heat stable salts and degradation build up; allow for reclaimer or purge.
- Hydrocarbon co-absorption in physical solvents lowers product yield.

## Verify
- [ ] Equilibrium data source cited for each candidate.
- [ ] Energy estimate for regeneration per tonne of solute removed.
