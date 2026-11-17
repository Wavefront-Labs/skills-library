---
id: computing-software.cloud-infrastructure-engineering.aws.drs-failback-and-reverse-replication
name: drs-failback-and-reverse-replication
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, elastic-disaster-recovery, drs, drs-failback, reverse-replication, failback-client, recovery-instance, cross-region-dr, on-premises-dr, failover, rpo, rto]
level: advanced
status: docs-checked
description: "Return from an Elastic Disaster Recovery failover: reverse replication for AWS-to-AWS, the failback client for on-prem/VMware, cutover back, and re-protecting the source."
sources: ["https://docs.aws.amazon.com/drs/latest/userguide/failback-performing-main.html", "https://docs.aws.amazon.com/drs/latest/APIReference/API_ReverseReplication.html", "https://docs.aws.amazon.com/drs/latest/APIReference/API_StartFailbackLaunch.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Elastic Disaster Recovery: failback and reverse replication

**Goal:** after running production on DRS **recovery instances**, you return to the original
site (or Region) with the data written during the disaster, minimal downtime, and the
original protection re-established — a procedure as rehearsed as the failover itself.

## 1. Know which failback you have
| Original source | Failback path |
|---|---|
| EC2 in another Region/AZ (AWS → AWS) | **Reverse replication**: recovery instance replicates back to the original Region; then launch there |
| On-premises physical/VM | **Failback Client** on the original or a replacement machine pulls data from the recovery instance |

## 2. AWS → AWS (reverse replication)
```bash
aws drs describe-recovery-instances --region us-west-2
aws drs reverse-replication --recovery-instance-id <RI_ID> --region us-west-2
# a new source server appears in the ORIGINAL Region's DRS console, replicating DR -> original
aws drs describe-source-servers --region us-east-1      # wait for dataReplicationInfo.dataReplicationState = CONTINUOUS
```
Then, in a maintenance window:
1. Stop application writes on the recovery instances (or quiesce).
2. Wait for lag ≈ 0, launch (recovery or drill) from the reversed source server in the
   original Region using its launch settings.
3. Validate, switch DNS/routing back.
4. Terminate recovery instances only after the original is serving; re-enable the
   original direction of replication (the original source servers), and confirm replication reaches `CONTINUOUS`.

## 3. On-premises with the Failback Client
1. Generate DRS credentials (an IAM user/role with the failback permissions in the DRS User Guide).
2. Boot the target machine from the Failback Client ISO; give it the Region, credentials
   and (for each disk) the mapping to the recovery instance's volumes. The client must
   reach the recovery instance and the DRS endpoints (see the DRS network requirements).
3. Replication starts recovery instance → on-prem machine; console shows failback state
   moving to `FAILBACK_READY_FOR_LAUNCH`.
4. Cutover: API `start-failback-launch --recovery-instance-ids <RI_ID>`; the on-prem machine
   reboots into the replicated OS.
5. Reinstall/resume the DRS agent on the source to protect it again
   (re-start replication for the source server) and disconnect the recovery instance.

## Gotchas
- Network: on-prem failback needs inbound connectivity from the failback client to the
  recovery instance (VPN/DX, with security groups that allow it).
- Disk mapping mistakes overwrite the wrong volume; label disks by size/order before the
  window.
- Recovery instances keep accruing EC2 cost until terminated; tag them and track.
- Reverse replication creates a separate source server in the original Region (`reversedDirectionSourceServerArn`).
- Applications with external state (licensing tied to MAC/host, IP allowlists) behave like
  a migration in reverse; include them in the runbook.

## Verify
- [ ] Drill: fail over a test server, write a marker file, fail back, marker file present on the original.
- [ ] Original source servers return to continuous replication with lag below RPO after failback.
- [ ] No orphan recovery instances (`describe-recovery-instances` empty for the drill).
- [ ] Runbook records duration of each failback step against the agreed window.

## Checked

2026-10-28

Confirmed: reverse-replication and start-failback-launch operations, Failback Client runs the conversion and reboots the machine, x86_64 limit, dataReplicationState CONTINUOUS, FailbackState FAILBACK_READY_FOR_LAUNCH, reversedDirectionSourceServerArn (DRS API pages, botocore, check_commands).

Removed: DRSFA row, bootable ISO wording, describe-recovery-instances query fields, policy name, TCP ports 1500/443, console button names, stop-failback and start-replication names, Healthy state, separate-billing claim; replaced stub source pages.

Method: documentation only; no commands were run.
