---
id: engineering-technology.environmental-engineering.site-remediation.remedy-selection-and-pump-and-treat-design
name: remedy-selection-and-pump-and-treat-design
category: engineering-technology
field: environmental-engineering
product: site-remediation
tags: [environmental-engineering, site-remediation, contaminated-land, groundwater-remediation, conceptual-site-model, csm, site-characterisation, site-characterization, plume, lnapl, dnapl, retardation-factor, koc, remedy-selection, feasibility-study, cercla-nine-criteria, pump-and-treat, capture-zone, javandel-tsang, air-stripping, granular-activated-carbon, isco, in-situ-chemical-oxidation, enhanced-reductive-dechlorination, soil-vapour-extraction, soil-vapor-extraction, air-sparging, permeable-reactive-barrier, monitored-natural-attenuation, pfas]
level: practitioner
status: gated
description: "Characterise a contaminated site, screen and select remedies against standard criteria, and design pump-and-treat capture zones, pore-volume cleanup times and in-situ options."
sources: ["Fetter, Contaminant Hydrogeology", "US EPA, Guidance for Conducting Remedial Investigations and Feasibility Studies under CERCLA", "Javandel & Tsang (1986), Capture-zone type curves, Ground Water", "Federal Remediation Technologies Roundtable (FRTR), Remediation Technologies Screening Matrix", "ITRC technical guidance documents (chlorinated solvents, ISCO, LNAPL)", "UK Environment Agency, Land Contamination Risk Management (LCRM)"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Remedy selection and pump-and-treat design — clean up what the risk requires

**Goal:** turn site data into a conceptual site model (CSM), choose a remedy that
breaks the source-pathway-receptor linkage at acceptable cost, and size a groundwater
capture system or in-situ treatment that will actually reach its targets. Cleanup goals
and remedy approval are set by the regulator (e.g. CERCLA/state programmes in the US,
LCRM in the UK); a qualified professional must own the design.

## 1. Build the conceptual site model
- Sources (tanks, spills, NAPL), pathways (vadose zone, groundwater, vapour intrusion,
  surface water) and receptors (wells, basements, ecology).
- Delineate the plume in 3-D: vertical profiling (direct-push, MIP, HPT, LIF for
  petroleum NAPL) beats long-screened wells that average concentrations.
- Identify NAPL: LNAPL floats (petroleum); DNAPL sinks (chlorinated solvents, creosote).
  Dissolved concentrations above ~1 % of effective solubility suggest DNAPL is present (common rule of thumb (gated: unconfirmed, source is paywalled or blocked)).
- Hydrogeology: hydraulic conductivity K (slug/pumping tests), gradient i, effective
  porosity n_e. Seepage velocity v = K·i / n_e.
- Contaminant transport: retardation R = 1 + (ρ_b/n)·K_d, with K_d = K_oc·f_oc. A
  plume front moves at v/R; benzene (R ≈ 1–2) outruns PAHs (R in the hundreds+).

## 2. Screen and select the remedy
Screen technologies against contaminant, geology and depth (FRTR matrix or similar),
then compare alternatives. The US CERCLA framework uses nine criteria (list confirmed in 40 CFR 300.430(e)(9)):
- **Threshold:** overall protection of human health and the environment; compliance
  with applicable requirements (ARARs).
- **Balancing:** long-term effectiveness; reduction of toxicity, mobility or volume
  through treatment; short-term effectiveness; implementability; cost.
- **Modifying:** state and community acceptance.

| Situation | Usual candidates |
|---|---|
| Shallow VOCs in permeable vadose soil | Soil vapour extraction (SVE), excavation |
| Dissolved chlorinated solvents | Enhanced reductive dechlorination (ERD), ISCO, PRB (zero-valent iron) |
| Petroleum dissolved plume | Monitored natural attenuation, biosparging, ISCO |
| Free LNAPL | Recovery (skimming, multi-phase extraction) where mobile |
| Unknown/recalcitrant or plume containment | Pump-and-treat (hydraulic control) |
| DNAPL source in low-K zones | Thermal treatment, or containment |

Combine: aggressive source treatment plus MNA or containment for the dilute plume is
often the most cost-effective.

## 3. Design pump-and-treat
**Capture zone** (Javandel-Tsang, single well, confined/uniform flow, aquifer thickness
B, Darcy flux q = K·i):
- Maximum width far upgradient: W = Q / (B·q)
- Width at the well: Q / (2·B·q)
- Downgradient stagnation point: x₀ = Q / (2π·B·q)

Javandel-Tsang widths and stagnation point were re-derived from the uniform-flow plus sink stream function and match (Q/(B·q), Q/(2·B·q), Q/(2π·B·q)). Size Q so the capture width exceeds plume width with margin (often 1.5–2×, a rule of thumb (gated: unconfirmed, source is paywalled or blocked)), then
verify with a numerical model (MODFLOW + particle tracking) and field piezometer pairs
showing inward gradients. Multiple wells: use type curves or the model.

**Cleanup time** ≈ number of pore volumes × R × (pore volume / Q). Ideal flushing
predicts a few pore volumes; reality is often 10× longer because of matrix diffusion,
sorption kinetics and DNAPL — design for containment, not quick restoration.

**Treatment of extracted water:** air stripping for volatile compounds (dimensionless
Henry's constant above ~0.05 strips well; vendor or Onda-based design, air-to-water
ratio commonly 20:1–100:1+; these are typical figures (gated: unconfirmed, source is paywalled or blocked)), liquid-phase GAC for less volatile organics and polishing,
pre-treatment for iron/manganese to prevent fouling. Off-gas may need vapour-phase GAC.

## 4. In-situ design essentials
- **ISCO:** permanganate, activated persulfate, catalysed peroxide or ozone; dose from
  contaminant mass plus natural oxidant demand (bench test). Expect rebound; plan
  multiple injections.
- **ERD:** add electron donor (e.g. emulsified vegetable oil, lactate); confirm
  Dehalococcoides presence; watch for cis-DCE/vinyl chloride stall and pH drop.
- **SVE:** suits compounds with vapour pressure above ~0.5–1 mm Hg (gated: unconfirmed, source is paywalled or blocked) in permeable soils;
  design radius of influence from a pilot test, not a rule of thumb.
- **PFAS:** not destroyed by conventional ISCO/bio; current practice is containment,
  GAC/ion exchange treatment and evolving destruction technologies (rules changing fast).

## Gotchas
- Long-screened wells dilute and hide vertical plume structure.
- Pump-and-treat rebound after shutdown is the norm when sources remain.
- Injecting into a heterogeneous aquifer treats the permeable zones and misses the mass.
- Daughter products (vinyl chloride) can be more toxic than the parent.
- Remedies without an exit strategy (defined endpoints, monitoring) run forever.

## Verify
- [ ] CSM shows every source, pathway and receptor with supporting data.
- [ ] Remedy comparison documented against the governing criteria and cleanup goals.
- [ ] Capture confirmed by model and by measured inward gradients.
- [ ] Treatment system meets discharge/off-gas permits with breakthrough monitoring.
- [ ] Performance monitoring plan and exit criteria agreed with the regulator.
