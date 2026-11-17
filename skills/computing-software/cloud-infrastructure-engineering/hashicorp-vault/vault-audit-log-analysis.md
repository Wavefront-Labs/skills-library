---
id: computing-software.cloud-infrastructure-engineering.hashicorp-vault.vault-audit-log-analysis
name: vault-audit-log-analysis
category: computing-software
field: cloud-infrastructure-engineering
product: hashicorp-vault
tags: [vault, audit-analysis, jq, audit-hash]
level: practitioner
status: docs-checked
description: "Read Vault JSON audit logs with jq, and know what is hashed, which headers are logged and which endpoints are never audited."
sources: ["https://developer.hashicorp.com/vault/docs/audit", "https://developer.hashicorp.com/vault/docs/concepts/tokens", "https://developer.hashicorp.com/vault/api-docs/system/audit-hash", "https://developer.hashicorp.com/vault/api-docs/system/config-auditing"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Audit entries are JSON lines. The documented examples show a `type` of `response`, `request.operation` (for example `list`) and `response.data`.

```sh
jq -c 'select(.type=="response") | {op:.request.operation}' audit.log
```

What the log does and does not contain:
- Most string values are written as a keyed hash (HMAC-SHA256), not plaintext. Non-string values such as integers and booleans are not hashed, so send sensitive data as strings.
- To check whether a known value matches a logged hash, compute its hash for that device with the `sys/audit-hash` API. Hashes cannot be reversed.
- Token accessors are hashed by default; an audit device option (`hmac_accessor=false`) turns that off. Accessors are the handle for limited token actions such as lookup and revoke (tokens concept page), and unhashed accessors in logs can be used for a wide denial of service, so weigh that before disabling hashing.
- Request headers recorded by default: `User-Agent`, `Correlation-Id`, `X-Correlation-Id`. Their values are not hashed unless you configure it. Add or remove audited headers with `sys/config/auditing/request-headers/:name` (parameter `hmac`; root namespace only, `sudo` required).
- Never audited: `sys/init`, `sys/seal-status`, `sys/seal`, `sys/step-down`, `sys/unseal`, `sys/leader`, `sys/health`, the rekey endpoints, `sys/storage/raft/bootstrap`, `sys/storage/raft/join`, `sys/internal/ui/feature-flags`; and `sys/metrics`, `sys/pprof/*`, `sys/in-flight-req` when the listener allows unauthenticated access. A missing entry for these is normal.
- `elide_list_responses` replaces `keys` and `key_info` in LIST responses with a count.
- Disabling an audit device means you can no longer compute hashes for its old entries; re-enabling at the same path creates a new hashing key.
- If all enabled audit devices become unavailable, Vault becomes unavailable too.

## Checked
2026-11-03. Confirmed on the Vault audit devices page (HMAC-SHA256 hashing, non-string values, `sys/audit-hash`, `elide_list_responses`, default headers, exempted endpoints, new hashing key on re-enable, availability warning), the `/sys/config/auditing/request-headers` API page (`hmac`, sudo, root namespace), the tokens concept page (accessor actions and audit hashing of accessors) and the `sys/audit-hash` page. Removed: jq paths for `request.path`, `auth.accessor`, `auth.display_name`, `entity_id` and `request.id` linking (not shown on any page), the accessor-to-holder workflow (accessors are hashed by default), and advice on off-host log shipping and sampling.
Method: documentation only; no commands were run.
