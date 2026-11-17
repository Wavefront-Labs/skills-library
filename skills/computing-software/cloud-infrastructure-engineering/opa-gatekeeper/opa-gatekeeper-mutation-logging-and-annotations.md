---
id: computing-software.cloud-infrastructure-engineering.opa-gatekeeper.opa-gatekeeper-mutation-logging-and-annotations
name: opa-gatekeeper-mutation-logging-and-annotations
category: computing-software
field: cloud-infrastructure-engineering
product: opa-gatekeeper
tags: [opa-gatekeeper, log-mutations, mutation-annotations, mutation-id, idempotence, mutating-webhook]
level: advanced
status: docs-checked
description: "Log Gatekeeper mutations and stamp mutated objects with mutation-id and mutations annotations, noting that this breaks Kubernetes idempotence."
sources: ["https://github.com/open-policy-agent/gatekeeper/blob/master/website/docs/customize-startup.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Opa gatekeeper mutation logging and annotations

Two beta flags help trace what the mutating webhook did:
- `--log-mutations` logs mutation events and errors.
- `--mutation-annotations` adds two annotations to mutated objects.

| Annotation | Value |
|---|---|
| `gatekeeper.sh/mutation-id` | UUID of the mutation |
| `gatekeeper.sh/mutations` | comma-separated list in the form `<MutationType>/<MutationNamespace>/<MutationName>:<MutationGeneration>` |

Warning from the docs: enabling `--mutation-annotations` breaks the idempotence requirement Kubernetes places on mutating webhooks. Weigh that against the debugging value, and prefer `--log-mutations` where logs are enough.

Related: mutators with `match.source: Generated` apply only to expanded resources and never touch real objects, and the `gatekeeper_mutator_*` metrics show ingestion counts and conflicting mutators.

Both flags are described as beta features in the startup customisation guide.

## Checked

2026-11-08: read the Enable mutation logging and annotations section of website/docs/customize-startup.md, the Match Source section of website/docs/expansion.md and the mutator metric names in website/docs/metrics.md in the Gatekeeper repo. Confirmed the flags, annotation names and format, the idempotence warning, the Generated source behaviour and the gatekeeper_mutator metrics. Removed: the mutation-id UUID explanation and the walk-through paragraph, which the pages do not state.

Method: documentation only; no commands were run.
