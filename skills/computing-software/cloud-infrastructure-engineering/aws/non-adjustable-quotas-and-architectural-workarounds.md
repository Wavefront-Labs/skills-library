---
id: computing-software.cloud-infrastructure-engineering.aws.non-adjustable-quotas-and-architectural-workarounds
name: non-adjustable-quotas-and-architectural-workarounds
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, service-quotas, non-adjustable-quotas, hard-limits, claim-check-pattern, account-sharding, architecture-limits]
level: practitioner
status: draft
description: "Design around AWS hard limits: payload and size caps, timeouts and policy sizes, with claim-check, batching, sharding across accounts and splitting resources."
sources: ["Service Quotas User Guide - Viewing service quotas (Adjustable column)", "AWS Lambda Developer Guide - Lambda quotas", "Amazon API Gateway Developer Guide - Quotas", "IAM User Guide - IAM and AWS STS quotas"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Non-adjustable quotas and architectural workarounds

## Find them
```bash
aws service-quotas list-service-quotas --service-code lambda \
  --query 'Quotas[?Adjustable==`false`].[QuotaName,Value,Unit]' --output table
```
The Service Quotas console shows an "Adjustable" column; the per-service quotas page in each user guide is the full list (Service Quotas does not cover everything).

## Typical hard limits and the workaround
| Limit (check current values) | Workaround |
|---|---|
| Lambda synchronous payload ~6 MB, async payload, 15-minute timeout, deployment package size | claim-check: put the payload in S3 and pass the key; Step Functions or ECS/Batch for longer jobs; container images for bigger packages |
| API Gateway payload 10 MB | presigned S3 URLs for uploads/downloads |
| DynamoDB item 400 KB | store blobs in S3 with pointer; split items (vertical partitioning) |
| SQS/SNS/EventBridge message size | claim-check with S3 (Extended Client Library) |
| Step Functions state payload 256 KB | pass S3 pointers; Distributed Map reading S3 |
| IAM policy document size, managed policies per role (adjustable to a ceiling) | consolidate statements, wildcards with conditions, ABAC with tags, permission boundaries |
| Security group rules per ENI (rules x groups) | prefix lists, fewer broader groups, SG referencing |
| CloudFormation template size / resources per stack / outputs | nested stacks, split stacks by lifecycle, S3-hosted templates |
| Per-account API rate limits that are not adjustable | batching, caching, exponential backoff with jitter, spreading across accounts |

## Structural strategies
- **Account sharding:** cell-based architecture with many accounts, each with its own quotas (a standard way to scale past per-account limits).
- **Regional spreading** for per-region limits.
- **Batching and pagination:** Batch APIs (`SendMessageBatch`, `BatchWriteItem`), larger pages.
- **Caching** responses of describe/list calls instead of hot-polling control planes.

## Gotchas
- Some limits are soft in Service Quotas but have a ceiling AWS will not exceed; ask before designing around a raise.
- Hard limits change; re-check at design reviews and remove workarounds when no longer needed.

## Verify
- [ ] Design docs list the hard limits each component is near, with the chosen workaround.
- [ ] Load tests exercise payload sizes near limits (largest realistic document, upload).
