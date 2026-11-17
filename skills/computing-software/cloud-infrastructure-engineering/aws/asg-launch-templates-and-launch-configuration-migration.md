---
id: computing-software.cloud-infrastructure-engineering.aws.asg-launch-templates-and-launch-configuration-migration
name: asg-launch-templates-and-launch-configuration-migration
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, auto-scaling, launch-template-asg, launch-configuration-migration, instance-refresh]
level: practitioner
status: docs-checked
description: "Move Auto Scaling groups off deprecated launch configurations to launch templates, handle version pinning ($Latest vs $Default) and roll out with instance refresh."
sources: ["https://docs.aws.amazon.com/autoscaling/ec2/userguide/migrate-to-launch-templates.html", "https://docs.aws.amazon.com/autoscaling/ec2/userguide/launch-configurations.html", "https://docs.aws.amazon.com/cli/latest/reference/autoscaling/update-auto-scaling-group.html", "https://docs.aws.amazon.com/cli/latest/reference/autoscaling/start-instance-refresh.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Launch templates and migrating off launch configurations

Launch configurations are deprecated: since January 1, 2023 new EC2 instance types are not supported in them, and
accounts created on or after October 1, 2024 cannot create launch configurations by any method.

## 1. Convert
```bash
aws autoscaling describe-launch-configurations --launch-configuration-names web-lc-v7 > lc.json
# translate fields into a launch template (console: "Copy to launch template" does this)
aws ec2 create-launch-template --launch-template-name web --launch-template-data '{
  "ImageId":"ami-0abc","InstanceType":"m7g.large","IamInstanceProfile":{"Name":"web"},
  "SecurityGroupIds":["sg-0abc"],"UserData":"<BASE64>",
  "MetadataOptions":{"HttpTokens":"required","HttpPutResponseHopLimit":2},
  "TagSpecifications":[{"ResourceType":"instance","Tags":[{"Key":"app","Value":"web"}]}]}'
```
Check every field of the launch configuration against the template (the console's copy-to-template action does
this); keep security groups and IAM instance profiles that the old configuration used, and test rollback before you switch.

## 2. Point the ASG at it
```bash
aws autoscaling update-auto-scaling-group --auto-scaling-group-name web \
  --launch-template LaunchTemplateName=web,Version='$Default'
```
| Version | Meaning |
|---|---|
| `$Latest` | newest version at each launch: any new version goes live immediately |
| `$Default` | the version you promote with `modify-launch-template --default-version N` |
| `3` | pinned |
Prefer `$Default` or pinned numbers with a promotion step.

## 3. Roll existing instances
```bash
aws autoscaling start-instance-refresh --auto-scaling-group-name web \
  --preferences '{"MinHealthyPercentage":90,"InstanceWarmup":120,"SkipMatching":true,"AutoRollback":true}'
```
`SkipMatching` (and `DesiredConfiguration`) make the refresh fail on groups that use attribute-based instance selection (`InstanceRequirements`).

## 4. Unlocks
Mixed instances policies and attribute-based instance type selection need a launch template.

## Verify
- [ ] ``describe-auto-scaling-groups --query 'AutoScalingGroups[?LaunchConfigurationName!=`null`].AutoScalingGroupName'`` is empty.
- [ ] Instance refresh completes with all instances on the template version.

## Checked

Checked 2026-10-27 against the Amazon EC2 Auto Scaling User Guide (launch configurations, migrate to launch templates, instance refresh), the aws-cli update-auto-scaling-group and start-instance-refresh references and the botocore autoscaling model.
- Corrected: dates for the deprecation (no new instance types since January 1, 2023; accounts created on or after October 1, 2024 cannot create launch configurations); the group's default launch template version is `$Default`; `SkipMatching` fails with attribute-based instance selection; the JMESPath filter now uses a quoted `null`.
- Confirmed: `RefreshPreferences` keys (MinHealthyPercentage, InstanceWarmup, SkipMatching, AutoRollback).
- Removed: the unverified claim list about network interfaces and other features that launch templates unlock.

Method: documentation only; no commands were run.
