---
id: computing-software.cloud-infrastructure-engineering.vector.remap-transform-behaviour
name: remap-transform-behaviour
category: computing-software
field: cloud-infrastructure-engineering
product: vector
tags: [remap, drop-on-error, drop-on-abort, lazy-mutation, metrics, vrl, vector]
level: advanced
status: docs-checked
description: "Configure how remap treats errors and aborts, and know its limits on metric events."
sources:
  - https://vector.dev/docs/reference/configuration/transforms/remap/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Key `remap` options:

- `source`, `file` or `files`: exactly one must be set. `file` and `files` are paths to VRL programs, relative to the working directory.
- `drop_on_abort` (default true): an event aborted with `abort` is dropped; when false, the original unmodified event passes on.
- `drop_on_error` (default false): normally an event whose program errors is sent downstream unmodified. Set true when enrichment is strictly required.
- `reroute_dropped` (default false): send dropped events to a `<name>.dropped` output for logging and analysis.
- `timezone`: applied to timestamps lacking a zone; overrides the global option.

Lazy mutation: path assignments are not applied until the program finishes. If it fails part way, all changes are discarded and the event stays as it was. To guarantee the change, write programs that cannot fail at runtime, or drop failing events with `drop_on_error`.

Metrics: `remap` handles logs, metrics and traces but cannot convert between types (use `log_to_metric` or `metric_to_log`). For metrics VRL is restrictive: `type` is read only; `kind` is read/write but only `incremental` or `absolute`; `name` read/write; `namespace`, `timestamp`, `interval_ms` and `tags` are read/write/delete, and tags must be an object of string keys and values. Disallowed actions, such as `del(.type)`, are silently ignored rather than raising an error.

`remap` is a stateless transform.

Verify with unit tests covering both a valid and a malformed event.

## Checked

2026-11-03. Read transforms/remap. Confirmed: exactly one of `source`, `file`, `files`; paths relative to the working directory; `drop_on_abort`, `drop_on_error` and `reroute_dropped` defaults; `timezone`; lazy event mutation; logs, metrics and traces with no type conversion; the metric field access table; disallowed actions ignored silently; stateless. Fixed: `namespace` is read/write/delete, not read/write. Removed: the claim that remap is inlined into the source (runtime model page not read).

Method: documentation only; no commands were run.
