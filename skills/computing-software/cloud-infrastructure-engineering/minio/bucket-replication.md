---
id: computing-software.cloud-infrastructure-engineering.minio.bucket-replication
name: bucket-replication
category: computing-software
field: cloud-infrastructure-engineering
product: minio
tags: [minio, bucket-replication, server-side-replication, active-active, multi-site, site-replication-distinction, mc-mirror, replication-priority]
level: advanced
status: docs-checked
description: "Choose between MinIO server-side bucket replication and client-side mc mirror: same-version rule, active-active modes, rule priority, and how it differs from site replication."
sources: ["https://github.com/minio/docs/blob/main/source/administration/bucket-replication.rst", "https://github.com/minio/docs/blob/main/source/administration/bucket-replication/bucket-replication-requirements.rst"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# MinIO bucket replication

**Server-side** replication is a per-bucket rule that automatically synchronises objects from a source to a remote MinIO bucket. The deployment where you add the rule is the source. It runs as part of write operations (`PUT`) and replicates new objects and mutations (new versions, metadata changes, object lock and retention settings). Source and target must be separate MinIO clusters on the **same release**; for other S3-compatible services use client-side `mc mirror`.

On each write MinIO checks all rules for the bucket and applies the matching rule with the highest priority.

## MinIO extras over S3 replication
- Source and destination bucket names may match (site-to-site cases such as Splunk or Veeam BC/DR).
- Simpler config: no AccessControlTranslation, Metrics or SourceSelectionCriteria.
- Active-passive, active-active (two-way) and multi-site active-active (three or more deployments).

## Bucket vs site replication
They are distinct and mutually exclusive. Bucket replication works at the bucket or prefix level, can be configured any time, and targets may hold pre-existing data. Site replication adds IAM, access keys and bucket configuration, and is normally set up at initial deployment with only one site holding data (`computing-software.cloud-infrastructure-engineering.minio.site-replication`).

## Prerequisites
- Permissions to set up replication, per the requirements page.
- Matching object encryption settings.
- Versioning on both buckets; prefixes excluded from versioning do not replicate.
- Matching object locking state on both buckets.

Commands: `computing-software.cloud-infrastructure-engineering.minio.mc-replicate-add`.

## Checked
2026-11-03. Confirmed against the MinIO docs source: Bucket Replication page (bucket-replication.rst) and the requirements page headings. Removed: the claim that mc mirror syncs only current versions (not on this page) and the unsourced permission-role and retention-rule specifics.
Method: documentation only; no commands were run.
