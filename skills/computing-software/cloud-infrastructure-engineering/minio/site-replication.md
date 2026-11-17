---
id: computing-software.cloud-infrastructure-engineering.minio.site-replication
name: site-replication
category: computing-software
field: cloud-infrastructure-engineering
product: minio
tags: [minio, site-replication, peer-sites, what-replicates, iam-sync, site-healing, get-proxy, ilm-expiry-replication, idp]
level: advanced
status: docs-checked
description: "Understand MinIO site replication peer sites, what does and does not replicate, IAM sync order, retry and healing behaviour, and GET and HEAD proxying between sites."
sources: ["https://github.com/minio/docs/blob/main/source/operations/replication/multi-site-replication.rst", "https://github.com/minio/docs/blob/main/source/includes/common-replication.rst"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# MinIO site replication overview

Site replication joins independent deployments as peer sites that continuously replicate shared state. All sites must use the **same IDP** (the built-in MinIO IDP, OIDC or LDAP, with identical external config) and the same MinIO Server version. For production use Linux or Kubernetes, not macOS, Windows or unorchestrated containers.

## What replicates
Buckets and objects with their configuration, policies, tags, locks (retention and legal hold) and encryption settings; IAM users, groups, policies and policy mappings; STS credentials verifiable from the local root credentials; access keys (except those owned by `root`). Versioning is enabled on all buckets and cannot be disabled.

## What does not
Bucket notifications, lifecycle (ILM) configurations and site configuration settings. Since mc RELEASE.2023-12-02T02-03-28Z ILM *expiration* rules can be replicated: `mc admin replicate add --replicate-ilm-expiry`, or enable and disable later with `mc admin replicate update`.

## Initial IAM sync order
MinIO IDP: policies, local users, groups, access keys, policy mappings for users, mappings for STS users. OIDC and LDAP follow similar orders (LDAP includes groups; OIDC has no local users).

## Healing
- Peers resync damaged data from the site with the latest version.
- Since RELEASE.2023-07-18T17-49-40Z operations retry up to 3 times, then the scanner requeues them later.
- Failed or pending replications requeue on any GET or HEAD (for example `mc stat`) since RELEASE.2022-08-11T04-37-28Z.
- `mc admin replicate resync` actively rebuilds a site (since RELEASE.2022-12-02T23-48-47Z) without waiting for the scanner.

## Sync mode and proxying
Asynchronous is strongly recommended; synchronous (`mc admin replicate update --mode`) makes PUT performance depend on inter-site latency. Peers proxy GET/HEAD to other sites when an object is missing locally, which may return the latest version on the peer; LIST, DELETE and PUT are not proxied.

## Checked
2026-11-03. Confirmed against the MinIO docs source: Site Replication Overview page (multi-site-replication.rst) and the replication include (common-replication.rst). Removed: nothing; every claim was confirmed.
Method: documentation only; no commands were run.
