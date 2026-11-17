---
id: computing-software.data-engineering.polars.polars-string-case-strip-slice-concat
name: polars-string-case-strip-slice-concat
category: computing-software
field: data-engineering
product: polars
tags: [polars-string-modify, str, strip-chars, case-conversion, slice, concatenate, expressions]
level: practitioner
status: docs-checked
description: "Modify Polars string columns: concatenate with +, change case, strip characters or prefixes, and slice with str.slice, head and tail."
sources:
  - https://docs.pola.rs/user-guide/expressions/strings/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: transform string values with the `str` namespace.

**Concatenate** string expressions horizontally with `+` (equivalent to `Expr.add`):

```python
df.with_columns(full_name=pl.col("first_name") + pl.lit(" ") + pl.col("last_name"))
```

**Case:** `str.to_lowercase`, `str.to_titlecase`, `str.to_uppercase`.

**Strip.** Five functions:

| Function | Behaviour |
| --- | --- |
| `strip_chars` | Removes leading and trailing occurrences of the characters specified |
| `strip_chars_end` | Removes trailing occurrences of the characters specified |
| `strip_chars_start` | Removes leading occurrences of the characters specified |
| `strip_prefix` | Removes an exact substring prefix if present |
| `strip_suffix` | Removes an exact substring suffix if present |

The first three treat their argument as a SET of characters; `strip_prefix` and `strip_suffix` treat it as a literal string. With no argument, the three `strip_chars*` functions remove whitespace. Analogies: `strip_chars` ~ Python `strip`; `strip_prefix`/`strip_suffix` ~ `removeprefix`/`removesuffix`.

```python
addr = pl.col("addresses")
chars = ", 0123456789"
addresses.select(
    addr.str.strip_chars(chars).alias("strip"),
    addr.str.strip_chars_end(chars).alias("end"),
    addr.str.strip_chars_start(chars).alias("start"),
    addr.str.strip_prefix("128 ").alias("prefix"),
    addr.str.strip_suffix(", 158").alias("suffix"),
)
```

**Slice.** `str.slice` takes a starting offset and an optional length; if the length is omitted or runs past the end of the string, it slices to the end. `str.head(n)` and `str.tail(n)` slice the beginning and end. The page passes columns as arguments (negative values appear in the data):

```python
df.with_columns(
    pl.col("fruits").str.slice(pl.col("n")).alias("slice"),
    pl.col("fruits").str.head(pl.col("n")).alias("head"),
    pl.col("fruits").str.tail(pl.col("n")).alias("tail"),
)
```

## Checked

2026-11-07. Read in full and compared against this skill: https://docs.pola.rs/user-guide/expressions/strings/. Corrected: Reworded str.slice to the page's offset and optional length description. Any parameter, default, class, method or error string not found on those pages was removed.

Method: documentation only; no commands were run.
