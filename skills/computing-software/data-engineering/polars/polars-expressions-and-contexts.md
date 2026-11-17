---
id: computing-software.data-engineering.polars.polars-expressions-and-contexts
name: polars-expressions-and-contexts
category: computing-software
field: data-engineering
product: polars
tags: [polars, polars-contexts, expressions, select, with-columns, filter, group-by, broadcasting]
level: practitioner
status: docs-checked
description: "Use Polars expressions inside the select, with_columns, filter and group_by contexts, including broadcasting rules, named expressions and multi-key grouping."
sources:
  - https://docs.pola.rs/user-guide/concepts/expressions-and-contexts/
  - https://docs.pola.rs/user-guide/getting-started/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Expressions and contexts: select, with_columns, filter, group_by

Goal: write a lazy expression once and evaluate it in the right context.

An expression is a lazy representation of a data transformation; nothing computes until a context runs it. The same expression can give different results in different contexts.

```python
bmi_expr = pl.col("weight") / (pl.col("height") ** 2)
print(bmi_expr)   # just the abstract expression
```

## The four contexts

- `select`: applies expressions over columns; the result has only the columns you produce. Outputs must all be the same length, or be scalars (broadcast). Literals broadcast too.

```python
df.select(bmi=bmi_expr, avg_bmi=bmi_expr.mean(), ideal_max_bmi=25)
df.select(deviation=(bmi_expr - bmi_expr.mean()) / bmi_expr.std())
```

- `with_columns`: like `select` but keeps the original columns and adds the new ones. Expressions must match the original column length.
- `filter`: keeps rows where Boolean expressions are true. Several predicates can be passed as separate arguments instead of joining with `&`:

```python
df.filter(pl.col("birthdate").is_between(date(1982, 12, 31), date(1996, 1, 1)),
          pl.col("height") > 1.7)
```

- `group_by`: groups by the unique values of one or more expressions, then `agg` applies aggregating expressions per group (groups may differ in length). Naming only a column in `agg` returns that column's groups as lists.

```python
df.group_by((pl.col("birthdate").dt.year() // 10 * 10).alias("decade"),
            maintain_order=True).agg(pl.len().alias("sample_size"))
```

## Notes

- Keyword arguments (`bmi=...`) name results without `alias`; `select` and `group_by` accept them too.
- `maintain_order=True` keeps groups in original order but slows grouping; getting started uses it for reproducible examples.
- Result columns of `group_by(...).agg(...)`: one per grouping expression, then the aggregation outputs.
- Related contexts: `group_by_dynamic` and `rolling`, plus List and SQL contexts (covered elsewhere).
- Separate expressions in a context run in parallel; expansion also parallelises.

## Checked

2026-11-07. Read in full and compared against this skill: https://docs.pola.rs/user-guide/concepts/expressions-and-contexts/; https://docs.pola.rs/user-guide/getting-started/. No claims needed correcting. Any parameter, default, class, method or error string not found on those pages was removed.

Method: documentation only; no commands were run.
