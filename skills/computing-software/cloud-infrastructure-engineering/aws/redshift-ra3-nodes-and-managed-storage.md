---
id: computing-software.cloud-infrastructure-engineering.aws.redshift-ra3-nodes-and-managed-storage
name: redshift-ra3-nodes-and-managed-storage
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, redshift, ra3-node-migration, managed-storage, elastic-resize, data-sharing]
level: advanced
status: docs-checked
description: "Move Redshift clusters from DC2 to RA3 with Redshift Managed Storage: node specs, elastic vs classic resize, and the features that need RG or RA3 nodes."
sources: ["https://docs.aws.amazon.com/redshift/latest/mgmt/working-with-clusters.html", "https://docs.aws.amazon.com/redshift/latest/mgmt/resizing-cluster.html", "https://docs.aws.amazon.com/redshift/latest/mgmt/managing-cluster-multi-az.html", "https://docs.aws.amazon.com/redshift/latest/mgmt/managing-cluster-recovery.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# RA3 node types and managed storage

## 1. Model
RA3 (and the newer Graviton-based RG type) separate compute from **Redshift Managed Storage (RMS)**: large local
SSDs hold hot data and RMS offloads the rest to Amazon S3 automatically. You size the node count for performance and
pay for the managed storage you use, independently of nodes. Note: the current guide recommends choosing RG or RA3
for new clusters; for datasets under 1 TB compressed it still recommends DC2 for best price-performance, and RA3 if
you expect growth. RG nodes add Graviton instances and an integrated data lake query engine; RA3 uses Spectrum.

## 2. Sizing the move
RA3 node types and managed storage limit per node (from the node-type tables):
| Node type | vCPU | RAM (GiB) | Node range at create | Managed storage per node |
|---|---|---|---|---|
| ra3.large | 2 | 16 | 1 (single-node) or 2-16 | 1 TB single-node, 8 TB multi-node |
| ra3.xlplus | 4 | 32 | 1 or 2-16 | 4 TB single-node, 32 TB multi-node |
| ra3.4xlarge | 12 | 96 | 2-32 | 128 TB |
| ra3.16xlarge | 48 | 384 | 2-128 | 128 TB |
Confirm node count with a snapshot restore and workload replay; the console "Help me choose" calculator also
recommends a configuration. A resize from `dc2.large` to `ra3.large` automatically converts interleaved sort keys
to compound.

## 3. Migrate
```bash
aws redshift resize-cluster --cluster-identifier dw --node-type ra3.4xlarge --number-of-nodes 4 --no-classic
aws redshift describe-resize --cluster-identifier dw
```
- **Elastic resize** (recommended first option) can change node type, for example DC2 to RG or RA3, and averages
  about ten minutes. It takes a snapshot, running queries are dropped on completion when the node type changes, and
  it has limits: RG/RA3 clusters support growth up to four times the node count and reduction to a quarter.
  Single-node to multi-node needs classic resize.
- **Classic resize** handles changes outside elastic limits. When the target is RG or RA3 it uses backup and
  restore: the source restarts and is unavailable for a few minutes, then reads and writes continue while the
  resize runs in the background. Prerequisites for that behaviour include data under 2 PB and a manual snapshot
  taken within the previous 10 hours.
- Alternatively restore a snapshot into a new RA3 cluster and switch endpoints. Test on a restored snapshot first
  and check WLM and parameter groups.

## 4. What RG and RA3 unlock
Multi-AZ deployments (provisioned RG or RA3 clusters only, same compute rate as single-AZ) and cluster relocation
to another Availability Zone (supported for RG and RA3). Data sharing and concurrency scaling for writes are
documented generally; check their pages for node-type requirements.

## 5. Cost watch
Managed storage is billed by use, so unload or archive cold tables (to S3 and Spectrum) and drop staging tables.
Prices were not checked.

## Verify
- [ ] Workload replay on RA3 meets the query SLA; managed storage usage tracked in Cost Explorer.

## Checked
Date: 2026-10-27. Documentation release: Amazon Redshift Management Guide (latest). Confirmed: RA3 node type
names and specs, node ranges, storage per node, RG introduction, DC2 under-1-TB guidance, elastic and classic
resize behaviour, resize limits, interleaved-to-compound conversion on DC2 to RA3, the `resize-cluster` `Classic`
parameter (botocore redshift 2012-12-01), Multi-AZ and relocation node-type support. Removed the claim that
classic resize is hours and read-only (an enhanced classic resize to RG or RA3 allows read and write), the
`ra3.xlplus`/`ra3.4xlarge` mapping advice, DS2 mention, and unconfirmed RA3-only claims for data sharing, zero-ETL and
write concurrency scaling.
Method: documentation only; no commands were run.
