---
id: computing-software.qa-testing-engineering.test-case-design.gherkin-scenario-outlines-and-data-tables
name: gherkin-scenario-outlines-and-data-tables
category: computing-software
field: qa-testing-engineering
product: test-case-design
tags: [gherkin-data-tables, scenario-outline, gherkin, bdd, test-first]
level: practitioner
status: docs-checked
description: "Use Gherkin Scenario Outline Examples, Background, Rule and step data tables/doc strings correctly, and choose between them without bloating scenarios."
sources:
  - https://cucumber.io/docs/gherkin/reference/
  - https://cucumber.io/docs/cucumber/api/#data-tables
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Gherkin scenario outlines, backgrounds and data tables

**Goal:** express many examples compactly while scenarios stay readable. Cucumber Gherkin reference.

## Scenario Outline + Examples
```gherkin
Scenario Outline: Shipping fee by membership
  Given a <tier> member with a basket of <amount>
  When they check out
  Then the shipping fee is <fee>

  Examples: boundary of free shipping
    | tier   | amount | fee  |
    | gold   | 49.99  | 4.99 |
    | gold   | 50.00  | 0.00 |
    | silver | 50.00  | 4.99 |
```
Each row runs as a separate scenario. Multiple `Examples:` blocks can be tagged (`@smoke`) and named to group by intent.

## Step data table (input structure)
```gherkin
Given the catalogue contains:
  | sku  | price | stock |
  | A-1  | 10.00 | 5     |
  | B-2  | 20.00 | 0     |
```
Cucumber passes a table to the step definition as a `DataTable` object, or as a collection such as `List<Map<String, String>>` (Java; see the Cucumber step-definition docs for other languages).

## Doc strings
Triple-quoted block for a JSON body or email text: `"""json ... """`.

## Background and Rule
`Background` adds context that runs before each scenario; keep it short, only context every reader must know. `Rule:` (Gherkin 6 and later) groups scenarios illustrating one business rule.

## Choosing
| Need | Use |
|---|---|
| Same flow, varying values | Scenario Outline |
| Setting up structured data in one step | data table |
| Large payload | doc string |
| Shared context for all scenarios | Background (short) |

## Gotchas
- Outlines with dozens of rows belong in a unit-level parametrized test; keep a handful of key examples.
- Do not put expected outcomes for different behaviours in one outline; split by rule.
- Angle-bracket placeholders (`<tier>`) in steps are filled from the Examples header row, as in the Gherkin reference's `Given there are <start> cucumbers` example.

## Verify
Each Examples row has a distinct reason to exist (comment or Examples name), and the runner reports one result per row.

## Checked

2026-10-28 Confirmed against: Gherkin reference (Scenario Outline runs once per Examples row, `<placeholder>` syntax, Rule as of Gherkin 6, doc strings, data tables); Cucumber API page (tags on Examples blocks, `DataTable` and `List<Map<String, String>>` step parameters). Removed or generalised: the `asMaps()`, `@DataTableType`, `hashes()` and Reqnroll `CreateSet<T>()` names, the 1-3 step Background limit, the 3-6 example count, the claim about placeholders in doc strings and tags, and Rule having its own Background (all not found in the fetched pages).

Method: documentation only; no commands were run.
