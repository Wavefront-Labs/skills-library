---
id: computing-software.qa-testing-engineering.test-case-design.decision-table-completeness-and-infeasible-rules
name: decision-table-completeness-and-infeasible-rules
category: computing-software
field: qa-testing-engineering
product: test-case-design
tags: [infeasible-rules, decision-table-completeness, decision-table-testing, requirements-review, test-design]
level: practitioner
status: verified
description: "Check a decision table for completeness, consistency and redundancy, identify infeasible combinations, and turn gaps into specification questions."
sources:
  - https://www.istqb.org/certifications/certified-tester-foundation-level
  - https://glossary.istqb.org/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Infeasible combinations and table completeness checks

**Goal:** a decision table is a requirements-review tool: gaps and contradictions are defects found before any code runs. CTFL v4.0 section 4.2.3 (limited- and extended-entry tables; `-` means irrelevant, `N/A` means infeasible; coverage items are the feasible columns).

## Completeness check
- Full table for n boolean conditions has 2^n columns; for extended entries, the product of the number of values per condition.
- With collapsed columns, count each "-" (don't care) as covering all values: sum of covered combinations must equal the full count.
- Missing combinations -> ask: what happens here?

## Consistency and redundancy
- **Contradiction:** two rules cover the same combination with different actions -> spec defect.
- **Redundancy:** two rules cover the same combination with the same actions -> merge.
- Check by expanding all "-" entries and looking for duplicates.

## Infeasible combinations
Combinations that cannot occur: "age < 18" and "age > 65" both true; "payment = cash" and "card expired". Mark them **infeasible** with the reason; do not write test cases for them, but do test that the system rejects them if they can be forced via API or data import.

## Script it for larger tables
```python
import itertools
conditions = {"member": [True, False], "coupon": [True, False], "total": ["<50", ">=50"]}
rules = [  # (condition values, action); None = don't care
    ({"member": True, "coupon": None, "total": ">=50"}, "free-ship"),
    ({"member": False, "coupon": True, "total": None}, "10pct"),
]
for combo in itertools.product(*conditions.values()):
    c = dict(zip(conditions, combo))
    hits = [a for r, a in rules if all(v is None or c[k] == v for k, v in r.items())]
    if len(hits) != 1:
        print(c, "->", hits or "MISSING")
```

## Gotchas
- "Else" columns hide missing analysis; expand them and check each hidden combination.
- Infeasible today may be feasible after a data migration or API change; re-check on change.

## Verify
The sample script reports four MISSING combinations (e.g. non-member, no coupon) when run, which is the intended output. Table annotated with: covered count = full count, no contradictions, each infeasible column justified, open questions logged.
