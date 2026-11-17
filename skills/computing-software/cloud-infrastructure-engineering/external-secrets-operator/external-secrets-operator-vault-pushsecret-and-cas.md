---
id: computing-software.cloud-infrastructure-engineering.external-secrets-operator.external-secrets-operator-vault-pushsecret-and-cas
name: external-secrets-operator-vault-pushsecret-and-cas
category: computing-software
field: cloud-infrastructure-engineering
product: external-secrets-operator
tags: [vault, pushsecret, check-and-set, kv-v2]
level: advanced
status: docs-checked
description: "Push secrets into Vault with required policy permissions and enable check-and-set to prevent concurrent overwrites."
sources:
  - https://raw.githubusercontent.com/external-secrets/external-secrets/main/docs/provider/hashicorp-vault.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
PushSecret to Vault needs the pushed key to be valid JSON, or a `property` in `remoteRef`. Grant `create`, `read` and `update` on both the `data` and `metadata` paths you push to. KV v1 has no metadata API, so ESO adds a `custom_metadata` map to each secret and a pushed key named `custom_metadata` is not supported there.

Check-And-Set protects against overwrites when several clients write the same KV v2 secret:

```yaml
spec:
  provider:
    vault:
      version: "v2"
      checkAndSet:
        required: true
```

With `required: true` every PushSecret write carries a version: CAS version 0 for new secrets, and for existing ones ESO reads the current version first. CAS works only with KV v2.

## Checked

2026-11-03. Claims were read against provider/hashicorp-vault.md in the external-secrets docs source. Removed: nothing.

Method: documentation only; no commands were run.
