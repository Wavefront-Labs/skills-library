---
id: computing-software.cloud-infrastructure-engineering.jaeger.jaeger-ui-embedded-mode
name: jaeger-ui-embedded-mode
category: computing-software
field: cloud-infrastructure-engineering
product: jaeger
tags: [jaeger, ui-embed, uiembed-v0, ui-search-hide-graph, ui-timeline-hide-minimap]
level: advanced
status: docs-checked
description: "Embed the Jaeger search and trace pages in another app with uiEmbed=v0 and layout query parameters."
sources:
  - https://www.jaegertracing.io/docs/2.22/deployment/frontend-ui/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: integrate Jaeger UI pages into another application.

Embedded mode (since version 1.9) strips UI elements for space-constrained layouts. It is enabled and tuned by URL query parameters, and `uiEmbed=v0` is required. A button on each page opens the non-embedded page in a new tab. Supported pages: Search and Trace.

Trace page: `http://localhost:16686/trace/{trace-id}?uiEmbed=v0`
- `uiTimelineCollapseTitle=1`: trace header starts collapsed (hides summary and minimap)
- `uiTimelineHideMinimap=1`: removes the minimap entirely
- `uiTimelineHideSummary=1`: removes the summary (number of services and so on) entirely
Combine with `&`.

Search page: `http://localhost:16686/search?service=my-service&start=1543917759557000&end=1543921359557000&limit=20&lookback=1h&uiEmbed=v0`
- `uiSearchHideGraph=1`: hides the scatter plot above results

UI config options for embedding: `disableFileUploadControl` (hide JSON trace upload, default false), `disableJsonView` (hide JSON view, default false) and `forbidNewPage` (stop links opening new tabs or windows, default false).

## Checked

2026-11-03. Confirmed against the Frontend/UI page, Embedded Mode and UI Controls sections: version 1.9 introduction, uiEmbed=v0 requirement, supported pages, uiSearchHideGraph, the three uiTimeline parameters, and the disableFileUploadControl, disableJsonView and forbidNewPage options and defaults. Removed: a closing Notes paragraph of unverified inference.
Method: documentation only; no commands were run.
