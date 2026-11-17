---
id: computing-software.cloud-infrastructure-engineering.aws.storage-gateway-and-datasync
name: storage-gateway-and-datasync
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, storage-gateway, datasync, hybrid-storage, s3-file-gateway, fsx-file-gateway, volume-gateway, tape-gateway, vtl, cached-volumes, stored-volumes, datasync-agent, datasync-task, nfs-to-s3, smb-to-fsx, data-migration, bandwidth-throttling, refresh-cache, snowball, transfer-family, data-transfer, datasync-verification, datasync-schedule]
level: practitioner
status: gated
description: "Move and bridge on-premises data: pick File/Volume/Tape Gateway vs DataSync, deploy agents, size cache, schedule DataSync tasks, and verify transfers before cut-over."
sources: ["https://docs.aws.amazon.com/storagegateway/latest/userguide/WhatIsStorageGateway.html", "https://docs.aws.amazon.com/filegateway/latest/files3/what-is-file-s3.html", "https://docs.aws.amazon.com/storagegateway/latest/vgw/WhatIsStorageGateway.html", "https://docs.aws.amazon.com/datasync/latest/userguide/what-is-datasync.html", "https://docs.aws.amazon.com/datasync/latest/userguide/agent-requirements.html", "https://docs.aws.amazon.com/datasync/latest/userguide/create-task.html", "https://docs.aws.amazon.com/datasync/latest/userguide/filtering-datasync-task.html"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Storage Gateway and DataSync

**Goal:** choose the right bridge between an on-premises (or other-cloud) file/block/tape
world and AWS storage — a *gateway* when apps must keep using local protocols
continuously, *DataSync* when you are moving or syncing data — and run it so the first
cut-over is verified, not hopeful.

## 1. Decide
| Situation | Tool |
|---|---|
| Apps on-prem keep writing NFS/SMB; data should land in S3 as objects | **S3 File Gateway** |
| Windows users on-prem need low-latency access to an FSx for Windows share | **FSx File Gateway** |
| Block storage (iSCSI) for on-prem servers, backed by S3, with EBS snapshots | **Volume Gateway** (cached or stored) |
| Replace a physical tape library for Veeam/NetBackup/Commvault | **Tape Gateway** (VTL → S3/Glacier) |
| One-time or scheduled bulk transfer NFS/SMB/HDFS/object → S3/EFS/FSx (or AWS → AWS) | **DataSync** |
| Petabytes, poor link | **Snowball Edge** (then DataSync for the delta) |
| Partners pushing files over SFTP/FTPS/AS2 into S3 | **Transfer Family** |
| Continuous DB replication | DMS, not storage tools |

## 2. Storage Gateway: deploy the appliance
Gateway = VM (VMware/Hyper-V/KVM OVA), hardware appliance, or an EC2 AMI (for
in-cloud use cases). Sizing floor: see the gateway requirements page for CPU, RAM and disk (gated: unconfirmed, source is paywalled or blocked), plus local disks:
- **Cache disk** (all types): size to the active working set (check the requirements page for the minimum); more cache = fewer S3 round trips. SSD.
- **Upload buffer** (volume/tape): ≥ 150 GiB, sized to hold data written faster than the
  WAN uploads.
Network: outbound 443 to the Storage Gateway endpoints (use a VPC endpoint
`com.amazonaws.<REGION>.storagegateway` + Direct Connect to keep it private), port 80
inbound from the activating browser/CLI only during activation, NTP.
Activate: `aws storagegateway activate-gateway --activation-key <KEY from http://<gw-ip>/?activationRegion=...> --gateway-name gw1 --gateway-type FILE_S3 --gateway-region eu-west-1 --gateway-timezone GMT`
then `add-cache`/`add-upload-buffer` by disk id.

## 3. S3 File Gateway specifics
```bash
aws storagegateway create-nfs-file-share --client-token t1 --gateway-arn <GW_ARN> --role arn:aws:iam::<ACCOUNT_ID>:role/sgw-s3 \
  --location-arn arn:aws:s3:::bucket/prefix --default-storage-class S3_STANDARD_IA \
  --client-list 10.0.0.0/8 --squash RootSquash --nfs-file-share-defaults FileMode=0664,DirectoryMode=0775,OwnerId=1000,GroupId=1000 \
  --cache-attributes CacheStaleTimeoutInSeconds=300
```
- One file = one object; path = key. Metadata (POSIX mode, owner, mtime) is stored as
  object metadata; SMB shares store NTFS ACLs similarly and need AD join for user auth.
- Writes go to cache then upload asynchronously (watch `CloudBytesUploaded`,
  `CachePercentDirty`). Reads of objects written **by other clients directly to S3**
  are invisible until a **refresh**: `refresh-cache --file-share-arn ... --folder-list '["/"]'`
  or set `CacheStaleTimeoutInSeconds`. Two gateways on one bucket = both need refresh;
  writes to the same key from both corrupt — one writer per prefix.
- File upload notifications (`notification-policy`) emit EventBridge events when a file
  is fully uploaded — the trigger for downstream processing.
- Not for: millions of tiny files with constant listing (listing hits S3 LIST per directory
  on refresh), databases, or > ~1 GB/s.

## 4. Volume and Tape Gateway specifics
- **Cached volumes** : primary in S3, hot data local.
  **Stored volumes**: primary local, async backup to S3. Snapshots become EBS
  snapshots — restore in-cloud as EBS volumes for DR.
- iSCSI initiator with CHAP (`update-chap-credentials`); mount from one initiator only.
- **Tape Gateway**: presents a VTL (medium changer + 10 drives) to backup software;
  tapes live in S3 while "in the library" and move to **Glacier Flexible Retrieval /
  Deep Archive** when the software ejects/exports them (archive) — retrieval 3-5 h /
  12 h. Create tapes in bulk (`create-tapes --num-tapes-to-create 20 --tape-size-in-bytes 2199023255552`)
  or auto-create by barcode prefix.

## 5. DataSync
```bash
# 1. Agent (VM OVA / EC2 AMI / Snowcone) with 443 outbound to DataSync endpoints or a VPC endpoint; activate
aws datasync create-agent --agent-name dc1 --activation-key <KEY> --vpc-endpoint-id vpce-0abc --subnet-arns ... --security-group-arns ...
# 2. Locations
aws datasync create-location-nfs --server-hostname nas.corp --subdirectory /export/data \
  --on-prem-config AgentArns=<AGENT_ARN> --mount-options Version=NFS4_1
aws datasync create-location-s3 --s3-bucket-arn arn:aws:s3:::bucket --subdirectory /migrated \
  --s3-storage-class STANDARD --s3-config BucketAccessRoleArn=arn:aws:iam::<ACCOUNT_ID>:role/datasync-s3
# 3. Task
aws datasync create-task --source-location-arn <NFS> --destination-location-arn <S3> --name nas-to-s3 \
  --options 'VerifyMode=ONLY_FILES_TRANSFERRED,OverwriteMode=ALWAYS,PreserveDeletedFiles=PRESERVE,TransferMode=CHANGED,PosixPermissions=PRESERVE,Uid=INT_VALUE,Gid=INT_VALUE,BytesPerSecond=104857600,LogLevel=TRANSFER' \
  --excludes 'FilterType=SIMPLE_PATTERN,Value=/tmp*|*.lock|/.snapshot' \
  --cloud-watch-log-group-arn arn:aws:logs:<REGION>:<ACCOUNT_ID>:log-group:/aws/datasync \
  --schedule 'ScheduleExpression=cron(0 1 * * ? *)'
aws datasync start-task-execution --task-arn <TASK>
aws datasync describe-task-execution --task-execution-arn <EXEC>   # PREPARING -> TRANSFERRING -> VERIFYING -> SUCCESS
```
- Agent only for on-prem/self-managed sources; **AWS-to-AWS** (S3↔EFS/FSx, cross-region,
  cross-account S3) needs no agent.
- Each execution does a full metadata scan (PREPARING) then transfers deltas
  (`TransferMode=CHANGED`); tens of millions of files make PREPARING long — split into
  tasks by top-level directory with `--includes` and run them in parallel (one agent
  handles multiple tasks; add agents for throughput, ~up to 10 Gbps per agent).
- `VerifyMode=POINT_IN_TIME_CONSISTENT` re-reads everything (slow, strongest);
  `ONLY_FILES_TRANSFERRED` for scheduled syncs; `NONE` only for throwaway.
- Bandwidth: `BytesPerSecond` on the task, or a task-level schedule outside office hours.
  Enhanced-mode tasks (S3→S3) lift the file-count and throughput ceilings.
- S3 destination: objects store POSIX metadata as user metadata; small files cost
  per-request — Glacier classes applied directly on write with `--s3-storage-class` (and
  mind storage-class minimum-duration charges on re-syncs that overwrite).
- Task reports (`--task-report-config`) write per-file success/skipped/verified JSON to S3
  — the evidence for an audited migration.
- Cut-over pattern: full sync (days) → nightly deltas → freeze source → final delta
  with `PreserveDeletedFiles=REMOVE` → verify → repoint clients.

## Gotchas
- A File Gateway share does not "see" bucket changes from DataSync or other writers
  without refresh — if you combine them, refresh after each DataSync run (EventBridge
  on task `SUCCESS` → Lambda `refresh-cache`).
- DataSync NFS needs `no_root_squash` (or `all_squash` mapping) on the export for the
  agent to read everything; `PERMISSION_DENIED` on a subset of files is this.
- SMB locations need a user with Backup Operators-level rights to copy ACLs; otherwise
  only data moves.
- Gateway cache full → write stalls; `CacheFree` and `UploadBufferFree` alarms are mandatory.
- Gateway VM snapshots/vMotion with the cache disk can corrupt it; exclude from host backup.
- Unconfirmed: current per-agent throughput and file-count ceilings; see DataSync quotas.

## Verify
- [ ] Gateway `describe-gateway-information` shows `RUNNING`; `CachePercentDirty` returns near 0 after an idle period (uploads keep up).
- [ ] File written on-prem via the share appears in S3 within the expected upload lag; file written to S3 appears on the share after refresh.
- [ ] DataSync execution ends `SUCCESS` with `FilesVerified == FilesTransferred` and the task report lists zero `FAILED`; spot-check 10 random files with `sha256sum` vs `aws s3api head-object` checksum.
- [ ] Repeating the task moves ~0 bytes (`BytesTransferred` small) — delta logic works.
- [ ] Tape Gateway: backup software completes a backup and a restore from an archived tape within the documented retrieval window.

## Checked

Date: 2026-11-02. Confirmed on Storage Gateway, File Gateway, Volume Gateway and DataSync pages in sources (what is, agent requirements, create task) and by check_commands (all aws storagegateway/datasync flags exist): gateway types, DataSync agent and task concepts. Removed as not stated there: 20% cache rule and 150 GiB minimum, 32 TiB / 32-volume and 16 TiB volume limits, 90/180-day minimums. Left, marked gated: gateway VM sizing floor (confirm on the requirements page).

Method: documentation only; no commands were run.
