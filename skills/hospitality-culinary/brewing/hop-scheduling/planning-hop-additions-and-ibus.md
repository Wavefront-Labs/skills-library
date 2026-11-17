---
id: hospitality-culinary.brewing.hop-scheduling.planning-hop-additions-and-ibus
name: planning-hop-additions-and-ibus
category: hospitality-culinary
field: brewing
product: hop-scheduling
tags: [brewing, hop-scheduling, hops, ibu, bitterness, tinseth, hop-utilisation, alpha-acids, aa-percent, bittering-addition, flavour-addition, aroma-addition, flameout, whirlpool, hop-stand, dry-hopping, dry-hop, biotransformation, hop-creep, hop-burn, pellets, t90, cryo-hops, lupulin-powder, hop-varieties, citra, mosaic, saaz, east-kent-goldings, myrcene, linalool, oxidation, ipa, neipa, lager]
level: practitioner
status: draft
description: "Plan a hop schedule: choose varieties by role, estimate IBUs with Tinseth, set whirlpool and dry-hop timing and rates, and avoid hop creep, grassiness and oxidised aroma."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Planning hop additions and IBUs — bitterness by numbers, aroma by timing

**Goal:** land the bitterness you designed and the hop aroma you wanted, without
harshness, grassiness or an over-attenuated, diacetyl-tinged beer from hop creep.

## Hop roles and timing
| Addition | When | What you get |
|---|---|---|
| Bittering | 60–90 min boil | Isomerised alpha acids → bitterness; little aroma survives |
| Flavour | 10–20 min | Some bitterness, some hop flavour |
| Aroma / flameout | 0–5 min | Little bitterness, volatile oils partly retained |
| Whirlpool / hop stand | 15–40 min at ~70–90 °C | Rich flavour, modest IBU (more the hotter) |
| Dry hop | In fermenter | Aroma, little or no bitterness |
Use high-alpha, clean varieties (e.g. Magnum, Warrior) for bittering; save expensive aroma
varieties (Citra, Mosaic, Nelson Sauvin, Saaz, EKG) for late additions.

## Estimating IBU (Tinseth)
`IBU = U × (AA × g × 1000) ÷ L`, with AA as a decimal (6.5% = 0.065), g of hops, L of post-boil wort.
`U = bigness × time factor`
- bigness = 1.65 × 0.000125^(boil gravity − 1)
- time factor = (1 − e^(−0.04 × minutes)) ÷ 4.15
Example: 28 g at 10% AA, 60 min, 20 L, boil gravity 1.050 → U ≈ 0.23 → **IBU ≈ 32**.
- Tinseth ignores whirlpool time; software adds a whirlpool model, but treat late-addition IBUs as
  ±30% guesses (uncertain). Big commercial kettles get more utilisation than homebrew pots.
- Use the **AA% printed on the actual lot**, not the variety's typical; hops lose alpha with
  age and warm storage (HSI). Store cold, vacuum-sealed, dark.
- Perceived bitterness also depends on sulfate, FG and dryness — a dry 40 IBU tastes more bitter than a sweet 40.

## Dry hopping
- **Rates:** light 1–3 g/L; American IPA 4–8 g/L; heavy NEIPA 10–16+ g/L. (1 lb/bbl ≈ 3.9 g/L.)
- **Timing:** at the end of fermentation or after it, at ~12–18 °C, for 2–4 days. Longer
  contact adds grassy/vegetal notes, not more aroma.
- **During active fermentation** ("biotransformation" dry hop) — yeast converts some hop
  compounds and scavenges oxygen introduced with the hops; aroma differs, not necessarily better.
- **Hop creep:** hops contain enzymes that break down dextrins, letting yeast restart —
  extra attenuation, CO₂ and diacetyl after you thought fermentation ended. Allow a few
  days with yeast present, recheck gravity and diacetyl before crashing and packaging.
- **Oxygen is the enemy of hop aroma.** Purge hop-addition ports/bags with CO₂, add hops
  without opening the vessel wide, and keep dissolved oxygen low at packaging.
- Pellet form (T90, cryo/lupulin) settles better and extracts faster than whole cones;
  cryo is roughly twice the potency by weight (check the supplier).
- **Hop burn** (harsh, astringent bite in young heavily dry-hopped beer) fades with
  time and settling; cold-crash and allow clean-up time before release.

## Gotchas
- Fresh hops (wet hops) need ~5–6× the weight of dried hops.
- Hop debris clogs transfer lines — use a hop filter, settling cone or dump trub from a conical.
- Pine/onion/garlic notes from some varieties (sulfur compounds) vary by crop year.

## Verify
- [ ] Schedule table lists variety, lot AA%, weight, time and calculated IBU per addition.
- [ ] Measured or tasted bitterness matches spec within tolerance (lab IBU if available).
- [ ] Gravity stable for 2–3 days after the last dry hop before packaging.
- [ ] Aroma bright and fresh, no grassy or vegetal notes; no oxidised "papery" note.

*Status draft: IBU formulas are estimates; commercial brewers should confirm with lab IBU analysis.*
