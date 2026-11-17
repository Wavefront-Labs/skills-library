---
id: computing-software.cloud-infrastructure-engineering.open-policy-agent.data-filtering-with-partial-evaluation
name: data-filtering-with-partial-evaluation
category: computing-software
field: cloud-infrastructure-engineering
product: open-policy-agent
tags: [data-filtering, partial-evaluation, unknowns, compile-annotation, sql-where]
level: sme
status: docs-checked
description: "Turn authorisation into search with OPA partial evaluation: declare unknowns in a compile metadata annotation and derive filters for SQL WHERE clauses."
sources:
  - https://www.openpolicyagent.org/docs/filtering
  - https://www.openpolicyagent.org/docs/filtering/partial-evaluation
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: answer "which records may this user see" instead of "may this user see this record".

Evaluation asks whether a subject can do an action to a resource and returns allow or deny. Search asks which values of an unknown produce allow, and returns filters for application data. Examples: whose salaries can a Director see, who may approve payments over $10,000.

Flow: the application sends user context to OPA, OPA returns filters, and the application builds its query (for example `SELECT ... WHERE <filters>`) so the database returns only permitted rows. In the docs' example a Director of Engineering sees the Engineering rows of an `employees` table.

OPA derives the filters by partial evaluation: known values are evaluated away and expressions touching unknowns are kept as conditions. Declare the unknowns with a `compile` metadata annotation:

```rego
# METADATA
# scope: package
# compile:
#   unknowns:
#     - input.users
#     - input.products
package filters

user := input.user

include if {
    input.users.name == user
    input.budget != "low"
}
```

With input `{"user": "dana", "budget": "high"}`, `user` is known ("dana") while `input.users.name` is unknown, so `input.users.name == user` stays as a condition. `input.budget != "low"` has only known parts and is true, so it adds no condition. With budget `low` the docs show that this rule body is abandoned because the known expression is false. Each `include` rule contributes one alternative; rules combine as OR, statements inside a rule as AND.

The docs walk this step by step and show how the result is converted to SQL, Lucene and the UCAST syntax.

Check: run the walkthrough input and confirm conditions on the unknown references remain rather than evaluating to true or false.

## Checked

2026-11-04. Confirmed against the OPA docs Data Filtering overview and Evaluating a Data Filter Policy: evaluation versus search, the application/OPA/database flow, the Director example, the compile metadata annotation with unknowns, known values evaluated away, rule bodies combined with OR and expressions within a body with AND. Fixed the walkthrough input: with budget low the single include rule shown here would be abandoned (the docs use a second rule for the low case), so the input is now budget high. The SQL, Lucene and UCAST conversion pages exist in the same section (filtering/lucene, filtering/ucast-syntax).

Method: documentation only; no commands were run.
