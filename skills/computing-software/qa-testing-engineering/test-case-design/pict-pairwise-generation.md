---
id: computing-software.qa-testing-engineering.test-case-design.pict-pairwise-generation
name: pict-pairwise-generation
category: computing-software
field: qa-testing-engineering
product: test-case-design
tags: [pict, all-pairs-generation, pairwise-testing, combinatorial-testing, test-generation, allpairspy]
level: practitioner
status: verified
description: "Generate pairwise (and n-wise) test sets with Microsoft PICT: model files, constraints, sub-models, seeding required combinations, and negative values."
sources:
  - https://github.com/microsoft/pict/blob/main/doc/pict.md
  - https://github.com/thombashi/allpairspy
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Pairwise generation with PICT

**Goal:** a small test set covering every pair of parameter values. PICT is free, CLI-based and widely used.

## Model file (`checkout.txt`)
```
Browser:  Chrome, Firefox, Safari, Edge
OS:       Windows, macOS, iOS, Android
Payment:  Card, PayPal, ApplePay, Invoice
Locale:   en-GB, de-DE, ja-JP
Shipping: Standard, Express

IF [OS] = "iOS" THEN [Browser] = "Safari";
IF [Payment] = "ApplePay" THEN [OS] IN {"macOS", "iOS"} AND [Browser] = "Safari";
```
```bash
pict checkout.txt                # pairwise (default /o:2)
pict checkout.txt /o:3           # 3-wise
pict checkout.txt /r:42          # randomise with seed (reproducible variation; /r alone picks and prints a seed)
pict checkout.txt /e:seed.txt    # force rows you must have (seeding)
pict checkout.txt > cases.tsv    # tab-separated output for data-driven tests
```
Full combinations here = 4x4x4x3x2 = 384; with the two constraints PICT 3.7.4 generated 21 rows at the default order 2 (also 21 without constraints) and 61 rows at `/o:3`. Run it from PowerShell or cmd on Windows; Git Bash rewrites `/o:3` as a path unless `MSYS_NO_PATHCONV=1` is set. Without `/r` output is deterministic; `/r:42` printed `Used seed: 42` and gave identical output on repeat.

## Useful features
- **Negative values**: prefix with `~` (`Payment: Card, ~ExpiredCard`); PICT puts at most one negative value per row, avoiding masking (checked: every row had at most one `~` value).
- **Weights**: `Chrome (10)` to prefer common values.
- **Sub-models**: `{ Payment, Currency, Locale } @ 3` to cover a tighter interaction among some parameters. The order cannot exceed the number of parameters in the sub-model (`{ Browser, OS } @ 3` is rejected: "Order of a submodel cannot be larger than number of involved parameters").
- **Aliases**: `Windows | Win11` treated as one value (names rotate across rows; only the first name counts in constraints).

## Python alternative
`allpairspy` (`AllPairs([...params], filter_func=...)`) when you want generation in test code (2.5.1 gave 18 rows for the unconstrained model, 17 with a filter).

## Gotchas
- Pairwise only guarantees pairs; known 3-way risky interactions need sub-models or seeded rows.
- Missing constraints produce impossible rows; review output before automating.

## Verify
Generated file reviewed for impossible rows, committed with the model, and feeding a parametrised test.
