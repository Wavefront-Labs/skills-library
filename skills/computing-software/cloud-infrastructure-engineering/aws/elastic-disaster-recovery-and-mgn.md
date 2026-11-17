---
id: computing-software.cloud-infrastructure-engineering.aws.elastic-disaster-recovery-and-mgn
name: elastic-disaster-recovery-and-mgn
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, elastic-disaster-recovery, drs, application-migration-service, mgn, replication-agent, staging-area, launch-template, cutover, test-instance, failback, block-level-replication, rehost, lift-and-shift, replication-server, point-in-time-snapshots, recovery-instance, launch-settings, drs-launch-template, post-launch-actions, mgn-post-launch, mgn-waves, source-servers]
level: practitioner
status: draft
description: "Replicate servers block-level into AWS with Application Migration Service (MGN) for rehost cutovers and Elastic Disaster Recovery (DRS) for low-RPO DR: agents, staging, drills, failback."
sources: ["AWS Elastic Disaster Recovery User Guide - How Elastic Disaster Recovery works", "AWS Application Migration Service User Guide - Migration workflow", "AWS Elastic Disaster Recovery User Guide - Performing a failback", "AWS Application Migration Service User Guide - Launch settings and post-launch actions"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Elastic Disaster Recovery (DRS) and Application Migration Service (MGN) — same engine, two jobs

**Goal:** physical/virtual/other-cloud servers continuously replicated into a cheap staging
area in AWS, launchable as full EC2 instances in minutes — for a one-way migration (MGN) or
an ongoing DR posture with drills and failback (DRS).

## 1. Shared architecture
- A **replication agent** on each source server streams block-level changes (any OS/app,
  no snapshots on the source) to lightweight **replication servers** in a **staging area
  subnet** in your account; data lands on low-cost EBS volumes.
- Launch = convert staging volumes → EC2 instance from an **EC2 launch template** you control
  (instance type, subnet, SG, IAM role). Test/recovery/cutover instances are real EC2.
- Requirements: outbound TCP **443** (service API) and **1500** (replication data) from
  source to the staging subnet (or via a VPN/Direct Connect with private endpoints);
  agent needs root/admin; supported OS list is broad but check kernels.
- Both services bill per replicating source server (DRS hourly; MGN free for 90 days per server) plus staging EBS/EC2.

## 2. Setup steps (both services)
1. **Initialize** the service in the region; create the **replication configuration
   template**: staging subnet (private), replication server type (`t3.small` default; bump
   for > ~15 disks or high change rate), EBS type (`gp3`; `st1` for large low-churn disks),
   encryption key, bandwidth throttle, dedicated replication server for sensitive hosts.
2. Create an IAM user/role for agents (`AWSApplicationMigrationAgentPolicy` /
   `AWSElasticDisasterRecoveryAgentInstallationPolicy`); prefer temporary credentials.
3. Install the agent:
   ```bash
   wget -O ./aws-replication-installer-init https://aws-elastic-disaster-recovery-<region>.s3.<region>.amazonaws.com/latest/linux/aws-replication-installer-init
   sudo ./aws-replication-installer-init --region <region> --aws-access-key-id … --aws-secret-access-key … --no-prompt
   ```
   (MGN: `aws-application-migration-service-<region>` bucket.) Windows: `.exe` equivalent.
4. Watch **initial sync** (full copy, bandwidth-bound) → **Healthy / Continuous data replication**.
   Lag metrics in the console; alarm on `Lag` > RPO (DRS) or stalled replication.
5. Edit **launch settings** per server: launch template (right-size via
   "instance type right-sizing" or pin), subnet/SGs for test vs production, OS licensing
   (BYOL vs AWS), **post-launch actions** (SSM documents: install CloudWatch agent, join
   domain, validate app) and launch disposition (started/stopped).

## 3. MGN: the migration workflow
- Group servers into **applications** and **waves** (console or `mgn` API); import a CSV
  inventory for bulk agent-less planning.
- **Test launch** (`Launch test instances`) into an isolated subnet — validate boot, app,
  connectivity; `Mark as ready for cutover` after fixes. Terminate test instances (data keeps replicating).
- **Cutover**: stop source writes (or freeze app) → `Launch cutover instances` → DNS/LB
  switch → `Finalize cutover` (stops replication, deletes staging resources) once stable.
  Typical cutover downtime: minutes, dominated by the final sync and DNS.
- **Agentless** replication from VMware vCenter via the MGN connector when agents are prohibited.
- Post-migration: the launched instances are ordinary EC2 — put them under ASG/backup/patching as usual.

## 4. DRS: the DR workflow
- Same replication; **point-in-time snapshots** (every 10 min for 24 h, hourly for days,
  daily for retention you configure) let you recover to *before* a ransomware or bad deploy.
- **Recovery drill**: `Initiate recovery` → `Drill` → choose PIT → instances launch in the
  drill subnet; validate; terminate. Run quarterly; it costs only the drill instances' runtime.
- **Real recovery**: same, choosing "Recovery"; then flip traffic (Route 53 / ARC).
- **Failback**: once the original site is healthy, install the **failback client** (on-prem:
  boot the failback ISO / for EC2-to-EC2 use *reversed replication*) to replicate from the
  recovery instance back to the source, then cut back. Practise this — it is the step most teams skip.
- **Cross-region / cross-account DR for EC2** is a first-class mode (source = EC2 in region A,
  staging in region B), replacing homemade AMI-copy schemes with sub-second RPO.
- **Launch into existing instance** can preserve instance IDs/ENIs for EC2-to-EC2 recovery.
- Stage by **source network** (DRS can recreate VPC/subnets/SGs/route tables of an EC2 source environment as CloudFormation).

## 5. Sizing and bandwidth
- Initial sync time ≈ total disk used ÷ available bandwidth; 10 TB at 1 Gbps ≈ 1 day. Throttle
  per-server (`bandwidthThrottling` Mbps) during business hours.
- Change rate decides steady-state: a server writing 100 GB/day needs ~10 Mbps sustained.
  Replication servers handle multiple sources; the console flags when they are overloaded.
- Staging EBS = source used size (gp3, cheap); recovery instances = full cost only while running.

## Gotchas
- Agent needs free space on the source for its driver/logs and kernel headers on some Linux distros; `/var/lib/aws-replication-agent` logs explain failures.
- Launch fails with "no ENI/IP" when the launch template's subnet is full or the SG belongs to another VPC.
- Windows licensing: launching a BYOL image onto shared tenancy is a compliance problem; set the OS licensing option.
- Replication stalls after source reboots that change disk layout (new disk added) — re-run the installer to add disks.
- MGN finalize cutover is irreversible for that server (staging deleted); keep a snapshot if nervous.
- DRS drills in the production subnet with the same private IP = duplicate IP conflict; use a drill subnet.
- Unconfirmed: current MGN free-period length and DRS PIT retention defaults — check pricing/docs.

## Verify
- [ ] All source servers show `Healthy` replication with lag < RPO for 24 h.
- [ ] A test/drill launch boots, passes post-launch SSM checks and is reachable in the test subnet.
- [ ] MGN: cutover rehearsal measured end-to-end downtime; runbook updated with the number.
- [ ] DRS: a PIT recovery from 1 h ago restores a file deleted since (prove the snapshot works).
- [ ] DRS: failback rehearsed once; the reversed replication reached `Healthy`.
