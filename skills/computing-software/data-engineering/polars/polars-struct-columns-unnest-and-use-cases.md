---
id: computing-software.data-engineering.polars.polars-struct-columns-unnest-and-use-cases
name: polars-struct-columns-unnest-and-use-cases
category: computing-software
field: data-engineering
product: polars
tags: [polars-structs, struct, unnest, value-counts, is-duplicated, rank, expressions]
level: practitioner
status: docs-checked
description: "Work with Polars Struct columns: unnest value_counts, build from dicts, struct.field, rename_fields, duplicate detection and multi-column ranking."
sources:
  - https://docs.pola.rs/user-guide/expressions/structs/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: understand where `Struct` columns come from and use them.

A `Struct` stores multiple fields in one column (think `typing.TypedDict`). Expressions operate on a single series, so `Struct` is how an expression takes multiple columns in or returns multiple columns out.

**value_counts returns a Struct.** Use `unnest` to get ordinary columns:

```python
ratings.select(pl.col("Theatre").value_counts(sort=True)).unnest("Theatre")
```

**From dicts.** Dictionaries become `Struct` when building a Series or DataFrame. Field count, names, types and order are inferred from the first dictionary; later incongruences can give `null` values or errors (the page uses `strict=False` on `pl.Series` to show the nulls).

**Extract and rename:**

```python
rating_series.struct.field("Movie")
rating_series.struct.rename_fields(["Film", "State", "Value"])
result.to_frame().unnest("ratings")   # to see the new field names as columns
```

**Duplicates at multi-column level:**

```python
ratings.filter(pl.struct("Movie", "Theatre").is_duplicated())
```

`is_unique` works the same way.

**Multi-column ranking** (Count first, ties broken by Avg_Rating), per Movie and Theatre:

```python
ratings.with_columns(
    pl.struct("Count", "Avg_Rating")
    .rank("dense", descending=True)
    .over("Movie", "Theatre")
    .alias("Rank")
).filter(pl.struct("Movie", "Theatre").is_duplicated())
```

**Several columns into one custom function** (here the Ackermann function, which the page says cannot be composed from expressions):

```python
values.with_columns(
    pl.struct(["m", "n"])
    .map_elements(lambda s: ack(s["m"], s["n"]), return_dtype=pl.Int64)
    .alias("ack")
)
```

See the user-defined Python functions page for `map_elements` details.

## Checked

2026-11-07. Read in full and compared against this skill: https://docs.pola.rs/user-guide/expressions/structs/. No claims needed correcting. Any parameter, default, class, method or error string not found on those pages was removed.

Method: documentation only; no commands were run.
