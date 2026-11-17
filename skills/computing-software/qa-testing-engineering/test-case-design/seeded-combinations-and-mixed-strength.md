---
id: computing-software.qa-testing-engineering.test-case-design.seeded-combinations-and-mixed-strength
name: seeded-combinations-and-mixed-strength
category: computing-software
field: qa-testing-engineering
product: test-case-design
tags: [seeded-combinations, mixed-strength, combinatorial-testing, pict, covering-arrays]
level: practitioner
status: verified
description: "Seed must-have combinations into generated covering arrays and apply mixed strength to risky parameter groups, using PICT submodels and seed files."
sources:
  - https://github.com/microsoft/pict/blob/main/doc/pict.md
  - https://csrc.nist.gov/projects/automated-combinatorial-testing-for-software
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Seeding required combinations and mixed strength

**Goal:** make generated combinatorial suites include the combinations stakeholders insist on, and cover risky interactions more deeply than the rest.

## Seeding (PICT)
Seed file (tab-separated, header = parameter names), rows may be partial:
```text
Browser	OS	Payment
Safari	macOS	ApplePay
Chrome	Windows
```
```bash
pict model.txt /e:seeds.txt
```
PICT includes the seed rows (filling blanks; in a run the partial `Chrome, Windows` row came back completed, and row order was not the seed order) and then adds rows until the requested coverage is reached. Use seeds for: production's top configurations, combinations from past defects, contractually required configs, and existing regression tests you want to keep.

## Mixed strength (PICT submodels)
```text
Browser: Chrome, Firefox, Safari, Edge
OS: Windows, macOS, Linux
Payment: Card, PayPal, ApplePay, Voucher
Currency: GBP, EUR, USD
Locale: en, de, fr, ja

{ Payment, Currency, Locale } @ 3

IF [Browser] = "Safari" THEN [OS] = "macOS";
```
Default order 2 for the whole model (`/o:2`), order 3 inside the submodel. NIST ACTS offers the same idea as "relations" (groups of parameters with their own strength; mixed strength is supported with the IPOG algorithms, per the ACTS user guide; ACTS not run here, needs Java).

## Choosing groups for higher strength
- Parameters feeding the same calculation (price, tax, currency, rounding).
- Groups involved in past interaction defects.
- Safety/security-relevant configuration flags.

## Workflow
1. Base model at t=2 with constraints.
2. Add seeds from usage data and defect history.
3. Raise strength for 1-3 risky groups.
4. Compare suite sizes; justify the extra tests in the test design.

## Gotchas
- Seeds that violate constraints are dropped or cause errors; validate them.
- Too many submodels at high order approach exhaustive size; keep groups small.
- PICT randomisation: use `/r:<seed>` for a reproducible but varied set, or omit for deterministic output.

## Verify
Every seed row is present in the output, coverage check confirms t=3 for the submodel and t=2 overall. For the model above PICT 3.7.4 produced 192 rows and a script confirmed all 48 feasible Payment x Currency x Locale triples and all feasible pairs were covered.
