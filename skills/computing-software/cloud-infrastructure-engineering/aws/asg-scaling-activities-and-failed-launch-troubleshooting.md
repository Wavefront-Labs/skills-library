---
id: computing-software.cloud-infrastructure-engineering.aws.asg-scaling-activities-and-failed-launch-troubleshooting
name: asg-scaling-activities-and-failed-launch-troubleshooting
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, auto-scaling, scaling-activities, failed-launch-troubleshooting, insufficientinstancecapacity, asg-notifications, launch-template]
level: practitioner
status: docs-checked
description: "Read Auto Scaling activity history to fix failed launches: capacity, quota, launch template, KMS, subnet IP and IAM errors, plus scaling notifications and alerts."
sources: ["https://docs.aws.amazon.com/autoscaling/ec2/userguide/CHAP_Troubleshooting.html", "https://docs.aws.amazon.com/autoscaling/ec2/userguide/ts-as-instancelaunchfailure.html", "https://docs.aws.amazon.com/autoscaling/ec2/userguide/ts-as-ami.html", "https://docs.aws.amazon.com/autoscaling/ec2/userguide/ts-as-launch-template.html", "https://docs.aws.amazon.com/autoscaling/ec2/userguide/ec2-auto-scaling-sns-notifications.html", "https://docs.aws.amazon.com/autoscaling/ec2/userguide/ec2-auto-scaling-metrics.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Auto Scaling activities and failed launches

## 1. Read the activity history
```bash
aws autoscaling describe-scaling-activities --auto-scaling-group-name web-asg --max-items 20 \
  --query 'Activities[].{t:StartTime,s:StatusCode,d:Description,c:Cause,m:StatusMessage}' --output table
```
`StatusCode` `Failed` or `Cancelled` with a `StatusMessage` tells you why. Also include
deleted groups' history with `--include-deleted-groups`. Activities are kept for 6 weeks.

## 2. Messages and fixes
| StatusMessage (abridged) | Fix |
|---|---|
| `We currently do not have sufficient <type> capacity in the Availability Zone you requested` | Wait a few minutes, add AZs, and use a diverse set of instance types (mixed instances policy) |
| `<n> instance(s) are already running` | Regional instance limit reached: request a quota increase (Amazon EC2 service quotas) or launch fewer instances |
| `The requested configuration is currently not supported` | Launch template options incompatible with the instance type, Region or AZ (for example an AMI architecture mismatch); check `describe-instance-type-offerings` |
| `Client.InternalError: Client error on launch` | Encrypted EBS volume and the service-linked role has no access to the KMS customer managed key: update the key policy for the role (cross-account keys need a grant) or use a key in the group's account |
| `The AMI ID <id> does not exist` | AMI deregistered or not shared with the account; update the launch template |
| `The security group <name> does not exist` / `The key pair <name> does not exist` | Deleted resource referenced by the template; create a new template version and point the group at it |
| `Your Spot request price of X is lower than the minimum required Spot request fulfillment price of Y` | Remove or raise the max price |
| `There is no Spot capacity available that matches your request` | Wait, add AZs, diversify instance types |
| `The requested reservation does not have sufficient compatible and available capacity` | Capacity Reservation or Capacity Block limit reached; use a reservation resource group so overflow launches as On-Demand, or buy more capacity |
| `Instance failed to complete user's Lifecycle Action ... abandoned` | The lifecycle action completed with ABANDON; fix the hook handler |
For `iam:PassRole` errors, the identity making the request needs `iam:PassRole` for the instance profile role named in the launch template. Activity history is kept for 6 weeks.
Failed launches are retried automatically, so a fix can take a few minutes to show.

## 3. Instances launching then terminating in a loop
- Check the instance's console output (`get-console-output`) and user data logs
  (`/var/log/cloud-init-output.log`) of a recently terminated instance; keep one by
  suspending `ReplaceUnhealthy`/`Terminate` processes temporarily:
  `aws autoscaling suspend-processes --auto-scaling-group-name web-asg --scaling-processes ReplaceUnhealthy`.
- A health check grace period shorter than the instance startup time marks instances unhealthy before the app starts.
- Lifecycle launch hook timing out.
Resume processes after debugging.

## 4. Notifications and alerting
```bash
aws autoscaling put-notification-configuration --auto-scaling-group-name web-asg \
  --topic-arn arn:aws:sns:<REGION>:<ACCOUNT_ID>:asg-events \
  --notification-types autoscaling:EC2_INSTANCE_LAUNCH_ERROR autoscaling:EC2_INSTANCE_TERMINATE_ERROR
```
Or route Auto Scaling events through EventBridge to chat/on-call. Also alarm on `GroupInServiceInstances < GroupDesiredCapacity`
for longer than expected launch time (enable group metrics:
`enable-metrics-collection --granularity 1Minute`).

## Gotchas
- Launch template `$Latest` vs `$Default`: with `$Latest` a bad template edit breaks launches immediately (the group's default is `$Default`).
- Instance refresh failures also show in activities; check `describe-instance-refreshes`.
- Capacity rebalance and AZ rebalance generate launch/terminate activities that look like
  churn but are expected.
- To investigate without scaling interference, suspend `AlarmNotification` and `ScheduledActions`, or disable individual policies.

## Verify
- [ ] Recent activities show `Successful` launches after the fix.
- [ ] `InService` equals desired capacity; group metrics enabled.
- [ ] Launch-error notifications reach the on-call channel (test by temporarily referencing a bad AMI in a test ASG).

## Checked

Checked 2026-10-27 against the Amazon EC2 Auto Scaling User Guide (troubleshooting launch failures, AMI and launch template issues, health checks, SNS notifications, group metrics, suspend processes).
- Corrected: the message table now lists only messages shown in the docs (capacity, instance limit, unsupported configuration, KMS Client.InternalError, missing AMI/security group/key pair, Spot price and capacity, reservations, abandoned lifecycle action); activity history is kept for 6 weeks.
- Confirmed: `autoscaling:EC2_INSTANCE_LAUNCH_ERROR` and `autoscaling:EC2_INSTANCE_TERMINATE_ERROR`, `--include-deleted-groups`, group metrics at 1-minute granularity are free once enabled.
- Removed: vCPU-limit, subnet-IP, security-group-id message rows and the EventBridge detail-type string, which the docs did not show.

Method: documentation only; no commands were run.
