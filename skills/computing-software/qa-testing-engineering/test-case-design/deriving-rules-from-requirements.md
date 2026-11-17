---
id: computing-software.qa-testing-engineering.test-case-design.deriving-rules-from-requirements
name: deriving-rules-from-requirements
category: computing-software
field: qa-testing-engineering
product: test-case-design
tags: [business-rules-extraction, decision-tables, requirements-analysis, rule-discovery, ambiguity-detection]
level: practitioner
status: draft
description: "Extract decision rules from prose requirements and policies: find conditions and actions, spot gaps, overlaps and contradictions, and confirm with the business."
sources:
  - https://www.istqb.org/certifications/certified-tester-advanced-level-test-analyst-ctal-ta-v4-0
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Deriving decision rules from requirements

**Goal:** turn prose like policies and stories into an explicit, complete rule set before testing it.

## Procedure
1. **Mark up the text**: underline conditions (if, when, unless, only, except, for customers who...) and actions (then, receives, is charged, is blocked).
2. **Normalise conditions**: one fact each, with its domain ("customer is gold", "basket >= 100").
3. **Build the table** (Boolean or extended-entry) and fill actions from the text.
4. **Look for problems**:
   - **Gaps**: columns with no action in the text ("what happens to gold customers with international delivery?").
   - **Overlaps/contradictions**: two statements giving different actions for the same column.
   - **Implicit defaults**: "otherwise" behaviour never stated.
   - **Precedence**: when two discounts apply, which wins or do they stack?
5. **Confirm with the business** using the table; it is a much faster review format than prose.
6. Record the final table as the test basis (and suggest adding it to the spec).

## Example
Text: "Gold members get free shipping. Orders over 100 get free shipping, except bulky items." Question raised: gold member with bulky item?

## Gotchas
- Rules scattered across several stories, a policy document and code comments; gather all sources.
- Code may implement a rule the spec never mentions; read code or ask developers for hidden rules.

## Verify
The business owner has signed off the table, including resolutions for every gap and contradiction found.
