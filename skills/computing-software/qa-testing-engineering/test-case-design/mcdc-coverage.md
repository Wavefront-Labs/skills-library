---
id: computing-software.qa-testing-engineering.test-case-design.mcdc-coverage
name: mcdc-coverage
category: computing-software
field: qa-testing-engineering
product: test-case-design
tags: [mcdc, modified-condition-decision-coverage, white-box-testing, do-178c, iso-26262, structural-coverage]
level: practitioner
status: docs-checked
description: "Achieve MC/DC: show each condition independently affects the decision outcome, derive unique-cause test pairs, and measure it with coverage tools for safety standards."
sources:
  - https://ntrs.nasa.gov/citations/20010057789
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# MC/DC coverage

**Goal:** demonstrate that each condition in a decision independently affects its outcome. NASA's *A Practical Tutorial on Modified Condition/Decision Coverage* (Hayhurst et al.) covers MC/DC for DO-178B level A software.

## Requirements
1. Every decision takes all outcomes (true/false).
2. Every condition takes all outcomes.
3. Each condition is shown to **independently** change the decision while other conditions are held fixed (unique-cause), or with a masking variant (check which your standard accepts) where other conditions may vary but cannot affect the outcome.

## Deriving pairs: `A && (B || C)`
| Test | A | B | C | Result |
|---|---|---|---|---|
| 1 | T | T | F | T |
| 2 | F | T | F | F |  -> pair (1,2) shows A
| 3 | T | F | F | F |  -> pair (1,3) shows B
| 4 | T | F | T | T |  -> pair (3,4) shows C
Four tests vs 8 for all combinations.

## Tools
- Use a coverage tool that reports MC/DC for your language and certification standard; compiler and commercial tool support differs, so check each tool's documentation (not confirmed here).
- Where no tool exists, derive pairs by hand from the truth table.

## Gotchas
- Coupled conditions (`x > 0 && x < 10`, or the same variable twice) cannot always be varied independently; use masking MC/DC and document.
- Short-circuit evaluation affects which conditions are evaluated; tools measure on object/source code differently. Certification needs tool qualification.
- Compilers can restructure decisions; measure on the same build configuration you certify.

## Verify
Tool report shows 100% MC/DC for required modules, with justified exceptions recorded.

## Checked

- Date: 2026-10-28
- Confirmed: the NASA tutorial covers MC/DC for DO-178B level A software; the A && (B || C) pairs were checked against the truth table.
- Removed: DO-178C and ISO 26262 level claims, the CTAL-TTA section reference (ISTQB page unreadable), the n+1 remark, all gcc, LLVM and commercial tool names and flags.

Method: documentation only; no commands were run.
