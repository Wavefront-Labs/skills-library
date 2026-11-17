---
id: computing-software.cloud-infrastructure-engineering.hashicorp-vault.vault-auto-unseal
name: vault-auto-unseal
category: computing-software
field: cloud-infrastructure-engineering
product: hashicorp-vault
tags: [vault, auto-unseal, seal-stanza, recovery-keys]
level: practitioner
status: docs-checked
description: "Auto unseal Vault with a cloud KMS, HSM or another Vault's transit key, and understand recovery keys and the lost-key risk."
sources: ["https://developer.hashicorp.com/vault/docs/concepts/seal", "https://developer.hashicorp.com/vault/docs/commands/operator/init", "https://developer.hashicorp.com/vault/docs/commands/operator/rekey", "https://developer.hashicorp.com/vault/docs/configuration/seal/awskms"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
With auto unseal, a trusted external key decrypts the root key at startup, so nodes unseal themselves after a restart.

```hcl
seal "awskms" {
  region     = "eu-west-1"
  kms_key_id = "<key-id>"
}
```

Other seals include `gcpckms`, `azurekeyvault`, `pkcs11` (HSM) and `transit`. Initialising with a seal returns recovery keys rather than unseal keys; they authorise operations such as `generate-root` and `rekey -target=recovery`, but cannot unseal Vault.

Gotchas: auto unseal creates a strict lifecycle dependency on the seal mechanism. If it (for example the cloud KMS key) becomes unavailable or is deleted before you migrate the seal, you cannot recover access to the cluster until it is available again. Recovery keys cannot decrypt the root key. Seal migration cannot be done without downtime (the cluster is briefly taken down; Enterprise seal HA from Vault 1.16 allows online migration between most auto-unseal types) and needs both old and new seals available; take a backup first.

## Checked

2026-11-03. Confirmed on the Seal concepts, operator init, operator rekey, awskms/gcpckms/azurekeyvault/transit/pkcs11 seal pages: auto unseal delegates the unseal key to a trusted service, initialisation returns recovery keys, recovery keys authorise operations such as generate-root and `vault operator rekey -target=recovery`, recovery keys cannot unseal, seal migration downtime and the both-seals-available requirement, and the awskms `region` and `kms_key_id` fields. Removed: KMS deletion-protection and IAM advice, the unconfirmed claim that restarted nodes stay sealed when the KMS is unreachable beyond the documented dependency, and the invented Verify step.

Method: documentation only; no commands were run.
