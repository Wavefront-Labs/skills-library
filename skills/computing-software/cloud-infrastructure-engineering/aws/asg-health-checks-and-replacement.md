---
id: computing-software.cloud-infrastructure-engineering.aws.asg-health-checks-and-replacement
name: asg-health-checks-and-replacement
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, auto-scaling, health-check-grace-period, elb-health-check, unhealthy-replacement, asg]
level: practitioner
status: docs-checked
description: "Configure EC2 Auto Scaling health check types, the grace period and unhealthy-instance replacement, and diagnose launch-terminate loops."
sources: ["https://docs.aws.amazon.com/autoscaling/ec2/userguide/health-checks-overview.html", "https://docs.aws.amazon.com/autoscaling/ec2/userguide/health-check-grace-period.html", "https://docs.aws.amazon.com/autoscaling/ec2/userguide/replace-unhealthy-instance.html", "https://docs.aws.amazon.com/autoscaling/ec2/userguide/ts-as-healthchecks.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ASG health checks and replacement

**Goal:** an ASG replaces instances that are really unhealthy and does not kill instances that are still initialising.

## Types
- **EC2 status checks and scheduled events**: the default. An instance not in the running state (stopping, stopped, shutting-down, terminated) is marked Unhealthy immediately. Impaired status checks are tolerated for a few minutes first; insufficient-data does not mark it Unhealthy. An instance affected by a scheduled event is treated as unhealthy and replaced.
- **Elastic Load Balancing**: ignored by default; turn it on for the group. Once the load balancer reports a registered instance Unhealthy, Auto Scaling marks it Unhealthy on its next periodic check. It only acts after the load balancer is InService.
- **VPC Lattice** and **Amazon EBS** health checks: also opt-in.
- **Custom** health checks, and application status checks managed in EC2.
- EC2 status checks and scheduled events cannot be removed from the group's checks.

## Configure
```bash
aws autoscaling update-auto-scaling-group --auto-scaling-group-name web-asg \
  --health-check-type ELB --health-check-grace-period 300
```
- **Grace period**: the minimum time (seconds) to keep a new instance in service before terminating it for being unhealthy. Console default when creating a group is 300 s; via CLI or SDK the default is 0 (off). Too high a value reduces health check effectiveness; with launch lifecycle hooks it can be 0.
- It applies to newly launched instances, instances returned from standby, and instances manually attached.
- During the grace period an instance no longer in the EC2 running state (for example one you stopped) is still marked Unhealthy and replaced at once.
- Manually mark an instance: `aws autoscaling set-instance-health --instance-id i-0abc --health-status Unhealthy`. Setting back to Healthy is generally only useful when ReplaceUnhealthy or Terminate is suspended; an error usually means it is already terminating.

## Replacement behaviour
- By default a scaling activity terminates the unhealthy instance, and another launches the replacement. An instance maintenance policy can change this to launch first.
- Instances not running are replaced immediately. For other unhealthy instances, if a scaling activity is in progress and the group is 10 percent or more below desired capacity, Auto Scaling waits. Otherwise it replaces up to 10 percent of desired capacity at a time (one at a time if 10 percent is under one instance), waiting for the new instance to pass an initial health check and the default instance warmup. An instance maintenance policy can change the rate.
- Instances in Standby are not health checked. To stop replacement, suspend the ReplaceUnhealthy and HealthCheck processes.
- Terminated instances lose their Elastic IP association and attached EBS volumes (per DeleteOnTermination); handle these with a lifecycle hook if needed.

## Troubleshooting
1. `aws autoscaling describe-scaling-activities --auto-scaling-group-name web-asg`: the Cause field gives the reason, for example "taken out of service in response to a user health-check". Add `--include-deleted-groups` for deleted groups.
2. Messages: EC2 instance status check failure (system or instance check; see DescribeInstanceStatus or the StatusCheckFailed_System and StatusCheckFailed_Instance metrics); EC2 health check "terminated or stopped" (stopped, rebooted or terminated manually, Spot interruption, or Capacity Block end); ELB system health check failure.
3. ELB failures: check target group health check settings, expected success codes, security groups, and that the load balancer is in the same Availability Zones as the group. If the grace period is shorter than startup time, lengthen it to cover the consecutive successful checks ELB requires.
4. To stop or reboot instances deliberately, put them in Standby first.

## Checked
Date: 2026-11-07
Method: documentation only; no commands were run.
Read in full: "About the health checks for your Auto Scaling group", "Set the health check grace period", "View the reason for health check failures" and "Troubleshoot unhealthy instances". The `set-instance-health` and `update-auto-scaling-group` flags were taken from the command names and options shown on those pages and the botocore model.
Removed: "grace period starts after the lifecycle hook completes", "default is 300 s via API/CLI" (it is 0), the lifecycle-hook/instance-refresh advice for loops, and the root-only source.
