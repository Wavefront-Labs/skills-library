---
id: computing-software.qa-testing-engineering.test-case-design.gherkin-given-when-then-scenarios
name: gherkin-given-when-then-scenarios
category: computing-software
field: qa-testing-engineering
product: test-case-design
tags: [bdd, gherkin, given-when-then, test-first, scenario-outline, cucumber, declarative-scenarios]
level: practitioner
status: docs-checked
description: "Write maintainable BDD scenarios in Gherkin: declarative steps, short examples, Background and Scenario Outline used well, and pitfalls from the Cucumber reference."
sources:
  - https://cucumber.io/docs/gherkin/reference/
  - https://cucumber.io/docs/bdd/better-gherkin/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Gherkin: Given-When-Then scenarios

**Goal:** scenarios that read as business specifications and stay stable when the UI changes. Cucumber Gherkin reference.

## Shape
```gherkin
Feature: Loyalty discount
  Gold customers get 10% off baskets of 100 or more.

  Background:
    Given the catalogue has "Coffee" priced 25.00

  Scenario: Gold customer reaches the threshold
    Given Gina is a gold customer
    When she buys 4 "Coffee"
    Then she is charged 90.00

  Scenario Outline: Discount by basket total
    Given a gold customer
    When they spend <total>
    Then the discount is <discount>

    Examples:
      | total  | discount |
      | 100.00 | 10%      |
      | 99.99  | 0%       |
```

## Rules
- **Declarative, not imperative**: describe what, not how. "When Bob logs in", not a list of field entries and button presses. Test: "Will this wording need to change if the implementation does?" If yes, rework it.
- Keep examples short: Cucumber recommends 3-5 steps per example; too many steps lose their value as specification and documentation.
- `Given` sets the initial context (a known state, typically something that happened in the past) and avoids talking about user interaction. `When` is the event or action. `Then` compares actual to expected outcome through an assertion, on something observable (report, user interface, message), not a record buried in a database.
- Keep `Background` short: it holds Given steps that run before each scenario (after any Before hooks); if it is more than 4 lines long, consider moving irrelevant detail into higher-level steps. One Background per Feature or Rule.
- Use Scenario Outline (synonym Scenario Template) to run the same scenario with different values: `<param>` placeholders match Examples column headers, and it runs once per row below the header row.
- `Rule` (Gherkin 6 and later) groups the scenarios that illustrate one business rule.
- A `.feature` file holds a single Feature, and it must be the first primary keyword.
- Tags (`@` prefix) can be placed above Feature to group related features independent of file layout.

## Pitfalls
- Step text is matched to a step definition regardless of keyword, so a Given and a Then with identical text count as duplicates. Word them differently ("my account has a balance of 430" vs "my account should have a balance of 430").
- Putting a colon after a keyword that should not take one makes your tests get ignored.
- Imperative steps tied to UI mechanics ("I press the Submit button") are brittle when the interface changes; put such detail in the step definitions.

## Verify
Ask of each step: will this wording need to change if the implementation does? Rework any step where the answer is yes.

## Checked
Date: 2026-11-08
Read in full: Cucumber "Reference" (Gherkin keywords, Feature, Descriptions, Rule, Example, Steps, Given/When/Then/And/But, Background and its tips, Scenario Outline, Examples, Step Arguments, Spoken Languages) and "Writing better Gherkin" (Describe behaviour, Consider a more declarative style).
Confirmed: the 3-5 steps recommendation; Given as initial context with no user interaction; Then asserts observable output not database records; Background runs before each scenario after Before hooks, more than 4 lines is a smell, one per Feature or Rule; Scenario Outline runs once per Examples row, excluding the header row; Scenario Template synonym; Rule since Gherkin 6; single Feature per file; duplicate-step example; colon warning; the question about wording changing with implementation.
Removed or reworded: "one When per scenario" (not on either page), "Given preferably via API/DB", tags "for selection and traceability", the "wait 5 seconds" and conjunction-step anti-patterns, the opinion that business-unread scenarios should be plain test code, and the invented Verify step. Fixed the sample Scenario Outline whose data (standard customer 5%) contradicted the feature text.
Method: documentation only; no commands were run.
