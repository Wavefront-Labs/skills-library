---
id: computing-software.cloud-infrastructure-engineering.minio.site-replication-setup
name: site-replication-setup
category: computing-software
field: cloud-infrastructure-engineering
product: minio
tags: [minio, site-replication-setup, mc-admin-replicate-add, mc-admin-replicate-info, mc-admin-replicate-status, expand-site-replication, mc-admin-replicate-rm, load-balancer-alias]
level: advanced
status: docs-checked
description: "Set up and expand MinIO site replication with mc admin replicate add, info and status: one site with data, load balancer aliases, backups, switching from bucket replication."
sources: ["https://github.com/minio/docs/blob/main/source/operations/replication/multi-site-replication.rst"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Setting up MinIO site replication

## Prerequisites
- Back up first: `mc admin cluster bucket export` and `mc admin cluster iam export`.
- Only one site may hold data at setup; the others must have no buckets or objects.
- Same IDP, same MinIO Server version (and a close `mc` version), and shared access to one KMS for SSE-S3 or SSE-KMS (a central KES or one per site on a central vault).
- A load balancer or reverse proxy in front of each site. Use its URL for the alias.
- Switching from bucket replication: delete all bucket replication rules (`mc replicate rm`) on the site with data first, since the two methods are mutually exclusive.

## Configure
```
mc alias set minio1 https://minio1.example.com:9000 adminuser adminpassword
mc admin replicate add minio1 minio2 minio3
mc admin replicate info minio1
mc admin replicate status minio1
```
Environment variables such as `MC_HOST_minio1=https://adminuser:adminpassword@minio1.example.com` work in place of aliases. If all sites are empty, alias order does not matter; if one has data, list it first. `status` reports counts such as buckets, policies, users and groups in sync.

## Expand
The new site must be fully deployed, share the IDP, use the same root credentials and be empty. List *all* existing aliases then the new one: `mc admin replicate add minio1 minio2 minio3 minio4`. If any peer is unreachable or permanently lost, remove it first with `mc admin replicate rm`.

Concepts: `computing-software.cloud-infrastructure-engineering.minio.site-replication`.

## Checked
2026-11-03. Confirmed against the MinIO docs source: Site Replication Overview page, prerequisites and tutorials (multi-site-replication.rst). Removed: the unsourced single-point-of-failure remark.
Method: documentation only; no commands were run.
