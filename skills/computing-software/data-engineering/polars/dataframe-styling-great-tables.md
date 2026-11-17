---
id: computing-software.data-engineering.polars.dataframe-styling-great-tables
name: dataframe-styling-great-tables
category: computing-software
field: data-engineering
product: polars
tags: [polars-styling, great-tables, dataframe-style, tab-header, tab-spanner, fmt-number, tab-style, selectors]
level: practitioner
status: docs-checked
description: "Style a Polars DataFrame for presentation with DataFrame.style (Great Tables GT): header, stub, spanner, number formats and conditional row highlighting."
sources:
  - https://docs.pola.rs/user-guide/misc/styling/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Style tables with DataFrame.style

`DataFrame.style` returns a `GT` object from Great Tables for structuring, formatting and styling table display.

Base frame (Iris means per species):
```python
import polars as pl
import polars.selectors as cs

df = (
    pl.scan_csv(path)
    .group_by("species")
    .agg(cs.starts_with("petal").mean().round(3))
    .collect()
)
```

## Structure
- Header: `df.style.tab_header(title="Iris Data", subtitle="Mean measurement values per species")`
- Row stub: `df.style.tab_stub(rowname_col="species")`
- Column spanner and labels:
```python
df.style.tab_spanner("Petal", cs.starts_with("petal")).cols_label(
    petal_length="Length", petal_width="Width"
)
```

## Format
Limit decimals: `df.style.fmt_number("petal_width", decimals=1)`.

## Style
Highlight the row with the max value using a Polars expression for `rows`:
```python
from great_tables import loc, style

df.style.tab_style(
    style.fill("yellow"),
    loc.body(rows=pl.col("petal_length") == pl.col("petal_length").max()),
)
```
Bold a column: `df.style.tab_style(style.text(weight="bold"), loc.body(columns="species"))`.

## Combine
Calls chain:
```python
(
    df.style.tab_header(title="Iris Data", subtitle="Mean measurement values per species")
    .tab_stub(rowname_col="species")
    .cols_label(petal_length="Length", petal_width="Width")
    .tab_spanner("Petal", cs.starts_with("petal"))
    .fmt_number("petal_width", decimals=2)
    .tab_style(
        style.fill("yellow"),
        loc.body(rows=pl.col("petal_length") == pl.col("petal_length").max()),
    )
)
```

Use Great Tables' own docs for the full API.

## Checked
2026-11-07: every claim compared with the cited Polars user guide page(s). Removed or trimmed claims the cited page does not confirm.

Method: documentation only; no commands were run.
