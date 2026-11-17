---
id: computing-software.data-science-and-analytics.jupyter-notebooks.ipywidgets-interactive-controls
name: ipywidgets-interactive-controls
category: computing-software
field: data-science-and-analytics
product: jupyter-notebooks
tags: [ipywidgets, interact-sliders, widget-observe, jn-interactivity]
level: practitioner
status: draft
description: "Build sliders and dropdowns with ipywidgets interact and observe to explore parameters live in a notebook."
sources:
  - https://ipywidgets.readthedocs.io/en/stable/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# ipywidgets
```python
from ipywidgets import interact, widgets
@interact(n=widgets.IntSlider(10, 1, 100), kind=["line", "bar"])
def plot(n, kind): ...
w = widgets.Dropdown(options=df.region.unique()); w.observe(callback, names="value")
```
## Gotchas
- Widgets do not survive static HTML export without state embedding.
- Heavy callbacks on every slider tick freeze the UI; use `interact_manual` or debounce.
## Verify
- [ ] Moving the control updates the output exactly once.
