---
id: agriculture-environment.crop-farming.variety-selection.choosing-cultivars-and-calculating-seeding-rate
name: choosing-cultivars-and-calculating-seeding-rate
category: agriculture-environment
field: crop-farming
product: variety-selection
tags: [variety-selection, cultivar, cultivar-selection, variety-trials, nvt, recommended-list, ahdb-recommended-list, maturity, phenology, disease-resistance-rating, lodging, quality-grade, seed-quality, germination-test, thousand-seed-weight, tsw, thousand-grain-weight, seeding-rate, sowing-rate, plant-population, establishment-percentage, farm-saved-seed, certified-seed, seed-treatment, pbr, end-point-royalty]
level: practitioner
status: gated
description: "Pick a crop variety from multi-site trial data and fit it to field and sowing window, then calculate a seeding rate from target plants, thousand-seed weight, germination and expected establishment."
sources: []
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Choosing cultivars and calculating seeding rate

**Goal:** the variety most likely to make money on *this* field in *this* sowing
window, sown at a rate that hits the target plant population. Picking off a single
trial's top yield or a brochure is the common mistake.

## 1. Use multi-site, multi-year trial data
- Sources: independent variety trial programmes (e.g. Australia's National Variety
  Trials, the UK AHDB Recommended Lists, US state university trials), not just seed-
  company plots.
- Prefer varieties that rank well **across several years and nearby sites**; one
  season's winner is often noise. Look at the yield *relative to a control* and the
  number of trials it's in.
- Filter by your region and by the **sowing time** trials matched yours (early vs late
  sowing series rank varieties differently).

## 2. Match the variety to the field and window
- **Maturity / phenology:** the variety must flower in your low-frost, low-heat window.
  Sowing date and variety maturity go together: long-season types sown early, quick
  types for late sowing. Getting this wrong costs more than a few % of yield potential.
- **Disease ratings** for the diseases your field actually has (check field history —
  e.g. stripe rust, septoria, blackleg, crown rot). Ratings like R/MR/MS/S or a 1–9
  scale; know which direction the scale runs. Resistance can break down when a new
  pathogen strain appears — check the current year's ratings.
- **Agronomic traits:** lodging and standing ability (high-N fields), shattering,
  straw strength, herbicide tolerance (e.g. HT canola, IMI-tolerant cereals),
  acid-soil/boron tolerance, height.
- **Quality/market:** grade (milling vs feed wheat, malting barley acceptance — malting
  varieties must be on the maltsters' accepted list), delivery site segregations.
- **Licensing:** many varieties carry plant breeders' rights; end-point royalties or
  restrictions on farm-saved seed may apply.
Spread risk: grow two or three varieties with different maturities on larger farms.

## 3. Seed quality
Before sowing, test your seed (lab or home test):
- **Germination %** — certified seed comes with it; farm-saved seed must be tested.
  Home test: 100 seeds between moist paper towels, 20–25 °C, count normal seedlings at
  ~7 days (crop-specific; cereals ~4–8 days).
- **Thousand-seed weight (TSW)**: count 1,000 seeds (or 2 × 500) and weigh in grams.
  TSW varies a lot by seed lot and season — never use last year's number.
- Vigour, purity (weed seed, other crops), disease (e.g. smut, ergot); grade out small seed.
- Seed treatments for seedborne diseases or early insects where justified.

## 4. Seeding rate calculation
```
seeding rate (kg/ha) = target plants/m² × TSW (g)
                       ÷ (germination fraction × establishment fraction × 100)
```
Example — wheat: target 150 plants/m², TSW 40 g, germination 0.95, expected
establishment 0.80 →
150 × 40 ÷ (0.95 × 0.80 × 100) = 6000 ÷ 76 ≈ **79 kg/ha** (recomputed 78.9).

Same target, but a big-seeded lot with TSW 48 g → **95 kg/ha** (recomputed 94.7). Sowing a fixed
"80 kg/ha every year" gives very different plant numbers.

Typical target plants/m² (orders of magnitude only; use local guidance (gated: unconfirmed, source is paywalled or blocked)): wheat and
barley ~100–250, canola ~20–50, field peas ~50–80, chickpeas ~20–50, soybeans
(in plants/ha) ~250,000–400,000, maize ~60,000–100,000 plants/ha.

**Establishment fraction** is the judgement: ~0.8-0.9 in a good seedbed with good
moisture; 0.5-0.7 for dry sowing, heavy stubble, deep sowing, cold soils, slugs,
or crusting soils. Lift the target or the establishment allowance for late sowing
(less tillering/branching time) or weedy fields (competition).

## 5. Calibrate and check
Set the seeder from the calculated rate and **calibrate it** (see tractor-implements
and planting-establishment skills) — then count plants after emergence and record the
real establishment % for next year's calculation.

## Gotchas
- Trial yields assume trial management; your relative ranking holds better than the
  absolute number.
- "Resistant" doesn't mean immune; still scout.
- Different seed lots of the same variety can differ noticeably in TSW (gated: unconfirmed, source is paywalled or blocked).

## Verify
- [ ] Variety chosen from multi-site, multi-year data in your region and sowing window.
- [ ] Disease ratings matched to the field's known diseases (current year's ratings).
- [ ] Germination and TSW measured for this seed lot.
- [ ] Seeding rate calculated from target plants, not a habit number.
- [ ] Post-emergence plant count recorded to refine establishment %.
