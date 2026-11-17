---
id: computing-software.data-engineering.polars.polars-concat-vertical-horizontal-diagonal
name: polars-concat-vertical-horizontal-diagonal
category: computing-software
field: data-engineering
product: polars
tags: [polars-concatenation, concat, vertical, horizontal, diagonal, rechunk, horizontal-extend]
level: practitioner
status: docs-checked
description: "Combine Polars DataFrames with pl.concat using how=vertical, horizontal, horizontal_extend or diagonal, and understand rechunking."
sources:
  - https://docs.pola.rs/user-guide/transformations/concatenation/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: stack or widen DataFrames with `pl.concat([...], how=...)`.

**`how="vertical"`** (longer): same column names required, otherwise it fails.

```python
pl.concat([df_v1, df_v2], how="vertical")
```

**`how="horizontal"`** (wider): combines the columns of all frames. It fails when frames have overlapping column names, and both must have the same height.

```python
pl.concat([df_h1, df_h2], how="horizontal")
```

**`how="horizontal_extend"`**: for different heights; pads shorter columns with `null` at the end to match the longest frame.

```python
pl.concat([df_h1, df_h2], how="horizontal_extend")   # 2 rows + 3 rows -> 3 rows, nulls padded
```

**`how="diagonal"`** (longer, wider, nullier): where column names overlap, values are concatenated vertically; where they do not, new rows and columns are added with missing values set to `null`.

```python
pl.concat([df_d1, df_d2], how="diagonal")   # columns a,b and a,d -> a,b,d
```

If shapes do not match but there is an overlapping semantic key, join the frames instead of concatenating.

**Rechunking.** Each column lives in one or more chunks. By default concat does not make the chunks contiguous: faster and less memory, but later operations that benefit from contiguous memory may be slower. Copying fragmented chunks into one new chunk is rechunking, which is expensive. Before version 0.20.26 the default was to rechunk; now it is not. Ask for it with:

```python
pl.concat([df1, df2], rechunk=True)
```

## Checked
2026-11-07: every claim compared with the cited Polars user guide page(s). No unconfirmed claims found.

Method: documentation only; no commands were run.
