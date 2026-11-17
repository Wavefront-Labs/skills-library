---
id: computing-software.cloud-infrastructure-engineering.google-cloud.dual-region-and-hierarchical-namespace-buckets
name: dual-region-and-hierarchical-namespace-buckets
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, cloud-storage, dual-region-buckets, turbo-replication, hierarchical-namespace, hns-buckets, bucket-location, rpo]
level: practitioner
status: docs-checked
description: "Choose Cloud Storage location and namespace at creation: predefined or configurable dual-regions with turbo replication RPO, and hierarchical namespace buckets for AI."
sources: ["https://cloud.google.com/storage/docs/locations", "https://cloud.google.com/storage/docs/availability-durability#turbo-replication", "https://cloud.google.com/storage/docs/hns-overview", "https://cloud.google.com/storage/docs/create-hns-bucket"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Dual-region and hierarchical namespace buckets

Both are **creation-time** decisions: a bucket's location is chosen at creation, and the hierarchical namespace
setting cannot be changed after the bucket is created.

## 1. Dual-region
- Predefined dual-regions such as `EUR4` pair fixed regions (Finland and Netherlands for EUR4).
- Configurable dual-regions let you pick the two regions yourself from the list the locations page gives for each
  location code (for example code `EU` offers Belgium, Finland, Netherlands, Paris, Madrid and others; `DE` offers Frankfurt and Berlin).
- Default replication between the two regions targets 99.9% of new objects within 1 hour and 100% within 12 hours.
  Turbo replication targets 100% of new objects within 15 minutes (RPO).
- Check the locations and availability pages for the current way to select placement and turbo replication in
  the console, gcloud or API before scripting it.

| Location type | Replication |
|---|---|
| region | in one region |
| dual-region | two regions; default or turbo replication as above |
| multi-region | across a larger geographic area |

## 2. Hierarchical namespace (HNS)
```bash
gcloud storage buckets create gs://BUCKET_NAME --location=BUCKET_LOCATION --uniform-bucket-level-access --enable-hierarchical-namespace
```
- Uniform bucket-level access is required to create a bucket with HNS; HNS cannot be enabled on an existing bucket.
- HNS gives folders in a logical file system structure, with create, list, delete and atomic rename of folders that
  rename a folder and its child folders without deleting objects. Buckets get up to 8 times higher initial read and write QPS limits.
- Intended for Hadoop and Spark workloads (via the Cloud Storage connector) and AI/ML workloads.
- Upload, Rewrite and Compose create missing parent folders automatically; folders must be deleted explicitly.
- Not supported on HNS buckets: Bucket Lock, bucket relocations with write downtime, cross-bucket replication, object holds,
  object-level ACLs, Object Retention Lock and Object Versioning.
- A folder renamed with the rename operation keeps its objects' creation times, so age-based lifecycle rules apply to the renamed objects immediately.
- A folder can have an associated managed folder for access control; deleting the folder deletes its managed folder and IAM policies.

## Verify
- [ ] The bucket describe output shows the intended location and, for lake buckets, hierarchical namespace enabled.
- [ ] None of the unsupported features above are required for the bucket.

## Checked
Method: docs-only read of cited pages, 2026-11-08

Confirmed on the locations page, the availability and durability page (turbo and default replication targets), the HNS overview and the create-HNS-bucket page.
Removed: the `--placement`, `--rpo` and `gcloud storage folders create/list/rename` commands (no such
syntax appears on the cited pages), replication metric names, egress and replication billing claims, and the Storage Transfer Service relocation advice.
