---
id: computing-software.cloud-infrastructure-engineering.external-secrets-operator.external-secrets-operator-aws-secretsmanager-pushsecret
name: external-secrets-operator-aws-secretsmanager-pushsecret
category: computing-software
field: cloud-infrastructure-engineering
product: external-secrets-operator
tags: [aws-secrets-manager, pushsecret, kms, replication]
level: advanced
status: docs-checked
description: "Push to AWS Secrets Manager with PushSecret, the extra IAM actions, and metadata for KMS, tags, replication and resource policies."
sources:
  - https://raw.githubusercontent.com/external-secrets/external-secrets/main/docs/provider/aws-secrets-manager.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
For `PushSecret` add to the IAM policy: `CreateSecret`, `PutSecretValue`, `TagResource`, `DeleteSecret`. The resource-policy actions (`GetResourcePolicy`, `PutResourcePolicy`, `DeleteResourcePolicy`) are needed only with `resourcePolicy`, and `ReplicateSecretToRegions` and `RemoveRegionsFromReplication` only with `replicationLocations`. A stricter policy can limit `DeleteSecret` to secrets carrying a given tag.

Per-entry `metadata`:
- `secretPushFormat`: `binary` (default) or `string`.
- `kmsKeyID`: key ID or ARN; default `alias/aws/secretsmanager`. A single key applies to the primary and all replicas.
- `description`, `tags`, `replicationLocations` (list of regions).
- `resourcePolicy` with `blockPublicPolicy` and `policySourceRef` (kind `ConfigMap` or `Secret`, `name`, `key` holding the policy JSON) for cross-account access.

ESO treats the PushSecret as the source of truth for tags, resource policy and replication: items not listed that exist remotely are removed.

## Checked

2026-11-03. Claims were read against provider/aws-secrets-manager.md in the external-secrets docs source. Removed: nothing.

Method: documentation only; no commands were run.
