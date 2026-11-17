---
id: computing-software.messaging-and-integration.nats.subject-mapping-transforms
name: subject-mapping-transforms
category: computing-software
field: messaging-and-integration
product: nats
tags: [subject-mapping, transforms, wildcard-function, nats-trace, mappings]
level: practitioner
status: docs-checked
description: "Write NATS subject mappings in server config and streams: scope, wildcard(n) reordering, split/slice functions, testing with nats server mapping."
sources:
  - https://github.com/nats-io/nats.docs/blob/master/nats-concepts/subject_mapping.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: rewrite subjects on entry to a scope (account, leaf node, import, stream) to translate namespaces, filter, merge or suppress subjects.

Where transforms live: the root `mappings` block of the server config (applies to the default `$G` account), an account's own `mappings`, subject imports, and JetStream contexts (stream `subject_transform`, `republish`, and source/mirror, where a transform also acts as a filter). With JWT accounts the transform sits in the account JWT and takes effect once the updated JWT is pushed; with config accounts, reload the config.

Rules: transforms apply when a message enters the scope, before routing; they are not recursive within a scope (only the first matching rule applies, which prevents loops) but are applied in sequence across scopes.

Syntax examples from the page:
- `orders.* orders.central.{{wildcard(1)}}` and `orders.> orders.central.>` (one full wildcard, used once in both source and destination).
- Reorder: `"bar.*.*" : "baz.{{wildcard(2)}}.{{wildcard(1)}}"` maps `bar.a.b` to `baz.b.a` (server 2.8.0+). The old `$1` style is deprecated.
- Functions: `split(1,-)`, `splitfromleft(1,4)`, `splitfromright(1,4)`, `slicefromleft(1,2)`, `slicefromright(1,2)`, `random(n)`.
- Stream form: `"subject_transform":{"src":"orders.local.*","dest":"orders.{{wildcard(1)}}"}`.

Test rules offline: `nats server mapping "bar.*.*" "baz.{{wildcard(2)}}.{{wildcard(1)}}" bar.a.b`. From server 2.11, `nats trace <subject>` shows the mapping, JetStream store and delivery path.

## Checked

2026-11-03. Read against the nats.docs repository (the pages listed in `sources`, plus the neighbouring concept, release-note and nsc/nk tool pages): configuration keys, flags, CLI commands, defaults, limits, subjects, header names and version gates were confirmed there.
Removed: the unsourced Verify step, plus statements that no page supports (see the PR notes for the per-skill list).
Method: documentation only; no commands were run.
