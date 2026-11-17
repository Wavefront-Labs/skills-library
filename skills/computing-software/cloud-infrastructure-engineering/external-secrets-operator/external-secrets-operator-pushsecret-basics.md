---
id: computing-software.cloud-infrastructure-engineering.external-secrets-operator.external-secrets-operator-pushsecret-basics
name: external-secrets-operator-pushsecret-basics
category: computing-software
field: cloud-infrastructure-engineering
product: external-secrets-operator
tags: [pushsecret, updatepolicy, deletionpolicy, reverse-sync]
level: practitioner
status: docs-checked
description: "Push a local Kubernetes Secret to a provider with PushSecret and control overwrites with updatePolicy and cleanup with deletionPolicy."
sources:
  - https://raw.githubusercontent.com/external-secrets/external-secrets/main/docs/guides/pushsecrets.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`PushSecret` is the reverse of `ExternalSecret`: it reads a local `kind=Secret` and writes its content to a secret provider.

`spec.updatePolicy`:
- `Replace` (default): overwrite the provider secret regardless of whether one exists at that location.
- `IfNotExists`: never overwrite; the provider is the source of truth. The in-cluster value may then differ from the provider value.

`spec.deletionPolicy`: by default the provider secret is not deleted when the PushSecret is deleted. Set `deletionPolicy: Delete` to remove it too.

## Checked

2026-11-03. Claims were read against guides/pushsecrets.md in the external-secrets docs source. Removed: a closing pointer to provider docs.

Method: documentation only; no commands were run.
