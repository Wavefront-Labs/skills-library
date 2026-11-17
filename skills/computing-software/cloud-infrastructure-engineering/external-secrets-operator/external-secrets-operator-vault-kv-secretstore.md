---
id: computing-software.cloud-infrastructure-engineering.external-secrets-operator.external-secrets-operator-vault-kv-secretstore
name: external-secrets-operator-vault-kv-secretstore
category: computing-software
field: cloud-infrastructure-engineering
product: external-secrets-operator
tags: [vault, kv, secretstore, metadatapolicy]
level: practitioner
status: docs-checked
description: "Configure an ESO SecretStore for HashiCorp Vault KV v1 or v2 and fetch values, labels and system metadata."
sources:
  - https://raw.githubusercontent.com/external-secrets/external-secrets/main/docs/provider/hashicorp-vault.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The Vault provider supports only the KV secrets engine; for other engines use the Vault generator.

```yaml
spec:
  provider:
    vault:
      server: "http://my.vault.server:8200"
      path: "secret"
      version: "v2"        # v1 or v2, default v2
      auth:
        tokenSecretRef:
          name: "vault-token"
          key: "token"
```

Check the engine version with `vault secrets list -detailed` (Options column shows `version:2`). In a ClusterSecretStore, add `namespace` to the secret reference.

ExternalSecret `remoteRef.key` is the path under the mount (`foo` for `secret/foo`) and `property` selects a field. `metadataPolicy: Fetch` returns the secret's `custom_metadata` as JSON, or a single label when `property` names it; it also exposes `created_time`, `current_version` and `delete_version_after` (all strings). Metadata fetching works only with KV v2. Leaving `property` empty returns the JSON of all key-value pairs at that path.

## Checked

2026-11-03. Claims were read against provider/hashicorp-vault.md in the external-secrets docs source. Removed: nothing.

Method: documentation only; no commands were run.
