---
id: computing-software.cloud-infrastructure-engineering.hashicorp-vault.vault-response-wrapping
name: vault-response-wrapping
category: computing-software
field: cloud-infrastructure-engineering
product: hashicorp-vault
tags: [vault, response-wrapping, cubbyhole, wrap-ttl]
level: practitioner
status: docs-checked
description: "Wrap secrets in single-use tokens with -wrap-ttl, look up before unwrapping, and detect interception."
sources: ["https://developer.hashicorp.com/vault/docs/concepts/response-wrapping", "https://developer.hashicorp.com/vault/docs/auth/approle"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A wrapped response puts the secret in a cubbyhole behind a single-use token, so only the intended recipient can unwrap it.

```sh
vault kv get -wrap-ttl=60s -mount=secret app/db
vault write sys/wrapping/lookup token=<wrapping-token>
vault unwrap <wrapping-token>
vault write sys/wrapping/rewrap token=<wrapping-token>
```

Lookup shows the creation path and TTL without consuming the token and needs no authentication.

Gotchas: wrapping tokens are not signed, so validate with `sys/wrapping/lookup` and check the exact creation path (checking only a `secret/` prefix is not enough). If a lookup says the token is invalid, or unwrap fails, treat it as a possible compromise and trigger an alert for immediate investigation. Keep TTLs short and make delivery and unwrap tightly coupled.

## Checked

2026-11-03. Confirmed against the Vault response wrapping page: single-use token with the response in its cubbyhole, no signed wrapping tokens, `sys/wrapping/lookup` (unauthenticated; creation time, path, TTL), `sys/wrapping/rewrap`, validate by lookup and creation path. Removed: slow-client expiry reasoning, an invented verify step and an accessor-logging tip.

Method: documentation only; no commands were run.
