---
id: computing-software.data-engineering.polars.polars-column-selectors
name: polars-column-selectors
category: computing-software
field: data-engineering
product: polars
tags: [polars, polars-expression-expansion, selectors, cs, set-operations, as-expr, expand-selector, is-selector]
level: practitioner
status: docs-checked
description: "Select Polars columns with the selectors submodule: dtype and name-pattern selectors, set operators, as_expr to resolve the tilde ambiguity, and debugging helpers."
sources:
  - https://docs.pola.rs/user-guide/expressions/expression-expansion/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Column selectors (polars.selectors)

Goal: pick columns by dtype, name pattern or position and combine them with set logic. Python only: not available in Rust yet (Polars issue #10594).

```python
import polars.selectors as cs
df.select(cs.string() | cs.ends_with("_high"))
```

## Set operations

| Operator | Operation |
| --- | --- |
| `A | B` | union |
| `A & B` | intersection |
| `A - B` | difference |
| `A ^ B` | symmetric difference |
| `~A` | complement |

```python
df.select(cs.contains("_") - cs.string())          # non-string columns with an underscore
df.select((cs.contains("_") - cs.string()) / eur_usd_rate)   # expression methods chain on selectors
```

## The tilde ambiguity

`~` on a selector means complement; on an expression it means Boolean negation. To negate the Boolean columns `has_partner`, `has_kids`, `has_tattoos`, convert with `as_expr`; otherwise `~cs.starts_with("has_")` selects the other columns:

```python
wrong = people.select((~cs.starts_with("has_")).name.prefix("not_"))
right = people.select((~cs.starts_with("has_").as_expr()).name.prefix("not_"))
```

`as_expr` is a method on selectors, not a function of the submodule.

## Debugging

- `cs.is_selector(obj)` tells you whether you hold a selector or an expression. The page's example `cs.is_selector(~cs.starts_with("has_").as_expr())` checks the converted object.
- `cs.expand_selector(people, cs.starts_with("has_"))` shows which columns a selector expands to for a frame or schema.

## Reference

- Dtype selectors: `binary`, `boolean`, `by_dtype`, `categorical`, `date`, `datetime` (optionally time unit/zone), `decimal`, `duration`, `float`, `integer`, `numeric` (integers, floats, `Decimal`), `signed_integer`, `string`, `temporal` (`Date`, `Datetime`, `Duration`), `time`, `unsigned_integer`.
- Name selectors: `alpha`, `alphanumeric`, `by_name`, `contains`, `digit`, `ends_with`, `matches` (regex), `starts_with`.
- Positional: `all`, `by_index`, `first`, `last`.
- Misc: `exclude`, `expand_selector`, `is_selector`.

## Checked
2026-11-07: every claim compared with the cited Polars user guide page(s). No unconfirmed claims found.

Method: documentation only; no commands were run.
