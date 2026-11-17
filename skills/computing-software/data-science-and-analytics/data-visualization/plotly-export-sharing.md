---
id: computing-software.data-science-and-analytics.data-visualization.plotly-export-sharing
name: plotly-export-sharing
category: computing-software
field: data-science-and-analytics
product: data-visualization
tags: [plotly-write-html, plotly-static-export, dash-basics]
level: practitioner
status: docs-checked
description: "Write self-contained HTML, choose static image export with kaleido and know when Dash is the next step."
sources:
  - https://plotly.com/python/interactive-html-export/
  - https://plotly.com/python/static-image-export/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Export
```python
fig.write_html("chart.html")                    # self-contained by default
fig.write_image("chart.png", scale=2)           # needs the kaleido package
```
For input controls and callbacks use Dash, a separate package (`pip install dash`) for analytical apps built on Plotly figures.
## Gotchas
- `write_html` produces a fully self-contained HTML file by default, which can be emailed or uploaded. The downside is size (5 MB or more) because it inlines the Plotly.js library; the `include_plotlyjs` argument controls this (see the page's include_plotlyjs section for its values).
- `write_image` supports PNG, JPEG, WebP, SVG and PDF, inferring the format from the extension (or `format=`). Install the `kaleido` package first (`pip install --upgrade kaleido`).
- `write_image` and `to_image` accept `width`, `height` and `scale` (scale above 1 raises the physical resolution).
- `plotly.io.write_images` writes several figures faster than repeated `write_image` calls.
- The HTML embeds the figure data, so anyone with the file can read it; aggregate or remove sensitive columns before sharing.
## Verify
- [ ] The exported HTML opens in a browser without a server.

## Checked

2026-11-09. Confirmed against the Plotly interactive HTML export page (write_html, self-contained default, 5Mb+ size, include_plotlyjs controls it, Dash description) and the static image export page (kaleido install, write_image formats, width/height/scale, write_images). Removed: the specific include_plotlyjs values ("cdn", True) and the claim that the HTML opens offline with include_plotlyjs=True, because the stripped page text did not show that section; also removed the advice to host Dash behind authentication.
Method: docs-checked 2026-11-09 against the two Plotly pages named above, searched for the calls listed.
