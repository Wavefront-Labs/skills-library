---
id: agriculture-environment.soil-land-management.land-reclamation.managing-saline-sodic-and-acid-soils
name: managing-saline-sodic-and-acid-soils
category: agriculture-environment
field: soil-land-management
product: land-reclamation
tags: [soil-land-management, land-reclamation, problem-soils, salinity, dryland-salinity, irrigation-salinity, ece, ec1-5, leaching-requirement, sodicity, sodic-soil, esp, sar, dispersion, emerson-test, gypsum, gypsum-requirement, soil-acidity, acid-soil, aglime, lime-requirement, neutralising-value, aluminium-toxicity, subsoil-acidity, scald, scald-rehabilitation, waterponding, saltbush, puccinellia, tall-wheatgrass, compaction]
level: practitioner
status: gated
description: "Diagnose and treat problem soils: salinity (ECe, leaching, salt-tolerant species), sodicity (ESP, Emerson test, gypsum rates), acidity (lime rates, subsoil), and scalded ground (waterponding)."
sources: ["https://www.udel.edu/content/dam/udelImages/canr/pdfs/extension/factsheets/Salt-Measurements-and-Soil-Classifications.pdf", "https://vro.agriculture.vic.gov.au/DPI/Vro/vrosite.nsf/pages/sodic_soils"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Managing saline, sodic and acid soils

**Goal:** name the actual constraint (salt, sodium, acid or a mix), then apply the
treatment that fixes it — gypsum doesn't fix salt, and lime doesn't fix sodicity.

## 1. Diagnose — they look alike in the paddock
| Constraint | Field signs | Lab test | Common threshold |
|---|---|---|---|
| **Saline** | white crusts, salt-tolerant weeds (sea barley grass), patchy crop dying from the low spots | ECe (saturated paste) or EC1:5 × texture factor | ECe >4 dS/m saline (US convention); sensitive crops hurt from ~2 (gated: unconfirmed, source is paywalled or blocked) |
| **Sodic** | hard-setting crust, cloudy puddles that never clear, tunnel erosion, poor infiltration | ESP (exch. Na ÷ CEC) or SAR | ESP >6 sodic (Australia), >15 (US) |
| **Acid** | poor legume nodulation, stunted roots, clubbed root tips | pH CaCl2, exch. Al% | pH CaCl2 <5.0, Al >5% (gated: unconfirmed, source is paywalled or blocked) |
Sample 0–10, 10–20 and deeper layers: subsoil constraints are common and invisible
from the surface (see
`agriculture-environment.soil-land-management.soil-testing.soil-sampling-and-test-interpretation`).

**Emerson-style dispersion test (field version):** drop an air-dry crumb (pea-sized)
into a glass of rainwater or distilled water. Milky halo within 10 minutes–2 hours
= dispersive (sodic); repeat with a remoulded wet crumb — dispersing only when
remoulded means it will disperse after cultivation when wet.

## 2. Salinity
- **Find the water source.** Dryland salinity = rising groundwater carrying salt
  (fix recharge upslope with deep-rooted perennials, e.g. lucerne or trees).
  Irrigation salinity = salty water + inadequate drainage.
- **Leach** (where drainage exists): leaching requirement
  `LR ≈ ECw ÷ (5 × ECe_target − ECw)` (gated: unconfirmed, source is paywalled or blocked) — the extra fraction of water to apply above
  crop demand to push salt below the roots. Without drainage, leaching just raises
  the water table.
- **Live with it:** salt-tolerant pastures (puccinellia, tall wheatgrass) and
  saltbush on worst areas; barley tolerates more than wheat; most legumes are
  sensitive.
- **Cover:** mulch and keep plants on the surface — bare saline soil evaporates and
  concentrates salt at the top.

## 3. Sodicity → gypsum
Calcium displaces sodium; the electrolyte effect of gypsum also stops dispersion
quickly even before full exchange.
- **Gypsum requirement** (pure gypsum, t/ha) ≈
  `0.086 × ΔNa (cmol+/kg) × bulk density (t/m³) × depth (cm) (gated: unconfirmed, source is paywalled or blocked)`.
  Example: drop exch. Na by 1.5 cmol+/kg in the top 10 cm, BD 1.4 →
  0.086 × 1.5 × 1.4 × 10 ≈ **1.8 t/ha**; divide by product purity (e.g. ÷ 0.8) and
  allow extra for inefficiency.
- Common practical rates: 2.5–5 t/ha (gated: unconfirmed, source is paywalled or blocked), repeated every few years; responses need
  rain or irrigation to dissolve and move it.
- Incorporate or deep-place for subsoil sodicity; surface-spread gypsum mainly fixes
  crusting.
- Add organic matter and avoid working wet sodic soil (it smears and sets like brick).

## 4. Acidity → lime
- **Targets often used:** pH CaCl2 ≥5.5 in topsoil, ≥4.8 in the 10–30 cm subsoil (gated: unconfirmed, source is paywalled or blocked)
  (Western Australian guidance; check local).
- **Rate:** set by target pH change, soil buffer capacity (clay and OM) and lime
  quality. A rough guide is 2–2.5 t/ha of good lime (gated: unconfirmed, source is paywalled or blocked) to lift a sandy topsoil ~0.5–1
  unit over 0–10 cm; loams and clays need more. Labs offering buffer-pH give a
  calibrated lime requirement — use it.
- **Quality:** compare **neutralising value** (NV, vs pure CaCO3 = 100) and fineness
  (most should pass 0.5 mm). Cost per tonne of NV, not per tonne of product.
- **Subsoil acidity:** surface lime moves down only ~1 cm/year-ish (gated: unconfirmed, source is paywalled or blocked) in many soils;
  incorporate with deep tillage/spading once, or lift surface pH high enough
  (>5.5) for alkalinity to move down.
- **Ongoing:** acidification continues from N fertiliser and product removal —
  plan maintenance liming.
- Dolomite adds Mg; useful only where Mg is short.

## 5. Scalds and compacted bare ground
Bare, sealed, often sodic surfaces that shed water. **Waterponding:** build
horseshoe or rectangular low banks (~20–30 cm high) that pond ~10 cm of rain,
leaching salts and softening the crust; sow or let native grasses colonise once
the surface softens. Combine with stock exclusion until cover establishes. Rip
compacted (non-sodic) ground when dry; ripping wet sodic subsoil makes it worse.

## Gotchas
- Mixed constraints are common (saline-sodic, acid-sodic). Treat salinity's drainage
  first on saline-sodic soils — leaching sodic soil without gypsum disperses it.
- Gypsum and lime don't replace each other; lime has little effect on sodicity in
  neutral-alkaline soils.
- Expect years, not seasons, for subsoil fixes.

**Uncertainty:** thresholds and rate rules vary by country and lab method; the
gypsum formula is a standard stoichiometric estimate, not a guarantee of response.
Get local agronomist sign-off for large programmes. Not field-verified by the author.

## Verify
- [ ] Constraint confirmed by test at surface and subsoil depths, not by appearance.
- [ ] Gypsum or lime rate calculated (with purity/NV) and recorded.
- [ ] Untreated check strip left to measure response.
- [ ] Re-test same depths and points in 2–3 years.

## Checked

- Date: 2026-10-25. Jurisdiction: United States and Australia, as the skill's table labels each convention.
- Confirmed against: US convention ECe 4 dS/m for saline and ESP 15 for sodic (University of Delaware extension, citing the USDA Salinity Laboratory scheme; Handbook 60 itself not opened); Australian convention ESP above 6 is sodic (Agriculture Victoria, after Northcote and Skene 1972); the gypsum example was recomputed (0.086 x 1.5 x 1.4 x 10 = 1.8 t/ha).
- Not confirmed: the crop-sensitivity salinity figure, acid-soil thresholds, leaching requirement formula, gypsum coefficient, practical rates and lime figures (no free primary source reached).

Method: documentation only; no commands were run.
