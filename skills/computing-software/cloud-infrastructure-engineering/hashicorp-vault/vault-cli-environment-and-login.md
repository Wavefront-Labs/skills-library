---
id: computing-software.cloud-infrastructure-engineering.hashicorp-vault.vault-cli-environment-and-login
name: vault-cli-environment-and-login
category: computing-software
field: cloud-infrastructure-engineering
product: hashicorp-vault
tags: [vault, vault-cli, vault-addr, token-helper]
level: practitioner
status: docs-checked
description: "Set VAULT_ADDR, VAULT_CACERT and token helper correctly, log in with methods, and avoid secrets in history."
sources: ["https://developer.hashicorp.com/vault/docs/commands", "https://developer.hashicorp.com/vault/docs/commands/write", "https://developer.hashicorp.com/vault/docs/commands/kv/put", "https://developer.hashicorp.com/vault/docs/auth/jwt"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The CLI reads its configuration from environment variables.

```sh
export VAULT_ADDR=https://vault.example.com:8200
export VAULT_CACERT=/etc/ssl/vault-ca.pem
vault login -method=oidc role=dev
vault token lookup
vault kv put -mount=secret app/db password=@pw.txt
unset VAULT_TOKEN
```

The CLI caches the token from `vault login` through a token helper; the default file is `~/.vault-token`, and deleting it logs the user out.

Gotchas: `VAULT_TOKEN` is an environment variable that supplies the token to the CLI. In `vault write` and `vault kv put`, a value starting with `@` is loaded from a file and a value of `-` is read from stdin, so secrets need not appear inline. `VAULT_SKIP_VERIFY` skips certificate verification; the docs say not to use it in production. `vault print token` prints the token the CLI is using. `VAULT_NAMESPACE` (or `-namespace`) sets the namespace.

## Checked

2026-11-03. Confirmed on the Vault commands overview, write, kv put and JWT/OIDC auth pages: `VAULT_ADDR`, `VAULT_CACERT`, `VAULT_TOKEN`, `VAULT_NAMESPACE`, `VAULT_SKIP_VERIFY` and its production warning, the token helper and `~/.vault-token`, `@file` and `-` value syntax, `vault kv put -mount=`, `vault login -method=oidc role=...`, `vault print token`. Removed: the 0600 mode, the claim that a stale `VAULT_TOKEN` overrides the helper, short-lived-login and machine-identity advice, and the invented Verify step.

Method: documentation only; no commands were run.
