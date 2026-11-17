---
id: computing-software.cloud-infrastructure-engineering.external-secrets-operator.external-secrets-operator-azure-keyvault-pushsecret
name: external-secrets-operator-azure-keyvault-pushsecret
category: computing-software
field: cloud-infrastructure-engineering
product: external-secrets-operator
tags: [azure-key-vault, pushsecret, rbac-roles, soft-delete]
level: advanced
status: docs-checked
description: "Push Kubernetes Secrets into Azure Key Vault as secrets, keys or certificates, with the needed roles and soft-delete caveats."
sources:
  - https://raw.githubusercontent.com/external-secrets/external-secrets/main/docs/provider/azure-key-vault.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
PushSecret can create, update or delete Key Vault secrets, keys and certificates.

Secrets: optional per-entry `metadata` with `expirationDate` (RFC 3339, for example `2099-12-31T23:59:59Z`), `contentType` and `tags`. Needs the Key Vault Secrets Officer role. Notes: a write that conflicts with a soft-deleted secret recovers it only if it has the tag `managed-by: external-secrets`; omitting `contentType` means unchanged, not cleared; `expirationDate` applies only with the legacy SDK (it is ignored when `useAzureSDK: true`, which `customCloudConfig` requires).

Keys: private key in `PRIVATE KEY`, `RSA PRIVATE KEY` or `EC PRIVATE KEY` PEM; needs Key Vault Crypto Officer or equivalent access policy.

Certificates: P12 recommended and it must contain both certificate and a PKCS8 private key. PEM certificate and key can be converted to P12 by the PushSecret template. With cert-manager, set `spec.privateKey.encoding` to `PKCS8`, since its default is PKCS1.

## Checked

2026-11-03. Claims were read against provider/azure-key-vault.md in the external-secrets docs source. Removed: nothing.

Method: documentation only; no commands were run.
