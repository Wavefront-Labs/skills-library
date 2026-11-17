---
id: creative-arts.film-live-action.directing.movie-magic-budgeting-globals-subgroups-and-versions
name: movie-magic-budgeting-globals-subgroups-and-versions
category: creative-arts
field: film-live-action
product: directing
tags: [directing, film-live-action, globals, budget-globals, budget-variables, subgroups, budget-currency, budget-locations, budget-comparison, budget-versions, budget-variance, fringes, movie-magic-budgeting]
level: practitioner
status: draft
description: "Build a flexible budget in Movie Magic Budgeting: globals as variables, fringes, groups and subgroups for locations or currencies, saved budget versions, and comparing versions for variance."
sources:
  - "https://www.ep.com/movie-magic-budgeting/ (Entertainment Partners - Movie Magic Budgeting documentation)"
  - "Deke Simon, Film and Video Budgets (budget structure and versions)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Movie Magic Budgeting: globals, subgroups and versions

**Goal:** a budget where changing one assumption (weeks of shoot, exchange rate,
location) updates everything, and every version is comparable.

## 1. Globals (variables)
Define **globals** for every repeated quantity: `PREP` (weeks), `SHOOT` (weeks or days),
`WRAP`, `POST`, `DAYS`, `NIGHTS`, `LOCS`. Use them in detail lines instead of typing numbers
(`Amount: SHOOT, Units: Weeks, Rate: 2,500`). Change `SHOOT` from 6 to 7 and every
crew line updates. Name globals clearly; document them on the budget's notes page.

## 2. Fringes
Set **fringes** (payroll taxes, pension & health, holiday pay, agency fees) as
percentages or flat amounts with caps (cutoffs) and apply them per line or per account.
Union fringes differ (DGA, SAG-AFTRA, IATSE, Teamsters); non-union payroll tax by
jurisdiction. Fringe totals appear on the top sheet per account.

## 3. Groups and subgroups
- **Groups** tag lines across accounts (e.g. "Second Unit", "VFX-heavy sequence",
  "Location: Morocco") so you can include/exclude or report them - useful for "what if we
  cut the second unit?".
- **Subgroups** (in recent MMB versions) let a budget carry parallel versions of lines
  for different **locations or currencies** - e.g. the same crew lines priced for
  Budapest and London, toggled for comparison.
- **Currencies**: define each currency with an exchange rate; lines can be entered in
  local currency and totals shown in the base currency.

## 4. Versions and comparison
- Save each significant iteration as a **new file** or version with a clear name
  (`Title_Budget_v07_Draft3Script_7wk_2026-10-16`).
- Use MMB's compare feature (or export both to Excel/CSV) to produce a **variance
  report** by account: old, new, difference, % - with a note per material change
  ("shoot +1 week: +$212k").
- Keep the **locked budget** (financing/approved) as the baseline for cost reports
  during production.

## Gotchas
- Typed numbers instead of globals - a schedule change needs 200 manual edits.
- Fringes not applied to new lines.
- Exchange rates left stale in multi-currency budgets.
- No locked baseline; cost reports compare against a moving target.

## Verify
- [ ] Globals defined and used in all duration-driven lines.
- [ ] Fringes set per union/jurisdiction and applied.
- [ ] Groups/subgroups used for scenarios, currencies with current rates.
- [ ] Named versions saved; variance report against the locked budget.
