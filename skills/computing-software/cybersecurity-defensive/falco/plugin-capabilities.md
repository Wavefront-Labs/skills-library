---
id: computing-software.cybersecurity-defensive.falco.plugin-capabilities
name: plugin-capabilities
category: computing-software
field: cybersecurity-defensive
product: falco
tags: [falco-plugins, event-sourcing, field-extraction, event-parsing, async-events]
level: practitioner
status: docs-checked
description: "Know the four Falco plugin capabilities, why plugins are trusted code, and the rules for event sources and overlapping fields."
sources:
  - https://falco.org/docs/concepts/plugins/architecture/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Plugins are dynamic shared libraries (.so on Unix, .dll on Windows) exporting C calling-convention functions that Falco loads at runtime. They use semantic versioning, can be written in any language, with Go preferred and C/C++ next. Optional SDKs exist for Go, C++ and Rust.

Four capabilities, composable in one plugin:
- Event sourcing: provides a new event source, opening and closing a stream of events (`plugin_open`, `plugin_next_batch`). It needs a unique plugin event ID registered in the falcosecurity plugins `registry.yaml`.
- Field extraction: extracts fields (for example `ct.name`, or `jevt.value[...]` from generic JSON) from events of other plugins or the core libraries, and does not provide events.
- Event parsing: sees every event of a stream sequentially in the parse phase before extraction and can update state.
- Async events: injects events asynchronously into a stream; the libraries use it for container runtime metadata enrichment.

Plugins are trusted: they run in the same thread and address space as Falco and can crash it.

Event sources are distinct from plugin names, so several plugins can produce the same source. Only one loaded plugin may export a given source, for example gke-k8saudit or eks-k8saudit with source `k8s_audit`, not both. Fields must not overlap within one event source, but different sources can reuse a field name.

Gotcha: `plugin_get_id` and `plugin_get_event_source` apply only to event sourcing plugins.

## Checked

2026-11-08. Read the cited plugin architecture page in full. Replaced a misattributed ka.verb extraction example with ct.name.

Method: documentation only; no commands were run.
