---
id: computing-software.cloud-infrastructure-engineering.jaeger.jaeger-ui-search-menu-link-patterns
name: jaeger-ui-search-menu-link-patterns
category: computing-software
field: cloud-infrastructure-engineering
product: jaeger
tags: [jaeger, link-patterns, search-max-lookback, custom-menu, epoch-micros-to-date-iso]
level: advanced
status: docs-checked
description: "Add custom menu items, limit search lookback and limit, and build templated links with linkPatterns formatting functions."
sources:
  - https://www.jaegertracing.io/docs/2.22/deployment/frontend-ui/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: tailor navigation and deep links.

Menu: `menu` adds right-aligned links to the global nav. A link has `label`, optional `url` and optional `anchorTarget` (_self, _blank, _parent, _top). Group links as `{"label": "Dropdown button", "items": [ ... ]}`.

Search limits: `search.maxLimit` caps the number of results the input allows; `search.maxLookback` (`{"label": "2 Days", "value": "2d"}`) hides Lookback dropdown options longer than the value.

Link patterns: `linkPatterns` entries have `type` (process, tags, logs, traces), `key` (not needed for traces), `url` and `text`. Both url and text accept templates like `#{field-name}`. For traces, template fields are duration, endTime, startTime, traceName and traceID; in process/logs/tags types prefix them with `trace.` (for example `trace.traceID`).

Formatting functions use `#{field | function}` and chain:
- `epoch_micros_to_date_iso`: microseconds since epoch to ISO date time
- `pad_start targetLength padCharacter`: for example `#{traceID | pad_start 32 0}`
- `add offset`: for example `#{startTime | add 1000000}`

Chained example: `#{startTime | add 60000000 | epoch_micros_to_date_iso}`.

## Checked

2026-11-03. Confirmed against the Frontend/UI page: menu items and anchorTarget values, search.maxLimit and maxLookback, linkPatterns fields and types, template fields for traces and the trace. prefix, and the epoch_micros_to_date_iso, pad_start and add functions with chaining. Nothing removed.
Method: documentation only; no commands were run.
