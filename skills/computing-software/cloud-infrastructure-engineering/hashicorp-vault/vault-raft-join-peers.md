---
id: computing-software.cloud-infrastructure-engineering.hashicorp-vault.vault-raft-join-peers
name: vault-raft-join-peers
category: computing-software
field: cloud-infrastructure-engineering
product: hashicorp-vault
tags: [vault, raft-join, raft-list-peers, remove-peer]
level: practitioner
status: docs-checked
description: "Add a Vault node with operator raft join, remove one with remove-peer, and wipe data before a removed node rejoins."
sources: ["https://developer.hashicorp.com/vault/docs/commands/operator/raft", "https://developer.hashicorp.com/vault/docs/configuration/storage/raft"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Join order depends on how Raft is used. With Raft as `storage`, join first and then unseal; with Raft only as `ha_storage`, unseal first and do not pass the leader address.

```sh
vault operator raft join https://vault-0.example.com:8200
vault operator raft list-peers
vault operator raft remove-peer vault-3
```

Certificate flags (`-leader-ca-cert`, `-leader-client-cert`, `-leader-client-key`) take the certificate or key contents, not file paths.

Gotchas: a removed node cannot rejoin until Vault is stopped and its Raft data deleted, otherwise it retains stale membership. `list-peers` and `remove-peer` accept a DR operation token (`-dr-token`). `remove-peer` is also for a failed peer left in the Raft configuration after the server is gone, so it no longer affects quorum. Replacing a node: join the new one, confirm in `list-peers` that it was promoted to a voter, then remove the old.

## Checked

2026-11-03. Confirmed against the Vault `operator raft` command page (join order for `storage` versus `ha_storage`, certificate flags take contents not paths, `remove-peer` note on deleting Raft data, `list-peers` output). Removed: DR peer-set mirroring, odd-voter advice and an invented verify step.

Method: documentation only; no commands were run.
