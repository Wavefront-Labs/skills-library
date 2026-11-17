---
id: business-finance.accounting.carbon-accounting.ghg-protocol-scope-1-2-3-inventory
name: ghg-protocol-scope-1-2-3-inventory
category: business-finance
field: accounting
product: carbon-accounting
tags: [carbon-accounting, ghg-protocol, greenhouse-gas-inventory, carbon-footprint, scope-1, scope-2, scope-3, location-based, market-based, emission-factors, activity-data, co2e, gwp, organisational-boundary, operational-control, base-year, spend-based, csrd, esrs, issb, ifrs-s2, sbti, esg-reporting, renewable-energy-certificates]
level: practitioner
status: gated
description: "Build a GHG Protocol corporate inventory: set boundaries, collect activity data, apply emission factors, report scope 2 both ways, screen scope 3 and keep a base year."
sources: ["GHG Protocol Corporate Accounting and Reporting Standard (WRI/WBCSD)", "GHG Protocol Scope 2 Guidance", "GHG Protocol Corporate Value Chain (Scope 3) Standard", "https://ghgprotocol.org/scope-3-calculation-guidance-2", "https://ghgprotocol.org/scope-2-guidance"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# GHG Protocol scope 1, 2 and 3 inventory

**Goal:** an annual greenhouse-gas inventory that is complete, consistent year to
year, and traceable from every tonne back to an invoice, meter or estimate — the
foundation for any disclosure (CSRD/ESRS E1, ISSB IFRS S2, CDP) or target (SBTi).
This is the preparer's side; third-party assurance is covered by
law-government.regulatory-inspection-and-certification.sustainability-verification.

## 1. Boundaries
- **Organisational boundary:** choose *operational control*, *financial control* or
  *equity share*, and apply it to every entity. Operational control is the most common.
  Align with financial-reporting consolidation where possible and say so.
- **Operational boundary:** which emissions are in which scope:
  - **Scope 1** — direct: fuel burned in owned boilers, vehicles and generators;
    process emissions; refrigerant leaks (often forgotten, often large per kg).
  - **Scope 2** — purchased electricity, heat, steam, cooling.
  - **Scope 3** — the 15 value-chain categories (list confirmed on ghgprotocol.org: purchased goods, capital goods,
    fuel-and-energy related, transport, waste, business travel, commuting, leased
    assets, use and end-of-life of sold products, investments, ...).

## 2. Calculate
`emissions (t CO2e) = activity data × emission factor (× GWP if factor is per gas)`
- **Activity data** hierarchy: metered/invoiced quantities (kWh, litres, kg) >
  supplier-specific data > physical estimates > spend.
- **Emission factors:** use a recognised, dated source matched to geography and year
  (national government factor sets, IEA for grid electricity, DEFRA/DESNZ in the UK,
  EPA in the US). Record the source, version and unit for every factor.
- **GWP:** use one IPCC assessment report's values consistently (AR5 or AR6 100-year
  are common); mixing them silently breaks comparability.
- **Scope 2 dual reporting:** *location-based* (average grid factor) **and**
  *market-based* (contractual instruments: renewable certificates, PPAs, supplier
  factors, then residual mix). Both are required under the Scope 2 Guidance (the guidance page confirms eight market-based quality criteria; the dual-reporting wording itself was not visible there (gated: unconfirmed, source is paywalled or blocked)).

## 3. Scope 3 in practice
1. **Screen** all 15 categories with spend-based (EEIO) factors to find the big ones;
   for most non-energy companies purchased goods and services dominates.
2. Improve the top categories with supplier-specific or activity data over time.
3. Explain exclusions — "not relevant" needs a reason, not silence.
Spend-based numbers move with prices and inflation, not real emissions; flag that in
year-on-year commentary.

## 4. Base year and recalculation
Fix a base year and a **recalculation policy** (e.g. restate if structural changes,
methodology changes or errors move the base year by more than a stated significance threshold; 5% is a common choice (gated: unconfirmed, source is paywalled or blocked)). Acquisitions and
divestments trigger restatement — otherwise a "reduction" is just a sold subsidiary.

## Gotchas
- Double counting between scopes inside the boundary (own fleet fuel isn't also
  business travel).
- Unit traps: kWh vs MWh, gross vs net calorific value, litres vs kg for fuels.
- Renewable certificates must match the market, period and be retired for you;
  otherwise they don't count in market-based scope 2.
- Offsets are **never** netted inside the inventory; report them separately.
- Specific disclosure requirements (CSRD datapoints, ISSB phase-ins) change often;
  confirm current versions before reporting .

## Verify
- [ ] Boundary approach stated and applied to every entity.
- [ ] Every line has activity data source, factor source/version, unit and GWP basis.
- [ ] Scope 2 reported both location- and market-based.
- [ ] All 15 scope 3 categories screened with exclusions justified.
- [ ] Base year and recalculation policy documented; year-on-year change explained.
