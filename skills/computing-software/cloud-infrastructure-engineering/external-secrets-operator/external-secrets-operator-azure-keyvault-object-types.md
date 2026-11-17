---
id: computing-software.cloud-infrastructure-engineering.external-secrets-operator.external-secrets-operator-azure-keyvault-object-types
name: external-secrets-operator-azure-keyvault-object-types
category: computing-software
field: cloud-infrastructure-engineering
product: external-secrets-operator
tags: [azure-key-vault, secrets-keys-certificates, externalsecret, pkcs12]
level: practitioner
status: docs-checked
description: "Fetch Azure Key Vault secrets, keys and certificates by object-type prefix, with dataFrom and PKCS#12 certificates."
sources:
  - https://raw.githubusercontent.com/external-secrets/external-secrets/main/docs/provider/azure-key-vault.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Azure Key Vault holds three object types, selected with a prefix in `remoteRef.key`:
- `secret` (default): passwords, connection strings.
- `key`: returned as a JWK; Key Vault never exports the private key, so use template functions to turn the JWK into PEM.
- `cert`: X.509 certificates, encoded as you need through template functions.

Example `remoteRef.key`: `secret/dev-secret-test` or `cert/my-cert`. `dataFrom` can fetch all secrets in the vault or all tags in a secret. To place a P12 (PKCS12 or PFX) certificate into a `kubernetes.io/tls` Secret, fetch it with the `cert` prefix and use the PKCS#12 template functions to emit `tls.crt` and `tls.key`.

Check the result with `kubectl get secret NAME -n NS -o jsonpath='{.data.dev-secret-test}' | base64 -d`.

## Checked

2026-11-03. Claims were read against provider/azure-key-vault.md in the external-secrets docs source. Removed: nothing.

Method: documentation only; no commands were run.
