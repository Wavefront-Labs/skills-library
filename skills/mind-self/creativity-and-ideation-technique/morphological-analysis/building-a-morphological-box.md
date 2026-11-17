---
id: mind-self.creativity-and-ideation-technique.morphological-analysis.building-a-morphological-box
name: building-a-morphological-box
category: mind-self
field: creativity-and-ideation-technique
product: morphological-analysis
tags: [morphological-analysis, morphological-box, zwicky-box, zwicky, general-morphological-analysis, morphological-chart, parameter-decomposition, combinatorial-ideation, forced-combination, cross-consistency-assessment, solution-space, design-space, concept-generation, ideation, creativity, spreadsheet]
level: practitioner
status: draft
description: "Explore a whole solution space with a Zwicky box: pick independent parameters, list options per parameter, generate combinations, prune inconsistent pairs, and pick candidates."
sources: ["Zwicky, Discovery, Invention, Research through the Morphological Approach (1969)", "Ritchey on general morphological analysis and cross-consistency assessment"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Building a morphological box (Zwicky box)

**Goal:** instead of having one idea, map the *space* of possible ideas — every
combination of the key choices — and then find promising combinations you would never
have thought of directly.

## 1. Frame the problem
One sentence on what is being designed or decided: "A weekend activity for a family of
four with a budget under 100." Keep scope tight; a vague frame produces too many
parameters.

## 2. Choose the parameters (the columns)
Parameters are the independent dimensions any solution must specify.
- Aim for **4–7 parameters**. More explodes the space (see the arithmetic below).
- They should be **independent**: changing one shouldn't automatically fix another.
- They should be **essential**: every solution has *some* value for each.
Example: *Location, Activity type, Duration, Who plans, Food arrangement.*

## 3. List options for each parameter (the cells)
3–6 options per parameter, deliberately including at least one unusual one:
- Location: home / park / city centre / another town / *a stranger's farm (WWOOF-style visit)*
- Activity: making / sport / learning / helping others / *swap roles: kids plan*
- Duration: 2 h / half-day / full day / overnight
- Who plans: parents / kids / random draw / a local guide
- Food: cook together / picnic / café / *forage-and-cook*

## 4. Do the arithmetic
The number of combinations is the product of option counts: 5 × 5 × 4 × 4 × 5 = 2,000.
That is why you prune rather than enumerate by hand.

## 5. Prune with cross-consistency
Compare each *pair* of options across parameters and mark impossible or nonsensical
pairs (e.g. "home" + "overnight" is fine; "2 h" + "another town" probably isn't).
Ritchey's general morphological analysis formalises this as a cross-consistency matrix;
a spreadsheet with one cell per pair, marked ✓ / ✗, is enough for personal use. Removing
inconsistent pairs often cuts the space by well over half.

## 6. Generate and pick candidates
- **Forced walk:** pick one cell per column at random (dice, `RAND()` in a spreadsheet)
  several times; describe each result as a concrete idea.
- **Deliberate path:** draw a line through one option per column that you would never
  normally choose, and make it work.
- **Filter:** apply your criteria (cost, fun, effort) to shortlist 3–5 combinations.

## Spreadsheet setup
One column per parameter, options listed down it. For random combinations, use
`=INDEX(B2:B6, RANDBETWEEN(1, 5))` per column (adjust ranges). Formula syntax shown is
standard in Excel, Google Sheets and LibreOffice; check your app if it errors.

## Gotchas
- **Parameters that overlap** ("cost" and "luxury level") create duplicates; merge them.
- **Too many parameters** — the space becomes unusable. Group minor ones under "details".
- **Only listing safe options** — the method's value comes from unusual cells.
- **Treating the box as the answer** — it generates candidates; you still have to evaluate.
- Formal GMA for policy or engineering uses software and facilitated workshops; this is
  the lightweight personal version.

## Verify
- [ ] 4–7 parameters, each independent and essential.
- [ ] Each parameter has 3–6 options, including at least one unusual one.
- [ ] You calculated the total space size.
- [ ] Inconsistent pairs were marked and removed.
- [ ] At least 3 candidate combinations are described as concrete ideas.
- [ ] One candidate surprised you.
