---
id: computing-software.data-science-and-analytics.data-visualization.plotly-express-charts
name: plotly-express-charts
category: computing-software
field: data-science-and-analytics
product: data-visualization
tags: [plotly-express, hover-data, plotly-facets, viz-interactive]
level: practitioner
status: docs-checked
description: "Create line, bar, scatter and facet charts from DataFrames with Plotly Express, controlling hover text, colour and facets."
sources:
  - https://plotly.com/python/plotly-express/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Plotly Express
```python
import plotly.express as px
fig = px.line(df, x="day", y="v", color="region", hover_data=["orders"])
fig.update_layout(template="simple_white", legend_title_text="Region")
fig.show()
```
## Gotchas
- PX functions accept lists, dicts, long-form or wide-form DataFrames, numpy arrays, xarrays and GeoPandas GeoDataFrames.
- They create one trace per unique combination of discrete colour, symbol, line-dash and facet values, and set the legend so one item appears per combination.
- Hover labels are populated automatically; `hover_name` and `hover_data` give extra control.
- Styling comes from the default figure template; `category_orders` and `color_discrete_map` control categorical variables, and `template=` sets a template per call (the page uses `simple_white` and `plotly_dark`).
- Faceting uses `facet_row`, `facet_col` and `facet_col_wrap` on the 2D Cartesian functions.
- `render_mode` is an argument of some functions (the page shows `render_mode="svg"` on `px.line`).
## Verify
- [ ] Hover shows units and rounded values.

## Checked

2026-11-09. Confirmed against the Plotly Express overview page: input formats, trace and legend behaviour, hover_name and hover_data, category_orders, color_discrete_map, facet arguments, template names in examples, render_mode="svg". Removed: markers=True, template="plotly_white", rangemode, the advice to use webgl for thousands of points, and the claim that Express expects long-format data (the page says both long and wide forms are accepted).
Method: docs-checked 2026-11-09 against the Plotly Express overview page, searched for each argument named.
