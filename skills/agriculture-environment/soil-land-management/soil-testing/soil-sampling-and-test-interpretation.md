---
id: agriculture-environment.soil-land-management.soil-testing.soil-sampling-and-test-interpretation
name: soil-sampling-and-test-interpretation
category: agriculture-environment
field: soil-land-management
product: soil-testing
tags: [soil-land-management, soil-testing, soil-sampling, soil-test, soil-analysis, lab-report, ph, ph-water, ph-cacl2, buffer-ph, cec, ecec, exchangeable-cations, base-saturation, colwell-p, olsen-p, bray-p, mehlich-3, potassium, sulfur, kcl-40, electrical-conductivity, ece, organic-carbon, soil-texture, ribbon-test, texture-by-feel, sampling-design, zone-sampling, grid-sampling, soil-probe, agronomy]
level: practitioner
status: gated
description: "Take a soil sample a lab result can be trusted on (depth, cores, zones, timing), then read the report: pH in water vs CaCl2, P tests, K, CEC, EC, texture, and turning numbers into actions."
sources: ["https://vro.agriculture.vic.gov.au/DPI/Vro/vrosite.nsf/pages/sodic_soils"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Soil sampling and test interpretation

**Goal:** get a soil test that represents the paddock, read it correctly, and turn
it into two or three decisions (lime? which nutrient is limiting? any problem soil?).
Most bad fertiliser decisions come from a bad sample, not a bad lab.

## 1. Design the sample before you pick up the probe
- **One sample = one management unit.** Split a paddock where soil type, history or
  yield clearly differ (creek flat vs ridge, old stockyard, ex-lime-dump). Mixing
  them averages two soils into one that doesn't exist.
- **Zone vs grid.** Zones (from yield maps, EM survey, NDVI or just soil type) are
  cheaper and usually enough. Grid sampling (commonly 1 ha cells in precision
  systems) suits variable-rate lime and P where history is unknown.
- **Use a transect, not random wandering.** Walk a fixed W or zig-zag inside the
  zone; record GPS start/end so you can resample the same line next time — trends
  are worth more than any single result.
- **Avoid:** gateways, troughs, camps, fence lines, headlands, old fertiliser bands,
  burnt heaps, within ~20 m of trees.

## 2. Take the cores
- **Cores:** 20–40 per composite (30 is a good default) (gated: unconfirmed, source is paywalled or blocked). Fewer than ~15 and the
  result swings with whichever core landed on a dung pat or fertiliser band.
- **Depth is the calibration.** Interpretation tables are built for a set depth —
  0–10 cm is standard in much of Australia/NZ pasture and cropping; 0–15 or
  0–20 cm (6–8 in) in the US and UK. Use the depth your lab's guidelines assume and
  never change it between years.
- **Subsoil:** for acidity, add a 10–20 cm (and sometimes 20–30 cm) sample — surface
  liming can hide an acid layer below. For deep N, sulfur, salinity or sodicity,
  sample 0–30/30–60/60–90 cm separately.
- **Timing:** same season every time, ideally before the main fertiliser decision and
  ~2–3 months after the last fertiliser, lime or heavy grazing. pH and K drift with
  season and moisture.
- **Handling:** clean plastic bucket (no galvanised buckets if testing zinc), mix
  well, send ~500 g. Mineral N samples must be chilled and posted fast; most other
  tests tolerate air-drying.

## 3. Read the report
Check the **method code** next to each number before comparing to anything.

| Test | What it tells you | Rough guide (check your region's tables) |
|---|---|---|
| pH (1:5 water) | acidity | most crops happy ~6.0–7.5 (gated: unconfirmed, source is paywalled or blocked) |
| pH (CaCl2) | acidity, less seasonal noise | reads ~0.5–0.8 lower than water pH (gated: unconfirmed, source is paywalled or blocked); lime commonly considered below ~5.0–5.5 CaCl2 |
| Exchangeable Al % | aluminium toxicity risk | >5% hurts sensitive crops (gated: unconfirmed, source is paywalled or blocked) (canola, lucerne, barley) |
| Colwell P / Olsen / Bray / Mehlich-3 | plant-available P | each has its own scale; Colwell targets also depend on PBI (P buffering) |
| K (Colwell or exchangeable) | potassium | sandy soils run low first |
| KCl-40 S | sulfur | low results matter most for canola and legumes |
| ECEC / CEC (cmol+/kg) | nutrient-holding capacity | <5 is a light, leachy soil; >15 heavy (gated: unconfirmed, source is paywalled or blocked) |
| Exch. Na % (ESP) | sodicity | >6% sodic (Australian convention) — see land-reclamation skill |
| EC (1:5) / ECe | salinity | convert EC1:5 to ECe with a texture factor before comparing to crop tolerance |
| Organic carbon % | OM trend (OM ≈ OC × 1.72 (gated: unconfirmed, source is paywalled or blocked)) | compare only with same method and depth |

## 4. Texture by feel (ribbon test)
Moisten a walnut-sized ball until it's like putty, then push it out between thumb
and forefinger into a ribbon:
- won't form a ball / gritty — **sand**; ribbon <15 mm — **loamy sand / sandy loam**;
- ~25 mm, slightly spongy — **loam**; 40–50 mm — **clay loam**;
- >75 mm, smooth and plastic (gated: unconfirmed, source is paywalled or blocked) — **clay**. Gritty = sand, silky = silt, sticky = clay.
Texture sets CEC expectations and the lime rate needed to shift pH.

## 5. Turn it into decisions
1. Fix pH first — nutrients and herbicide behaviour depend on it
   (see `agriculture-environment.soil-land-management.land-reclamation.managing-saline-sodic-and-acid-soils`).
2. Identify the **most limiting** nutrient against the critical value for the crop.
3. Above target? Maintenance only (replace removal). Well above? Skip a year.
4. Feed the numbers into a nutrient budget
   (`agriculture-environment.soil-land-management.nutrient-management.nutrient-budget-and-fertiliser-rates`).

## Gotchas
- Comparing Colwell P from one lab with Olsen P from another is meaningless.
- One test is a snapshot; three years on the same transect is a trend.
- A low K result on a sodic clay can be an extraction artefact — check ratios.
- Lab "recommendations" sometimes sell product; check against independent guides.

**Uncertainty:** thresholds above are generalised from Australian, US and UK
extension guidance and vary by crop, region and lab method — always use the
calibration tables your lab and local extension service publish. Not field-verified
by the author.

## Verify
- [ ] Each sample maps to one management zone with a recorded GPS transect.
- [ ] 20–40 cores at the lab's calibration depth, same season as last time.
- [ ] You can name the method behind every number you're acting on.
- [ ] pH decision made (water vs CaCl2 not confused).
- [ ] The limiting nutrient and its action are written down before ordering fertiliser.

## Checked

- Date: 2026-10-25. Jurisdiction: Australia assumed for the ESP convention; US and UK sampling depths are noted in the skill.
- Confirmed against: Agriculture Victoria: ESP above 6 is generally regarded as sodic in Australia (Northcote and Skene 1972).
- Not confirmed: the pH ranges, aluminium and CEC bands, ribbon-test lengths, core counts, grid size, sampling depth and sample mass, and the 1.72 organic matter factor (no free primary source reached).

Method: documentation only; no commands were run.
