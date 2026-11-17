---
id: computing-software.cloud-infrastructure-engineering.external-dns.owner-migration-shared-zones
name: owner-migration-shared-zones
category: computing-software
field: cloud-infrastructure-engineering
product: external-dns
tags: [external-dns, shared-hosted-zone, per-cluster-owner-id, policy-sync, orphan-deletion, multi-cluster]
level: sme
status: docs-checked
description: "Avoid ExternalDNS deleting other clusters' records in a shared zone: unique per-cluster txt-owner-id and a safe migration sequence away from owner default."
sources:
  - https://raw.githubusercontent.com/kubernetes-sigs/external-dns/master/docs/registry/txt.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Owner migration in shared zones

**The hazard:** several clusters share a hosted zone and all their records use `owner=default`. One cluster is upgraded to `policy=sync`, `--txt-owner-id=<cluster-name>` and `--migrate-from-txt-owner=default`. That cluster treats the other clusters' records as orphans and schedules them for deletion. The docs say not to use this pattern.

**Rules**
- Give every cluster a unique `--txt-owner-id` (for example `cluster1`, `cluster2`) and document the convention in platform configuration.
- Do not share an owner such as `default` across clusters in any zone where `policy=sync` or the migration flag is used.

**Safe sequence**
1. While still on `policy=upsert-only` (or equivalent), roll out cluster-specific owner IDs so new records carry each cluster's own owner.
2. Avoid `--migrate-from-txt-owner=<old-owner>` unless only one cluster has records under `<old-owner>` in that zone, or migrate in an isolated zone where only that cluster writes.
3. Otherwise prefer per-cluster zones, manual TXT record adjustment, or a fully coordinated migration of all clusters.

When several clusters must publish the same hostname, use the patterns in the multi-cluster shared records page instead.

**Verify:** before enabling `policy=sync`, list registry TXT records and confirm each cluster's records show its own `external-dns/owner=` value.

## Checked

2026-11-04. Read the TXT registry page (OwnerID migration: multi-cluster considerations, per-cluster owner IDs, example sequence, when to avoid). Confirmed the hazard, the unique owner rule and the safe sequence. Removed nothing.

Method: documentation only; no commands were run.
