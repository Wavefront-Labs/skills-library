---
id: computing-software.cloud-infrastructure-engineering.hashicorp-vault.vault-rekey-unseal-keys
name: vault-rekey-unseal-keys
category: computing-software
field: cloud-infrastructure-engineering
product: hashicorp-vault
tags: [vault, operator-rekey, rekey, key-rotation]
level: practitioner
status: docs-checked
description: "Rotate Vault unseal or recovery key shares with operator rekey, changing share counts and holders without downtime."
sources: ["https://developer.hashicorp.com/vault/docs/commands/operator/rekey"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Rekeying generates new shares for the same root key, used when custodians change or a share may be exposed. It needs Vault unsealed and a quorum of the existing shares, and causes no downtime.

```sh
vault operator rekey -init -key-shares=5 -key-threshold=3 -pgp-keys="a.asc,b.asc,c.asc,d.asc,e.asc"
vault operator rekey -nonce=<nonce>        # enter existing shares until threshold met
vault operator rekey -status
vault operator rekey -cancel
vault operator rekey -target=recovery -init   # for auto-unseal clusters
```

`-verify` runs a verification step to prove the new shares before they replace the old ones.

Gotchas: threshold must not exceed shares. The `-nonce` from init must accompany every submitted share. The default target is the barrier key; recovery rekey applies only with auto unseal or an HSM. `-backup` stores a backup of the current PGP-encrypted unseal keys in Vault's core, and applies only when the existing unseal keys were PGP-encrypted (`-backup-retrieve` and `-backup-delete` manage it). With `-pgp-keys`, the number of entries must match the share count. Rekeying does not rotate the underlying encryption key (that is `vault operator rotate`).

## Checked

2026-11-03. Confirmed against the Vault `operator rekey` and `operator rotate` command pages and the seal concepts page: zero downtime, needs unsealed Vault and a quorum of existing keys, flags `-init`, `-key-shares`, `-key-threshold`, `-nonce`, `-pgp-keys`, `-status`, `-cancel`, `-verify`, `-target` (default `barrier`; `recovery` for auto unseal or HSM), `-backup` options. Removed: share-distribution advice and an invented verify step.

Method: documentation only; no commands were run.
