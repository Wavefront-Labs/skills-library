---
id: computing-software.devops-ci-cd.packer.vault-function
name: vault-function
category: computing-software
field: devops-ci-cd
product: packer
tags: [vault, secrets, function, hashicorp-vault, fn-vault]
level: advanced
status: docs-checked
description: "Fetch a secret from HashiCorp Vault in a template with vault(path, key) using VAULT_ADDR and VAULT_TOKEN."
sources:
  - "https://developer.hashicorp.com/packer/docs/templates/hcl_templates/functions/contextual/vault/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

`vault(path, key)` retrieves a secret from a HashiCorp Vault KV store. For it to work you must set the environment variables `VAULT_TOKEN` and `VAULT_ADDR` to valid values:

```bash
export VAULT_TOKEN=<token>
export VAULT_ADDR=https://vault.example.com:8200
```

KV version 2 example (the secret was stored with `vault kv put secret/hello foo=world`; note the `data/` segment in the path):

```hcl
locals {
  foo = vault("/secret/data/hello", "foo")
}
```

This assigns `local.foo` the value "world". For a KV version 1 engine (enabled with `vault secrets enable -version=1 -path=secrets kv`), the path has no `data/`:

```hcl
locals {
  foo = vault("secrets/hello", "foo")
}
```

`path` is the secret's path and `key` selects the field stored at that key.

To keep a highly sensitive value out of the build output, use the singular `local` block (not `locals`) with `sensitive = true`; the value is then replaced with `<sensitive>` in Packer output:

```hcl
local "foo" {
  expression = vault("secrets/hello", "foo")
  sensitive  = true
}
```

Notes from the docs:

- The page also says `vault` is available only within the default value of a user variable, so you can default a variable to a Vault secret, and that HCL functions can be used in local variable definitions or inline with a provisioner or post-processor, but not in global variable definitions.
- The Vault client can be configured with these environment variables: `VAULT_ADDR`, `VAULT_AGENT_ADDR`, `VAULT_CACERT`, `VAULT_CAPATH`, `VAULT_CLIENT_CERT`, `VAULT_CLIENT_KEY`, `VAULT_CLIENT_TIMEOUT`, `VAULT_SKIP_VERIFY`, `VAULT_NAMESPACE`, `VAULT_TLS_SERVER_NAME`, `VAULT_WRAP_TTL`, `VAULT_MAX_RETRIES`, `VAULT_TOKEN`, `VAULT_MFA`, `VAULT_RATE_LIMIT`.

## Checked

Method: docs-checked 2026-11-09 against the Packer vault function page (read in full as published page source). Dropped the aws_secretsmanager comparison, short-lived token advice and the claims about debug logs and manifests, which the page does not make.
