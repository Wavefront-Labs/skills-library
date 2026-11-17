---
id: agriculture-environment.livestock-farming.livestock-nutrition.feed-budget-and-ration-check
name: feed-budget-and-ration-check
category: agriculture-environment
field: livestock-farming
product: livestock-nutrition
tags: [livestock-nutrition, ration-formulation, ration-balancing, feed-budget, feed-budgeting, dry-matter, dm, dry-matter-intake, dmi, metabolisable-energy, me, mj-me, crude-protein, cp, ndf, feed-test, forage-test, hay-analysis, silage-analysis, supplementary-feeding, drought-feeding, as-fed, dse, livestock-units, cattle-nutrition, sheep-nutrition, grain-introduction, acidosis]
level: practitioner
status: draft
description: "Check a ruminant ration and feed budget: dry matter intake, ME and crude protein demand vs supply from a feed test, as-fed conversion and a season feed budget."
sources: ["AFRC / CSIRO Feeding Standards for Australian Livestock (ruminants) summary", "Extension drought-feeding and ration calculators (e.g. NSW DPI Drought Feed Calculator, MLA feed demand calculator)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Feed budget and ration check (ruminants)

**Goal:** answer two questions with numbers instead of guesses — *does this ration meet
the animals' energy and protein needs?* and *do I have enough feed to get through until
the next pasture growth?*

## 1. Work in dry matter, always
Feeds differ hugely in water: silage ~30–40% DM, hay ~85–90%, grain ~90%, lush pasture
~15–20%. Do every calculation in **kg DM**, then convert back:
```
kg as-fed = kg DM ÷ (DM% / 100)
```
A cow needing 6 kg DM from 35% DM silage gets 6 ÷ 0.35 ≈ 17 kg as fed.

## 2. Get a feed test
Send a representative sample (core-sample 10–20 bales or several silage pit faces)
to a lab. You need at least: **DM%, metabolisable energy (ME, MJ/kg DM), crude protein
(CP %), NDF %**. Rough book values for comparison:
| Feed | ME (MJ/kg DM) | CP (%) |
|---|---|---|
| Cereal straw | 6–7 | 3–5 |
| Average grass hay | 8–9 | 8–12 |
| Lucerne/alfalfa hay | 9–10 | 17–22 |
| Good grass silage | 10–11 | 12–16 |
| Barley/wheat grain | 12–13 | 10–13 |
| Lush spring pasture | 11–12 | 20–25 |
Feed tests often surprise — a "good" hay can be 7.5 MJ.

## 3. Animal demand
Use your country's standards or calculator; typical maintenance figures to sanity-check:
- **Intake limit:** cattle ~2–3% of liveweight as DM (lower on poor, high-NDF feed —
  low-quality roughage physically limits intake).
- **Energy:** maintenance ME (MJ/day) ≈ roughly **0.5 × W^0.75 to 0.6 × W^0.75** for
  cattle depending on activity; a 500 kg dry cow ≈ 55–65 MJ ME/day. Add for growth,
  late pregnancy (substantially more in the last trimester), lactation (≈ 5 MJ per
  litre of milk in dairy cows is a common rule).
- **Protein:** dry adult stock ~7–8% CP in the diet; growing stock and lactating animals
  ~12–18%. Below ~7% CP, rumen microbes slow down and intake falls.
- **Sheep:** a dry ewe ~50 kg needs roughly 8–9 MJ ME/day at maintenance; much more
  in late pregnancy with twins.

## 4. Check the ration (worked example)
500 kg dry beef cow, maintenance, needs ~60 MJ ME and ~8% CP.
Hay: 88% DM, 8.5 MJ/kg DM, 9% CP. She can eat ~2% LW = 10 kg DM.
- 10 kg DM × 8.5 = 85 MJ — energy met; CP 9% — met. As fed: 10 ÷ 0.88 ≈ 11.4 kg hay/day.
Now feed **straw** (6.5 MJ, 4% CP): intake drops to maybe ~1.5% LW = 7.5 kg DM → 49 MJ,
CP 4% — short on both. Fix with a protein/energy supplement (e.g. part lucerne hay or a
urea-based lick per label) and/or grain.

## 5. Feed budget (season)
```
Demand (kg DM) = head × kg DM/head/day × days
Supply (kg DM) = Σ (feed on hand × DM%) + expected pasture growth − wastage
```
Allow **10–25% wastage** for hay fed on the ground or in rings, less with good feeders.
Example: 100 cows × 10 kg DM × 120 days = 120 t DM. 300 round bales × 400 kg × 0.88 =
105.6 t DM, minus 15% waste = 90 t → **30 t short**: buy feed now, sell stock, or wean early.

## 6. Introducing grain safely
Introduce cereal grain over **~2–3 weeks**, starting at ~0.25–0.5 kg/head/day for cattle
(proportionally less for sheep), increasing every 2–3 days, with roughage always
available. Sudden access to large amounts of grain causes **acidosis** (grain poisoning),
which can kill. Also beware urea overdose (follow label rates strictly).

## Gotchas
- Mixing units (as-fed vs DM, MJ vs Mcal: 1 Mcal = 4.184 MJ) is the commonest error.
- Bale weights vary ±20%: weigh a few.
- The maintenance coefficients above are rough rules **not drawn from one standard** —
  use a recognised calculator for real decisions; ask a nutritionist for dairy and feedlot rations.

## Verify
- [ ] Every feed has a test or a clearly labelled book value.
- [ ] Ration checked in kg DM for ME, CP and intake limit, per stock class.
- [ ] Feed budget shows surplus/deficit with a decision date.
- [ ] Grain introductions follow a step-up plan with roughage available.
- [ ] Animal condition re-scored after 3–4 weeks to confirm the ration works.
