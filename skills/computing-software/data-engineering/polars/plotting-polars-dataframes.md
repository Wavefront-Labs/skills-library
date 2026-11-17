---
id: computing-software.data-engineering.polars.plotting-polars-dataframes
name: plotting-polars-dataframes
category: computing-software
field: data-engineering
product: polars
tags: [polars-visualization, altair, hvplot, matplotlib, plotnine, seaborn, plotly, narwhals]
level: practitioner
status: docs-checked
description: "Plot a Polars DataFrame with Altair (df.plot), hvPlot, Matplotlib, Plotnine, Seaborn or Plotly, including which libraries need pandas conversion."
sources:
  - https://docs.pola.rs/user-guide/misc/visualization/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Visualise Polars data

Examples use the Iris CSV: `df = pl.read_csv(path)`; scatter of `sepal_width` vs `sepal_length`, colored by `species`.

## Altair (built in)
`df.plot` is a convenience shorthand for Altair:
```python
chart = (
    df.plot.point(x="sepal_width", y="sepal_length", color="species")
    .properties(width=500, title="Irises")
    .configure_scale(zero=False)
    .configure_axisX(tickMinStep=1)
)
```
Equivalent to `alt.Chart(df).mark_point(tooltip=True).encode(...)`. Tweaks: `.properties(width=500, height=350, title=...)`, `.configure_axisX(labelAngle=30)`, `.configure_point(opacity=.5)`.

## hvPlot
`import hvplot.polars` registers `df.hvplot`:
```python
df.hvplot.scatter(x="sepal_width", y="sepal_length", by="species", width=650, title="Irises")
```

## Matplotlib
Pass Series directly; Matplotlib converts to NumPy (zero-copy for numeric data without nulls). A non-numeric column used for `c` must be converted first:
```python
ax.scatter(x=df["sepal_width"], y=df["sepal_length"],
           c=df["species"].cast(pl.Categorical).to_physical())
```

## Plotnine
ggplot2 reimplementation; accepts a Polars DataFrame by internally converting to pandas:
```python
ggplot(df, mapping=aes(x="sepal_width", y="sepal_length", color="species")) + geom_point()
```

## Seaborn
Accepts pandas DataFrames. Convert with `df.to_pandas()`; pandas may not support all Polars dtypes:
```python
sns.scatterplot(df.to_pandas(), x="sepal_width", y="sepal_length", hue="species", ax=ax)
```

## Plotly
Accepts a Polars DataFrame via Narwhals since plotly v6.0.0, executing natively without conversion:
```python
px.scatter(df, x="sepal_width", y="sepal_length", color="species", width=650)
```

## Checked
2026-11-07: every claim compared with the cited Polars user guide page(s). No unconfirmed claims found.

Method: documentation only; no commands were run.
