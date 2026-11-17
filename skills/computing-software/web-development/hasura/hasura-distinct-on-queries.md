---
id: computing-software.web-development.hasura.hasura-distinct-on-queries
name: hasura-distinct-on-queries
category: computing-software
field: web-development
product: hasura
tags: [hasura, queries, distinct-on, order-by, postgres]
level: practitioner
status: docs-checked
description: "Return one row per distinct column value with distinct_on, pairing it with order_by to pick the top row per group, such as highest salary per department."
sources:
  - https://github.com/hasura/graphql-engine/blob/master/docs/docs/queries/postgres/distinct-queries.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: unique values or top-per-group results.

`distinct_on` takes an array of the table's select-column enum values (for `employees` it is `employees_select_column`: id, name, department, salary).

Example, highest salary per department:

```graphql
query {
  employees(
    distinct_on: [department]
    order_by: [{ department: asc }, { salary: desc }]
  ) { id name department salary }
}
```
Rules from the docs:
- Use `order_by` with `distinct_on` for predictable results; otherwise any arbitrary row with a distinct value of the column may be returned.
- The `distinct_on` column needs to be the first column in the `order_by` expression.
- The complete argument specification is in the API reference (`distinctonexp`).

## Checked

2026-11-04. Confirmed against the cited pages: distinct-queries page: argument type, employees example, order_by recommendation and first-column rule. Removed or corrected: the claim about combining with where/limit, the error-on-wrong-order claim and the Verify step.

Method: documentation only; no commands were run.
