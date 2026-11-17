---
id: computing-software.cloud-infrastructure-engineering.aws.s3-bucket-naming-rules-and-namespaces
name: s3-bucket-naming-rules-and-namespaces
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, s3, bucket-naming, global-namespace, directory-buckets, bucket-sniping]
level: practitioner
status: docs-checked
description: "Name S3 buckets correctly: length and character rules, reserved prefixes and suffixes, why to avoid dots, directory bucket formats and defending against name squatting."
sources: ["https://docs.aws.amazon.com/AmazonS3/latest/userguide/bucketnamingrules.html", "https://docs.aws.amazon.com/AmazonS3/latest/userguide/directory-bucket-naming-rules.html", "https://docs.aws.amazon.com/AmazonS3/latest/userguide/bucket-owner-condition.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Bucket naming rules and namespaces

## 1. General purpose bucket rules
- 3-63 characters; lowercase letters, digits, hyphens and dots; start and end with a letter or digit.
- Not formatted like an IP address; no two adjacent dots.
- Reserved: prefixes `xn--`, `sthree-`, `amzn-s3-demo-`; suffixes `-s3alias`, `--ol-s3`, `.mrap`, `--x-s3`, `--table-s3`; the suffix `-an` is allowed only for account regional namespace buckets.
- Names in the shared global namespace are unique across all AWS accounts in a partition. After you delete a bucket, another account in the partition can create a bucket with the same name and receive requests meant for the old one; the name may not become reusable right away (or at all).

## 2. Avoid dots
With periods in the name you cannot use virtual-hosted-style addressing over HTTPS (the certificates do not match), and Transfer Acceleration cannot be used with such buckets. AWS recommends avoiding periods except for buckets used only for static website hosting (which is HTTP only). Use hyphens.

## 3. Directory buckets (S3 Express One Zone)
Format `base-name--<zone-id>--x-s3`, for example `scratch--use1-az4--x-s3`; the Zone ID (Availability Zone or Local Zone) suffix is mandatory, names are 3-63 characters including the suffix, and with the API you must supply the full suffix.

## 4. Naming convention that survives
Prefer the **account regional namespace**: create the bucket as `<your-prefix>-<12-digit-account-id>-<region>-an` and send `x-amz-bucket-namespace: account-regional` on CreateBucket (API parameter `BucketNamespace`, enum `account-regional` or `global`). AWS states only your account can ever own names in that namespace.
In the shared global namespace use `<org>-<purpose>-<env>-<guid>` (AWS recommends a GUID suffix, and not assuming a name is free until you have created it).
- Account ID and Region in a global-namespace name make collisions unlikely but do not reserve the name.
- Never derive names from user input or predictable patterns an attacker could pre-register (bucket sniping
  against your IaC or a deleted bucket your code still writes to).

## 5. Defend writes against the wrong owner
```bash
aws s3api put-object --bucket acme-logs-prod-123456789012-eu-west-1-an --key a.txt --body a.txt \
  --expected-bucket-owner 123456789012
```
`ExpectedBucketOwner` (SDK) / `x-amz-expected-bucket-owner` fails the call if someone else owns the bucket.

## Verify
- [ ] IaC lint rule enforces the convention; code paths writing to buckets set the expected owner.

## Checked

Checked 2026-10-27 against the S3 User Guide pages Bucket naming rules and Directory bucket naming rules, and the botocore s3 model (BucketNamespace enum).
Confirmed: 3-63 characters, allowed characters, no adjacent periods, not IP-formatted; reserved prefixes and suffixes; -an suffix for account regional namespace buckets; global namespace uniqueness per partition and name-reuse caveat; periods break HTTPS virtual-hosted addressing and Transfer Acceleration; directory bucket suffix uses a Zone ID and --x-s3. Corrected the directory bucket suffix wording and added the account regional namespace.

Method: documentation only; no commands were run.
