---
id: computing-software.cloud-infrastructure-engineering.cortex.cortex-v1-compatibility-guarantees
name: cortex-v1-compatibility-guarantees
category: computing-software
field: cloud-infrastructure-engineering
product: cortex
tags: [upgrades, compatibility, deprecated-flags, experimental-features]
level: practitioner
status: docs-checked
description: "Know Cortex's stability promises for flags, config, old data and the Prometheus API, and which features are experimental."
sources:
  - https://github.com/cortexproject/cortex/blob/master/docs/configuration/v1-guarantees.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Upgrading from one minor version to the next is meant to just work. Deprecated flags are kept for two minor releases, and the metric `deprecated_flags_inuse_total` lets you alert on any you still use. The same two-minor-version rule applies to config file changes, with a metric for it too.

Data compatibility: maintainers commit that future versions can read data written by versions up to two years old.

API compatibility: Cortex aims to be 100% compatible with the Prometheus API under `/prometheus/*` and `/api/prom/*`, and any deviation is a bug, except extra endpoints for alerts and recording rules, the push API under `/api/push`, and endpoints for managing Cortex itself, such as the ring, which carry no compatibility guarantee.

Experimental features carry no backward compatibility promise and their config and flags can break. The list includes the Overrides API (runtime configuration of tenant limits) and several ruler features: evaluating rules via the query frontend with `-ruler.frontend-address`, the response format flag `-ruler.query-response-format`, and federated rule groups (`-ruler.enable-federated-rules` and the allowed and disallowed tenant lists). Check the page before using these in production.

## Checked

Method: docs-checked 2026-11-09 against the Cortex v1-guarantees.md (raw markdown, master; read the guarantees and the start of the experimental list). Claims match the page.
