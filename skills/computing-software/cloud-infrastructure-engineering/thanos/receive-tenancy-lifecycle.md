---
id: computing-software.cloud-infrastructure-engineering.thanos.receive-tenancy-lifecycle
name: receive-tenancy-lifecycle
category: computing-software
field: cloud-infrastructure-engineering
product: thanos
tags: [thanos-receive, multi-tenancy, tenant-header, tenant-lifecycle]
level: advanced
status: docs-checked
description: "Understand how tenants are created, labelled and decommissioned in Thanos Receive."
sources: ["https://thanos.io/tip/components/receive.md/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Receive tenants and their lifecycle

Tenants are created dynamically: a new value in the tenant HTTP header causes Receive to provision an independent TSDB for it. No pre-provisioning is needed.

Relevant flags and defaults:
- `--receive.tenant-header="THANOS-TENANT"`: header carrying the tenant.
- `--receive.default-tenant-id="default-tenant"`: used when the header is absent.
- `--receive.tenant-label-name="tenant_id"`: label announcing the tenant; blocks uploaded to the bucket carry it so they can be compacted per tenant.
- `--receive.tenant-certificate-field`: derive the tenant from the TLS client certificate (`organization`, `organizationalUnit` or `commonName`); the header flag is then ignored.
- `--receive.split-tenant-label-name`: split one request into multiple tenants by a label; it takes precedence over the header.

**Decommissioning.** A tenant is decommissioned when no new samples arrive for longer than `--tsdb.retention`. In-memory samples are flushed, unsent blocks uploaded, and the tenant TSDB removed. New samples later create a fresh TSDB.

So receiver `--tsdb.retention=t` means data for a tenant is kept t after its last sample, unlike Prometheus, which always keeps the last t of data.

**Stats.** `/api/v1/status/tsdb` with the `THANOS-TENANT` header returns per-tenant stats (`limit` default 10); only local, non-replicated series are shown.

## Checked

2026-11-03. Confirmed against the Thanos Receive page (components/receive.md) and the Thanos troubleshooting page (operating/troubleshooting.md): hashrings and ketama, shuffle sharding, tenancy and decommissioning, quorum formula, Cap'n Proto, limits and gates, defaults, out-of-bound and out-of-order causes. Added the documented fixes and the out-of-order window flag warnings. Removed: closing 'Verify' tips and other statements the page does not state.

Method: documentation only; no commands were run.
