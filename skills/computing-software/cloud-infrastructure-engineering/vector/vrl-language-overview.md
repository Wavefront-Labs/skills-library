---
id: computing-software.cloud-infrastructure-engineering.vector.vrl-language-overview
name: vrl-language-overview
category: computing-software
field: cloud-infrastructure-engineering
product: vector
tags: [vrl, remap, language, safety, performance, stateless, vector]
level: intro
status: docs-checked
description: "Understand what VRL is, what it deliberately omits and where it runs in Vector."
sources:
  - https://vector.dev/docs/reference/vrl/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Vector Remap Language (VRL) is an expression-oriented language for transforming logs and metrics safely and quickly. Programs act on a single event and are used in the `remap` transform to change events, and in conditions that route or filter events (for example a `filter` transform's `condition`).

```yaml
transforms:
  modify:
    type: remap
    inputs: [logs]
    source: |
      del(.user_info)
      .timestamp = now()
```

Design points from the docs:

- VRL compiles to native Rust code: no runtime, no FFI cost per event, no garbage collection.
- It is stateless: one event at a time. Cross-event work such as deduplication belongs to other transforms.
- It has no loops, which makes it hard to write slow or buggy scripts.
- Compile-time fail safety checks (fallible function errors must be handled) and type safety checks.
- A rich set of built-in functions for observability, for example `parse_syslog` and `parse_json`.

Within a program `.` is the whole event and `.kubernetes.pod_id` style paths read nested fields. The reference has pages for functions, errors, examples and expressions, and there is an online VRL playground (some functions are unsupported there).

## Checked

Method: docs-checked 2026-11-09 against the Vector VRL index page (raw markdown) and the VRL feature and principle definitions it renders (compilation, native, stateless, performance cue files in the vectordotdev/vector repo). Dropped unsourced claims about custom functions, recursion, system I/O, log rate limiting, the `vector vrl` REPL and a verification line.
