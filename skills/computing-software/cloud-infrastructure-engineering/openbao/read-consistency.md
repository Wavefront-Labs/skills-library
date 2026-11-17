---
id: computing-software.cloud-infrastructure-engineering.openbao.read-consistency
name: read-consistency
category: computing-software
field: cloud-infrastructure-engineering
product: openbao
tags: [openbao, consistency, x-vault-index, x-vault-inconsistent, standby-reads]
level: advanced
status: docs-checked
description: "Handle OpenBao eventual consistency on standby reads with X-Vault-Index, X-Vault-Inconsistent modes, 429 retries and SSCT limits."
sources:
  - https://raw.githubusercontent.com/openbao/openbao/main/website/content/docs/concepts/consistency.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Read consistency

Clusters are eventually consistent unless `disable_standby_reads=true`. Only the leader writes; standbys may serve stale data until invalidations are processed, so read-after-write can fail on Integrated Storage or PostgreSQL.

## Headers

Write responses may carry `X-Vault-Index: <opaque>` (not guaranteed when nothing was written to storage). Send it back with:

- `X-Vault-Inconsistent: forward-active-node`: a standby lacking state forwards to the active node.
- `X-Vault-Inconsistent: fail` (default): missing state returns HTTP 429 with `Retry-After`.
- `X-Vault-Inconsistent: await-state`: standby holds the request up to `consistency_max_index_wait`; on timeout `consistency_fallback_behavior` (`fail` default, or `forward-active-node`) applies. A second header value overrides it.

## Config

- Listener options: `consistency_max_index_wait` (for `await-state`), `consistency_fallback_behavior`, and `consistency_missing_header_forward` (read-enabled standbys forward requests lacking these headers, for legacy clients).
- `disable_ssct_tokens=false` in the global server configuration: re-enables Server-Side Consistent Tokens (v2.7 and later; disabled by default).

## Clients

The Go API retries 412 and 429 and has helpers to propagate `X-Vault-Index`; other clients need equivalent logic. `DefaultStrongConsistency = true` opts in.

## Trade-offs

Forwarding can bottleneck the active node, limiting standby read scalability. Await-state spools the request on the standby instead of loading the active node. SSCTs only give strict consistency between token creation and its use; further writes are not guaranteed, which is why they stay off by default.

## Checked

2026-11-04. Read the OpenBao eventual consistency page in full. Confirmed: the eventual consistency model and `disable_standby_reads`, `X-Vault-Index` and its caveat, the three `X-Vault-Inconsistent` modes and the 429 with `Retry-After`, fallback behaviour and the second header override, legacy client option, SSCT option, Go API retries of 412 and 429 and `DefaultStrongConsistency`. Removed: the unsupported claim that await-state adds latency.
Method: documentation only; no commands were run.
