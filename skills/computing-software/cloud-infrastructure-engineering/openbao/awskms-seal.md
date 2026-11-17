---
id: computing-software.cloud-infrastructure-engineering.openbao.awskms-seal
name: awskms-seal
category: computing-software
field: cloud-infrastructure-engineering
product: openbao
tags: [openbao, awskms, auto-unseal, kms-key-id, iam]
level: advanced
status: docs-checked
description: "Auto-unseal OpenBao with AWS KMS: stanza parameters, credentials via environment, required kms actions and key rotation caveat."
sources:
  - https://raw.githubusercontent.com/openbao/openbao/main/website/content/docs/configuration/seal/awskms.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# AWS KMS seal

The seal is distributed as an external plugin in the openbao-plugins collection.

```hcl
seal "awskms" {
  region     = "<region>"
  kms_key_id = "<key id, ARN or alias/key-alias-name>"
  endpoint   = "<optional VPC endpoint URL>"
}
```

## Parameters

- `region`: defaults to `us-east-1`; may come from env, `~/.aws/config` or instance metadata
- `access_key` (`AWS_ACCESS_KEY_ID`), `secret_key` (`AWS_SECRET_ACCESS_KEY`), `session_token` (`AWS_SESSION_TOKEN`)
- `kms_key_id` (env `VAULT_AWSKMS_SEAL_KEY_ID`): key ID or ARN, or an alias
- `endpoint` (env `AWS_KMS_ENDPOINT`): useful for VPC endpoints
- `disabled`: `true` only when migrating from an auto seal

Env activation: `VAULT_SEAL_TYPE=awskms` with `VAULT_AWSKMS_SEAL_KEY_ID`; region from `AWS_REGION` or `AWS_DEFAULT_REGION`.

## IAM actions needed on the key

`kms:Encrypt`, `kms:Decrypt`, `kms:DescribeKey` (via IAM permissions, key policy or grants).

## Warnings

- Strongly prefer environment variables over config-file credentials.
- Old keys must not be disabled or deleted after rotation; they decrypt older data.

## Checked

2026-11-04. Confirmed against the AWS KMS seal page: plugin availability, parameters and the us-east-1 default, environment variables, the three kms permissions, the environment-variable recommendation and the key rotation note. Removed the claim that deleting the KMS key makes the cluster unrecoverable, which the page does not state.

Method: documentation only; no commands were run.
