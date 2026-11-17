---
id: engineering-technology.chemical-engineering.separation-processes.dryer-selection-and-psychrometrics
name: dryer-selection-and-psychrometrics
category: engineering-technology
field: chemical-engineering
product: separation-processes
tags: [chemical-engineering, separation-processes, sep-crystallisation-drying-evaporation, dryer-selection-and-psychrometrics, dryer-selection, psychrometrics, humidity-ratio, wet-bulb, drying-curve, critical-moisture, spray-dryer, fluid-bed-dryer, rotary-dryer]
level: practitioner
status: draft
description: "Select a dryer type from material and product constraints and compute drying air requirements with psychrometric balances, drying curves and critical moisture."
sources:
  - "Seader Henley and Roper Separation Process Principles, Perry Chemical Engineers Handbook separations sections, Kister Distillation Design, Treybal Mass-Transfer Operations, McCabe Smith and Harriott Unit Operations, Mullin Crystallization"
  - "https://www.aiche.org"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Dryer selection and psychrometrics

**Goal:** a dryer type and drying-air flow for the duty.

## Psychrometrics
- Humidity ratio H (kg water per kg dry air); relative humidity from partial pressure; adiabatic saturation (wet-bulb) temperature from the psychrometric chart or equations.
- Air heat balance: Q = m_air c_humid (T_in - T_out); evaporation rate W = m_air (H_out - H_in).
- Water removal: solids feed with moisture X_in to X_out (dry basis): W = m_solids (X_in - X_out).

## Drying kinetics
Drying curve: constant-rate period (surface moisture; set by external heat/mass transfer) then falling-rate period(s) (internal diffusion). Critical moisture content separates them. Obtain curves from laboratory or pilot tests; design drying time for the falling-rate zone.

## Selection factors
Feed form (solution, slurry, paste, granular, sheet), heat sensitivity, product form (powder, granule), throughput, solvent (flammable solvents need inert gas loops and explosion protection), and dust handling.
- **Spray dryer**: solutions and slurries to powder, fast, heat-sensitive products.
- **Fluid bed dryer**: granular solids, good heat transfer.
- **Rotary dryer**: large tonnages of free-flowing solids.
- **Tray, vacuum and freeze dryers**: small and sensitive batches.
- **Flash (pneumatic) dryer**: fine solids with surface moisture.
- **Drum and belt dryers**: pastes and sheets.

## Procedure
1. Compute water to be removed and heat requirement (latent heat of vaporisation plus sensible heat).
2. Select the inlet air temperature below product degradation temperature; choose the outlet temperature to keep adequate driving force.
3. Compute air flow and dryer size from heat transfer or residence time data.
4. Add dust collection, emissions treatment and safety (dust explosion, solvent) requirements.

## Gotchas
- Cold spots below dew point cause condensation and caking.
- Dust explosion risk requires specific protection design with a qualified specialist.

## Verify
- [ ] Moisture and enthalpy balance closes within 5%.
- [ ] Outlet air above dew point with margin.
