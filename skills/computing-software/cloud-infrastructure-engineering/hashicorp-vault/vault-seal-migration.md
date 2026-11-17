---
id: computing-software.cloud-infrastructure-engineering.hashicorp-vault.vault-seal-migration
name: vault-seal-migration
category: computing-software
field: cloud-infrastructure-engineering
product: hashicorp-vault
tags: [vault, seal-migration, unseal-migrate, seal-ha]
level: practitioner
status: docs-checked
description: "Migrate from Shamir to auto unseal, or between auto seals, with the -migrate flag and a backup snapshot taken first."
sources: ["https://developer.hashicorp.com/vault/docs/concepts/seal", "https://developer.hashicorp.com/vault/docs/commands/operator/rekey"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Seal migration changes how the root key is protected. Seal migration outside Seal HA requires briefly taking the whole cluster down, and both old and new seals must be available during the operation.

```sh
vault operator raft snapshot save pre-seal-migration.snap
# edit config: add the new auto seal block; for auto-to-other or auto-to-Shamir, set disabled = true on the old seal block
vault operator unseal -migrate
vault operator rekey -target=recovery -init -key-shares=5 -key-threshold=3
```

The unseal keys of the old seal become recovery keys after migration. Enterprise Seal HA allows two or three auto seals and online migration, monitored with `sys/seal-backend-status` until `fully_wrapped` is true.

Gotchas: take standby nodes down one at a time and unseal each with `-migrate`, bringing each back before the next, then step down the active node; the new active node performs the migration. With integrated storage, take the cluster offline and update every node's seal configuration together so a quorum comes back. Any change to the `seal` stanza invokes seal rewrap. Seal HA does not support migrating Shamir seals.

## Checked

2026-11-03. Confirmed against the Vault seal concepts page (seal migration section: downtime, both seals available, `-migrate`, `disabled = true`, standby-first sequence, integrated storage variant, recovery key conversion, Seal HA with two to three auto seals, `sys/seal-backend-status` and `fully_wrapped`). Removed: reversed node order (active first), config-change blocking claim, old-key retention advice and an invented verify step. The rekey command is covered by the `operator rekey` page.

Method: documentation only; no commands were run.
