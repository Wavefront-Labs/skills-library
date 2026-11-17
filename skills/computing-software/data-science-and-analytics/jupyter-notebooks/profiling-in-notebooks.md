---
id: computing-software.data-science-and-analytics.jupyter-notebooks.profiling-in-notebooks
name: profiling-in-notebooks
category: computing-software
field: data-science-and-analytics
product: jupyter-notebooks
tags: [prun-profiling, timeit-magic]
level: advanced
status: docs-checked
description: "Find hotspots with the %prun magic and compare statements with %timeit before optimising."
sources:
  - https://ipython.readthedocs.io/en/stable/interactive/magics.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Profiling
```python
%prun -l 15 -s cumulative run_pipeline(df)
%timeit -n 10 -r 3 run_pipeline(df)
```
To profile a whole script, use `%run -p [prof_opts] filename.py [args]`.
## Gotchas
- `%prun -l 15` limits the report to 15 lines and `-s cumulative` sorts by that key; see the page for `-r`, `-T` and `-D` to return the stats object or save output.
- Profile with realistic data sizes; small samples hide the real bottleneck.
- Use `%timeit` to compare before and after; `%time` is only basic timing.
## Verify
- [ ] Re-profile after the fix and confirm the hotspot shrank.

## Checked

2026-11-09. Confirmed against the IPython built-in magics page: %prun options (-l, -s, -r, -T, -D), %run -p, %timeit options. Removed: line_profiler / %lprun, memory_profiler and tracemalloc advice, and the overhead remark (not on the page); source anchor replaced by the page URL.
Method: docs-checked 2026-11-09 against the IPython built-in magics page.
