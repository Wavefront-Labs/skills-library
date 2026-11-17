---
id: computing-software.data-science-and-analytics.apache-superset.dashboard-virtualization
name: dashboard-virtualization
category: computing-software
field: data-science-and-analytics
product: apache-superset
tags: [dashboard-performance, virtualization, lazy-rendering, viewport, defer-data]
level: practitioner
status: docs-checked
description: "Tune Superset dashboard virtualization: DASHBOARD_VIRTUALIZATION, DEFER_DATA, viewport render rules, tab lazy loading and chart-count guidance."
sources:
  - https://github.com/apache/superset/blob/master/docs/admin_docs/configuration/dashboard-performance.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: keep large dashboards fast by rendering and fetching only what is needed.

Perceived speed depends on how many charts render, how many queries the backend runs concurrently, and how fast the warehouse answers. Superset has levers for the first two.

Chart count: no hard limit and no config key caps it. Rough guidance: under about 25 charts usually fine; 25 to 50 fine but use tabs; over about 50 split into several dashboards or use tabs. These are guidelines, not guarantees.

`DASHBOARD_VIRTUALIZATION` (default `True`; stable, marked for path to deprecation) virtualizes the layout by row:
- A chart's visualization renders when its row scrolls within 1 viewport height of the visible area, and goes back to a placeholder beyond 4 viewport heights.
- The chart component stays mounted and still issues its data request, so this alone does not reduce backend query load.
- Swap-back is skipped in embedded mode; both halves are skipped for headless rendering, so screenshot and report jobs load every chart.

`DASHBOARD_VIRTUALIZATION_DEFER_DATA` (default `False`) also skips the data request for charts not in view. It only takes effect when virtualization is on. Enable it if warehouse load spikes on dashboard open although most charts are off-screen.

```python
FEATURE_FLAGS = {
    "DASHBOARD_VIRTUALIZATION": True,
    "DASHBOARD_VIRTUALIZATION_DEFER_DATA": True,
}
```

Tabs: a tab's content is not rendered until activated (default, no flag), so unselected tabs fetch nothing on open. This is the cheapest fix for a large dashboard.

There is no switch to cap concurrent chart queries; throttle at the warehouse, in Celery pool size when async queries are on, or by splitting dashboards.

Splitting options in order of effort: tabs, aggressive caching (for example Redis), async queries via Celery, multiple dashboards linked from a landing dashboard, pre-aggregation in the warehouse.

## Checked

2026-11-08: read dashboard-performance.mdx in full. Corrected "unmounted" (the visualization is swapped for a placeholder; the component stays mounted) and the 25 and 50 chart thresholds. Removed claims not on the page.
Method: documentation only; no commands were run.
