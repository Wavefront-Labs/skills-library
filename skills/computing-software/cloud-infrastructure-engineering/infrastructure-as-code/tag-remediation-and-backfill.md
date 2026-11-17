---
id: computing-software.cloud-infrastructure-engineering.infrastructure-as-code.tag-remediation-and-backfill
name: tag-remediation-and-backfill
category: computing-software
field: cloud-infrastructure-engineering
product: infrastructure-as-code
tags: [infrastructure-as-code, iac, tagging-naming, tag-backfill, tag-remediation, aws-resource-groups-tagging-api, azure-policy-modify, cloud-custodian, default-tags, cost-allocation]
level: advanced
status: draft
description: "Find untagged or mistagged cloud resources and backfill tags safely: inventory queries, fixing in code first, bulk tagging APIs for unmanaged resources, policy auto-remediation and verification."
sources: ["AWS Resource Groups Tagging API reference - GetResources, TagResources (https://docs.aws.amazon.com/resourcegroupstagging/latest/APIReference/)", "Microsoft Learn - Azure Policy modify effect and remediation tasks (https://learn.microsoft.com/azure/governance/policy/how-to/remediate-resources)", "Cloud Custodian documentation - tag actions and mark-for-op (https://cloudcustodian.io/docs/)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Tag remediation and backfill

Goal: bring existing resources up to the tagging standard (owner, cost-center, environment,
managed-by) without fighting IaC drift and without breaking anything that keys off tags.

## 1. Measure the gap
AWS (per region; repeat across regions/accounts):
```bash
aws resourcegroupstaggingapi get-resources --region eu-west-1 --output json \
  | jq -r '.ResourceTagMappingList[] | select([.Tags[]?.Key] | index("cost-center") | not) | .ResourceARN'
```
(The Tagging API lists only resources that have, or once had, tags for some services — cross-check with AWS Config or Resource Explorer for full inventory.)
Azure:
```kusto
resources
| where isnull(tags['cost-center']) or tags['cost-center'] == ''
| summarize count() by type, subscriptionId
```
GCP: Cloud Asset Inventory export filtered on missing labels.
Split results into **managed by IaC** (has `managed-by` tag or appears in state) and **unmanaged**.

## 2. Fix managed resources in code (never by API)
Tagging a Terraform-managed resource by API is drift; the next apply removes it (or with
`default_tags`, fights it). Fix in code:
```hcl
provider "aws" {
  default_tags { tags = { cost-center = var.cost_center, owner = var.owner, environment = var.env, managed-by = "terraform" } }
}
```
Roll out per state with plan review: tag-only plans should show only `~ tags`/`tags_all` changes.
Resources not supporting `default_tags` (ASG-propagated tags, launch templates' instance tags,
some child resources) need explicit tag arguments. Ansible-managed hosts: add tags in the
provisioning role's `tags:` and rerun.

## 3. Backfill unmanaged resources
Derive values from evidence (account → cost center map, CloudTrail creator → owner, VPC → environment), then bulk-apply:
```bash
aws resourcegroupstaggingapi tag-resources --resource-arn-list <ARN1> <ARN2> ... \
  --tags cost-center=CC123,owner=team-data,tag-source=backfill-2026-10
```
(max 20 ARNs per call; script it with a CSV of ARN → tags reviewed by owners). Add a marker tag
(`tag-source=backfill-<date>`) so inferred values are distinguishable from authoritative ones.
Azure: `az tag update --resource-id <id> --operation merge --tags cost-center=CC123`.

## 4. Keep it fixed
- Azure Policy `modify` effect (inherit tag from resource group / subscription) + remediation task for existing resources.
- AWS: tag policies (enforced keys/values), SCP denying create without required tags for supported services, Cloud Custodian `mark-for-op` (notify owner, then stop/delete after N days for truly orphaned resources).
- CI policy as code (OPA/Checkov) blocks untagged resources in plans.

## Gotchas
- Changing tag values can break things: IAM ABAC conditions, cost allocation reports, backup selections, automation targeting by tag. Search for consumers before renaming keys.
- Tag keys are case-sensitive (`Owner` vs `owner` are different) — normalise in code and in policy.
- Cost allocation tags must be activated in the billing console and apply only going forward.

## Verify
- [ ] Untagged count per account trends to zero in the weekly report; managed resources show no tag drift in plans.
- [ ] `tag-source=backfill-*` resources are reviewed by owners and either confirmed (tag removed) or corrected.
