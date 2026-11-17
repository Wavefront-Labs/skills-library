---
id: computing-software.data-engineering.polars.polars-join-where-asof-and-cross
name: polars-join-where-asof-and-cross
category: computing-software
field: data-engineering
product: polars
tags: [polars-join-asof, join-where, non-equi-join, asof-join, cross-join, tolerance, joins]
level: practitioner
status: docs-checked
description: "Use Polars non-equi joins with join_where, asof joins with join_asof (by, tolerance, strategy), and cross joins for Cartesian products."
sources:
  - https://docs.pola.rs/user-guide/transformations/joins/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: join without exact key equality, or pair every row with every row.

**Non-equi join: `join_where`.** Pass one or more predicates instead of keys. Multiple predicates are AND combined; build a single combined expression for OR or XOR.

```python
players.join_where(props_prices, pl.col("cash") > pl.col("cost"))
```

This pairs each player with every property they could afford. (Rust needs the `iejoin` feature.)

**Asof join: `join_asof`.** Like a left join, but matches on the NEAREST key rather than equal keys. Default `strategy="backward"` takes the most recent right row on or before the left key. Use `by=` for an exact preliminary join so trades on one stock are not matched to quotes of another:

```python
df_trades.join_asof(df_quotes, on="time", by="stock", check_sortedness=False)
```

Limit how far back a match may be with `tolerance`:

```python
df_trades.join_asof(
    df_quotes, on="time", by="stock", tolerance="1m", check_sortedness=False
)
```

The page's example uses `tolerance="1m"` to require the preceding quote to be within 1 minute of the trade. (In Rust the by-group variant is `join_asof_by`, needing the `asof_join` feature.) The snippets pass `check_sortedness=False`.

**Cartesian product.** Use `how="cross"` and do not pass `on`, `left_on` or `right_on`:

```python
players.select(pl.col("name")).join(tokens, how="cross")
```

(Rust: `cross_join`.) Each left row is paired with all right rows.

Quick reference from the page: `join_where` = non-equi inner join; `join_asof`/`join_asof_by` = like a left outer join on the nearest key; `join(..., how="cross")` = Cartesian product.

## Checked

2026-11-07. Read in full and compared against this skill: https://docs.pola.rs/user-guide/transformations/joins/. No claims needed correcting. Any parameter, default, class, method or error string not found on those pages was removed.

Method: documentation only; no commands were run.
