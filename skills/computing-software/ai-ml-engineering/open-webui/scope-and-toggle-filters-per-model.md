---
id: computing-software.ai-ml-engineering.open-webui.scope-and-toggle-filters-per-model
name: scope-and-toggle-filters-per-model
category: computing-software
field: ai-ml-engineering
product: open-webui
tags: [functions-pipe-filter-action, filter, global-filter, toggle, priority, default-filter-ids, open-webui]
level: practitioner
status: docs-checked
description: "Control which Open WebUI filters run: global vs model-specific, user-toggleable chips with self.toggle, start-enabled defaults and priority ordering."
sources:
  - https://docs.openwebui.com/features/extensibility/plugin/functions/filter
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: decide who controls a filter and in what order filters run.

## States (flags `is_active`, `is_global`)
- active + global: applied to all models, shown checked and greyed in each model, cannot be unchecked.
- active, not global: only on models whose admin selected it.
- inactive: runs nowhere.
Make global: Admin Panel > Functions > the filter's three-dot menu > **Global** switch, and keep **Active** on. API: `POST /api/v1/functions/id/{filter_id}/toggle/global`. The list does not show global state; open the menu.

## Per-model selection
Model settings > **Filters** picker saves `model.meta.filterIds`; the **Start enabled in new chats** switch (only for toggleable filters) saves `model.meta.defaultFilterIds`:
```json
{"meta": {"filterIds": ["f1","f2","f3"], "defaultFilterIds": ["f2"]}}
```

## User-toggleable filter
```python
def __init__(self):
    self.valves = self.Valves()
    self.toggle = True
    self.icon = "https://example.com/icons/lightbulb.svg"   # hosted URL, not base64
```
Shows an inline chip in the input bar and a Switch in the Integrations menu. Clicking the chip opens the `UserValves` modal if defined, otherwise removes the filter from this chat's selection. Selection lives in browser sessionStorage per chat (not saved on the server); initial state comes from `defaultFilterIds`. The backend runs a toggleable filter only if its id is in the request `filter_ids`; otherwise it is not invoked. `self.toggle` is never flipped at runtime, so do NOT branch on it inside `inlet()` (that pattern is dead on 0.9.0+); do the work unconditionally and expose settings through `UserValves`.

Always-on filters (no `toggle`) have no UI control; use them for PII scrubbing, moderation, logging, rate limiting.

## Ordering
`priority: int = Field(default=0)` in `Valves`: ascending order, 0 first; ties are sorted alphabetically by function id. Each filter receives the previous filter's returned body. Execution per turn: inlet filters, request filters, model call, stream filters, (request and stream repeat on each tool-loop call), then outlet.

## Compilation
Backend `get_sorted_filter_ids(request, model, filter_ids)` merges global active filters with `model.meta.filterIds`, drops inactive, keeps only selected toggleable ones, sorts by priority.

## Checked
2026-11-07. Confirmed against the Open WebUI docs: features/extensibility/plugin/functions/filter (read in full). Nothing removed.
Method: documentation only; no commands were run.
