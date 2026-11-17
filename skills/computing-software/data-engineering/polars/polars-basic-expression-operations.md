---
id: computing-software.data-engineering.polars.polars-basic-expression-operations
name: polars-basic-expression-operations
category: computing-software
field: data-engineering
product: polars
tags: [polars, polars-basic-operations, arithmetic, comparison, boolean-operators, bitwise, null-propagation, named-operators]
level: practitioner
status: docs-checked
description: "Do arithmetic, comparisons, Boolean and bitwise operations on Polars expressions, with named method equivalents and the null and keyword gotchas."
sources:
  - https://docs.pola.rs/user-guide/expressions/basic-operations/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Basic operations on Polars expressions

Goal: use native operators (or their named methods) on columns inside any context.

## Arithmetic

Works between series of the same length or between a series and a literal; literals are broadcast. If an operand is `null`, the result is `null`.

```python
df.select(
    (pl.col("nrs") + 5).alias("nrs + 5"),
    (pl.col("nrs") * pl.col("random")).alias("nrs * random"),
    (pl.col("nrs") / pl.col("random")).alias("nrs / random"),
    (pl.col("nrs") ** 2).alias("nrs ** 2"),
    (pl.col("nrs") % 3).alias("nrs % 3"),
)
```

Python named equivalents: `add`, `sub`, `mul`, `truediv`, `pow`, `mod`. The page checks them with `result.equals(result_named_operators)`.

## Comparisons

Overloaded operators or named functions: `>` `gt`, `>=` `ge`, `<` `lt`, `<=` `le`, `!=` `ne`, `==` `eq`.

```python
df.select((pl.col("nrs") > 1).alias("nrs > 1"), (pl.col("random") < 0.2).alias("random < .2"))
```

## Boolean and bitwise

Use `&`, `|`, `~` for and, or, not, or the functions of the same name. In Python the named methods are `and_`, `or_`, `not_`, because `and`, `or`, `not` are reserved keywords. The keywords cannot be overloaded: they evaluate operands through `__bool__` (truthy/falsy), so the bitwise operators are overloaded instead.

```python
((~pl.col("nrs").is_null()) & (pl.col("groups") == "A")).alias("number not null and group A")
((pl.col("random") < 0.5) | (pl.col("groups") == "B"))
pl.col("nrs").is_null().not_().and_(pl.col("groups") == "A")
```

The same `&`, `|`, `~` work as bitwise operations on integers, plus `^` / `xor`:

```python
df.select(pl.col("nrs"), (pl.col("nrs") & 6), (pl.col("nrs") | 6), (~pl.col("nrs")), (pl.col("nrs") ^ 6))
```

## Gotchas

- A `null` arithmetic operand yields `null`.
- Do not use Python `and`/`or`/`not` on expressions; use `&`, `|`, `~` or the named methods.
- For counting unique values and when/then/otherwise see the polars-count-unique-and-conditionals skill.

## Checked
2026-11-07: every claim compared with the cited Polars user guide page(s). No unconfirmed claims found.

Method: documentation only; no commands were run.
