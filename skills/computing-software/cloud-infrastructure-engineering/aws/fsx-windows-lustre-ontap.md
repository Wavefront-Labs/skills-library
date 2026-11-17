---
id: computing-software.cloud-infrastructure-engineering.aws.fsx-windows-lustre-ontap
name: fsx-windows-lustre-ontap
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, fsx, fsx-lustre, fsx-windows, fsx-ontap, fsx-openzfs, smb, active-directory, dfs-namespaces, shadow-copies, lustre, data-repository-association, s3-linked, scratch, persistent, netapp, snapmirror, flexcache, iscsi, multi-protocol, hpc-storage, sql-server-fci, file-server-migration]
level: advanced
status: gated
description: "Pick and run the right FSx flavour: Windows (SMB, AD, Multi-AZ, shadow copies), Lustre (S3-linked, striping), NetApp ONTAP (multi-protocol, SnapMirror, tiering) and OpenZFS."
sources: ["https://docs.aws.amazon.com/fsx/latest/WindowsGuide/what-is.html", "https://docs.aws.amazon.com/fsx/latest/LustreGuide/what-is.html", "https://docs.aws.amazon.com/fsx/latest/ONTAPGuide/what-is-fsx-ontap.html", "https://docs.aws.amazon.com/fsx/latest/OpenZFSGuide/what-is-fsx.html", "https://docs.aws.amazon.com/fsx/latest/LustreGuide/create-dra-linked-data-repo.html", "https://docs.aws.amazon.com/fsx/latest/WindowsGuide/high-availability-multiAZ.html", "https://docs.aws.amazon.com/fsx/latest/ONTAPGuide/volume-styles.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# FSx — Windows File Server, Lustre, NetApp ONTAP, OpenZFS

**Goal:** choose the FSx flavour that matches the protocol and performance need, size
its throughput tier correctly (the thing you cannot change freely later), and run it
with AD/S3/replication wired in rather than bolted on.

## 1. Choose
| Need | Flavour |
|---|---|
| SMB shares for Windows clients, AD permissions, DFS, SQL Server FCI storage | **FSx for Windows File Server** |
| HPC/ML scratch at GB/s to TB/s, POSIX, data in S3 | **FSx for Lustre** |
| NFS + SMB on the same data, snapshots, clones, dedup/compression, on-prem NetApp replication, iSCSI | **FSx for NetApp ONTAP** |
| NFS with ZFS snapshots/clones, lowest latency small files, Linux-only | **FSx for OpenZFS** |
Not FSx: shared Linux files at modest throughput with elastic sizing → EFS.

## 2. FSx for Windows File Server
```bash
aws fsx create-file-system --file-system-type WINDOWS --storage-capacity 2048 --storage-type SSD \
  --subnet-ids subnet-a subnet-b --security-group-ids sg-fsx \
  --windows-configuration 'ActiveDirectoryId=d-0abc,DeploymentType=MULTI_AZ_1,ThroughputCapacity=64,PreferredSubnetId=subnet-a,AutomaticBackupRetentionDays=14,DailyAutomaticBackupStartTime=02:00,Aliases=[files.corp.example.com]'
```
- **AD**: AWS Managed Microsoft AD (simplest) or self-managed AD via
  `SelfManagedActiveDirectoryConfiguration` (needs a service account with rights to
  create computer objects in the target OU, DNS from the FSx subnets to the DCs,
  ports 53/88/123/135/389/445/464/636/3268-3269/9389/49152-65535 open).
- **Multi-AZ** gives an active/standby pair with automatic failover (SMB continuous
  availability makes it transparent to Windows clients); Single-AZ 2 is cheaper for
  dev. Choose at creation; migrating = new FS + `robocopy`/DataSync.
- **Throughput capacity** (tiers 32/64/128/256/512/1024/2048 MB/s on SSD)
  sets network throughput, CPU and in-memory cache; disk throughput is separate
  (SSD IOPS 3/GiB baseline, provisionable). Can be modified later (with brief
  unavailability on Single-AZ). HDD storage is for cold shares only.
- Manage shares with the FSx **remote PowerShell endpoint** (`New-PSSession -ComputerName
  amznfsx...corp.example.com -ConfigurationName FSxRemoteAdmin`), e.g.
  `New-FSxSmbShare -Name data -Path "<DATA_DRIVE>:\share\data" -FolderEnumerationMode AccessBased`
  (the FSx data volume is drive D on the file server),
  `Enable-FsxDedup`, `Set-FsxShadowStorage -Default` then `Set-FsxShadowCopySchedule -Default`
  (users get Previous Versions in Explorer).
- **DNS alias** + SPN registration (`setspn`) so `\\files.corp.example.com` works with
  Kerberos; CNAME in AD DNS to the FSx DNS name.
- Audit via Windows event forwarding to CloudWatch Logs/Kinesis (`AuditLogConfiguration`).
- Migrate from an existing file server: **DataSync** (preserves NTFS ACLs with SMB) or
  `robocopy /MIR /COPY:DATSOU /SEC /B /MT:32`.

## 3. FSx for Lustre
```bash
aws fsx create-file-system --file-system-type LUSTRE --storage-capacity 4800 \
  --subnet-ids subnet-a --security-group-ids sg-lustre \
  --lustre-configuration 'DeploymentType=PERSISTENT_2,PerUnitStorageThroughput=250,DataCompressionType=LZ4,ImportedFileChunkSize=1024'
aws fsx create-data-repository-association --file-system-id fs-0abc --file-system-path /s3data \
  --data-repository-path s3://bucket/dataset/ --batch-import-meta-data-on-create \
  --s3 'AutoImportPolicy={Events=[NEW,CHANGED,DELETED]},AutoExportPolicy={Events=[NEW,CHANGED,DELETED]}'
```
- `SCRATCH_2`: temporary, no replication, cheapest.
  `PERSISTENT_2`: replicated within AZ, a per-TiB throughput tier provisioned (see the Lustre performance page),
  supports backups and compression. Throughput = `PerUnitStorageThroughput × TiB`, so
  **size for throughput, not capacity**: total throughput scales with capacity times the tier.
- Capacity increases in fixed increments (see the Lustre docs); increases allowed, no shrink (gated: unconfirmed, source is paywalled or blocked).
- **Data Repository Association** mirrors S3 metadata into the FS lazily; file bodies
  load on first read (`lfs hsm_restore` to prefetch) and auto-export writes back.
  Legacy `ImportPath/ExportPath` is replaced by DRAs (multiple per FS on PERSISTENT_2).
- Clients: `lustre-client` kernel module (AL2023 `dnf install -y lustre-client`;
  version must match kernel), mount
  `mount -t lustre -o relatime,flock fs-0abc.fsx.<REGION>.amazonaws.com@tcp:/<MOUNT_NAME> /fsx`
  (mount name from `describe-file-systems`). SG: TCP 988 and 1018-1023 between clients and FS.
- Striping: default 1 stripe; big files read by many ranks → `lfs setstripe -c -1 -S 4m /fsx/big/`
  (all OSTs). Many small files → keep stripe count 1. `lfs df`, `lfs getstripe` to inspect.
- Compression (LZ4) is free in CPU terms and shrinks billed usage for text/CSV.
- EKS/Batch/ParallelCluster integrate natively (CSI driver, launch-template mount).

## 4. FSx for NetApp ONTAP
```bash
aws fsx create-file-system --file-system-type ONTAP --storage-capacity 2048 \
  --subnet-ids subnet-a subnet-b --security-group-ids sg-ontap \
  --ontap-configuration 'DeploymentType=MULTI_AZ_2,ThroughputCapacity=384,PreferredSubnetId=subnet-a,FsxAdminPassword=<PASSWORD>,RouteTableIds=[rtb-0abc]'
aws fsx create-storage-virtual-machine --file-system-id fs-0abc --name svm1 --root-volume-security-style UNIX
aws fsx create-volume --volume-type ONTAP --name data --ontap-configuration 'StorageVirtualMachineId=svm-0abc,JunctionPath=/data,SizeInMegabytes=1048576,StorageEfficiencyEnabled=true,TieringPolicy={Name=AUTO,CoolingPeriod=31}'
```
- Model: file system (HA pair, or multiple pairs for scale-out) → **SVMs** (tenants, each
  can join a different AD) → **volumes** (junction paths, exported via NFS/SMB/iSCSI/NVMe).
- Multi-AZ uses a **floating IP outside the VPC CIDR**; you must list `RouteTableIds` so
  AWS inserts the route, and clients must mount the SVM's NFS/SMB DNS name, not an ENI IP.
  Transit Gateway/peering reaching that floating IP needs static routes to the
  `EndpointIpAddressRange`.
- Primary storage (SSD) vs **capacity pool** (S3-backed, auto-tiered by `TieringPolicy`,
  ~1/6 the price): size SSD for the hot set and let `AUTO` tier the rest. Capacity pool
  reads add latency; `SNAPSHOT_ONLY` for latency-sensitive volumes.
- **SnapMirror** to/from on-prem ONTAP (`snapmirror create` on the destination via the
  ONTAP CLI `ssh fsxadmin@management.fs-0abc...`): the migration and DR path for NetApp
  shops; cutover = `snapmirror break`. **FlexCache** gives on-prem or cross-region
  read caches of a cloud volume.
- Snapshots (`snapshot policy default` = hourly/daily/weekly, instant, ~0 cost) and
  FlexClone (writable clone in seconds) are the ONTAP superpowers — use them for dev/test DBs.
- Throughput capacity 128-4,096 MB/s per HA pair; modifiable. SSD IOPS 3/GiB auto or provisioned.
- Enterprise features via ONTAP CLI/REST: dedup/compression/compaction (on by default),
  quotas, `vserver cifs` options, NFS Kerberos, autosize (`volume autosize -mode grow`).

## 5. FSx for OpenZFS
NFS v3/v4.x, up to 21 GBps throughput and millions of IOPS, snapshots and instant clones, ZSTD
compression, user/group quotas. Create a root volume then child volumes (`create-volume --volume-type OPENZFS`),
mount `fs-0abc.fsx.<REGION>.amazonaws.com:/fsx/data`. Best for migrating ZFS/NFS Linux servers
and latency-sensitive small-file workloads (record size tunable per volume).

## Gotchas
- All flavours: **storage capacity and throughput tier are the cost**; you cannot
  shrink, and some (Lustre scratch, Windows deployment type) cannot change at all.
  Start smaller, grow.
- FSx for Windows cannot join AD if the FSx subnets' DHCP options/VPC DNS do not
  resolve the AD domain — point the VPC DHCP option set (or Route 53 Resolver rule) at the DCs.
- Lustre client module mismatch after a kernel update = `mount.lustre: Operation not supported`; pin kernel or reinstall `lustre-client`.
- ONTAP capacity-pool "free" space in `df` hides tiering; `volume show-footprint` for the truth.
- Backups: Windows/ONTAP/OpenZFS have daily automatic backups (FS-level or volume-level); Lustre only on PERSISTENT.
- Unconfirmed: current throughput ceilings per flavour (they rise regularly); check the performance pages.

## Verify
- [ ] Windows: `Test-NetConnection fs-dns -Port 445` from a domain client; `Get-FSxSmbShare` lists the share; failover (`Start-FSxFailover`-equivalent via modify/maintenance) interrupts a copy briefly.
- [ ] Lustre: `lfs df -h` shows all OSTs; `IOR`/`fio` aggregate across 4 clients reaches ≥ 80% of `PerUnitStorageThroughput × TiB`; `ls /fsx/s3data` lists S3 keys and a new S3 object appears within minutes.
- [ ] ONTAP: NFS and SMB clients see the same file with mapped permissions; `snapmirror show` is `SnapMirrored`/`Idle`; capacity-pool tiering reported in `volume show-footprint`.
- [ ] A snapshot/backup restore to a new file system reproduces a checksum-verified sample.

## Checked

Date: 2026-11-02. Confirmed on FSx User Guides in sources (Windows what-is and Multi-AZ HA, Lustre what-is and data repository associations, ONTAP what-is, OpenZFS what-is) and by check_commands: file system types, OpenZFS 21 GBps and millions of IOPS, DRA linking to S3. Removed as not stated there: Lustre per-TiB MB/s tiers and the worked 300 MB/s example, 1.2/2.4 TiB capacity steps (kept as a gated note without figures), OpenZFS 1M IOPS figure, 4-1024 KiB record size range, < 30 s Windows failover time.

Method: documentation only; no commands were run.
