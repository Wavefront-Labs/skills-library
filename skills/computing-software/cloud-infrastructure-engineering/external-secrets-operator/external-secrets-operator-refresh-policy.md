---
id: computing-software.cloud-infrastructure-engineering.external-secrets-operator.external-secrets-operator-refresh-policy
name: external-secrets-operator-refresh-policy
category: computing-software
field: cloud-infrastructure-engineering
product: external-secrets-operator
tags: [refreshpolicy, refreshinterval, externalsecret, sync]
level: practitioner
status: docs-checked
description: "Choose an ExternalSecret refreshPolicy of Periodic, OnChange or CreatedOnce and know when provider changes are actually pulled."
sources:
  - https://raw.githubusercontent.com/external-secrets/external-secrets/main/docs/guides/ownership-deletion-policy.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`spec.refreshPolicy` defines how the operator refreshes the target Secret:
- `Periodic` (default): refresh at the fixed `spec.refreshInterval`. For backwards compatibility an interval of 0 behaves like `CreatedOnce`.
- `OnChange`: refresh only when the ExternalSecret itself is updated.
- `CreatedOnce`: sync once, on the first reconcile of that ExternalSecret object.

ESO is pull-based and does not watch providers, so only `Periodic` notices a changed provider value (at each interval). `OnChange` re-syncs when the ExternalSecret spec or metadata changes, or when you set the `force-sync` annotation. `CreatedOnce` never re-syncs.

The sync state for `CreatedOnce` lives in the ExternalSecret status, so deleting and recreating the object resets it and triggers another one-time sync, which may overwrite operator-managed keys of an existing Secret. `creationPolicy=None` does not update it, and `spec.target.immutable: true` prevents data rewrites. Provider-side deletions are only detected on a re-sync, so under `CreatedOnce` they are never detected.

## Checked

2026-11-03. Claims were read against guides/ownership-deletion-policy.md in the external-secrets docs source. Removed: nothing.

Method: documentation only; no commands were run.
