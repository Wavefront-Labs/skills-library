---
id: computing-software.cloud-infrastructure-engineering.aws.tagging-strategy-and-tag-policies
name: tagging-strategy-and-tag-policies
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, tagging, tag-policy, tag-policies, resource-tags, cost-allocation-tags, tag-editor, resource-groups, abac, aws-organizations, scp, enforce-tags, tag-compliance, aws-config, required-tags, resource-explorer, tag-policy-syntax, tag-compliance-report]
level: practitioner
status: draft
description: "Design and enforce an AWS tagging standard: the minimal tag set, Organizations tag policies, SCPs that deny untagged creates, Config required-tags remediation, cost allocation activation and ABAC use."
sources: ["AWS Whitepaper - Best Practices for Tagging AWS Resources", "AWS Organizations User Guide - Tag policies", "AWS Billing User Guide - User-defined cost allocation tags", "AWS Config - required-tags managed rule"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Tagging strategy and tag policies — tags that are actually there when the bill arrives

**Goal:** every billable resource carries the same small set of tags, new resources cannot
be created without them, drift is reported and fixed, and the tags drive cost reports and
ABAC permissions.

## 1. The tag set (keep it small)
| Key | Values | Used by |
|---|---|---|
| `owner` | team alias / email list | paging, cleanup |
| `cost-center` | finance code | chargeback |
| `environment` | `prod`/`staging`/`dev`/`sandbox` | SCPs, backup plans, ABAC |
| `application` | service name | Cost Explorer grouping, Resource Groups |
| `data-classification` | `public`/`internal`/`confidential`/`restricted` | security controls |
| `managed-by` | `terraform`/`cdk`/`manual` | drift triage |
- Lowercase kebab keys; fixed value vocabularies; no PII in values. Tags are visible to
  anyone with `Describe*` — never secrets.
- Prefix org-mandated keys if you must coexist with vendor tags (`org:owner`).
- Decide now: keys are case-sensitive in most services, and tag policies treat `Owner` and
  `owner` as different.

## 2. Enforce with Organizations tag policies
```json
{"tags":{"environment":{
  "tag_key":{"@@assign":"environment"},
  "tag_value":{"@@assign":["prod","staging","dev","sandbox"]},
  "enforced_for":{"@@assign":["ec2:instance","ec2:volume","rds:db","s3:bucket","lambda:function"]}
}}}
```
- Enable the **tag policies** feature in Organizations; attach to OUs. Without
  `enforced_for`, a policy only *reports* non-compliance; with it, tagging operations using a
  wrong value/case on listed resource types are **rejected**.
- Compliance report: Organizations → Policies → Tag policies → *Resources compliance*, or
  `aws organizations ... ` + `aws resourcegroupstaggingapi get-compliance-summary`.
- Tag policies cannot require a tag's *presence* — that is the job of SCPs/Config.

## 3. Deny creation without tags (SCP)
```json
{"Effect":"Deny","Action":["ec2:RunInstances"],"Resource":"arn:aws:ec2:*:*:instance/*",
 "Condition":{"Null":{"aws:RequestTag/cost-center":"true"}}}
```
- Works only for actions that support `aws:RequestTag` at create time (EC2, RDS, Lambda,
  S3 `CreateBucket` partly, many others — check the service authorization reference).
- Pair with `Deny ec2:CreateTags/DeleteTags` unless `aws:ResourceTag` conditions, to stop
  tag tampering, and allow exceptions for the IaC deploy role via `aws:PrincipalArn`.

## 4. Detect and fix drift
- AWS Config managed rule **`required-tags`** (`tag1Key=cost-center,tag2Key=owner,…`) across
  the org via an organization conformance pack; remediation: SSM Automation
  `AWS-SetRequiredTags` or an EventBridge → Lambda that copies tags from the
  parent (e.g. volume ← instance, ENI ← instance).
- **Tag Editor** (console) for bulk fixes across regions; **Resource Explorer** / Tagging
  API for queries: `aws resourcegroupstaggingapi get-resources --tag-filters Key=owner`
  (note: not every service is covered — a resource missing from the API is not proof it is tagged).
- Propagate automatically where the service can: ASG `PropagateAtLaunch`, EKS
  `--tags` on node groups, `Service Catalog` TagOptions, CDK `Tags.of(app).add()`,
  Terraform `default_tags` in the provider block.

## 5. Cost allocation and ABAC
- Billing → **Cost allocation tags** → activate `cost-center`, `application`, `environment`.
  Tags only appear in Cost Explorer/CUR **from activation onward**; old spend is untagged
  forever. Activation takes up to 24 h; the CUR column is `resource_tags_user_<key>`.
- AWS-generated `aws:createdBy` tag shows who created a resource (CloudTrail-based).
- **ABAC**: IAM policies with `"Condition":{"StringEquals":{"aws:ResourceTag/environment":"${aws:PrincipalTag/environment}"}}`
  let one policy scale across teams; mark the tag `environment` as a *control* tag and
  lock changes to it (SCP denying `*:TagResource` on that key).

## 6. Rollout
1. Publish the standard (one page, with value lists) and a "tags for IaC" snippet.
2. Report-only tag policy + Config rule for 2–4 weeks; dashboard of non-compliance per account.
3. Bulk fix with Tag Editor / scripts, by owner.
4. Switch to `enforced_for` + SCP denies, starting with sandboxes.
5. Activate cost allocation tags and build Cost Explorer views grouped by `cost-center`.

## Gotchas
- EBS volumes, snapshots, ENIs and NAT gateways are the usual untagged cost — they inherit
  nothing by default.
- Data transfer, support plans and marketplace charges cannot be tagged; expect an
  "untagged" residual.
- Tag limits: 50 tags/resource, key ≤ 128 chars, value ≤ 256, `aws:` prefix reserved.
- Tag policies evaluate only *tagging operations*; existing wrong-case tags remain until touched.
- Cost allocation tag activation is per payer account; member-account activation does nothing.
- Unconfirmed: current `enforced_for` resource-type list — check the tag policy syntax page.

## Verify
- [ ] `RunInstances` without `cost-center` is denied in a sandbox account; the IaC role is exempt.
- [ ] `required-tags` rule shows < 5 % non-compliant resources after remediation.
- [ ] Cost Explorer grouped by `cost-center` shows < 10 % "No tag key" after a full month.
- [ ] A tagging operation with `Environment=Prod` (wrong case) is rejected where enforced.
- [ ] An ABAC test user can only stop instances with their own `environment` tag.
