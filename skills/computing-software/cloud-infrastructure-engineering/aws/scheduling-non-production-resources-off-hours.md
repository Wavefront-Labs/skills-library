---
id: computing-software.cloud-infrastructure-engineering.aws.scheduling-non-production-resources-off-hours
name: scheduling-non-production-resources-off-hours
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, instance-scheduler, non-production-scheduling, off-hours, eventbridge-scheduler, cost-optimization, rds-stop]
level: practitioner
status: docs-checked
description: "Stop non-production EC2 and RDS outside working hours with Instance Scheduler on AWS or EventBridge Scheduler universal targets, plus RDS stop limits."
sources:
  - https://docs.aws.amazon.com/solutions/latest/instance-scheduler-on-aws/solution-overview.html
  - https://docs.aws.amazon.com/scheduler/latest/UserGuide/managing-targets-universal.html
  - https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_StopInstance.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Scheduling non-production resources off-hours

AWS says Instance Scheduler can save up to 70% on instances needed only during business
hours (weekly utilisation reduced from 168 hours to 50 hours).

## 1. Instance Scheduler on AWS (solution)
Automates starting and stopping of EC2 and RDS instances. It uses resource tags and Lambda
to stop and restart instances across multiple Regions and accounts on a customer-defined
schedule, and supports hibernation for stopped EC2 instances. Points from the guide:
- It acts on appropriately tagged instances in all configured Regions, even though the
  Lambda function runs in one Region; cross-account scheduling applies to all configured
  Regions in all accounts.
- With multiple deployments, use a different tag name per stack and non-overlapping Regions,
  since each deployment checks every instance in its Regions for its tag key.
- Schedules are defined in the scheduler configuration table (see the guide); the guide's
  stated estimated cost to run the solution in N. Virginia was USD 13.15 per month.

## 2. Lightweight alternative: EventBridge Scheduler universal target
A universal target invokes an AWS API directly. Specify `RoleArn` (execution role with
permission to call the API), `Arn` in the form `arn:aws:scheduler:::aws-sdk:<service>:<apiAction>`
(the service must match the AWS SDK service identifier), and `Input` as JSON matching the
API's request parameters. Read-only actions (prefixes such as get, describe, list) are not
supported. Pattern, modelled on the page's Lambda example:
```bash
aws scheduler create-schedule --name dev-stop \
  --schedule-expression 'cron(0 19 ? * MON-FRI *)' --schedule-expression-timezone Europe/London \
  --flexible-time-window Mode=OFF \
  --target '{"RoleArn":"<role-arn>","Arn":"arn:aws:scheduler:::aws-sdk:ec2:stopInstances","Input":"{\"InstanceIds\":[\"<instance-id>\"]}"}'
```
Schedule expression and time-zone options are not covered by the cited page; check the
EventBridge Scheduler schedule types guide. Selecting resources by tag needs another target
type (for example Lambda).

## 3. RDS stop/start limits
- A DB instance can be stopped for a maximum of 7 consecutive days, after which RDS
  automatically starts it. A scheduler must stop it again.
- While stopped you are not charged for instance hours but are charged for provisioned
  storage, backup storage, and the public IPv4 address if publicly accessible.
- Supported engines: Db2, MariaDB, SQL Server, MySQL, Oracle, PostgreSQL. You cannot stop an
  instance that has a read replica or is a read replica, nor a SQL Server Multi-AZ instance.
- Stopped instances cannot be modified; starting needs instance recovery and can take minutes
  to hours, so be cautious with production.
- A stopped instance keeps its DNS endpoint and any public IP; RAM contents are lost.

## 4. Operating it (practitioner guidance)
- Tag non-production resources by IaC with a schedule, with an approved always-on exception.
- Provide a self-service way to start late; the next scheduled stop handles it.
- Measure savings in Cost Explorer by account or tag, before and after.
- Start databases before applications by using separate schedules.

## Verify
- [ ] Non-production resources tagged with schedules; stop and start happen at the right local times.
- [ ] RDS instances do not stay running after the 7-day auto-start.

## Checked
Method: docs-checked 2026-11-09 against the Instance Scheduler overview, the EventBridge Scheduler universal targets page and the RDS stopping page, read via summarising fetch. Dropped unconfirmed: the resource table for ASG, ECS, EKS, Redshift, SageMaker, NAT and load balancers, the scheduler-cli commands, ASG, Neptune and DocumentDB support, and the 64% figure.
