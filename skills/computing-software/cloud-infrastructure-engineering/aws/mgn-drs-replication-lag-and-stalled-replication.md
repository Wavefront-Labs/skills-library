---
id: computing-software.cloud-infrastructure-engineering.aws.mgn-drs-replication-lag-and-stalled-replication
name: mgn-drs-replication-lag-and-stalled-replication
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, application-migration-service, elastic-disaster-recovery, replication-lag, stalled-replication, replication-server, port-1500]
level: advanced
status: docs-checked
description: "Fix MGN and Elastic Disaster Recovery replication that lags or stalls: agent-to-replication-server path (TCP 1500/443), bandwidth, disk churn, staging subnet and server sizing."
sources: ["https://docs.aws.amazon.com/mgn/latest/ug/Network-Requirements.html", "https://docs.aws.amazon.com/drs/latest/userguide/individual-replication-settings.html", "https://docs.aws.amazon.com/drs/latest/userguide/Network-Requirements.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# MGN/DRS replication lag and stalled replication

Both services use the same replication engine: an agent on the source server sends block
changes to **replication servers** (EC2 instances in a staging subnet), which write to
staging EBS volumes.

## 1. Read the state
```bash
aws mgn describe-source-servers --query 'items[].{id:sourceServerID,host:sourceProperties.identificationHints.hostname,state:dataReplicationInfo.dataReplicationState,lag:dataReplicationInfo.lagDuration,err:dataReplicationInfo.dataReplicationError.error}'
aws drs describe-source-servers --query 'items[].{id:sourceServerID,state:dataReplicationInfo.dataReplicationState,lag:dataReplicationInfo.lagDuration,err:dataReplicationInfo.dataReplicationError}'
```
States (`DataReplicationState`): `STOPPED`, `INITIATING`, `INITIAL_SYNC`, `BACKLOG`, `CREATING_SNAPSHOT`,
`CONTINUOUS`, `PAUSED`, `RESCAN`, `STALLED`, `DISCONNECTED` (MGN also has `PENDING_SNAPSHOT_SHIPPING`
and `SHIPPING_SNAPSHOT`).

## 2. Network path checks
- Source servers to the staging area subnet: **TCP 1500** (replicated data).
- Source servers, and the staging area subnet, to the service over **TCP 443**.
- The staging subnet also needs Amazon S3 access (agent installer and replication software are downloaded
  from S3 URLs of your Region); behind a firewall or proxy, allowlist the documented S3 URLs.
- `DataReplicationErrorString` values include `AGENT_NOT_SEEN`, `FAILED_TO_CONNECT_AGENT_TO_REPLICATION_SERVER`,
  `FAILED_TO_LAUNCH_REPLICATION_SERVER`, `FAILED_TO_AUTHENTICATE_WITH_SERVICE`, `SNAPSHOTS_FAILURE`,
  `NOT_CONVERGING`, `UNSTABLE_NETWORK` and `FAILED_TO_START_DATA_TRANSFER` (botocore model).

## 3. Lag that never catches up (`NOT_CONVERGING`, BACKLOG grows)
- Review the replication settings: `bandwidthThrottling` (botocore range 0-10000), a larger
  `replicationServerInstanceType`, `useDedicatedReplicationServer` for sources with frequent lag or backlog
  (the DRS docs suggest watching `EBSWriteBytes`/`EBSWriteOps` on the replication server), and
  `defaultLargeStagingDiskType` (`AUTO`, `GP2`, `GP3`, `IO1`, `SC1`, `ST1`, `STANDARD` ...).

## 4. Stalled / disconnected
- Start from the `dataReplicationError` value and the network checks above; reinstall the
  replication agent only if it is the cause.

## 5. Settings to review
```bash
aws mgn get-replication-configuration --source-server-id s-123 \
  --query '{bw:bandwidthThrottling,ded:useDedicatedReplicationServer,type:replicationServerInstanceType,subnet:stagingAreaSubnetId,publicIp:createPublicIP}'
```

## Verify
- [ ] Servers in `CONTINUOUS` with `lagDuration` within your target.
- [ ] TCP 1500 and 443 reachability confirmed from every source network segment.
- [ ] Sources with frequent lag or backlog use adequately sized (or dedicated) replication servers.

## Checked

2026-10-28. Confirmed against AWS documentation: TCP 1500/443 paths and S3 access requirement, DataReplicationState and DataReplicationErrorString enums, replication configuration fields and bandwidthThrottling range, lagDuration/dataReplicationError output fields (botocore mgn and drs models), dedicated-server and EBS write-metric guidance from the DRS replication settings page.
Removed: telnet/Test-NetConnection and proxy-TLS claims, change-rate/off-peak advice, agent log paths, reboot-rescan and credential-revocation claims, replication-template sentence; replaced stub troubleshooting sources.
Method: documentation only; no commands were run.
