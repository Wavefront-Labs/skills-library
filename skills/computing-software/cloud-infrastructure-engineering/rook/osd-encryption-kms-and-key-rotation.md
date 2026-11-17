---
id: computing-software.cloud-infrastructure-engineering.rook.osd-encryption-kms-and-key-rotation
name: osd-encryption-kms-and-key-rotation
category: computing-software
field: cloud-infrastructure-engineering
product: rook
tags: [encrypted, kms, vault, keyrotation, connectiondetails, tokensecretname, security]
level: sme
status: docs-checked
description: "Encrypt PVC-based OSDs with encrypted true, store keys in Kubernetes Secrets or a KMS such as Vault, and rotate keys on a cron schedule."
sources:
  - https://rook.io/docs/rook/latest-release/Storage-Configuration/Advanced/key-management-system/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Rook can encrypt OSDs on PVC clusters with `encrypted: true` in the `storageClassDeviceSets` template. By default the key encryption keys are stored in a Kubernetes Secret; if a Key Management System exists, Rook can use it. Rook can also rotate OSD encryption keys with a CronJob per OSD.

The cluster CR `security` section:
- `security.kms.connectionDetails`: the list of KMS connection parameters.
- `security.kms.tokenSecretName`: the Secret holding the KMS auth token.
- `security.keyRotation.enabled`: default false.
- `security.keyRotation.schedule`: cron format, default `@weekly`.

Key rotation is currently supported when KEKs are in a Kubernetes Secret or in Vault KMS.

Supported KMS options include HashiCorp Vault, IBM Key Protect, KMIP and Azure Key Vault.

Vault authentication has two methods:
- Token-based: a user-provided token stored in a Secret named by `tokenSecretName` (for example `rook-vault-token` with a `token` key holding the base64 token). The token expires and must be renewed by updating the Secret.
- Kubernetes ServiceAccount: Vault's native Kubernetes authentication, which avoids token renewal problems and is generally recommended over tokens.

Rook supports all Vault environment variables. A token is created in Vault with the vault CLI according to its own docs, with the policy given in the next section of the page.

## Checked

2026-11-03. Confirmed against the Key Management System page: encrypted: true on PVC clusters, connectionDetails, tokenSecretName, keyRotation enabled (default false) and schedule (default @weekly), rotation support for Secret and Vault KEKs, the list of KMS options including Azure Key Vault, and token versus Kubernetes ServiceAccount auth. Removed: nothing.

Method: documentation only; no commands were run.
