---
id: mathematics.numeracy-and-mental-calculation.everyday-numeracy.unit-prices-percent-change-and-conversions
name: unit-prices-percent-change-and-conversions
category: mathematics
field: numeracy-and-mental-calculation
product: everyday-numeracy
tags: [numeracy-and-mental-calculation, everyday-numeracy, functional-numeracy, unit-price, price-per-unit, best-buy, multibuy, discounts, percentage-change, percentage-points, compound-interest, apr, aer, interest-rates, unit-conversion, metric-imperial, recipe-scaling, proportional-reasoning, ratio, energy-bill, kwh, fuel-economy, reading-bills, rates, money-maths]
level: intro
status: verified
description: "Everyday number decisions: compare unit prices and multibuys, read percent changes and points, understand APR vs simple interest, convert units, scale recipes, and check a bill line by line."
sources: []
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Unit prices, percent change and conversions

**Goal:** make routine money and quantity decisions correctly — which pack is cheaper,
what a "rise of 8%" really means, how much a loan costs, whether a bill adds up.
(For a full monthly budget, see
business-finance.personal-and-household-finance.household-budgeting.zero-based-household-budget.)

## 1. Unit prices: compare like with like
**Unit price = price ÷ quantity**, in the same unit for every option.
- 500 g for £2.40 → £0.48 per 100 g. 750 g for £3.30 → £0.44 per 100 g. Larger pack wins.
- Shelf labels usually show a unit price, but check they use the same unit (per kg vs per
  100 g vs "per each") — they sometimes don't.
- **Multibuys:** "3 for 2" = a third off each item *only if you'd use all three*.
  "Buy one get one half price" = 25% off two items.
- Bigger isn't always cheaper — supermarkets sometimes price large packs higher per unit.
- Value includes waste: a cheaper-per-kg pack you throw half of away costs more.

## 2. Percent change done right
- **Change ÷ original × 100.** 80 → 92: +12/80 = +15%.
- **Successive changes multiply:** +10% then +10% = ×1.1 × 1.1 = ×1.21 (+21%).
  −50% then +50% = ×0.75 — you're down 25%.
- **Reversing:** to undo a 20% cut you need +25% (×0.8 then ×1.25 = 1).
- **Percent vs percentage points:** a mortgage rate going from 4% to 5% is +1 point, a
  25% rise in the rate.
- **Relative vs absolute risk:** "doubles the risk" from 1 in 10,000 to 2 in 10,000 is +1
  in 10,000 in absolute terms. Always ask "out of how many?"

## 3. Interest and borrowing
- **Simple interest** = principal × rate × time. **Compound** = P × (1 + r)ⁿ.
  £1,000 at 5% for 10 years: simple £1,500, compound ≈ £1,629.
- **Monthly rates compound:** 1.5% per month ≈ 19.6% per year (1.015¹² ≈ 1.196), not 18%.
- **APR / AER** (UK) and **APR / APY** (US) put loans and savings on an annual,
  comparable basis; which fees an APR includes depends on national rules, so read the lender's disclosure.
  Compare offers by APR for borrowing and AER/APY for saving.
- **Rule of 72:** debt at 24% doubles in about 3 years if unpaid (exact compounding: 3.2 years).
- Total cost of a loan = monthly payment × number of months − amount borrowed.
  Check this; a lower monthly payment over a longer term usually costs more in total.
(All arithmetic here was recomputed in Python; unit factors checked against NIST SP 811 Appendix B.8: 1 mi = 1.609344 km, 1 imperial gallon = 4.54609 L, 1 US gallon = 3.785412 L, 1 US pint = 473.18 ml, 1 oz = 28.35 g, 1 lb = 453.59 g; 1 UK pint = 1/8 imperial gallon = 568.26 ml.)

## 4. Unit conversion
Use the **multiply-by-one** method: write the conversion as a fraction equal to 1 and
cancel units.
60 mph × (1.609 km / 1 mile) ≈ 96.5 km/h.
Handy approximations: 1 kg ≈ 2.2 lb; 1 lb ≈ 454 g; 1 oz ≈ 28 g; 1 inch = 2.54 cm;
1 foot ≈ 30.5 cm; 1 mile ≈ 1.61 km (5 miles ≈ 8 km); 1 UK pint ≈ 568 ml; 1 US pint ≈ 473 ml;
1 US cup ≈ 237 ml (NIST 236.59 ml; US nutrition labels round to 240 ml); °F = °C × 1.8 + 32 (quick: double and add 30).
Area and volume scale by the square and cube: 1 m² = 10,000 cm², not 100.

## 5. Proportion and scaling
- **Recipes:** scale factor = servings wanted ÷ servings in recipe; multiply every
  ingredient. 4 → 6 servings: ×1.5. Cooking times don't scale linearly — check visually.
- **Unitary method:** find the value for 1, then for the amount needed. 6 m of fabric
  costs £27 → £4.50 per m → 9 m costs £40.50.
- **Ratios:** mix 1:4 concentrate to water → 5 parts total; for 2 L, 400 ml concentrate.

## 6. Reading bills and rates
Check each line: **quantity × unit rate = line cost**, then standing charges, then tax.
Energy example: 250 kWh × 25p = £62.50, + 30 days × 50p standing charge = £15,
subtotal £77.50, + 5% VAT ≈ £81.38 (rates illustrative). Compare meter readings
(estimated "E" vs actual "A") with your own.
Fuel: litres per 100 km vs miles per gallon run in **opposite** directions (lower L/100 km
is better, higher mpg is better); UK and US gallons differ (4.55 L vs 3.79 L).

## Gotchas
- Mixing units in a comparison (per kg vs per 100 g) — normalise first.
- Subtracting a percentage to remove tax: £120 incl. 20% VAT is £100 before tax, not £96.
- "Up to 50% off" means at least one item is 50% off — most aren't.
- Rounding intermediate steps in money sums: keep pence until the end.

## Verify
- [ ] Every comparison uses a unit price in one common unit.
- [ ] Successive percentages multiplied, not added; reversals divided.
- [ ] Loans compared by APR and total amount repayable.
- [ ] Conversions written with units cancelling.
- [ ] A bill's lines recomputed and matched to the total.
