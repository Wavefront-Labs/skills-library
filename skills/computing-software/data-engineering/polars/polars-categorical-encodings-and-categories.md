---
id: computing-software.data-engineering.polars.polars-categorical-encodings-and-categories
name: polars-categorical-encodings-and-categories
category: computing-software
field: data-engineering
product: polars
tags: [polars, polars-categorical-enum, categories, global-mapping, physical-encoding, uint8, concat, performance]
level: advanced
status: docs-checked
description: "Control Polars Categorical encodings with pl.Categories (name, namespace, physical), combine categorical columns without re-encoding, and understand the locking cost."
sources:
  - https://docs.pola.rs/user-guide/expressions/categorical-data-and-enums/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Categorical encodings, pl.Categories and combining columns

Goal: understand why categoricals are fast, and manage independent category spaces.

## Why they are faster than strings

Strings repeat the same value over and over and joins need expensive string comparisons. `Enum` and `Categorical` store inexpensive numeric placeholders (the physical representation) mapped to the original strings, so each string is stored once. Sorting and counting can work directly on the physical values, much faster than on strings.

## Enum encodings are fixed

Categories are specified in advance, so different columns and even different datasets share the same encoding: no re-encoding and no cache lookups.

## Categorical encodings and the global mapping

Inferred categories mean you have no control over the order in which the encoding is built. Two series built independently (for example with `extend`) would get encodings in order of appearance and could disagree. To avoid this, all `Categorical` columns share a global mapping by default: the same string always gets the same physical value, so combining is cheap and needs no re-encoding:

```python
bears = pl.concat([male_bears, female_bears], how="vertical")  # species: pl.Categorical in both
```

Cost: lookups and edits to the global mapping can cause locking. This does not occur for `Enum`, whose mapping is immutable and freely shared.

## pl.Categories for independent category spaces

```python
bear_categories = pl.Categories(name="bear_species", physical=pl.UInt8)
bears = pl.DataFrame(
    {"species": ["Polar", "Brown", "Panda", "Brown", "Polar"]},
    schema_overrides={"species": pl.Categorical(bear_categories)},
)
```

Arguments:

- `name`: identifies the mapping. Two columns have compatible encodings when their `Categories` share the same name, namespace and physical type.
- `namespace`: optional scope for the name, for independent category spaces that share a name.
- `physical`: integer type for the encodings. `pl.UInt32` (default) can encode over four billion categories, `pl.UInt16` up to 65,535, `pl.UInt8` up to 255. A smaller type reduces memory when the category count is low.

Columns sharing the same `Categories` are always compatible and combine without re-encoding.

## Checked
2026-11-07: every claim compared with the cited Polars user guide page(s). No unconfirmed claims found.

Method: documentation only; no commands were run.
