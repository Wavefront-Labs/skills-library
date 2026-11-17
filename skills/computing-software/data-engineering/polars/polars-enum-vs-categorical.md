---
id: computing-software.data-engineering.polars.polars-enum-vs-categorical
name: polars-enum-vs-categorical
category: computing-software
field: data-engineering
product: polars
tags: [polars, polars-categorical-enum, enum, categorical, ordered-categories, string-comparison, invalid-values, dtype-choice]
level: practitioner
status: docs-checked
description: "Choose between the Polars Enum and Categorical dtypes, define ordered categories, handle invalid values, and compare with strings correctly."
sources:
  - https://docs.pola.rs/user-guide/expressions/categorical-data-and-enums/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Enum versus Categorical in Polars

Goal: store low-cardinality string data efficiently and pick the right type.

Rule of thumb from the docs: for performance prefer `Enum` over `Categorical` whenever possible. You can always cast from one to the other if requirements change.

| | `Enum` | `Categorical` |
| --- | --- | --- |
| Categories | fixed, defined up front | not defined up front; mapping grows dynamically |
| Ordering | ordered (order of declaration) | cannot be ordered; compares lexically |

## Enum

```python
bears_enum = pl.Enum(["Polar", "Panda", "Brown"])
bears = pl.Series(["Polar", "Panda", "Brown", "Brown", "Polar"], dtype=bears_enum)
```

Use it when creating a series, a dataframe (`schema_overrides`), or when casting a string column.

Invalid values: if the series holds a value outside the categories (the example adds `"Shark"`), Polars raises `InvalidOperationError`. If you cannot know all values in advance and erroring is semantically wrong, use `Categorical`.

Ordering and comparison, using log levels:

```python
log_levels = pl.Enum(["debug", "info", "warning", "error"])
logs = pl.DataFrame({"level": ["debug", "info", "debug", "error"], "message": [...]},
                    schema_overrides={"level": log_levels})
logs.filter(pl.col("level") > "debug")
```

- An `Enum` column compares with a string only if the string is a valid category; `pl.col("level") > "Pretty bad"` raises an error.
- An `Enum` column can be compared with another column of the same `Enum` type, or with a string column if all its strings are valid `Enum` values (`logs["level"] == str_series`).

## Categorical

```python
bears_cat = pl.Series(["Polar", "Panda", "Brown", "Brown", "Polar"], dtype=pl.Categorical)
```

Cast a string column or pass `Categorical` as the dtype of a series or dataframe column.

- Comparing a `Categorical` with a string, or with a string column, is lexical (alphabetical): `pl.col("categorical") < "Cat"`.
- Comparing two `Categorical` columns directly is typically more efficient than comparing against a string column, and is always lexical.

## Gotcha

Letting Polars infer categories is easier but has a performance cost (continuous inference and bookkeeping). See polars-categorical-encodings-and-categories for why and for `pl.Categories`.

## Checked
2026-11-07: every claim compared with the cited Polars user guide page(s). Removed or trimmed claims the cited page does not confirm.

Method: documentation only; no commands were run.
