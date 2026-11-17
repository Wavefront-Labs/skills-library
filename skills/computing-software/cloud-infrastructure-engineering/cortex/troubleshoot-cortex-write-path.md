---
id: computing-software.cloud-infrastructure-engineering.cortex.troubleshoot-cortex-write-path
name: troubleshoot-cortex-write-path
category: computing-software
field: cloud-infrastructure-engineering
product: cortex
tags: [troubleshooting, distributor, push-errors, tenant-id, inflight-requests]
level: practitioner
status: docs-checked
description: "Work through Cortex write-path symptoms: 5xx on push, accepted samples missing from queries, and inflight push request rejections."
sources:
  - https://github.com/cortexproject/cortex/blob/master/docs/operations/troubleshooting.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Distributors return 5xx on `/api/v1/push`:

1. Read distributor logs at warn and error level; the cause is ingester unreachable, rate limit exceeded or validation error.
2. Check the ring page (`/ring` on any distributor): all ingesters should be ACTIVE. UNHEALTHY or missing ones point at a partition or the KV store.
3. If the `CortexIngesterUnhealthy` alert fires, its labels name the ingester.
4. Inspect `cortex_distributor_ingester_append_failures_total`; a rate matching the 5xx rate confirms ingester-side rejection.

If the cause is a per-user limit being exceeded, raise the limit in `runtime_config` overrides rather than scaling out.

Samples accepted but never appear in queries:

1. Verify the push and the query use the same `X-Scope-OrgID`; a tenant-ID mismatch is the most common cause of missing data.
2. Check `cortex_ingester_memory_series` on the receiving ingester; non-zero means the data is in memory.
3. Confirm the time range: ingesters serve recent data until it ages out per `-blocks-storage.tsdb.retention-period` (default 6h), and queriers stop consulting them for ranges older than `-limits.query-ingesters-within` (per tenant, when set). Older data must have shipped and be visible via the bucket index (`cortex_ingester_shipper_uploads_total`, alerts `CortexIngesterHasNotShippedBlocks` and `CortexBucketIndexNotUpdated`).

`CortexDistributorReachingInflightPushRequestLimit` means distributors near `-distributor.instance-limits.max-inflight-push-requests`: scale out or raise the limit if CPU and memory allow.

## Checked

2026-11-04. Claims were read against the Cortex docs page: Troubleshooting Cortex (Write path) (see sources). Removed filler and unconfirmed wording.

Method: documentation only; no commands were run.
