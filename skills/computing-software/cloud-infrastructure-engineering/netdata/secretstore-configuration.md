---
id: computing-software.cloud-infrastructure-engineering.netdata.secretstore-configuration
name: secretstore-configuration
category: computing-software
field: cloud-infrastructure-engineering
product: netdata
tags: [netdata, secretstore, vault, aws-secrets-manager]
level: advanced
status: docs-checked
description: "Configure go.d secretstores for Vault, AWS Secrets Manager, Azure Key Vault and Google Secret Manager, with file locations, operand formats and restart behaviour."
sources:
  - https://raw.githubusercontent.com/netdata/netdata/master/src/collectors/SECRETS.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Configure the store first, then reference it with `${store:<kind>:<name>:<operand>}`.

Where: Dynamic Configuration at Collectors, go.d, SecretStores, or files in `/etc/netdata/go.d/ss/`: `aws-sm.conf`, `azure-kv.conf`, `gcp-sm.conf`, `vault.conf`. The filename picks the backend; each file has a `jobs` array.

| Backend | Kind | Operand |
|---|---|---|
| AWS Secrets Manager | `aws-sm` | `secret-name[#key]` |
| Azure Key Vault | `azure-kv` | `vault-name/secret-name` |
| Google Secret Manager | `gcp-sm` | `project/secret[/version]` |
| Vault | `vault` | `path#key` |

Example reference:

```
password: "${store:vault:vault_prod:secret/data/netdata/mysql#password}"
```

Steps:
1. If missing, create the directory: `sudo mkdir -p /etc/netdata/go.d/ss`, owner `netdata:netdata`, mode `0750`.
2. Create the backend file; restrict permissions to the `netdata` user (tokens and client secrets may be inside).
3. Restart the Agent (files load at startup).

Gotchas:
- `${store:...}` is not supported inside secretstore configs; use `${env:...}`, `${file:...}` or `${cmd:...}` for their tokens.
- Prefer instance roles, managed identities or metadata credentials where supported.
- Updating a store restarts running and failed jobs that use it; accepted or disabled jobs pick it up on next start.

## Checked

2026-11-04. Confirmed against the Netdata Secrets page: the four backend files under /etc/netdata/go.d/ss/ and the jobs array, the kind and operand table, the store reference form, directory creation with owner and mode 0750, permission advice, startup loading and restart, the no-nested-store rule, platform-native identity advice, and restart behaviour on store updates. Nothing removed.

Method: documentation only; no commands were run.
