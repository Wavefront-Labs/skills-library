---
id: computing-software.cloud-infrastructure-engineering.fluentd.labels-and-error-routing
name: labels-and-error-routing
category: computing-software
field: cloud-infrastructure-engineering
product: fluentd
tags: [cloud-infrastructure-engineering, fluentd, label, error-label, root-label, routing]
level: practitioner
status: docs-checked
description: "Group filters and outputs with label, route inputs via @label, and use the built-in @ERROR and @ROOT labels."
sources:
  - https://docs.fluentd.org/configuration/config-file
  - https://docs.fluentd.org/configuration/plugin-common-parameters
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Fluentd labels
`<label @NAME>` groups `filter` and `match` sections so events skip tag-based routing. An input selects a label with the built-in `@label` parameter; the value must start with `@`.

```
<source>
  @type tail
  @label @SYSTEM
</source>
<label @SYSTEM>
  <filter var.log.middleware.**>
    @type grep
  </filter>
  <match **>
    @type s3
  </match>
</label>
```
In this example forward events (no `@label`) use the top-level filters and matches, while `tail` events are routed to the grep filter and s3 output inside `@SYSTEM`. Labels keep complex configs modular without modifying tags.

Built-in labels:
- `@ERROR`: receives records a plugin emits through `emit_error_event`, for example when the buffer is full or a record is invalid. Define `<label @ERROR>` to catch them.
- `@ROOT`: lets a plugin use `event_emitter_router` to send events back to the default route (introduced in v1.14.0). The page's example is timed-out records from the concat filter.

## Checked

2026-11-04. Confirmed against the Fluentd Config File page (docs.fluentd.org/configuration/config-file), label section, and the Common Parameters page: label grouping, @ prefix rule, @ERROR and @ROOT semantics and v1.14.0. Removed: the out_relabel sentence (not on the cited pages); reworded the sentence about sources without @label.

Method: documentation only; no commands were run.
