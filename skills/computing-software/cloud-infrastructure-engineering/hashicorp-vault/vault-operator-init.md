---
id: computing-software.cloud-infrastructure-engineering.hashicorp-vault.vault-operator-init
name: vault-operator-init
category: computing-software
field: cloud-infrastructure-engineering
product: hashicorp-vault
tags: [vault, operator-init, vault-init, key-shares]
level: practitioner
status: docs-checked
description: "Initialise Vault once with operator init, choose key shares and threshold, and distribute unseal keys and the initial root token safely."
sources: ["https://developer.hashicorp.com/vault/docs/commands/operator/init", "https://developer.hashicorp.com/vault/docs/concepts/seal"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Initialisation happens once per cluster, on one node; the others share the same storage. It generates the root key split into unseal key shares (Shamir) and the initial root token.

```sh
vault operator init -key-shares=5 -key-threshold=3 -format=json > init.json   # handle as a secret
vault operator init -status; echo $?     # 0 initialised, 2 not initialised, 1 error
```

Use `-pgp-keys` to encrypt each share to a different operator's key so no single person sees all shares, and `-root-token-pgp-key` for the root token. With auto unseal, the shares become recovery keys (`-recovery-shares`, `-recovery-threshold`).

Gotchas: the threshold must not exceed the share count. The init output holds the shares and root token, so treat the saved file as a secret and do not keep it in a repository or shared drive. The command cannot be run against an already-initialised cluster, and nodes sharing the same storage in HA mode need only one init. With PGP keys, the number of entries must match `-key-shares`.

## Checked

2026-11-03. Confirmed against the Vault `operator init` command page (flags, `-status` exit codes 0/1/2, recovery flags for auto unseal only, one init per shared storage) and the seal concepts page. Removed: share-loss arithmetic and an invented verify step.

Method: documentation only; no commands were run.
