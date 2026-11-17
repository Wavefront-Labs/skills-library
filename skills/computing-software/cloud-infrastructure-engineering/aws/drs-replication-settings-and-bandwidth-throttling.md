---
id: computing-software.cloud-infrastructure-engineering.aws.drs-replication-settings-and-bandwidth-throttling
name: drs-replication-settings-and-bandwidth-throttling
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, elastic-disaster-recovery, drs, replication-settings, drs-bandwidth, staging-area, point-in-time-snapshots]
level: practitioner
status: docs-checked
description: "Tune AWS Elastic Disaster Recovery replication: replication server type, staging subnet, private vs public routing, EBS types, bandwidth throttling and point-in-time retention."
sources: ["https://docs.aws.amazon.com/drs/latest/userguide/individual-replication-settings.html", "https://docs.aws.amazon.com/drs/latest/userguide/Network-Requirements.html", "https://docs.aws.amazon.com/drs/latest/userguide/replication-settings.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# DRS replication settings and bandwidth throttling

## Default replication template vs per-server
DRS has default replication settings; change an individual server afterwards with
`update-replication-configuration`.

## Key settings
| Setting | Guidance |
|---|---|
| Staging area subnet | where replication servers and staging volumes live; sources with different staging subnets are not consolidated onto one replication server |
| Replication server instance type | default `t3.small`, which suits most workloads; monitor replication-server CloudWatch metrics (for example `EBSWriteBytes`/`EBSWriteOps`) and move to a larger type if the source has frequent lag or backlog |
| Dedicated replication server | sources share replication servers unless this is set; a dedicated server is for sources with frequent lag or backlog (it may increase cost) |
| Staging disk type | `AUTO`, `GP2`, `GP3`, `IO1`, `SC1`, `ST1` or `STANDARD` (botocore enum) |
| EBS encryption | `DEFAULT`, `CUSTOM` or `NONE`; changing it may need a full sync |
| Data routing | `PRIVATE_IP` or `PUBLIC_IP`; replication servers must be in a public subnet unless private IP is enabled and valid VPC routing exists. Source servers reach the staging subnet on TCP 1500 |
| Bandwidth throttling | per source server; changing it has no impact on replication |
| Point-in-time policy | retention policy; changing it disconnects the replication server as a safety measure |
```bash
aws drs update-replication-configuration --source-server-id s-0abc \
  --bandwidth-throttling 50 --replication-server-instance-type m5.large \
  --use-dedicated-replication-server --data-plane-routing PRIVATE_IP
```

## Throttling strategy
- The network requirements page has a section on the bandwidth needed between source servers and the staging subnet; size throttling against it.
- Throttling changes can be scripted with `update-replication-configuration`.

## Monitoring
- Per server `dataReplicationInfo` (state, lag, backlog): `aws drs describe-source-servers`.
  States: `STOPPED`, `INITIATING`, `INITIAL_SYNC`, `BACKLOG`, `CREATING_SNAPSHOT`, `CONTINUOUS`, `PAUSED`, `RESCAN`, `STALLED`, `DISCONNECTED`.
- Network paths: source servers to the staging subnet on TCP 1500; source servers to DRS, and the staging subnet to AWS DRS endpoints, on TCP 443.

## Verify
- [ ] All servers in `CONTINUOUS` replication with lag under your RPO.
- [ ] Drill launch from a recent point in time succeeds.

## Checked

2026-10-28. Confirmed against AWS documentation: t3.small default and dedicated-server guidance, subnet consolidation, public-subnet/private-IP rule, TCP 1500 and 443 paths, which settings pause or disconnect replication; staging disk type, encryption, routing and replication state enums via the botocore drs model.
Removed: burstable/CPU-credit and st1/sc1 guidance, CMK-in-recovery-account claim, security-group claim, Mbps/0=unlimited, example PIT schedule and snapshot-cost claim, throttling schedule/estimate advice, stall list beyond port requirements.
Method: documentation only; no commands were run.
