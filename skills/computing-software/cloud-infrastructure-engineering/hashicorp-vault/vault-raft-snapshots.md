---
id: computing-software.cloud-infrastructure-engineering.hashicorp-vault.vault-raft-snapshots
name: vault-raft-snapshots
category: computing-software
field: cloud-infrastructure-engineering
product: hashicorp-vault
tags: [vault, raft-snapshot, vault-backup, snapshot-restore]
level: practitioner
status: docs-checked
description: "Back up Vault integrated storage with operator raft snapshot save, restore it, and wait for post-unseal setup to complete."
sources: ["https://developer.hashicorp.com/vault/docs/commands/operator/raft"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Snapshots capture all Vault data on an integrated-storage cluster. They are the main backup mechanism.

```sh
vault operator raft snapshot save vault-$(date +%F-%H%M).snap
vault operator raft snapshot inspect <snapshot>.snap
vault operator raft snapshot restore -force <snapshot>.snap
```

Schedule saves from a periodic job and copy them off-site encrypted.

Gotchas: save is supported only when Raft is the storage backend, not when used only for HA. A restore needs a working cluster on integrated storage and the original cluster unseal keys. `-force` is required when the auto-unseal or Shamir keys are not consistent with the snapshot data, which came from a different cluster. The snapshot contains secrets, so encrypt it.

## Checked

2026-11-03. Confirmed against the Vault `operator raft` command page (`snapshot save`, `inspect`, `restore`; no snapshots when Raft is only HA storage) and the Vault "Restore a snapshot" page (original unseal keys needed, `-force` for a snapshot from a different cluster). Removed: asynchronous-restore log wording, dedicated-token advice and an invented verify step.

Method: documentation only; no commands were run.
