---
id: computing-software.qa-testing-engineering.test-case-design.persona-based-scenario-design
name: persona-based-scenario-design
category: computing-software
field: qa-testing-engineering
product: test-case-design
tags: [persona-testing, scenario-testing, use-case-testing, user-centred-testing, exploratory-testing]
level: practitioner
status: gated
description: "Design test scenarios from personas: build test personas with goals, skills and constraints, and derive realistic scenarios and data from them."
sources:
  - https://www.nngroup.com/articles/persona/
  - https://www.kaner.com/pdfs/ScenarioIntroVer4.pdf
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Persona-based scenario design

**Goal:** tests that reflect how different real people use the product, revealing usability, accessibility and workflow defects that feature-by-feature tests miss.

## Build test personas
Start from UX research personas if they exist; otherwise from support tickets, analytics and sales input. For each:
- Name and role, goals and motivation.
- Skill and familiarity (first-time vs power user), devices and connectivity.
- Constraints: accessibility needs (screen reader, low vision, motor), language, time pressure, interruptions.
- Data profile: account age, volume of data, edge data (long names, multiple addresses, foreign characters).
- Misuse potential: impatient double-clicker, fraudster, curious tinkerer.

## Example
| Persona | Scenario |
|---|---|
| "Priya", accountant, keyboard-only, 2,000 invoices | bulk-export a year's invoices using only keyboard; filters and pagination with large data |
| "Tom", first-time mobile user on 3G | sign up and buy in one session, with an interruption by a phone call |
| "Ahmed", Arabic RTL locale | complete onboarding; check layout mirroring and mixed-direction text |
| "Eve", attacker | tamper with price parameter during checkout |

## Deriving tests
1. For each persona, write 2-4 goal-based scenarios (Kaner: a story that is credible, motivating, complex and easy to evaluate (gated: unconfirmed, source is paywalled or blocked)).
2. Create persona test accounts with matching data and settings; reuse them across sessions.
3. Run as exploratory charters or scripted end-to-end tests; note friction, not only failures.

## Gotchas
- Personas based on assumptions repeat team biases; validate against data.
- Too many personas dilute effort; a few well-chosen ones cover most risk.
- Persona scenarios complement, not replace, systematic techniques.

## Verify
Each persona has documented attributes, at least two scenarios with results, and persona accounts exist in the test environment.

## Checked

2026-10-28. Confirmed: NN/g persona article: a persona is a fictional yet realistic description of a typical or target user. Gated: the Kaner scenario criteria could not be matched in the fetched PDF text. Removed: The "4-6 personas" figure.

Method: documentation only; no commands were run.
