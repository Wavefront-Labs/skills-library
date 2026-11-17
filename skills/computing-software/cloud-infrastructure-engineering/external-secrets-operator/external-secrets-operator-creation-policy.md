---
id: computing-software.cloud-infrastructure-engineering.external-secrets-operator.external-secrets-operator-creation-policy
name: external-secrets-operator-creation-policy
category: computing-software
field: cloud-infrastructure-engineering
product: external-secrets-operator
tags: [creationpolicy, owner, orphan, merge]
level: practitioner
status: docs-checked
description: "Pick an ExternalSecret target creationPolicy of Owner, Orphan, Merge, CreateOrMerge or None and understand garbage collection."
sources:
  - https://raw.githubusercontent.com/external-secrets/external-secrets/main/docs/guides/ownership-deletion-policy.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`spec.target.creationPolicy` controls how the target Secret is created:
- `Owner` (default): ESO creates the Secret and sets an `ownerReference`, so Kubernetes garbage-collects it when the ExternalSecret is deleted. A same-name Secret owned by someone else is a conflict and errors. An existing Secret with no ownerReference is treated as orphaned and ESO adopts it.
- `Orphan`: creates and updates the Secret but sets no ownerReference, so deleting the ExternalSecret leaves the Secret. Manual edits to it are overwritten on the next sync.
- `Merge`: never creates; expects the Secret to exist and merges provider values into it. Several ExternalSecrets may merge into one Secret only if their keys do not collide, otherwise they oscillate.
- `CreateOrMerge`: creates if missing, otherwise merges while preserving keys owned by others, with no ownerReference. The Secret survives ExternalSecret deletion.
- `None`: no-op, nothing is created or updated.

`spec.target.immutable: true` marks the Secret immutable so its data is never rewritten once it exists; it does not stop a missing Secret being created.

## Checked

2026-11-03. Claims were read against guides/ownership-deletion-policy.md in the external-secrets docs source. Removed: nothing.

Method: documentation only; no commands were run.
