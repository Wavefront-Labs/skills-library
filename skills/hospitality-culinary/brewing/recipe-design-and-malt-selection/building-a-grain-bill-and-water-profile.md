---
id: hospitality-culinary.brewing.recipe-design-and-malt-selection.building-a-grain-bill-and-water-profile
name: building-a-grain-bill-and-water-profile
category: hospitality-culinary
field: brewing
product: recipe-design-and-malt-selection
tags: [brewing, recipe-design-and-malt-selection, recipe-design, grain-bill, malt, base-malt, specialty-malt, crystal-malt, roasted-malt, adjuncts, original-gravity, og, ppg, extract-potential, brewhouse-efficiency, srm, ebc, colour, morey, bjcp, style-guidelines, water-chemistry, residual-alkalinity, mash-ph, sulfate-chloride-ratio, gypsum, calcium-chloride, recipe-scaling, brewing-software, brewfather, beersmith, homebrew, craft-brewing]
level: practitioner
status: draft
description: "Design a beer recipe to hit a style: pick base and specialty malts, calculate gravity from extract and efficiency, estimate colour, set water chemistry for mash pH, and scale between systems."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Building a grain bill and water profile — design to numbers, then taste

**Goal:** a recipe that lands on a target original gravity (OG), colour, bitterness
and character on *your* system, written so it scales to a different brewhouse.

## 1. Start from targets
Pick the style's ranges (e.g. BJCP guidelines for homebrew/competition; your brand spec
commercially): OG, FG, ABV, IBU, colour (SRM/EBC), and two or three words for the
malt character ("bready, light caramel, dry finish"). Write them down before choosing grain.

## 2. Choose malts by role
- **Base malt (70–100%)** gives most extract and the backbone: pale ale / Maris Otter
  (biscuity), pilsner (light, needs a vigorous boil for DMS), Munich/Vienna (malty).
- **Crystal/caramel (0–15%)** adds sweetness, body and colour; above ~15% it turns
  cloying and the beer finishes high.
- **Roasted (0–10%)** — chocolate, black, roast barley — for colour and dry roast;
  debittered versions for colour without harshness.
- **Adjuncts:** flaked oats/wheat for body and haze; sugar or rice to dry it out.
- Rule of thumb: the simplest grain bill that hits the character wins; each malt should earn its place.

## 3. Calculate gravity
Gravity points (GP) = (OG − 1) × 1000; e.g. 1.050 → 50.
`total points needed = GP × batch volume (gal)`
Each malt contributes `kg-or-lb × extract potential × efficiency`. In US units potential
is PPG (points per pound per gallon): pale malt ≈ 36–37, crystal ≈ 33–35, sugar ≈ 46.
Brewhouse efficiency is your system's real number (homebrew 65–80%; commercial often
85–95%). Use your *measured* efficiency from the last few brews, not the software default.
Metric: most software (Brewfather, BeerSmith) works with extract % (malt
spec sheet, fine-grind as-is) — prefer the maltster's analysis sheet over generic values.

## 4. Colour
Malt colour units: MCU = Σ(lb × °L) ÷ gal. Morey: SRM ≈ 1.4922 × MCU^0.6859. EBC ≈ SRM × 1.97.
Estimates drift above ~30 SRM; trust them for direction, not precision.

## 5. Water: set mash pH first, flavour second
- Target **mash pH 5.2–5.6** at room temperature (measure ~15 min in).
  Pale grists with alkaline water run high (harsh, dull); dark grists acidify the mash.
- Get a water report (or use RO water and build up). Key figures: Ca, Mg, Na, Cl, SO₄,
  alkalinity as CaCO₃.
- Lower pH with acid malt or lactic/phosphoric acid; raise it with baking soda or
  slaked lime in dark beers.
- **Calcium** ~50–150 ppm for yeast health and clarity.
- **Sulfate:chloride:** ~2–4:1 crisper, drier hop expression (pale ales/IPAs);
  ~1:2 rounder, fuller malt (NEIPA, stouts). Add gypsum (CaSO₄) and calcium chloride.
- Software calculators predict pH within roughly ±0.1–0.2; always check with a calibrated meter.

## 6. Scaling between systems
Scale by **percentages** (grist %, IBU target, water ppm), not kg. Recalculate grain
for the new system's efficiency, hop utilisation (larger kettles and long whirlpools
add IBU), and boil-off rate. First batch on a new system is a test batch.

## Gotchas
- Changing maltsters changes the beer — colour and extract vary by lot; read the COA.
- Too many specialty malts muddy flavour.
- Unmeasured efficiency is the #1 reason recipes miss OG.

## Verify
- [ ] Recipe sheet lists targets, grist %, water additions, and the efficiency assumed.
- [ ] Measured mash pH 5.2–5.6.
- [ ] Pre-boil and OG within ±2 gravity points of plan; if not, update efficiency.
- [ ] Finished beer tasted against the written character words.

*Status draft: PPG and colour formulas are standard homebrew references; commercial maltster data should override them.*
