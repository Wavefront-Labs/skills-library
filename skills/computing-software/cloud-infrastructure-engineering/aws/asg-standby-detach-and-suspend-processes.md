---
id: computing-software.cloud-infrastructure-engineering.aws.asg-standby-detach-and-suspend-processes
name: asg-standby-detach-and-suspend-processes
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, auto-scaling, standby-state, suspend-processes, detach-instances, scale-in-protection]
level: practitioner
status: docs-checked
description: "Take Auto Scaling instances out of service safely with Standby, detach, scale-in protection and suspending processes like ReplaceUnhealthy and AZRebalance."
sources: ["https://docs.aws.amazon.com/autoscaling/ec2/userguide/as-enter-exit-standby.html", "https://docs.aws.amazon.com/autoscaling/ec2/userguide/as-suspend-resume-processes.html", "https://docs.aws.amazon.com/autoscaling/ec2/userguide/ec2-auto-scaling-instance-protection.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Standby, detach and suspending scaling processes

## 1. Standby (troubleshoot or patch, then return)
```bash
aws autoscaling enter-standby --auto-scaling-group-name web --instance-ids i-0abc --should-decrement-desired-capacity
# ... debug, patch ...
aws autoscaling exit-standby --auto-scaling-group-name web --instance-ids i-0abc
```
- The instance stays in the group, is deregistered from attached load balancer target groups, and is not health-checked while on standby.
- Without `--should-decrement-desired-capacity` the ASG launches a replacement; exiting standby increments desired capacity back (min/max must allow it).
- You are billed for instances on standby, and `AZRebalance` can still rebalance the group unless suspended.

## 2. Detach (remove for good, keep the instance)
```bash
aws autoscaling detach-instances --auto-scaling-group-name web --instance-ids i-0abc --should-decrement-desired-capacity
```

## 3. Scale-in protection
```bash
aws autoscaling set-instance-protection --auto-scaling-group-name workers --instance-ids i-0abc --protected-from-scale-in
```
Workers can protect themselves while busy and unprotect when idle. Does not protect against health replacement or manual termination.

## 4. Suspend processes
```bash
aws autoscaling suspend-processes --auto-scaling-group-name web --scaling-processes ReplaceUnhealthy AZRebalance
aws autoscaling resume-processes --auto-scaling-group-name web --scaling-processes ReplaceUnhealthy AZRebalance
```
| Process | Suspend when |
|---|---|
| `ReplaceUnhealthy` / `HealthCheck` | debugging an instance that keeps failing checks |
| `AZRebalance` | stateful nodes you do not want terminated for balance |
| `Launch` / `Terminate` | freezing the group during an incident (breaks scaling) |
| `AlarmNotification`, `ScheduledActions` | maintenance windows |
| `AddToLoadBalancer` | launching without registering, then register manually |
| `InstanceRefresh` | pausing refreshes |

## Gotchas
- Suspended processes are easy to forget: alarm on `describe-auto-scaling-groups --query 'AutoScalingGroups[?SuspendedProcesses]'`.
- Auto Scaling can itself suspend processes (administrative suspension) for groups that have failed to launch instances for more than 24 hours; resume them after fixing the cause.

## Verify
- [ ] Instance in Standby shows `LifecycleState: Standby` and is absent from target health.

## Checked

Checked 2026-10-27 against the Amazon EC2 Auto Scaling User Guide (standby, suspend and resume processes, instance scale-in protection).
- Confirmed: standby deregisters from load balancers, no health checks while on standby, decrement versus replacement behaviour, billing continues, AZRebalance still applies, process names and meanings, scale-in protection limits.
- Added: administrative suspension after 24 hours of failed launches. Removed: unsupported claim that suspending Launch blocks replacement after standby.

Method: documentation only; no commands were run.
