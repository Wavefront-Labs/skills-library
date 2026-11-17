---
id: computing-software.cloud-infrastructure-engineering.aws.drs-cross-region-and-cross-az-recovery-for-ec2
name: drs-cross-region-and-cross-az-recovery-for-ec2
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, elastic-disaster-recovery, drs-cross-region, ec2-disaster-recovery, cross-az-recovery, failback, recovery-instances]
level: practitioner
status: docs-checked
description: "Protect EC2 with Elastic Disaster Recovery across regions or AZs: agent, launch settings in the recovery region, drills, failover and reverse replication for failback."
sources: ["https://docs.aws.amazon.com/drs/latest/userguide/what-is-drs.html", "https://docs.aws.amazon.com/drs/latest/userguide/launch-general-settings.html", "https://docs.aws.amazon.com/drs/latest/userguide/failback.html", "https://docs.aws.amazon.com/drs/latest/userguide/preparing-failover.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# DRS cross-region and cross-AZ recovery for EC2

**Goal:** continuous block-level replication of EC2 instances to another region (or AZ), with
recovery in minutes to the latest or a chosen point in time, and a path back.

## Set up
1. Initialise DRS in the **recovery** region.
2. Install the AWS Replication Agent on each source server, following the Elastic Disaster
   Recovery User Guide agent installation steps (installer URL and required IAM policy are in that guide).
3. A source server must be able to open connections to its staging area subnet (see the network requirements).

## Launch settings (per source server)
- Instance type right-sizing: choose whether DRS may pick a drill, recovery or failback instance type that
  best matches the source hardware.
- Copy private IP: makes the drill or recovery instance use the source's private IP; do not use it when the
  source network is connected through a VPN and the IP is already in use.
- Recovery instances that should run post-launch actions need an instance profile with the documented DRS policies.

## Drill and recover
```bash
aws drs start-recovery --is-drill --source-servers sourceServerID=s-0abc
aws drs start-recovery --source-servers sourceServerID=s-0abc,recoverySnapshotID=pit-0def   # real event, chosen point in time
aws drs describe-jobs
```
- A drill is a non-disruptive test that launches drill instances using the same process as recovery without
  affecting source servers or ongoing replication; terminate the instances afterwards (console
  "Terminate recovery instances", or `terminate-recovery-instances`).
- Recovery can use the most up-to-date server state or a previous point in time.

## Failback
- For AWS-to-AWS failback, start **reverse replication** on the protected recovery instance (in the failover
  account for cross-account failback), per the failback page.

## Verify
- [ ] Periodic drill: all servers launch and your health checks pass; record time against your RTO.
- [ ] Reverse replication tested once end to end.

## Checked

2026-10-28. Confirmed against AWS documentation: drill definition, point-in-time or latest recovery, right-sizing and Copy private IP launch settings, post-launch instance profile requirement, reverse replication for same/cross-account failback, staging-subnet connectivity; CLI commands via check_commands (botocore).
Removed: installer download URL and agent policy name, SSM install document, cross-AZ and cross-account setup advice, copy-tags and Elastic IP claims, wave ordering, licensing/managed-service/instance-id gotchas; replaced prose-only sources.
Method: documentation only; no commands were run.
