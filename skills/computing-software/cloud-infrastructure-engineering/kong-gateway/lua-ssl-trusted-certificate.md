---
id: computing-software.cloud-infrastructure-engineering.kong-gateway.lua-ssl-trusted-certificate
name: lua-ssl-trusted-certificate
category: computing-software
field: cloud-infrastructure-engineering
product: kong-gateway
tags: [kong-gateway, kong, lua-ssl-trusted-certificate, lua-ssl-verify-depth, cosocket, tls, ca-bundle]
level: practitioner
status: docs-checked
description: "lua_ssl_trusted_certificate sets the CA bundle Kong's Lua cosockets trust (database, logging plugins, hybrid cluster); default system, depth 1."
sources:
  - https://raw.githubusercontent.com/Kong/kong/master/kong.conf.default
  - https://developer.konghq.com/gateway/hybrid-mode/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# lua_ssl_trusted_certificate

Lua cosockets are the outbound connections Kong itself makes (PostgreSQL, log shipping from plugins, and so on). These settings control how it verifies the servers it calls:

| Setting | Default |
|---|---|
| `lua_ssl_trusted_certificate` | `system` |
| `lua_ssl_verify_depth` | `1` |
| `lua_ssl_protocols` | `TLSv1.2 TLSv1.3` |

`system` makes Kong search a list of usual distribution CA bundle paths and use the first one found. It can be used by itself or alongside other CA file paths, which may also be given as certificate content or base64. If the verification depth is reached before the end of the chain, verification fails.

When `pg_ssl_verify` is enabled, these CA files verify Kong's database connections. `lua_ssl_protocols` does not affect connections to the upstream Service or from downstream clients.

Hybrid mode use: if the control plane certificate comes from a well-known CA, set `lua_ssl_trusted_certificate=system` on the data plane and leave `cluster_ca_cert` empty.

## Checked

2026-11-04. Confirmed against kong.conf.default (the three defaults, `system` behaviour, `pg_ssl_verify`, depth failure, scope of `lua_ssl_protocols`) and the Hybrid mode page (well-known CA note). Removed the per-Service `tls_verify`, `tls_verify_depth` and `ca_certificates` clause and the advice to replace `system`, which the sources do not support.
Method: documentation only; no commands were run.
