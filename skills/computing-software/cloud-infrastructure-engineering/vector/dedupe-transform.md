---
id: computing-software.cloud-infrastructure-engineering.vector.dedupe-transform
name: dedupe-transform
category: computing-software
field: cloud-infrastructure-engineering
product: vector
tags: [dedupe, transform, cache, lru, fields-match, fields-ignore, vector]
level: practitioner
status: docs-checked
description: "Drop duplicate events using an LRU cache and choose which fields define equality."
sources:
  - https://vector.dev/docs/reference/configuration/transforms/dedupe/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`dedupe` drops events that duplicate a recent one. It is stateful, and state is not preserved across restarts.

```yaml
transforms:
  unique:
    type: dedupe
    inputs: [logs]
    cache:
      num_events: 5000
    fields:
      match: [message, host]
```

Equality: with no `fields` setting events are compared on `timestamp`, `host` and `message`. Use `fields.match` to compare only the listed fields, or `fields.ignore` to compare all fields except those listed (it is an alternative, not combined).

The cache is an LRU of the last `cache.num_events` events (default 5000). A duplicate is moved to the head, which resets its eviction order. Optionally add `time_settings` with `max_age_ms` so duplicates are allowed again after that age, and `refresh_on_drop` (default false) to restart the age when a duplicate is dropped.

Memory: each cache entry copies the values of the fields considered. With `fields.match`, estimate memory as the average data size of the matched fields times `num_events`. With `fields.ignore` field names are also stored, so it costs more.

Null versus missing: a field with an explicit null differs from the field being absent.

With end-to-end acknowledgements a dropped duplicate counts as delivered.

Verify by sending the same event twice and confirming one output.

## Checked

2026-11-03. Read transforms/dedupe. Confirmed: the default matching fields, `fields.match` and `fields.ignore`, `cache.num_events` default 5000, LRU behaviour and head-of-cache reset, `time_settings.max_age_ms` and `refresh_on_drop` default false, the memory formulas, null versus missing, and that dedupe drops count as delivered under end-to-end acknowledgements. Removed: the claim about running as its own task (runtime model page not read).

Method: documentation only; no commands were run.
