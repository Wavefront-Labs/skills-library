---
id: computing-software.cloud-infrastructure-engineering.aws.finding-and-backfilling-untagged-resources
name: finding-and-backfilling-untagged-resources
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, tagging, untagged-resources, tag-backfill, resource-explorer, tag-editor, required-tags, resourcegroupstaggingapi]
level: practitioner
status: draft
description: "Find untagged AWS resources across accounts and regions (Resource Explorer, Config required-tags, Tag Editor), infer owners from CloudTrail, and bulk-apply tags safely."
sources: ["AWS Resource Explorer User Guide - Search query syntax (tag:none)", "AWS Config Developer Guide - required-tags managed rule", "Resource Groups Tagging API Reference - GetResources and TagResources", "AWS Billing User Guide - AWS-generated cost allocation tags (aws:createdBy)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Finding and backfilling untagged resources

## Find them
- **Resource Explorer** (aggregator index, org-wide view):
```bash
aws resource-explorer-2 search --query-string "tag:none" --max-results 100
aws resource-explorer-2 search --query-string "resourcetype:ec2:instance -tag.key:cost-center"
```
- **AWS Config `required-tags`** rule: lists noncompliant resources per supported type; deploy via conformance pack across the org.
- **Tag Editor** (console, Resource Groups): search all regions by resource type and "(not tagged)" for a key; edit tags in bulk in the grid.
- Cost side: Cost Explorer grouped by the tag shows "No tag" spend; the CUR line items give resource ids for that spend.

Caveat: `resourcegroupstaggingapi get-resources` only returns resources that have, or once had,
tags (and supported types). Never-tagged resources can be missing from it, so do not use it alone to find untagged ones.

## Work out the owner
- Activate the AWS-generated `aws:createdBy` cost allocation tag (records the creator for many resource types from activation on).
- CloudTrail Lake / Athena on the trail: find the `Run*`/`Create*` event for the resource id and the principal.
- Account/OU ownership as the fallback: tag with the account's owning team.

## Apply in bulk
```bash
aws resourcegroupstaggingapi tag-resources \
  --resource-arn-list arn:aws:ec2:eu-west-1:111122223333:instance/i-0abc arn:aws:ec2:eu-west-1:111122223333:volume/vol-0def \
  --tags cost-center=100,owner=orders
```
- Up to 20 ARNs per call; check `FailedResourcesMap` in the response (unsupported types, permissions).
- Loop per account/region from a script assuming a role; log every change.
- Resources managed by CloudFormation/Terraform: tag in code, or the next deploy removes your tag (Terraform shows drift; CloudFormation leaves unmanaged tags but stack updates may reset tags it manages).

## Prevent recurrence
- SCP/IAM `aws:RequestTag` conditions require tags on create for key services.
- Tag policies to enforce values; default tags in IaC providers.
- Weekly report of `tag:none` counts per account to owners.

## Verify
- [ ] Untagged count per account recorded before and after; target < 5% of spend untagged.
- [ ] Bulk tagging script logs successes/failures; no IaC drift introduced.
