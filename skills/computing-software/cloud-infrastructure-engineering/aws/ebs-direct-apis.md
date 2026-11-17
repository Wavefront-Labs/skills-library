---
id: computing-software.cloud-infrastructure-engineering.aws.ebs-direct-apis
name: ebs-direct-apis
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, ebs, ebs-direct-apis, changed-block-tracking, snapshots, backup]
level: advanced
status: docs-checked
description: "Read and write EBS snapshot blocks directly with the EBS direct APIs: list changed blocks between snapshots, fetch blocks, and build snapshots from external data."
sources: ["https://docs.aws.amazon.com/ebs/latest/userguide/ebs-accessing-snapshot.html", "https://docs.aws.amazon.com/ebs/latest/userguide/ebsapi-elements.html", "https://docs.aws.amazon.com/ebs/latest/userguide/ebsapi-permissions.html", "https://docs.aws.amazon.com/ebs/latest/userguide/ebsapi-performance.html", "https://docs.aws.amazon.com/ebs/latest/userguide/ebsapi-pricing.html", "https://docs.aws.amazon.com/ebs/latest/APIReference/Welcome.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# EBS direct APIs

**Use:** backup tools and migrations that need snapshot data without attaching a volume, or incremental
diffs between snapshots.

## 1. Read side
```bash
aws ebs list-snapshot-blocks --snapshot-id snap-0new --max-results 1000
aws ebs list-changed-blocks --first-snapshot-id snap-0old --second-snapshot-id snap-0new
aws ebs get-snapshot-block --snapshot-id snap-0new --block-index 1024 --block-token <TOKEN> block.bin
```
- Block size 512 KiB. `ListChangedBlocks` works between snapshots of the same volume lineage.
- Each block returns a checksum (SHA256, base64) to verify.

## 2. Write side: create a snapshot from arbitrary data
```bash
SNAP=$(aws ebs start-snapshot --volume-size 100 --timeout 60 --description "from on-prem image" --query SnapshotId --output text)
aws ebs put-snapshot-block --snapshot-id $SNAP --block-index 0 --block-data fileb://block0.bin \
  --data-length 524288 --checksum <BASE64_SHA256> --checksum-algorithm SHA256
aws ebs complete-snapshot --snapshot-id $SNAP --changed-blocks-count 1
```
`--parent-snapshot-id` on `start-snapshot` creates an incremental snapshot on top of an existing one.

## 3. Practicalities
- Billing: ListSnapshotBlocks and ListChangedBlocks are charged per request, GetSnapshotBlock per block returned and PutSnapshotBlock per block written (see EBS pricing); millions of blocks add up.
- High throughput needs parallel requests with a separate connection per thread (the performance page's worked example reaches about 500 MB/s with 100 connections); build in retries for throttling and timeouts, and check the EBS direct APIs service quotas.
- Interface VPC endpoints are supported for the EBS direct APIs and avoid NAT gateway data processing for private subnets.
- Encrypted snapshots also need KMS permissions: see the "Control access" page for the key policy example; a customer managed key needs an explicit key policy, while the default AWS managed EBS key is usable by principals in the account.

## Verify
- [ ] Volume created from the written snapshot mounts and checksums of files match the source.

## Checked

Checked 2026-10-27 against the EBS User Guide pages on the EBS direct APIs (concepts, permissions, checksums, performance, pricing) and the botocore ebs service model (2019-11-02).
Confirmed: block index in units of 512 KiB; Base64-encoded SHA256 checksums on read and required on write; ListChangedBlocks only between snapshots of the same volume and lineage; command shapes: ListSnapshotBlocks MaxResults 100-10000, StartSnapshot Timeout 10-4320 minutes and ParentSnapshotId, PutSnapshotBlock with Checksum and ChecksumAlgorithm SHA256, CompleteSnapshot ChangedBlocksCount; pricing structure per request or per block; VPC interface endpoint support. Removed the unconfirmed endpoint service name, KMS action names and per-snapshot rate limit statement.

Method: documentation only; no commands were run.
