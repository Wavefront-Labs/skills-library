---
id: computing-software.cloud-infrastructure-engineering.openbao.rate-limit-quotas
name: rate-limit-quotas
category: computing-software
field: cloud-infrastructure-engineering
product: openbao
tags: [openbao, resource-quotas, rate-limit, block-interval, exempt-paths]
level: practitioner
status: docs-checked
description: "OpenBao rate limit quotas: scope levels, rate and block_interval fields, role login quotas, per-IP per-node behaviour and exempt paths."
sources:
  - https://raw.githubusercontent.com/openbao/openbao/main/website/content/docs/concepts/resource-quotas.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Rate limit quotas

## Scope

- Root level (empty `path`): global limiter inherited by all namespaces and mounts.
- Namespace, mount or full API path: the most specific matching quota wins.
- Role-based login quotas (`role` on an auth mount): override all other quotas.

## Fields

- `path`: scope of the quota
- `rate`: requests per second, token bucket (a client can burst `rate` in one second, then continues at `rate` per second)
- `block_interval`: optional; non-zero blocks an over-limit client for that many seconds
- `role`: target a role for login quotas
- `rate_limit_exempt_paths`: overrides the default exempt list

## Behaviour

Limits apply per client IP address on each node; quotas are not replicated across nodes.

Default exempt paths: `sys/generate-recovery-token/attempt`, `sys/generate-recovery-token/update`, `sys/generate-root/attempt`, `sys/generate-root/update`, `sys/health`, `sys/seal-status`, `sys/unseal`.

Managed via the HTTP Rate Limit Quotas API; observe through quota metrics and optional audit logging.

## Why

High-volume API use can exhaust resources on a node or the cluster, especially when endpoints are exposed to many services.

## Checked

2026-11-04. Read the OpenBao resource quotas concepts page in full. Confirmed: token bucket algorithm, root, namespace, mount and path scope with most-specific precedence, `role` login quotas overriding all others, per-client-IP per-node limiting without replication, `block_interval`, `rate_limit_exempt_paths` and the seven default exempt paths. Removed: nothing.
Method: documentation only; no commands were run.
