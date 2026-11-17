---
id: computing-software.software-engineering.fsharp.query-expressions
name: query-expressions
category: computing-software
field: software-engineering
product: fsharp
tags: [fsharp, query-expressions, fsharp-ce, query-builder, linq]
level: practitioner
status: docs-checked
description: "Use the query builder with for, where, select, sortBy and join over IQueryable or in-memory sequences."
sources:
  - https://learn.microsoft.com/en-us/dotnet/fsharp/language-reference/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Query expressions
**Goal:** write LINQ-style queries in F# syntax.

```fsharp
let q =
    query {
        for p in people do
        where (p.Age >= 18)
        sortByDescending p.Age
        select p.Name
        take 10
    }

let total = query { for o in orders do sumBy o.Total }
let first = query { for p in people do where (p.Id = 1); headOrDefault }
let joined =
    query {
        for o in orders do
        join c in customers on (o.CustomerId = c.Id)
        select (c.Name, o.Total)
    }
```
- Operators include `where`, `select`, `sortBy`, `sortByDescending`, `thenBy`, `groupBy`, `join`, `leftOuterJoin`, `count`, `exists`, `head`, `headOrDefault`, `take`, `skip`, `distinct`, `sumBy`.
- Queries work over `IQueryable<T>` and `IEnumerable<T>`; for database queries only constructs that translate to SQL are allowed (the page notes that arbitrary function calls are not).

## Gotchas
- Do not call arbitrary F# functions inside a query that targets a database.

## Self-check
Run the query over an in-memory list and confirm the order and count.

## Checked
2026-11-03. Confirmed against the Query expressions language-reference page (operator table including headOrDefault, thenBy, sumBy, join, IQueryable/IEnumerable, no function calls in SQL queries). Removed: the EF Core runtime-failure claim, the in-memory seq claim and the parentheses claim.
Method: documentation only; no commands were run.
