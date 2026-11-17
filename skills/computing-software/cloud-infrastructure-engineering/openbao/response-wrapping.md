---
id: computing-software.cloud-infrastructure-engineering.openbao.response-wrapping
name: response-wrapping
category: computing-software
field: cloud-infrastructure-engineering
product: openbao
tags: [openbao, response-wrapping, wrap-ttl, cubbyhole, unwrap]
level: advanced
status: docs-checked
description: "Wrap OpenBao responses in single-use cubbyhole tokens, and validate wrapping tokens through lookup, path check and unwrap."
sources:
  - https://raw.githubusercontent.com/openbao/openbao/main/website/content/docs/concepts/response-wrapping.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Response wrapping

Set the TTL per request with the `X-Vault-Wrap-TTL` header (seconds, or `15s`, `20m`, `25h`) or the CLI flag `-wrap-ttl`. OpenBao serializes the original response, stores it in the cubbyhole of a new single-use token, and returns the token ID, TTL and creation path. Policies can set minimum and maximum wrapping TTLs.

## sys/wrapping endpoints

- `lookup`: creation time, path and TTL; unauthenticated, available to the token holder
- `unwrap`: returns the original response
- `rewrap`: moves data into a new wrapping token (long-lived secrets, rotation)
- `wrap`: echoes submitted data inside a new wrapping token

## Validate before trusting

1. Expected token never arrived: treat as possible interception.
2. Look it up; if already unwrapped, expired or revoked, alert and check audit logs.
3. Confirm the creation path is what you expect. For `kv` secrets require an exact match; a path beginning `cubbyhole` or `sys/wrapping/wrap` suggests re-wrapped data.
4. Unwrap. If that fails, alert.

## Gotchas

- Wrapping tokens are not signed; always validate against the server.
- An invalid token does not prove an attack; a slow client may have outlived the TTL.
- Blocking `sys/wrapping/wrap` does not prevent wrapping, since other paths can wrap data.

## Checked

2026-11-04. Read the OpenBao response wrapping concepts page in full. Confirmed: `X-Vault-Wrap-TTL` formats, `-wrap-ttl`, the five-step wrapping process, the `sys/wrapping` operations and their descriptions, the unsigned token rationale, the four validation steps and the policy-controlled TTL note. Removed: nothing.
Method: documentation only; no commands were run.
