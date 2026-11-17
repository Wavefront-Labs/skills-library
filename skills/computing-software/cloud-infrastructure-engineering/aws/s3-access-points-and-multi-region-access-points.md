---
id: computing-software.cloud-infrastructure-engineering.aws.s3-access-points-and-multi-region-access-points
name: s3-access-points-and-multi-region-access-points
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, s3, s3-access-points, multi-region-access-point, vpc-only-access-point, bucket-policy-delegation, failover]
level: practitioner
status: docs-checked
description: "Split shared-bucket access into S3 Access Points (per-app policies, VPC-only, bucket policy delegation) and serve multi-region data via Multi-Region Access Points."
sources: ["https://docs.aws.amazon.com/AmazonS3/latest/userguide/access-points.html", "https://docs.aws.amazon.com/AmazonS3/latest/userguide/access-points-policies.html", "https://docs.aws.amazon.com/AmazonS3/latest/userguide/access-points-restrictions-limitations-naming-rules.html", "https://docs.aws.amazon.com/AmazonS3/latest/userguide/MultiRegionAccessPoints.html", "https://docs.aws.amazon.com/AmazonS3/latest/userguide/MultiRegionAccessPointRestrictions.html", "https://docs.aws.amazon.com/AmazonS3/latest/userguide/MrapOperations.html", "https://docs.aws.amazon.com/AmazonS3/latest/userguide/MultiRegionAccessPointRequests.html", "https://docs.aws.amazon.com/AmazonS3/latest/userguide/access-points-vpc.html", "https://docs.aws.amazon.com/AmazonS3/latest/userguide/MultiRegionAccessPointBucketReplication.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# S3 Access Points and Multi-Region Access Points

## 1. Access points: one policy per consumer
A data-lake bucket with 30 consumers turns its bucket policy into a 20 KB monster. Give each
consumer an access point with its own policy and network origin.
```bash
aws s3control create-access-point --account-id <ACCOUNT_ID> --name analytics-ro --bucket datalake \
  --vpc-configuration VpcId=vpc-analytics
aws s3control put-access-point-policy --account-id <ACCOUNT_ID> --name analytics-ro --policy '{
 "Version":"2012-10-17","Statement":[{"Effect":"Allow",
  "Principal":{"AWS":"arn:aws:iam::<ACCOUNT_ID>:role/analytics"},
  "Action":["s3:GetObject","s3:ListBucket"],
  "Resource":["arn:aws:s3:<REGION>:<ACCOUNT_ID>:accesspoint/analytics-ro","arn:aws:s3:<REGION>:<ACCOUNT_ID>:accesspoint/analytics-ro/object/curated/*"]}]}'
```
Delegate from the bucket policy so it doesn't need per-consumer statements:
```json
{"Effect": "Allow", "Principal": {"AWS": "*"}, "Action": "*",
 "Resource": ["arn:aws:s3:::datalake", "arn:aws:s3:::datalake/*"],
 "Condition": {"StringEquals": {"s3:DataAccessPointAccount": "<ACCOUNT_ID>"}}}
```
Clients use the access point ARN or alias as the bucket name:
`aws s3 ls s3://arn:aws:s3:<REGION>:<ACCOUNT_ID>:accesspoint/analytics-ro/curated/` or the
`...-s3alias` alias (works with tools expecting a bucket name).
- **VPC-only** access points reject requests that do not originate from the specified VPC; the network origin cannot be changed after creation.
- Block Public Access settings exist per access point too; they cannot be changed after the access point is created.

## 2. Multi-Region Access Points (MRAP)
A global endpoint that routes requests to the replicated data in the closest available Region
(AWS Global Accelerator underneath). Use the ARN `arn:aws:s3::<ACCOUNT_ID>:accesspoint/<alias>.mrap` as
the bucket name; the alias and the ARN cannot be used interchangeably.
```bash
aws s3control create-multi-region-access-point --account-id <ACCOUNT_ID> --details \
  'Name=docs-global,Regions=[{Bucket=docs-use1},{Bucket=docs-euw1}]' --region us-west-2
```
- Pair with **two-way replication** (with replica modification sync) between the buckets.
- **Failover controls**: set routing to active/passive (`submit-multi-region-access-point-routes`
  with `TrafficDialPercentage` 100/0) and flip during an incident. The routes call goes to the
  failover control plane in one of five Regions (us-east-1, us-west-2, ap-southeast-2,
  ap-northeast-1, eu-west-1); the caller also needs `s3:ListAllMyBuckets`.
- Requests require SigV4A signing (supported by current SDKs/CLI).

## Gotchas
- Access point names are unique per account and Region (not globally); a VPC configuration cannot be changed after creation.
- `ListBucket` through an access point needs the access point ARN resource (not `/object/*`).
- MRAP control-plane operations (create, delete) must be sent to us-west-2; see the S3 pricing page for MRAP charges.

## Verify
- [ ] Consumer role reads via its access point; the same role is denied when calling the bucket name directly (if bucket policy only delegates).
- [ ] VPC-only access point denies a request from outside the VPC.
- [ ] MRAP failover drill: dial one region to 0% and reads continue from the other.

## Checked

Checked 2026-10-27 against the S3 User Guide pages Access points, access point restrictions and limitations, access point policies, Multi-Region Access Points, MRAP restrictions and operations, and the botocore s3control model.
Confirmed: s3:DataAccessPointAccount delegation condition and the accesspoint/<name>/object/* resource form; names unique per account and Region; maximum 10,000 access points per account per Region; BPA fixed at creation; MRAP control plane in us-west-2 and failover routes in five Regions; TrafficDialPercentage 100 (active) or 0 (passive); SigV4A signing; two-way replication and replica modification sync guidance; MRAP routing via Global Accelerator; the MRAP is addressed by an arn:aws:s3::<account>:accesspoint/<alias>.mrap ARN; VPC-only access points reject requests that do not originate from the VPC.

Method: documentation only; no commands were run.
