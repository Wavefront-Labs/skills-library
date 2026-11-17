---
id: computing-software.cloud-infrastructure-engineering.aws.image-builder-lifecycle-policies
name: image-builder-lifecycle-policies
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, image-builder, image-lifecycle-policy, ami-cleanup, deprecation]
level: advanced
status: docs-checked
description: "Automate retirement of old Image Builder AMIs and container images with lifecycle policies: deprecate, disable, delete by age or count, with exclusion rules."
sources: ["https://docs.aws.amazon.com/imagebuilder/latest/userguide/manage-image-lifecycles.html", "https://docs.aws.amazon.com/cli/latest/reference/imagebuilder/create-lifecycle-policy.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Image Builder lifecycle policies

## 1. Execution role
Create an IAM role whose trust policy lets the Image Builder service principal assume it and which
grants the lifecycle actions; you need permission to pass it. Enabled policies run once per day.

## 2. Policy: deprecate after 30 days, delete beyond the last 5
```bash
aws imagebuilder create-lifecycle-policy --name web-ami-retention \
  --execution-role arn:aws:iam::<ACCOUNT_ID>:role/ImageBuilderLifecycle \
  --resource-type AMI_IMAGE \
  --policy-details '[
    {"action":{"type":"DEPRECATE"},"filter":{"type":"AGE","value":30,"unit":"DAYS"}},
    {"action":{"type":"DELETE","includeResources":{"amis":true,"snapshots":true}},
     "filter":{"type":"COUNT","value":5},
     "exclusionRules":{"amis":{"isPublic":true,"lastLaunched":{"value":14,"unit":"DAYS"},"tagMap":{"keep":"true"}}}}]' \
  --resource-selection '{"recipes":[{"name":"web","semanticVersion":"1.x.x"}]}'
```
- Actions: `DEPRECATE`, `DISABLE`, `DELETE`; at most one rule per action type per policy.
- Filters: `AGE` (with `unit` DAYS, WEEKS, MONTHS or YEARS) or `COUNT`, with optional `retainAtLeast`.
- AMI exclusions: public, shared accounts, Regions, last launched, tags.
- Select by recipe or by tags (`--resource-selection '{"tagMap":{"pipeline":"web"}}'`).
- `CONTAINER_IMAGE` policies support only `DELETE`.

## 3. Check runs
```bash
aws imagebuilder list-lifecycle-executions --resource-arn <POLICY_ARN>
aws imagebuilder list-lifecycle-execution-resources --lifecycle-execution-id <ID>
```

## Gotchas
- Use the `lastLaunched` exclusion so AMIs still in use are kept.
- The name and resource type cannot be changed after creation.

## Verify
- [ ] After a run, only the newest 5 AMIs (plus exclusions) remain and their snapshots are gone.

## Checked
2026-10-28. Confirmed against the Image Builder user guide page "Manage image lifecycles", the AWS CLI reference for create-lifecycle-policy (daily run, trust policy, one rule per action, container policies DELETE only, name and type immutable) and the imagebuilder botocore model (actions, AGE/COUNT filters, units, retainAtLeast, exclusion rule members, resource selection by recipes or tagMap, resource types). Removed unconfirmed claims: the managed policy name and service principal string, DEPRECATE launch-hiding behaviour, ECR wording and the cross-Region copy note.
Method: documentation only; no commands were run.
