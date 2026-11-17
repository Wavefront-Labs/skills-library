---
id: computing-software.cloud-infrastructure-engineering.hashicorp-vault.vault-audit-devices
name: vault-audit-devices
category: computing-software
field: cloud-infrastructure-engineering
product: hashicorp-vault
tags: [vault, audit-devices, audit-log, audit-hash]
level: practitioner
status: docs-checked
description: "Enable at least two Vault audit devices, understand fail-closed behaviour, hashing of sensitive values, and log rotation."
sources: ["https://developer.hashicorp.com/vault/docs/audit"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Auditing is off on a new cluster. Enable devices before applications connect.

```sh
vault audit enable file file_path=/var/log/vault/audit.log
vault audit enable -path=audit_syslog syslog tag=vault
vault audit list -detailed
vault write sys/audit-hash/file input="known-value"
```

Gotchas: if Vault cannot write to any enabled audit device it refuses requests, so enable at least two devices and monitor disk space and log shipping. Vault does not hash non-string values such as integers and booleans, so send sensitive data as strings. Disabling a device loses the ability to compute hashes for its old entries. The `local` option applies only to performance replication and marks the device as local to the cluster. Use `elide_list_responses` for big LIST outputs. Rotate files with `SIGHUP` and logrotate.

## Checked

2026-11-03. Confirmed against the Vault audit devices page, the file audit device page and the `/sys/audit` and `/sys/audit-hash` API pages: auditing is off on a new cluster, refusal when no device can log, advice to enable at least two, non-string values not hashed, `elide_list_responses`, `SIGHUP` log rotation, `local`, and loss of hash computation after disabling. Removed: per-device salt, DR secondary audit behaviour, header logging from the description, an invented verify step and a generic tip.

Method: documentation only; no commands were run.
