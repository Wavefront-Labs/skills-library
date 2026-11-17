---
id: computing-software.cloud-infrastructure-engineering.apache-apisix.secret-references
name: secret-references
category: computing-software
field: cloud-infrastructure-engineering
product: apache-apisix
tags: [apache-apisix, apisix, secrets, vault, env, secret-manager, credentials]
level: advanced
status: docs-checked
description: "Keep credentials out of APISIX config with $secret:// and $env:// references: supported managers, the Vault secret resource and what happens on an unresolved reference."
sources:
  - https://raw.githubusercontent.com/apache/apisix/master/docs/en/latest/terminology/secret.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Secret references

Supported managers: environment variables, HashiCorp Vault (KV engine v1), AWS Secrets Manager, GCP Secrets Manager.

Reference syntax:
- Managers: `$secret://$manager/$id/$secret_name/$key`
- Environment: `$ENV://$env_name/$sub_key` (the page also lists `$env://`). `$sub_key` is optional and only for variables holding a JSON string.

Register a Vault secret manager:

```shell
curl http://127.0.0.1:9180/apisix/admin/secrets/vault/1 \
-H "X-API-KEY: $admin_key" -X PUT -d '
{
    "uri": "https://127.0.0.1:8200",
    "prefix": "apisix",
    "token": "<VAULT_TOKEN>"
}'
```

A value stored at `apisix/jack` under key `auth-key` is then referenced as `$secret://vault/1/jack/auth-key`, for example as a plugin `key`.

Environment variables can be set before startup or with the NGINX `env` directive.

If a reference cannot be resolved, APISIX uses the literal reference string as the value and logs an error (for example `failed to resolve secret reference: $secret://vault/1/foo/bar, field: password`).

## Checked

2026-11-04: read the Secret page; the four supported managers, Vault KV engine v1, both reference syntaxes, the Vault secret resource and the $secret://vault/1/jack/auth-key example, the env directive note and the unresolved-reference behaviour match. Added the logged error text from the page.

Method: documentation only; no commands were run.
