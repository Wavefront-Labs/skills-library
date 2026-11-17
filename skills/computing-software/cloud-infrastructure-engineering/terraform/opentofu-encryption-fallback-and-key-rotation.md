---
id: computing-software.cloud-infrastructure-engineering.terraform.opentofu-encryption-fallback-and-key-rotation
name: opentofu-encryption-fallback-and-key-rotation
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [opentofu, encryption-fallback, encryption-migration, key-rotation, unencrypted-method, state-encryption]
level: advanced
status: docs-checked
description: "Migrate existing OpenTofu state to encryption, roll over keys and methods, and decrypt back using fallback blocks and the unencrypted method without losing access mid-way."
sources:
  - "https://opentofu.org/docs/language/state/encryption/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Encryption fallback, migration and key rotation

From the OpenTofu state-encryption page: if OpenTofu fails to read state or plan data with the
primary method it automatically tries the `fallback` method, and when it saves it always uses the
primary method, never the fallback. That one rule drives every migration below. All blocks live inside
`terraform { encryption { ... } }`.

Before enabling encryption, exercise your disaster recovery plan, make a temporary backup of the
unencrypted state, and back up your keys: once encrypted, OpenTofu cannot read the state without the
correct key.

## Unencrypted to encrypted (pre-existing project)
OpenTofu by default refuses to read unencrypted state or plan data (it could have been manipulated), so
you must declare an `unencrypted` method and reference it as a fallback:
```hcl
terraform {
  encryption {
    method "unencrypted" "migrate" {}
    key_provider "pbkdf2" "new" { passphrase = var.passphrase }
    method "aes_gcm" "new" { keys = key_provider.pbkdf2.new }

    state {
      method = method.aes_gcm.new
      fallback { method = method.unencrypted.migrate }
    }
    plan {
      method = method.aes_gcm.new
      fallback { method = method.unencrypted.migrate }
    }
  }
}
```
Run `tofu apply`, then remove the `fallback` block and consider adding `enforced = true`. The page's
example makes the passphrase at least 16 characters and `sensitive`; do not leave a default value in code.
The `plan` block is only needed if you use plan files.

## Key and method rollover
To rename a method, change a passphrase or switch key management systems, make the new method primary
and put the old one in `fallback`:
```hcl
state {
  method = method.aes_gcm.new
  fallback { method = method.aes_gcm.old }
}
```
Keep both key providers and methods defined while the fallback is in use. After the next write with the
new method you can drop the fallback and the old key.

Once data is encrypted, do not rename key providers or methods: the stored data contains metadata with their
names. Use a `fallback` for changes, or set `encrypted_metadata_alias` on the key provider to fix its metadata
key so the provider can be renamed safely.

## Encrypted to unencrypted (rolling back)
```hcl
state {
  enforced = false
  fallback { method = method.aes_gcm.old }
  method = method.unencrypted.migrate
}
```
Steps from the page: leave the original method unchanged, add the `unencrypted` method, disable or remove
`enforced`, move the original method into `fallback`, make `unencrypted` primary, run `tofu apply`, then
remove the block when done. Do not remove or modify the original method until the migration is finished.

## Remote state data sources
Consumers of `terraform_remote_state` get their own `remote_state_data_sources` block inside `encryption`,
with a `default` entry and optional `remote_state_data_source "<name>"` entries (names can be `name`,
`module.name` or `module.name[0]`). If key provider names conflict between projects, use
`encrypted_metadata_alias`.

## Gotchas
- `enforced = true` rejects unencrypted data, so it conflicts with an `unencrypted` primary; disable it
  during a decrypt migration.
- Values used in the encryption block may be variables and locals, but cannot reference state data or
  provider-defined functions: they must resolve during `tofu init`.
- Repeat each migration for the `plan` block if you use plan files.

## Verify
- [ ] After removing the fallback, `tofu plan` still reads the state.
- [ ] Keys and a pre-migration backup are stored somewhere independent of the state backend.

## Checked
Checked 2026-11-08 against the OpenTofu "State and Plan Encryption" page (sections on migrating, key and method
rollover, initial setup, rolling back and remote state data sources). Removed: the `tofu apply -refresh-only`
shortcut, the claim that KMS key material rotation is transparent, the per-workspace tracking advice, saved plan
file behaviour, and the stored-object verification markers, none of which that page states.
Method: docs-only read of cited pages, 2026-11-08
