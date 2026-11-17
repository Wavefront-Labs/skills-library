---
id: computing-software.cloud-infrastructure-engineering.external-secrets-operator.external-secrets-operator-vault-enterprise-and-token-cache
name: external-secrets-operator-vault-enterprise-and-token-cache
category: computing-software
field: cloud-infrastructure-engineering
product: external-secrets-operator
tags: [vault, namespaces, token-cache, performance-standby]
level: sme
status: docs-checked
description: "Tune ESO against Vault Enterprise namespaces, performance standby consistency and the optional token cache."
sources:
  - https://raw.githubusercontent.com/external-secrets/external-secrets/main/docs/provider/hashicorp-vault.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Namespaces: set `provider.vault.namespace`; authenticate into another namespace with `provider.vault.auth.namespace`. Performance standby nodes are eventually consistent, so a read just after login can fail if the login has not propagated; the docs offer the read-your-writes and forward-inconsistent options as solutions.

Token cache flags on the controller: `--enable-vault-token-cache` (default false) and `--vault-token-cache-size` (default 262144). The cache key is store name, namespace and kind; the TTL is checked before reuse; least recently used tokens are evicted and revoked in Vault. It helps with short-lived tokens from AppRole or Kubernetes auth, by cutting login requests.

## Checked

2026-11-03. Claims were read against provider/hashicorp-vault.md in the external-secrets docs source. Removed: nothing.

Method: documentation only; no commands were run.
