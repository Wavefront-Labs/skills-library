---
id: computing-software.cloud-infrastructure-engineering.terraform.opentofu-state-and-plan-encryption
name: opentofu-state-and-plan-encryption
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [opentofu, tofu-encryption-block, encryption-block, key-provider, pbkdf2, aws-kms-key-provider, plan-encryption, encrypted-plan, state-encryption]
level: advanced
status: docs-checked
description: "Enable OpenTofu client-side encryption of state and plan files: the encryption block, pbkdf2/KMS key providers, aes_gcm methods, enforced mode and TF_ENCRYPTION."
sources: ["https://opentofu.org/docs/language/state/encryption/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# OpenTofu state and plan encryption

Encrypts state and plan files at rest, for local storage and for backends, so a
bucket reader without the key sees ciphertext. Also works with `terraform_remote_state`.

## Minimal config (passphrase)
```hcl
terraform {
  encryption {
    key_provider "pbkdf2" "main" {
      passphrase = var.state_passphrase      # min 16 characters
    }
    method "aes_gcm" "main" {
      keys = key_provider.pbkdf2.main
    }
    state {
      method   = method.aes_gcm.main
      enforced = true                        # refuse to write unencrypted state
    }
    plan {
      method   = method.aes_gcm.main
      enforced = true
    }
  }
}
```
Variables and locals may be used in this block, but they must not reference state
data or provider-defined functions: all values must resolve during `tofu init`.
PBKDF2 defaults: `key_length` 32, `iterations` 600,000 (minimum 200,000),
`salt_length` 32, `hash_function` `sha512` (`sha256` also allowed).

## KMS key provider
```hcl
key_provider "aws_kms" "main" {
  kms_key_id = "<KMS_KEY_ID>"
  region     = "<REGION>"
  key_spec   = "AES_256"
}
```
Others: `gcp_kms`, `azure_vault`, `openbao` (transit) and `external`. A KMS provider
generates a fresh data key per state or plan file and wraps it with the KMS key.
Use a separate KMS key per state file.

## Reading other states
```hcl
remote_state_data_sources {
  default { method = method.aes_gcm.main }
  remote_state_data_source "network" { method = method.aes_gcm.network }
}
```
Needed when `terraform_remote_state` reads an encrypted state; it can reuse the main
setup or define its own keys and methods.

## Config from the environment
`TF_ENCRYPTION` accepts the same configuration (HCL, or JSON syntax). If you use both
it and the code block, OpenTofu merges them and the environment settings override
code settings. To avoid writing unencrypted data when the variable is missing, keep a
code block with `enforced = true`.

## Gotchas
- Once enabled, OpenTofu cannot read state without the correct key. Back up the keys
  and an unencrypted copy of state first, and rehearse recovery.
- Do not rename key providers or methods after encrypting: the encrypted data stores
  their names. Use a `fallback` block, or set `encrypted_metadata_alias` on the key
  provider so it can be renamed.
- Enabling on an existing unencrypted state is not enough: OpenTofu refuses to read
  plain text by default. Add `method "unencrypted"` as a `fallback`, apply, then
  remove the fallback and consider `enforced = true`.
- Deprecated key providers or methods raise a console warning on plan or apply;
  switch before upgrading to the next minor version.

## Verify
- [ ] The stored state is encrypted data, not readable resources.
- [ ] `tofu plan` works with the key and fails clearly without it.

## Checked
2026-10-31. Confirmed against the OpenTofu state-encryption page: configuration block
structure, `TF_ENCRYPTION` merge and override rule, JSON syntax note, `enforced`,
`remote_state_data_sources` / `remote_state_data_source` blocks, PBKDF2 option table
(minimum 16-character passphrase, defaults), provider list, per-state key advice,
rename warning and `encrypted_metadata_alias`, unencrypted-method migration, variable
restrictions. Removed: the "1.7+" version claim, "Terraform has no equivalent",
`kms:Decrypt` as the access rule, the claim about third-party tools that parse state,
and the `tofu show plan.bin` and `aws s3 cp` verification commands.
Method: documentation only; no commands were run.
