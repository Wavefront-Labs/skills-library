---
id: computing-software.cloud-infrastructure-engineering.terraform.opentofu-openbao-vault-transit-key-provider
name: opentofu-openbao-vault-transit-key-provider
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, openbao-key-provider, transit-key-provider, state-encryption, vault, tofu]
level: practitioner
status: docs-checked
description: "Encrypt OpenTofu state and plans with keys from OpenBao transit: key_provider openbao options, auth, key rotation, Vault compatibility limit and failure modes."
sources: ["https://opentofu.org/docs/language/state/encryption/", "https://openbao.org/docs/secrets/transit/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# OpenTofu `openbao` key provider (transit)

The `openbao` key provider asks an OpenBao **Transit Secret Engine** to generate data
keys. OpenTofu generates a fresh data key for each state or plan file and wraps it with
the transit key you name. Use a separate transit key per state file so access can be
scoped per state and one compromised key or credential limits the blast radius.

## Transit setup
```bash
bao secrets enable transit
bao write -f transit/keys/tofu-state     # default type aes256-gcm96
```
Write a policy for the CI token that lets it generate data keys and decrypt with that
one key; take the exact endpoint paths from the OpenBao transit API docs.

## OpenTofu config
```hcl
terraform {
  encryption {
    key_provider "openbao" "main" {
      key_name = "tofu-state"                 # required, must already exist
      address  = "https://bao.example.com:8200"   # or BAO_ADDR; default https://127.0.0.1:8200
      # token via BAO_TOKEN env var; do not hard-code
      # transit_engine_path = "/transit"      # default
      # key_length = 32                       # 16, 32 or 64 bytes; default 32
      # associated_data = base64encode("myapp")
    }
    method "aes_gcm" "main" { keys = key_provider.openbao.main }
    state { method = method.aes_gcm.main }
    plan  { method = method.aes_gcm.main }
  }
}
```
The server's TLS certificate must be trusted by the machine running `tofu`.

## Vault compatibility
The docs say the provider is compatible with the last MPL-licensed HashiCorp Vault
(1.14) and does not support the later BUSL-licensed versions. The documented env vars
are `BAO_TOKEN` and `BAO_ADDR`; the page does not document `VAULT_*` variables.

## Rotation
- `bao write -f transit/keys/tofu-state/rotate` adds a new key version to the keyring.
  Transit ciphertext carries its key version (`vault:v1:...`), so older versions can
  still be decrypted after a rotate.
- To change provider (e.g. pbkdf2 -> openbao), use a `fallback` block on the state and
  plan blocks, apply once, then remove the fallback.

## Failure modes
| Symptom | Cause |
|---|---|
| Error on data-key generation | transit policy missing the key, or token lacks the policy |
| State unreadable after key deletion | transit key deleted; restore from backup |
| Works locally, fails in CI | `BAO_ADDR`/`BAO_TOKEN` not provided, or the server's TLS certificate is not trusted |

## Gotchas
- The token must be available to every `tofu` command that touches state (plan,
  output, state list), not just apply.
- Never delete a transit key without a migration plan.

## Verify
- [ ] Pulled state is unreadable ciphertext, not plain resources.
- [ ] CI token can decrypt; a token without the policy cannot.

## Checked
2026-10-31. Confirmed against the OpenTofu state-encryption page (OpenBao key provider
section: `key_name` required, `token`/`BAO_TOKEN`, `address`/`BAO_ADDR` default
`https://127.0.0.1:8200`, `transit_engine_path` default `/transit`, `key_length` 16/32/64
default 32, `associated_data`, Vault 1.14 compatibility note, per-state key warning,
`fallback` blocks) and the OpenBao transit page (`aes256-gcm96` default, `rotate`
command, `vault:v1:` key-version prefix). Removed: the "OpenTofu 1.7+" version claim,
the "experimental" label, the explicit policy paths, `VAULT_ADDR`/`VAULT_TOKEN`,
`BAO_CACERT`, `min_decryption_version`, `deletion_allowed` and the `encrypted_data`
check, none of which the fetched pages confirm.
Method: documentation only; no commands were run.
