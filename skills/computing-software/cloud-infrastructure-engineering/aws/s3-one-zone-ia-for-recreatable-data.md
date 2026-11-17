---
id: computing-software.cloud-infrastructure-engineering.aws.s3-one-zone-ia-for-recreatable-data
name: s3-one-zone-ia-for-recreatable-data
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, s3, one-zone-ia, storage-classes, lifecycle, cost-optimization]
level: practitioner
status: docs-checked
description: "Use S3 One Zone-IA for re-creatable or secondary-copy data: when the single-AZ risk is acceptable, minimums and fees, lifecycle and replication destinations."
sources: ["https://docs.aws.amazon.com/AmazonS3/latest/userguide/storage-class-intro.html", "https://docs.aws.amazon.com/AmazonS3/latest/userguide/lifecycle-transition-general-considerations.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# One Zone-IA for re-creatable data

## 1. Trade-off
Stores data in **one AZ**, which is less expensive than Standard-IA. Designed for the same 99.999999999% durability as Standard-IA,
but the data is not resilient to the physical loss of the AZ, and availability is lower (designed for 99.5%).

## 2. Good fits
- Thumbnails, transcodes, derived datasets you can regenerate from a master copy.
- Object replicas when configuring Cross-Region Replication (a use AWS recommends).
- On-prem backup copies where another copy exists elsewhere.
Bad fit: the only copy of anything.

## 3. Costs that bite
- 30-day minimum storage charge, 128 KB minimum billable object size, per-GB retrieval fee.
- Lifecycle transition request charges per object: many small objects can cost more to move than they save.

## 4. Use it
```bash
aws s3 cp renders/ s3://media-derived/renders/ --recursive --storage-class ONEZONE_IA
```
Lifecycle:
```json
{"Rules":[{"ID":"derived-to-ozia","Status":"Enabled","Filter":{"Prefix":"thumbs/"},
  "Transitions":[{"Days":30,"StorageClass":"ONEZONE_IA"}]}]}
```
Replication rule: `"Destination":{"Bucket":"arn:aws:s3:::backup-dr","StorageClass":"ONEZONE_IA"}`.

## Verify
- [ ] `aws s3api head-object` shows `StorageClass: ONEZONE_IA`.
- [ ] A regeneration path (job or source copy) is documented for every One Zone-IA prefix.

## Checked

2026-10-24 against the AWS documentation (docs.aws.amazon.com, current Amazon S3 User Guide) and the botocore API models. Confirmed: single AZ, 99.5% designed availability, designed durability, 30-day minimum storage duration, 128 KB minimum billable size, per-GB retrieval fee, recommended uses (re-creatable data, CRR replicas), transition request charge per object, `StorageClass` in replication Destination. Removed the unconfirmed 30-days-in-Standard prerequisite.

Method: documentation only; no commands were run.
