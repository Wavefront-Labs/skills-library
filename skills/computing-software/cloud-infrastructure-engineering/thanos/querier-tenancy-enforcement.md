---
id: computing-software.cloud-infrastructure-engineering.thanos.querier-tenancy-enforcement
name: querier-tenancy-enforcement
category: computing-software
field: cloud-infrastructure-engineering
product: thanos
tags: [thanos-query, multi-tenancy, tenant-header, enforce-tenancy]
level: advanced
status: docs-checked
description: "Capture tenant metrics and enforce per-tenant label matchers on the Thanos Querier."
sources: ["https://thanos.io/tip/components/query.md/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Querier tenancy

**Tenant metrics.** Send the tenant ID in the HTTP header named by `--query.tenant-header`. It is propagated through Query Frontend down to Store, producing per-tenant metrics. Without the header, `--query.default-tenant-id` (default `default-tenant`) is used.

**Enforcement.** `--query.enforce-tenancy` makes the Querier add a matcher to every selector so only series with `--query.tenant-label-name` equal to the header value are read. This requires that series carry a tenant label at ingest, for example by running Thanos Receive with tenancy enabled.

Caveats stated in the docs:
- With nested Queriers, enforcement only happens in the Querier that received the original request.
- Thanos has no authentication, so anyone can set an arbitrary tenant header. Put an authenticating proxy in front if that matters.
- The Query UI includes an option to set an arbitrary tenant, so do not expose it to end users who must not see each other's data.

## Checked

2026-11-03. Confirmed against the Thanos Query page (components/query.md): API parameters and defaults, deduplication algorithms (penalty default, chain), partial response strategies (abort default), endpoint flags and per-endpoint TLS, PromQL engine and distributed mode, tenancy flags, sub-path prefixing. Fixed: --store.sd-files is marked deprecated; per-endpoint TLS does not apply to DNS or static endpoints; partial-response default wording. Removed: closing 'Verify' tips and other statements the page does not state.

Method: documentation only; no commands were run.
