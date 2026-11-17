---
id: computing-software.data-engineering.polars.polars-string-regex-match-extract-replace
name: polars-string-regex-match-extract-replace
category: computing-software
field: data-engineering
product: polars
tags: [polars-strings, str, regex, contains, extract, replace, string-matching, expressions]
level: practitioner
status: docs-checked
description: "Check, extract and replace patterns in Polars string columns with str.contains, extract, extract_all, replace and replace_all."
sources:
  - https://docs.pola.rs/user-guide/expressions/strings/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: find, pull out or substitute text in a string column with the `str` namespace.

**Existence.** `str.contains(pattern)` treats the pattern as a regex by default; pass `literal=True` for a literal substring. `str.starts_with` and `str.ends_with` test fixed prefixes/suffixes:

```python
df.select(
    pl.col("fruit"),
    pl.col("fruit").str.starts_with("p").alias("starts_with_p"),
    pl.col("fruit").str.contains("p..r").alias("p..r"),
    pl.col("fruit").str.contains("e+").alias("e+"),
    pl.col("fruit").str.ends_with("r").alias("ends_with_r"),
)
```

**Regex flavour.** Polars uses the Rust crate `regex`, which differs from Python's `re`; check its syntax documentation for supported features and flags.
**Extract.** `str.extract` takes a regex with one or more capture groups and returns the group given as the second argument (`group_index`):

```python
pl.col("urls").str.extract(r"candidate=(\w+)", group_index=1)
```

`str.extract_all` returns a list of all matches, e.g. all numbers from a string:

```python
pl.col("text").str.extract_all(r"(\d+)").alias("extracted_nrs")
```

**Replace.** `str.replace` makes at most one replacement; `str.replace_all` makes all non-overlapping replacements. Both accept a regex or, with `literal=True`, a literal substring:

```python
pl.col("text").str.replace(r"\d", "-"),
pl.col("text").str.replace_all(r"\d", "-").alias("text_replace_all"),
```

**Length.** `str.len_bytes` and `str.len_chars` give byte and character counts. For ASCII-only text they are equal, and `len_bytes` is recommended because it is faster.

The namespace has 40+ functions in total; see the API docs for the rest.

## Checked

2026-11-07. Read in full and compared against this skill: https://docs.pola.rs/user-guide/expressions/strings/. Corrected: Removed a (?i) sentence the page does not state. Any parameter, default, class, method or error string not found on those pages was removed.

Method: documentation only; no commands were run.
