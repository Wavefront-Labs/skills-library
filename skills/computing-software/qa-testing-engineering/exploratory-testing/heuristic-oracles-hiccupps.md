---
id: computing-software.qa-testing-engineering.exploratory-testing.heuristic-oracles-hiccupps
name: heuristic-oracles-hiccupps
category: computing-software
field: qa-testing-engineering
product: exploratory-testing
tags: [hiccupps, heuristic-oracles, test-oracles, consistency-heuristics, rapid-software-testing, exploratory-testing]
level: practitioner
status: draft
description: "Recognise problems without a spec using heuristic oracles: FEW HICCUPPS consistency heuristics, and how to cite the oracle when reporting a bug."
sources:
  - https://developsense.com/blog/2012/07/few-hiccupps
  - https://www.satisfice.com/rapid-testing-methodology
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Heuristic oracles (FEW HICCUPPS)

**Goal:** judge whether behaviour is a problem when no exact expected result exists, and explain why credibly. Michael Bolton, Rapid Software Testing.

## The heuristics: a product should be consistent with...
| Oracle | Question | Example finding |
|---|---|---|
| **H**istory | its past versions | export used to include headers, now not |
| **I**mage | the company's image | rude error message, broken branding |
| **C**omparable products | similar products | every other app lets you undo delete |
| **C**laims | docs, marketing, specs, help | help says CSV supports 10k rows, fails at 2k |
| **U**ser desires | what reasonable users want | search ignores typo-tolerance users expect |
| **P**roduct | itself, internally | date format differs between two screens |
| **P**urpose | its explicit and implicit purpose | "save draft" loses attachments |
| **S**tatutes and standards | laws, regulations, standards | missing cookie consent, WCAG failure |
| **F**amiliarity | patterns of known problems | looks like the timezone bug from last year |
| **E**xplainability | being explainable | nobody can say why totals differ |
| **W**orld | the world as we know it | delivery date before order date |

## Using them
- During exploration, run through the list when something feels off.
- In bug reports, **state the oracle**: "Inconsistent with Product: the Orders page shows 12, the dashboard shows 11 for the same filter". This turns opinion into evidence and speeds triage.
- Combine with partial oracles (checks for sanity: totals non-negative, dates ordered).

## Gotchas
- Heuristics can be wrong (the comparable product may be the one with the bug). They point to possible problems; product owners decide.

## Verify
Your bug reports name an oracle; fewer get closed as "works as designed" without discussion.
