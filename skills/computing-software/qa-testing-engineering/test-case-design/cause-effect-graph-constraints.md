---
id: computing-software.qa-testing-engineering.test-case-design.cause-effect-graph-constraints
name: cause-effect-graph-constraints
category: computing-software
field: qa-testing-engineering
product: test-case-design
tags: [cause-effect-constraints, cause-effect-graphing, decision-table-testing, black-box-testing, test-design]
level: practitioner
status: draft
description: "Model cause-effect graph constraints (exclusive, inclusive, one-and-only-one, requires, masks) to prune impossible cause combinations before building a decision table."
sources:
  - https://glossary.istqb.org/
  - https://www.istqb.org/certifications/certified-tester-foundation-level
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Cause-effect graph constraints

**Goal:** derive a decision table only from combinations that can actually occur. Cause-effect graphing per Myers, *The Art of Software Testing*.

## Elements
- **Causes** (conditions, boolean inputs) C1..Cn, **effects** (outputs/actions) E1..Em.
- Logical links: identity, NOT, AND, OR between causes and effects, possibly via intermediate nodes.

## Constraints between causes
| Symbol | Name | Meaning |
|---|---|---|
| E | Exclusive | at most one of the causes true |
| I | Inclusive | at least one true |
| O | One and only one | exactly one true |
| R | Requires | if C1 true then C2 must be true |

Constraint between effects:
| M | Masks | if E1 occurs, E2 is forced false |

## Example: file update command
C1 = first char is "A", C2 = first char is "B" (exclusive, E), C3 = second char is a digit.
E1 = update file if (C1 OR C2) AND C3; E2 = message X12 if NOT(C1 OR C2); E3 = message X13 if NOT C3.
Without constraints: 8 combinations; with E between C1 and C2, the row C1=T, C2=T is impossible, leaving 6.

## Procedure
1. Extract causes and effects from the spec; number them.
2. Draw the graph with logic and constraints (or write as boolean expressions).
3. Generate the decision table by tracing back from each effect, skipping combinations that violate constraints.
4. Review impossible combinations with the analyst: is it impossible by physics/data, or merely unhandled?

## Gotchas
- A constraint you assume but the system does not enforce (UI prevents it, API does not) is a test idea, not a pruning rule; test that the API rejects it.
- Large graphs are hard to maintain; use them for complex logic only and keep the table as the living artefact.

## Verify
Each pruned combination is justified by a named constraint traceable to the spec or data model.
