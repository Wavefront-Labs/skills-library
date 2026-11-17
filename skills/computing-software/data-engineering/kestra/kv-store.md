---
id: computing-software.data-engineering.kestra.kv-store
name: kv-store
category: computing-software
field: data-engineering
product: kestra
tags: [kv-store, state, ttl, kv-function, namespace, set-get-delete]
level: practitioner
status: docs-checked
description: "Persist state across Kestra executions with the namespace-scoped KV Store: Set, Get, GetKeys, Delete tasks, the kv() function, TTL and missing-key behaviour."
sources:
  - https://kestra.io/docs/concepts/kv-store
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Kestra executions are stateless by design; the KV Store carries data between runs and flows. Values live in internal storage; the database holds only metadata (key, TTL, timestamps). Pairs are scoped to a namespace.

Values are typed: string, number, boolean, datetime, date, duration, JSON. A pair may have an optional TTL (ISO 8601 or standard duration) after which it expires.

Tasks:

- `Set`: `key`, `value`, `namespace`, `overwrite` (default `true`; false fails if the key exists), optional `ttl`.
- `Get`: returns `value`; supports `errorOnMissing`.
- `GetKeys`: keys matching a `prefix`, or an empty list.
- `Delete`: returns a boolean `deleted`.

The `kv()` function reads inline: key, optional namespace, and `errorOnMissing`. A missing key fails the task by default; `errorOnMissing` false returns `null`. Wrap JSON values in `fromJson()` to read properties.

Use Variables for single-execution values and Secrets for sensitive ones. Other access: UI (copy gives a ready `kv()` expression), REST API, Terraform `kestra_kv`, `kestractl kv`.

KV pairs are readable across namespaces when those namespaces are allowed.

## Checked

2026-11-04. Confirmed against the Kestra KV Store page: namespace-scoped pairs with values in internal storage and metadata in the database, the seven value types, optional TTL, Set (overwrite default true), Get, GetKeys and Delete behaviour, kv() signature and errorOnMissing, fromJson() for JSON values, UI copy of the kv() expression, REST API, Terraform kestra_kv, kestractl kv. Reworded the cross-namespace sentence to the page's own wording (readable when those namespaces are allowed) instead of an unstated permissions claim.

Method: documentation only; no commands were run.
