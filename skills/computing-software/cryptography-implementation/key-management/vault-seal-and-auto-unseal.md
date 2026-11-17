---
id: computing-software.cryptography-implementation.key-management.vault-seal-and-auto-unseal
name: vault-seal-and-auto-unseal
category: computing-software
field: cryptography-implementation
product: key-management
tags: [cryptography-implementation, key-management, secrets-managers, vault-unseal, auto-unseal, shamir, recovery-keys, hashicorp-vault, kms, seal-migration]
level: practitioner
status: docs-checked
description: "Operate Vault sealing: Shamir unseal keys versus KMS or HSM auto-unseal, recovery keys, seal migration, and protecting the seal key from deletion."
sources: ["https://developer.hashicorp.com/vault/docs/concepts/seal", "https://developer.hashicorp.com/vault/docs/configuration/seal/awskms", "https://developer.hashicorp.com/vault/docs/commands/operator/init"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Vault seal and auto-unseal

A sealed Vault knows where its data is but cannot decrypt it until the seal
is satisfied.

## Shamir (default)

```bash
vault operator init -key-shares=5 -key-threshold=3 \
  -pgp-keys="keybase:a,keybase:b,keybase:c,keybase:d,keybase:e"
```

- `-key-shares` and `-key-threshold` set how many shares exist and how many
  unseal; `-pgp-keys` encrypts each share to a PGP key so no one sees all of
  them in plaintext.
- Operations that need a quorum (such as generating a root token) use the
  unseal keys.

## Auto-unseal

```hcl
seal "awskms" {
  region     = "<region>"
  kms_key_id = "alias/<key-alias>"
}
```

- `kms_key_id` takes a key ID, ARN, or an alias in the form `alias/key-alias-name`.
- Init then yields **recovery keys**, not unseal keys. They are Shamir shares of
  an internal recovery key and authorise operations such as `generate-root` and
  rekeying; Vault selects them automatically. Init options for them are
  `-recovery-shares`, `-recovery-threshold` and `-recovery-pgp-keys`.
- If the seal mechanism or its keys are permanently deleted, the cluster cannot
  be recovered, even from backups. HashiCorp recommends careful controls on the
  seal key, for example AWS Service Control Policies.

## Seal migration

Shamir to auto-unseal: take the cluster offline, change the `seal` stanza,
bring a node back and run `vault operator unseal -migrate` on every unseal
command with the Shamir keys; Vault migrates them to recovery keys. From an
auto seal, supply recovery keys with `-migrate`. Any change to the seal stanza
invokes seal rewrap. AWS KMS to AWS KMS of the same type is a documented
limitation. Read the seal concepts page for the multi-node procedure.

## Verify

- [ ] Restart test: Vault unseals (auto) or the quorum can unseal.
- [ ] Deletion of the seal key is controlled to break-glass only.

## Checked

2026-11-01. Confirmed against the Vault seal concepts page (recovery keys, generate-root, rekey, deletion warning, migration
with `-migrate`, rewrap, AWS KMS limitation), the `awskms` seal page (`region`, `kms_key_id`, alias form) and the
`operator init` page (`-key-shares`, `-key-threshold`, `-pgp-keys`, recovery options). Removed: other KMS seal type list,
CloudTrail advice, `vault status` fields, `vault operator seal`, HA step-down order, annual quorum test.
Method: documentation only; no commands were run.
