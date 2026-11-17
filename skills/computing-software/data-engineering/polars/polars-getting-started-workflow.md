---
id: computing-software.data-engineering.polars.polars-getting-started-workflow
name: polars-getting-started-workflow
category: computing-software
field: data-engineering
product: polars
tags: [polars, polars-getting-started, read-csv, write-csv, join, concat, expression-expansion, group-by]
level: intro
status: docs-checked
description: "First Polars workflow: write and read a CSV, then select, with_columns, filter, group_by and agg, join with how=left, and concat vertically."
sources:
  - https://docs.pola.rs/user-guide/getting-started/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Getting started with Polars: a first end-to-end workflow

Goal: run the core operations once, in order.

## Read and write

```python
df.write_csv("output.csv")
df_csv = pl.read_csv("output.csv", try_parse_dates=True)
```

Polars also reads and writes json, parquet, cloud storage (S3, Azure Blob, BigQuery) and databases (postgres, mysql); see the IO section.

## Contexts

```python
# select: each expression maps to a result column
df.select(pl.col("name"),
          pl.col("birthdate").dt.year().alias("birth_year"),
          (pl.col("weight") / (pl.col("height") ** 2)).alias("bmi"))

# expansion with a suffix on the original names
df.select(pl.col("name"),
          (pl.col("weight", "height") * 0.95).round(2).name.suffix("-5%"))

# with_columns adds columns; named expressions replace alias
df.with_columns(birth_year=pl.col("birthdate").dt.year(),
                bmi=pl.col("weight") / (pl.col("height") ** 2))

# filter, one or several predicates
df.filter(pl.col("birthdate").dt.year() < 1990)
df.filter(pl.col("birthdate").is_between(dt.date(1982, 12, 31), dt.date(1996, 1, 1)),
          pl.col("height") > 1.7)
```

## group_by

`maintain_order=True` presents groups in original order; it slows grouping but makes examples reproducible.

```python
df.group_by((pl.col("birthdate").dt.year() // 10 * 10).alias("decade"),
            maintain_order=True).agg(
    pl.len().alias("sample_size"),
    pl.col("weight").mean().round(2).alias("avg_weight"),
    pl.col("height").max().alias("tallest"),
)
```

## Chaining

Contexts chain: `with_columns` (decade, first name via `pl.col("name").str.split(by=" ").list.first()`), then `select(pl.all().exclude("birthdate"))`, then `group_by(...).agg(pl.col("name"), pl.col("weight", "height").mean().round(2).name.prefix("avg_"))`.

## Combine dataframes

```python
df.join(df2, on="name", how="left")           # left outer join on a unique identifier
pl.concat([df, df3], how="vertical")          # taller dataframe
```

Concatenation also supports horizontal and diagonal; see the joins and concatenations sections.

## Checked

2026-11-07. Read in full and compared against this skill: https://docs.pola.rs/user-guide/getting-started/. No claims needed correcting. Any parameter, default, class, method or error string not found on those pages was removed.

Method: documentation only; no commands were run.
