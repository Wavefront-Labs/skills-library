---
id: computing-software.cloud-infrastructure-engineering.aws.asg-capacity-rebalancing-for-spot
name: asg-capacity-rebalancing-for-spot
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, auto-scaling, capacity-rebalance, spot-instances, rebalance-recommendation, lifecycle-hooks]
level: advanced
status: docs-checked
description: "Enable Capacity Rebalancing on Auto Scaling groups so Spot instances at elevated interruption risk are replaced proactively, with draining via lifecycle hooks."
sources: ["https://docs.aws.amazon.com/autoscaling/ec2/userguide/ec2-auto-scaling-capacity-rebalancing.html", "https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/rebalance-recommendations.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Capacity Rebalancing for Spot in Auto Scaling groups

## 1. What it does
EC2 emits a **rebalance recommendation** when a Spot instance is at elevated risk, often before the
2-minute interruption notice. With Capacity Rebalancing on, the ASG launches a replacement first, waits
for it to pass health checks, then terminates the at-risk instance.

## 2. Enable
```bash
aws autoscaling update-auto-scaling-group --auto-scaling-group-name workers --capacity-rebalance
```
Use multiple instance types and AZs. The docs recommend `price-capacity-optimized` allocation, not
`lowest-price`, because lowest-price can put replacements in pools that are about to be interrupted.

## 3. Drain gracefully
Add a termination lifecycle hook so the old instance finishes in-flight work:
```bash
aws autoscaling put-lifecycle-hook --auto-scaling-group-name workers --lifecycle-hook-name drain \
  --lifecycle-transition autoscaling:EC2_INSTANCE_TERMINATING --heartbeat-timeout 300 --default-result CONTINUE
```
Worker code: on the hook (EventBridge or polling instance metadata `/latest/meta-data/autoscaling/target-lifecycle-state`),
stop taking work, finish, then `complete-lifecycle-action`.

## 4. Behaviour to expect
- Auto Scaling launches the new instance first and terminates the old one only after the new one passes its
  health check (plus the lifecycle hook timeout, if you added a hook). It can temporarily exceed the group's
  maximum size by up to 10 percent of desired capacity.
- A replacement is launched only if its availability is the same or better than the at-risk instance.
- The recommendation can arrive together with the two-minute interruption notice, so keep the custom action under two minutes.
- Enabling it does not raise the interruption rate, but more instances may be replaced than without it.

## Verify
- [ ] Activity history shows replacement launches for instances that received a rebalance recommendation.
- [ ] Interruption-related job failures drop after enabling.

## Checked

Checked 2026-10-27 against the Amazon EC2 Auto Scaling User Guide (Capacity Rebalancing, lifecycle hooks, target lifecycle state through IMDS) and the aws-cli update-auto-scaling-group reference.
- Corrected: the group can exceed its maximum size by up to 10 percent of desired capacity (not "one instance for small groups"); a replacement launches only if availability is the same or better; the recommendation can arrive together with the two-minute notice.
- Confirmed: launch-then-terminate order after the replacement passes its health check, `price-capacity-optimized` recommendation over `lowest-price`, `autoscaling/target-lifecycle-state` metadata path, `--capacity-rebalance` flag.

Method: documentation only; no commands were run.
