---
id: hospitality-culinary.winemaking.cellar-chemistry-and-analysis.so2-acid-and-routine-wine-analysis
name: so2-acid-and-routine-wine-analysis
category: hospitality-culinary
field: winemaking
product: cellar-chemistry-and-analysis
tags: [winemaking, cellar-chemistry-and-analysis, wine-analysis, so2, sulfur-dioxide, sulphites, free-so2, total-so2, molecular-so2, potassium-metabisulfite, kmbs, ph, titratable-acidity, ta, tartaric-acid, acid-adjustment, acidification, deacidification, potassium-bicarbonate, volatile-acidity, va, residual-sugar, alcohol, aeration-oxidation, ripper-titration, bench-trial, nutrient-additions, cellar-lab, wine-lab, legal-limits]
level: practitioner
status: draft
description: "Keep wine protected and balanced: dose SO2 to a molecular target by pH, run free/total SO2, pH, TA, VA and sugar tests, and adjust acid only after bench trials."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# SO₂, acid and routine wine analysis — measure, calculate, trial, then add

**Goal:** every addition in the cellar is based on a measurement and a bench trial, recorded,
and inside legal limits — so wine stays protected from oxidation and microbes without tasting
of sulphur or being acid-corrected by guesswork.

## 1. SO₂: dose to molecular, not to habit
Only **molecular SO₂** is strongly antimicrobial, and its share of free SO₂ collapses as pH rises.
`free SO₂ needed (mg/L) = molecular target × (1 + 10^(pH − 1.81))`
- Common targets: **0.8 mg/L molecular for whites/rosé**, ~0.5 for reds (tannins help).
- At pH 3.4 a white needs ~32 mg/L free; at pH 3.6 a red needs ~32 mg/L free at 0.5 molecular; at pH 3.8
  the numbers become impractical — another reason pH is managed at harvest.
- **Potassium metabisulfite (KMBS)** yields ~57% SO₂ by weight in theory (use ~0.5–0.55 in practice
  for older powder). Dose: `g KMBS = mg/L wanted × litres ÷ (1000 × 0.57)`.
  Dissolve in a little water or wine, mix well into the tank, re-test after 24 h — part binds.
- When: after MLF finishes (or after primary if MLF is blocked), after each racking, and before bottling.
- **Legal limits** on total SO₂ differ (e.g. EU dry wines roughly 150 mg/L red, 200 white; US 350 mg/L);
  check the market. Many people are sensitive to sulphites, and labelling is required above ~10 mg/L in many markets.

## 2. The routine panel
| Test | Method (small winery) | Why |
|---|---|---|
| Free / total SO₂ | Aeration–oxidation (A-O) — more accurate in reds; Ripper titration — fast, reads high in reds | Protection |
| pH | Calibrated meter (2-point, buffers at 4 and 7), at stable temperature | Stability, SO₂ maths |
| TA | Titrate with 0.1 N NaOH to pH 8.2 (meter end-point, not phenolphthalein in red) | Balance |
| VA | Cash still / enzymatic; alarm around 0.6–0.8 g/L acetic (sensory threshold), legal limits ~1.0–1.2 | Spoilage |
| Residual sugar | Enzymatic glucose + fructose, or Clinitest (rough) | Dryness, stability |
| Malic | Paper chromatography / enzymatic | MLF status |
| Alcohol | Ebulliometer or lab | Labelling tolerance |
Measure on schedule (e.g. SO₂ monthly in barrel), not just when worried.

## 3. Acid adjustment
- **Acidify** (warm climates): **tartaric acid** is standard; a rough rule is ~1 g/L tartaric lowers pH
  by ~0.1 and raises TA ~1 g/L, but buffering makes this unreliable — **bench trial**.
  Best done on must/juice before fermentation, where it integrates better.
- **Deacidify** (cool climates): potassium bicarbonate or calcium carbonate, or rely on MLF.
  Expect tartrate precipitation afterwards; cold-stabilise later.
- Check the jurisdiction: many regions forbid both acidifying and chaptalising the same wine,
  or limit additions (EU rules by zone).

## 4. Bench trials
Take a representative sample, make a stock solution of the additive, dose a range (e.g. 0, 0.5, 1.0,
1.5 g/L equivalents) into measured glasses, wait (acid: overnight; fining: 24–48 h), measure and
taste **blind**. Choose the *lowest* effective dose. Scale to tank volume with a written calculation
that a second person checks.

## Gotchas
- pH meters drift: calibrate each session, keep the probe wet, check slope.
- Adding SO₂ during active MLF stops it.
- Mixing KMBS as a powder into a big tank without dissolving leaves strata.
- Units matter: g/L vs mg/L vs ppm, and TA as tartaric vs sulfuric (EU/French) — convert (× 1.53 from sulfuric to tartaric).

## Verify
- [ ] Molecular SO₂ calculated from current pH; free SO₂ re-tested 24 h after adding.
- [ ] Analysis log per vessel with date, method, result.
- [ ] Every acid/fining addition preceded by a documented bench trial.
- [ ] Total SO₂, VA and alcohol within limits of the target market.

*Status draft: legal limits and conversion factors summarised from general references; verify for your market.*
