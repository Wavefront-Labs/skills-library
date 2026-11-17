---
id: computing-software.cloud-infrastructure-engineering.hashicorp-vault.vault-upgrade-procedure
name: vault-upgrade-procedure
category: computing-software
field: cloud-infrastructure-engineering
product: hashicorp-vault
tags: [vault, vault-upgrade, rolling-upgrade, vault-version]
level: practitioner
status: docs-checked
description: "Upgrade Vault HA with a snapshot first, standbys first and the active node last, shutting it down cleanly instead of using step-down."
sources: ["https://developer.hashicorp.com/vault/docs/upgrade/vault-ha-upgrade", "https://developer.hashicorp.com/vault/docs/commands/operator/raft", "https://developer.hashicorp.com/vault/docs/concepts/ha"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Read the upgrade guide and the version-specific upgrade notes for each version crossed. This is the procedure for Vault without Autopilot upgrade automation (earlier than 1.11, opted out, or an external storage backend).

```sh
vault operator raft snapshot save pre-upgrade.snap
# standbys first
# on each standby: stop Vault with SIGINT or SIGTERM, replace the binary, start it
vault operator unseal   # if Shamir
vault status            # check Version, and HA Mode is standby
# then stop the active node the same way and repeat; do not run operator step-down
```

Gotchas: take the snapshot first, because rolling back means replacing the upgraded data store with the pre-upgrade snapshot. Upgrade standbys first. Then shut the active node down properly (`SIGINT` or `SIGTERM`) so it releases the HA lock and a standby takes over quickly; if Vault is killed without releasing the lock, a standby cannot take over until the lock timeout expires. Do not issue `operator step-down` during the upgrade, and never fail over from a newer version to an older one. Add `mlock()` capability to the new binary with setcap unless `disable_mlock` is set. Vault does not support true zero-downtime upgrades. Run upgrade and restore tests in an isolated network environment.

## Checked

2026-11-03. Confirmed against the Vault "HA upgrades without Autopilot upgrade automation" page and the upgrade rollback page and the restore-a-snapshot page (isolation of test instances). Removed: the instruction to run `operator step-down` on the active node (the docs say not to), version-skipping advice, plugin re-registration claim and an invented verify step.

Method: documentation only; no commands were run.
