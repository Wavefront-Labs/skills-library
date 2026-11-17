---
id: hospitality-culinary.baking-and-pastry.baking-formulation.bakers-percentages-hydration-and-scaling
name: bakers-percentages-hydration-and-scaling
category: hospitality-culinary
field: baking-and-pastry
product: baking-formulation
tags: [baking-formulation, bakers-percentage, bakers-math, baker-math, formula, hydration, dough-yield, scaling, total-flour, preferment-percentage, levain-percentage, yeast-conversion, fresh-yeast, instant-yeast, active-dry-yeast, substitutions, butter-substitution, gluten-free, production-schedule, batch-sheet, spreadsheet, desired-dough-temperature, scaling-loss]
level: practitioner
status: draft
description: "Write formulas in baker's percentages, compute hydration with preferments, scale to any dough yield with loss allowance, convert yeasts and substitute safely, and build a production schedule."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Baker's percentages, hydration and scaling

**Goal:** express any recipe so it scales to any batch exactly, predict how a change
will behave, and plan a bake day that finishes on time.

## 1. Baker's percentages
Every ingredient is a percentage of **total flour weight (= 100 %)**.
Example: 1,000 g flour, 700 g water, 20 g salt, 10 g instant yeast →
flour 100 %, water 70 %, salt 2 %, yeast 1 %. **Total formula = 173 %.**
- All flours (white, wholemeal, rye) together make the 100 %.
- Percentages add up to more than 100 — that's normal.

## 2. Hydration
- **Hydration % = total water ÷ total flour × 100.**
- Count water in other ingredients if precise: milk ~87–88 % water, eggs ~75 %, butter
  ~16–18 %. Many bakers count only water and milk.
- **Preferments and levain contribute flour and water.** For a 100 %-hydration levain
  (equal flour and water), 200 g of levain adds 100 g flour and 100 g water to the totals.
- **Preferment %** = flour in the preferment ÷ total flour (e.g. 15–25 % prefermented
  flour is common for sourdough). Conventions differ: some bakers state levain as a % of
  the main-dough flour only. State which you use.
- Typical hydrations: bagels ~55–60 %, sandwich loaf ~60–65 %, baguette ~65–72 %,
  open-crumb sourdough ~75–85 %, ciabatta ~80 %+. Wholegrain flours absorb more.

## 3. Scaling to a dough yield
1. Decide **total dough needed**: pieces × piece weight, e.g. 40 × 500 g = 20,000 g.
2. Add **scaling/process loss** (dough stuck to the bowl and bench, trimming) — commonly
   ~2–5 %: 20,000 × 1.03 = 20,600 g.
3. **Flour = total dough ÷ (total formula % ÷ 100)** = 20,600 ÷ 1.73 = **11,908 g**.
4. Each ingredient = flour × its percentage: water 8,335 g, salt 238 g, yeast 119 g.
5. Round to the scale's resolution; use a gram scale for salt and yeast (a 0.1 g scale for
   small batches).
Spreadsheet columns: ingredient | % | weight = flour × % / 100. Change the dough total
and everything rescales.

## 4. Yeast conversions (approximate)
| From | To | Multiply by |
|---|---|---|
| Fresh (compressed) | Instant dry | ~0.33–0.4 |
| Fresh | Active dry | ~0.4–0.5 |
| Active dry | Instant | ~0.75 |
Suppliers quote slightly different factors; test in your own dough.

## 5. Substitutions that work (and what changes)
- **Butter ↔ oil:** butter ≈ 80–82 % fat, so ~80 g oil + ~20 g water replaces 100 g
  butter; texture and flavour change, creaming method no longer works.
- **Bread flour ↔ plain/all-purpose:** lower protein absorbs less water — cut hydration
  2–5 points and expect a weaker structure.
- **Wholemeal in place of white:** add water (+5–10 points), expect faster fermentation.
- **Sugar reduction:** sugar is also tenderiser and moisture-holder; cutting > ~25 %
  in cakes changes texture and shelf life.
- **Gluten-free:** not a 1:1 swap — needs a formulated blend plus binders (psyllium,
  xanthan); treat as a separate recipe.
- Salt holds near **1.8–2.2 %** for bread; it controls fermentation as well as taste.

## 6. Production scheduling
Work backwards from the "out of oven" time:
- List each product's steps with durations: mix, bulk, divide/pre-shape, rest, shape,
  proof, bake, cool.
- Use the **oven as the bottleneck**: stagger mixes so doughs reach the oven when it's
  free, by deck and temperature.
- Plan cold retards to move long steps overnight.
- Batch sheet per day: product, quantity, total dough, ingredient weights, DDT and water
  temperature, timings, initials.

## Gotchas
- Volume measures (cups) make scaling unreliable — convert everything to grams.
- Hydration percentage alone doesn't predict feel; flour protein and absorption vary
  by mill and harvest.
- Scaling a formula doesn't scale mixing time or fermentation time linearly.

## Verify
- [ ] Formula written in % with total flour = 100 % and total formula % shown.
- [ ] Hydration includes water from preferments (convention stated).
- [ ] Scaled batch landed within ~1 % of target dough weight after division.
- [ ] Yeast conversions noted and tested.
- [ ] Production schedule shows the oven booked without overlaps.
