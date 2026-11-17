---
id: computing-software.cloud-infrastructure-engineering.aws.s3-requester-pays-and-object-tagging
name: s3-requester-pays-and-object-tagging
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, s3, requester-pays, object-tagging, abac, data-sharing, cost-allocation]
level: practitioner
status: docs-checked
description: "Share datasets with Requester Pays buckets (headers, IAM, limits) and use S3 object tags for access control, lifecycle and replication filters, within their costs."
sources: ["https://docs.aws.amazon.com/AmazonS3/latest/userguide/RequesterPaysBuckets.html", "https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-tagging.html", "https://docs.aws.amazon.com/AmazonS3/latest/userguide/tagging-and-policies.html", "https://docs.aws.amazon.com/AmazonS3/latest/userguide/troubleshoot-403-errors.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# S3 Requester Pays and object tagging

## 1. Requester Pays
The **requester** pays request and data-transfer charges; the owner still pays storage.
For public/partner datasets where egress would otherwise land on you.
```bash
aws s3api put-bucket-request-payment --bucket genomes-data --request-payment-configuration Payer=Requester
# consumers must opt in on every request:
aws s3 cp s3://genomes-data/run1/sample.bam . --request-payer requester
aws s3api get-object --bucket genomes-data --key run1/sample.bam out.bam --request-payer requester
```
- Requests without `x-amz-request-payer: requester` get **403** — the classic confusion.
- **Anonymous access is not allowed** on Requester Pays buckets (requester must be an AWS
  identity to bill). Combine with a bucket policy granting the partners/`*` authenticated read.
- If the requester assumes a role in *your* account, you pay — they must use their own credentials.
- The bucket owner is still charged for requests that return AccessDenied (403) when they come from the owner's own account or organization.

## 2. Object tags
Up to **10 tags per object**, key ≤ 128 chars, value ≤ 256. Tags are set on upload or later:
```bash
aws s3api put-object --bucket docs --key a.pdf --body a.pdf --tagging 'classification=confidential&team=legal'
aws s3api put-object-tagging --bucket docs --key a.pdf --tagging 'TagSet=[{Key=classification,Value=public}]'
aws s3api get-object-tagging --bucket docs --key a.pdf
```
Uses:
- **Access control**: condition `s3:ExistingObjectTag/classification` in bucket/IAM policies;
  `s3:RequestObjectTag/<key>` and `s3:RequestObjectTagKeys` to force tags on upload.
- **Lifecycle filters** (`Filter.Tag` / `And` with prefix and size) — e.g. expire `temp=true` after 7 days.
- **Replication filters** and S3 Batch Operations "replace tags" jobs for bulk tagging.
- Analytics/storage class analysis filters.

## Gotchas
- `put-object-tagging` **replaces** the whole tag set; read-modify-write to add one tag.
- Tagging is billed (tag requests such as `PutObjectTagging` are charged as PUT requests, see S3 pricing), so
  tagging billions of objects is a line item. Prefixes are free; use prefixes for structure, tags for cross-cutting labels.
- A policy denying `GetObject` without the tag also blocks objects uploaded before tagging was enforced.

## Verify
- [ ] Partner request without `--request-payer` → 403; with it → success, and the charge appears on the partner's bill.
- [ ] Objects tagged `classification=confidential` are denied to roles without the matching principal tag.
- [ ] Lifecycle rule with a tag filter expires only tagged objects (check after rule runs).

## Checked

Checked 2026-10-27 against the S3 User Guide pages Using Requester Pays buckets, Categorizing your storage using tags, Tagging and access control policies, Troubleshoot access denied errors, and the botocore s3 model.
Confirmed: requester pays request and download costs while the owner pays storage; anonymous access is not allowed on Requester Pays buckets; x-amz-request-payer header, RequestPayer parameter and --request-payer; the account that owns an assumed role is charged; the owner is charged for AccessDenied requests from its own account or organization; up to 10 tags per object, key up to 128 and value up to 256 Unicode characters, case sensitive; put-object-tagging replaces the tag set; s3:ExistingObjectTag, s3:RequestObjectTag and s3:RequestObjectTagKeys condition keys; lifecycle, replication (ReplicationRuleFilter Tag) and analytics filters accept tags. Removed the unconfirmed per-10,000-tag price and cost-allocation claims.

Method: documentation only; no commands were run.
