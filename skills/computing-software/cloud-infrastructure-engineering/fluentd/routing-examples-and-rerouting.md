---
id: computing-software.cloud-infrastructure-engineering.fluentd.routing-examples-and-rerouting
name: routing-examples-and-rerouting
category: computing-software
field: cloud-infrastructure-engineering
product: fluentd
tags: [cloud-infrastructure-engineering, fluentd, routing, relabel, copy, rewrite-tag-filter, fluent-plugin-route]
level: practitioner
status: docs-checked
description: "Typical Fluentd routing layouts: two inputs one output, labels per pipeline, rerouting by tag, by record content, or to another label."
sources:
  - https://docs.fluentd.org/configuration/routing-examples
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Fluentd routing examples
Patterns from the routing page:

- **Simple**: `source forward` -> `filter app.**` (record_transformer) -> `match app.**`.
- **Two inputs, one output**: `<match {app.**,system.logs}>` handles a `forward` source and a `tail` source with `tag system.logs`.
- **Separate pipelines**: give one source `@label @METRICS` and handle it in `<label @METRICS>`; the other source stays on the default route.
- **Reroute by tag**: the third-party `fluent-plugin-route` rewrites the tag (`remove_tag_prefix`, `add_tag_prefix`) and can re-emit to another `@label`. Each `<route **>` needs `copy` to fall through; without it routing stops there.
- **Reroute by record content**: `fluent-plugin-rewrite-tag-filter` with `<rule>` blocks (`key`, `pattern`, `tag`, e.g. `tag $1.${tag}`), then match the new tags.
- **Reroute to another label**: inside `@type copy`, add a `<store>` with `@type relabel` and `@label @NOTIFICATION`; the label can then apply `grep` (e.g. `regexp1 message ERROR`) and a mail output.

`out_relabel` emits events to a label without rewriting the tag.

## Checked

2026-11-04. Confirmed against the Fluentd Routing Examples page (docs.fluentd.org/configuration/routing-examples): all six patterns, the plugin names, route fall-through comment, rewrite_tag_filter rule keys and the relabel example. Removed: the closing claim about only the first matching match receiving an event (not on this page).

Method: documentation only; no commands were run.
