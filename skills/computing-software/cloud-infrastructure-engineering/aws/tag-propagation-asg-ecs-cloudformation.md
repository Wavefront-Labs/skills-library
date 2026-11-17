---
id: computing-software.cloud-infrastructure-engineering.aws.tag-propagation-asg-ecs-cloudformation
name: tag-propagation-asg-ecs-cloudformation
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, tagging, tag-propagation, propagate-tags, auto-scaling, ecs, cloudformation, default-tags]
level: practitioner
status: draft
description: "Tag the resources AWS creates for you: ASG PropagateAtLaunch, launch template tag specifications, ECS propagateTags, CloudFormation stack tags, CDK and Terraform default tags."
sources: ["Amazon EC2 Auto Scaling User Guide - Tag Auto Scaling groups and instances", "Amazon ECS Developer Guide - Tagging your Amazon ECS resources (propagateTags, managed tags)", "AWS CloudFormation User Guide - Resource tag propagation from stack tags"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Tag propagation from ASGs, ECS and CloudFormation

**Problem:** you tag the group, service or stack, but the instances, volumes, tasks and snapshots
they create are untagged, so cost reports show "No tag".

## Auto Scaling groups
```bash
aws autoscaling create-or-update-tags --tags \
  ResourceId=web-asg,ResourceType=auto-scaling-group,Key=cost-center,Value=100,PropagateAtLaunch=true
```
- `PropagateAtLaunch=true` copies the tag to instances at launch (not to existing instances).
- Volumes and ENIs need **launch template** `TagSpecifications`:
```json
"TagSpecifications":[{"ResourceType":"instance","Tags":[{"Key":"cost-center","Value":"100"}]},
                     {"ResourceType":"volume","Tags":[{"Key":"cost-center","Value":"100"}]},
                     {"ResourceType":"network-interface","Tags":[{"Key":"cost-center","Value":"100"}]}]
```
- EKS managed node groups: tags on the node group do not reach instances; use a launch template.

## ECS
```bash
aws ecs create-service ... --enable-ecs-managed-tags --propagate-tags SERVICE
aws ecs run-task ... --propagate-tags TASK_DEFINITION
```
- `propagateTags` = `SERVICE` or `TASK_DEFINITION` copies those tags to tasks; managed tags add
  `aws:ecs:serviceName` / `clusterName`. Fargate task cost then shows up by tag (with split cost allocation data for EC2-backed tasks).
- Account setting `tagResourceAuthorization` and the new ARN format are prerequisites in older accounts.

## CloudFormation
- Stack-level tags (`aws cloudformation create-stack --tags Key=cost-center,Value=100`) propagate to
  every resource in the stack that supports tags, including nested stacks.
- Resources that CloudFormation creates indirectly (e.g. instances launched by an ASG) still need the ASG/launch template settings above.
- StackSets: tags set on the stack set apply to stack instances.

## IaC defaults
```hcl
provider "aws" {
  default_tags {
    tags = { cost-center = "100", owner = "orders" }
  }
}
```
```ts
Tags.of(app).add('cost-center', '100');   // CDK: applies to all taggable constructs
```

## Snapshots and backups
- RDS/Aurora `CopyTagsToSnapshot=true`; EBS snapshots via DLM `CopyTags`; AWS Backup `CopyTags` on recovery points (on by default for many types).
- EC2 `create-snapshots --copy-tags-from-source volume`.

## Gotchas
- Propagated tags do not update on existing children when you change the parent; re-tag or roll the fleet.
- Tag limits (50) can be hit when stack tags plus resource tags plus propagated tags combine.

## Verify
- [ ] Newly launched ASG instance, its root volume and ENI carry the tags.
- [ ] ECS tasks list propagated tags (`describe-tasks --include TAGS`).
- [ ] Cost Explorer "No tag" share for the key trends down.
