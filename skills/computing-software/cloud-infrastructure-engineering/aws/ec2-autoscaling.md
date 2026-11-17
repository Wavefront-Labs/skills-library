---
id: computing-software.cloud-infrastructure-engineering.aws.ec2-autoscaling
name: ec2-autoscaling
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, ec2, auto-scaling, autoscaling-group, asg, launch-templates, mixed-instances-policy, spot-instances, price-capacity-optimized, warm-pools, lifecycle-hooks, instance-refresh]
level: practitioner
status: docs-checked
description: "Run EC2 fleets with Auto Scaling groups: mixed instances and allocation strategies, lifecycle hooks, warm pools and instance refresh for rolling out new AMIs."
sources:
  - https://docs.aws.amazon.com/autoscaling/ec2/userguide/ec2-auto-scaling-mixed-instances-groups.html
  - https://docs.aws.amazon.com/autoscaling/ec2/userguide/allocation-strategies.html
  - https://docs.aws.amazon.com/autoscaling/ec2/userguide/lifecycle-hooks-overview.html
  - https://docs.aws.amazon.com/autoscaling/ec2/userguide/ec2-auto-scaling-warm-pools.html
  - https://docs.aws.amazon.com/autoscaling/ec2/userguide/asg-instance-refresh.html
  - https://docs.aws.amazon.com/autoscaling/ec2/userguide/instance-refresh-overview.html
  - https://docs.aws.amazon.com/autoscaling/ec2/userguide/understand-instance-refresh-default-values.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# EC2 Auto Scaling — fleets that grow, shrink, heal and roll themselves

**Goal:** an Auto Scaling group (ASG) that scales on policy, replaces unhealthy instances, mixes Spot and On-Demand sensibly, and rolls out new AMIs without an outage.

## 1. Launch template and rollout
- Put the AMI, instance profile and settings in a **launch template**; to deploy a new AMI or user data, create a new template version and use an **instance refresh** to roll it out.
- Keep user data short and bake heavy installs into the AMI, so scale-out time stays low.

## 2. Spot with a mixed instances policy
- One group can run On-Demand and Spot Instances together, with several instance types.
- Choose instance types by manual list or by **attribute-based instance type selection** (vCPU and memory ranges).
- Allocation strategy for Spot: `price-capacity-optimized` is the recommended strategy on the allocation strategies page. You can also set instance type priorities for launch template overrides; Amazon EC2 Auto Scaling honors them best effort but optimizes for capacity first.
- Design the app to tolerate termination: drain via a lifecycle hook and keep state off the instance.

## 3. Lifecycle hooks
- A launch hook puts the new instance into `Pending:Wait` while your custom action (for example a bootstrap script) runs, then you complete the lifecycle action.
- Without a response, the instance stays in the wait state for one hour by default, then the launch continues (`Pending:Proceed`); you can extend by recording a heartbeat.
- With a warm pool, instances are stopped or hibernated as they enter the pool without waiting for user data; use an `EC2_INSTANCE_LAUNCHING` lifecycle hook to hold an instance until its bootstrap finishes.

## 4. Warm pools
- Warm pool instances can be kept `Stopped`, `Running` or `Hibernated`. `Stopped` minimizes cost: you pay only for volumes and attached Elastic IP addresses.
- Scaling policies scale out only if the metric from `InService` instances exceeds the policy's alarm high threshold (the target utilization of a target tracking policy).
- Dynamic scaling does not count a new instance towards aggregated metrics until it has warmed up: set the default instance warmup for the group.

## 5. Roll out with instance refresh
```bash
aws autoscaling start-instance-refresh --auto-scaling-group-name <ASG_NAME> \
  --preferences '{"MinHealthyPercentage":90,"InstanceWarmup":180,"SkipMatching":true}'
```
- Minimum healthy percentage controls how many instances stay in service; at 100 percent new instances launch before old ones terminate, so capacity is maintained.
- Skip matching compares each instance's AMI ID with the desired configuration and replaces only those that do not match.
- You only need to specify instance warmup for a refresh if the default warmup is not enabled or you want to override it.
- Checkpoints pause the refresh after a set percentage of replacements so you can verify progress. See the rollback page for undoing a refresh.

## Verify
- [ ] The launch template version points at the intended AMI, and an instance refresh completes on it.
- [ ] Load test: scale-out happens before latency degrades; scale-in causes no errors.
- [ ] Lifecycle hook timeouts cover real bootstrap time.

## Checked
2026-10-28. Confirmed in the Amazon EC2 Auto Scaling User Guide pages on mixed instances groups, allocation strategies, lifecycle hooks overview, warm pools, instance refresh, instance refresh overview and default values: mixed On-Demand and Spot groups, attribute-based selection, `price-capacity-optimized` recommended, instance type priorities, `Pending:Wait` and one-hour default timeout, the `EC2_INSTANCE_LAUNCHING` hook with warm pools, warm pool states (Stopped, Running, Hibernated) and Stopped cost note, scaling with InService instances, warmup behaviour, `MinHealthyPercentage`, skip matching, checkpoints; `check_commands.py` accepted the CLI command.
Removed as unconfirmed: IMDSv2 and SSM AMI parameter advice, AZ rebalance and health-check settings, scaling policy table and numeric targets, queue backlog metric, the instance type examples, `OnDemandBaseCapacity`, Capacity Rebalancing, `AutoRollback`, `set-instance-protection`, suspended-processes note and the FIS action.
Method: documentation only; no commands were run.
