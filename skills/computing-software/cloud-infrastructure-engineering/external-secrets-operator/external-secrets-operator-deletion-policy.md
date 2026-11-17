---
id: computing-software.cloud-infrastructure-engineering.external-secrets-operator.external-secrets-operator-deletion-policy
name: external-secrets-operator-deletion-policy
category: computing-software
field: cloud-infrastructure-engineering
product: external-secrets-operator
tags: [deletionpolicy, retain, delete, secretsyncederror]
level: advanced
status: docs-checked
description: "Set deletionPolicy Retain, Delete or Merge to control what happens when a secret disappears from the provider, and avoid forbidden combinations."
sources:
  - https://raw.githubusercontent.com/external-secrets/external-secrets/main/docs/guides/ownership-deletion-policy.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`deletionPolicy` governs what happens when a secret is deleted from the provider (not when the ExternalSecret is deleted). It is only supported by some providers (see the stability and support table).
- `Retain` (default): keep the Kubernetes Secret if all provider secrets are gone. A missing provider secret puts the ExternalSecret into `SecretSyncedError`.
- `Delete`: delete the Secret when all provider secrets are gone. A deleted or inaccessible provider secret is not an error, and the same holds for a new ExternalSecret pointing at non-existing secrets. It only takes effect with `creationPolicy=Owner`; the operator refuses to delete a Secret it does not own.
- `Merge`: remove the keys from the Secret but keep the Secret itself, also without error.

Combinations rejected because they would delete existing secrets: `Delete` with `Merge`, `CreateOrMerge` or `None`; and `Merge` with `None`.

Deletion is detected only on a re-sync: never under `CreatedOnce`, on an ExternalSecret change under `OnChange`, and at the next interval under `Periodic`.

## Checked

2026-11-03. Claims were read against guides/ownership-deletion-policy.md in the external-secrets docs source. Removed: nothing.

Method: documentation only; no commands were run.
