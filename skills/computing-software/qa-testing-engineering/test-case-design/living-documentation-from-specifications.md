---
id: computing-software.qa-testing-engineering.test-case-design.living-documentation-from-specifications
name: living-documentation-from-specifications
category: computing-software
field: qa-testing-engineering
product: test-case-design
tags: [living-documentation, bdd, specification-by-example, test-first, cucumber-reports]
level: practitioner
status: docs-checked
description: "Publish living documentation from executable specifications: organise features, generate reports from Cucumber messages, and keep docs trustworthy."
sources:
  - https://cucumber.io/docs/bdd/
  - https://github.com/cucumber/html-formatter
  - https://gojko.net/books/specification-by-example/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Living documentation from executable specifications

**Goal:** documentation that cannot drift from the system because it is the test suite. Adzic, *Specification by Example*.

## Organise for readers
- Folders by business capability (`features/billing/`, `features/onboarding/`), not by screen or sprint.
- Each feature file starts with a short narrative and business rules (`Rule:` keyword, Gherkin 6 and later).
- Scenarios titled as rules or examples ("Gold members get free shipping over 50"), not test IDs.

## Generate the docs
- Cucumber JVM: `@CucumberOptions(plugin = {"pretty", "html:target/cucumber.html"})` writes an HTML report. The cucumber/html-formatter repository has java, javascript, ruby and dotnet packages.
- Publish to a stable URL per build (CI artifact, Pages site), linked from the product wiki.

## Keep it trustworthy
1. Docs show pass/fail/pending per scenario; failing docs are visible bugs.
2. Pending/undefined scenarios mark agreed-but-unbuilt behaviour; review them each sprint.
3. Product owner reviews new scenarios in the PR (they are the spec).
4. Delete scenarios for removed behaviour; never let them sit `@ignore`d.

## Gotchas
- UI-step scenarios ("click #submit") make useless docs; write declaratively.
- A thousand near-duplicate scenarios are unreadable; one or two key examples per rule, the rest in unit tests.
- Docs generated from a branch can mislead; publish from main/release builds.

## Verify
A product owner can find the current rule for a capability in the published docs within a minute, and it shows a green last run.

## Checked

2026-10-28 Confirmed against: Cucumber API page (`html:target/cucumber.html` plugin option), Gherkin reference (Rule as of Gherkin 6), cucumber/html-formatter repository (language folders), Cucumber BDD page (executable specification), Gojko Adzic's book page. Removed or generalised: the `--plugin` and `--format` command-line spellings, the NDJSON message-format claim, and the Reqnroll/SpecFlow/Serenity line (not in the fetched pages).

Method: documentation only; no commands were run.
