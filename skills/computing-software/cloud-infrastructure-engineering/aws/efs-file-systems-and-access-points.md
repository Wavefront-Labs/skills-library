---
id: computing-software.cloud-infrastructure-engineering.aws.efs-file-systems-and-access-points
name: efs-file-systems-and-access-points
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, efs, elastic-file-system, nfs, access-point, access-points, mount-target, efs-utils, efs-csi, elastic-throughput, bursting-throughput, provisioned-throughput, one-zone, efs-lifecycle, infrequent-access, efs-archive, efs-replication, file-system-policy, iam-authorization, tls-mount, lambda-efs, fargate-efs, posix, efs-performance-mode]
level: practitioner
status: docs-checked
description: "Design and operate EFS: mount targets, throughput modes, access points for POSIX isolation, IAM/TLS-enforced mounts, lifecycle to IA/Archive, and EFS from Lambda, ECS, EKS."
sources: ["https://docs.aws.amazon.com/efs/latest/ug/whatisefs.html", "https://docs.aws.amazon.com/efs/latest/ug/performance.html", "https://docs.aws.amazon.com/efs/latest/ug/efs-access-points.html", "https://docs.aws.amazon.com/efs/latest/ug/iam-access-control-nfs-efs.html", "https://docs.aws.amazon.com/efs/latest/ug/lifecycle-management-efs.html", "https://docs.aws.amazon.com/efs/latest/ug/efs-mount-helper.html", "https://docs.aws.amazon.com/lambda/latest/dg/configuration-filesystem.html"]
licence: Apache-2.0
version: 5
updated: 2026-11-17
---

# EFS file systems and access points

**Goal:** a shared POSIX file system that many instances, containers or functions mount
across AZs, with throughput that matches the workload, per-application isolation via
access points, encryption in transit enforced, and cold files tiered automatically.

## 1. When EFS is right
Shared read/write across many clients, POSIX semantics, elastic size — CMS uploads,
home directories, ML training data shared by workers, lift-and-shift apps that expect
a shared NFS. Not for: databases (latency ~ms per op), single-instance high-IOPS
(use EBS), Windows SMB (FSx for Windows), or > few-GB/s scratch (FSx for Lustre).

## 2. Create
```bash
aws efs create-file-system --performance-mode generalPurpose --throughput-mode elastic \
  --encrypted --kms-key-id alias/efs-prod --backup --tags Key=Name,Value=shared-uploads
# one mount target per AZ, in a private subnet, SG allowing NFS 2049 from clients
aws efs create-mount-target --file-system-id fs-0abc --subnet-id subnet-a --security-groups sg-efs
aws efs put-lifecycle-configuration --file-system-id fs-0abc --lifecycle-policies \
  '[{"TransitionToIA":"AFTER_30_DAYS"},{"TransitionToArchive":"AFTER_90_DAYS"},{"TransitionToPrimaryStorageClass":"AFTER_1_ACCESS"}]'
```
- **Performance mode**: `generalPurpose` (always; `maxIO` is legacy and raises latency).
- **Throughput mode**: `elastic` (default-right: pay per GB read/written, scales to
  tens of GB/s instantly); `bursting` (throughput tied to Standard-class size: base 50 KiB/s per GiB,
  bursting to 100 KiB/s per GiB while credits last; with no credits a small FS falls to the 1 MiB/s minimum); `provisioned`
  (fixed MB/s for a predictable monthly price when traffic is steady and high).
- **One Zone** (`--availability-zone-name`) stores in a single AZ (always General Purpose mode); only for
  reproducible data.
- Enable automatic backups (AWS Backup).

## 3. Mount
Install `amazon-efs-utils`. The mount helper does TLS (stunnel) and IAM:
```bash
sudo mount -t efs -o tls,iam,accesspoint=fsap-0abc fs-0abc:/ /mnt/uploads
# /etc/fstab
fs-0abc:/ /mnt/uploads efs _netdev,tls,iam,accesspoint=fsap-0abc 0 0
```
Plain NFS (NFSv4.1 or NFSv4.0) also works but cannot do TLS/IAM.

## 4. Access points
An access point pins a **root directory** and a **POSIX identity** for every client
that uses it, regardless of what user the client process runs as:
```bash
aws efs create-access-point --file-system-id fs-0abc --client-token app1 \
  --posix-user Uid=1001,Gid=1001 \
  --root-directory 'Path=/app1,CreationInfo={OwnerUid=1001,OwnerGid=1001,Permissions=750}'
```
Use one per application/tenant; combine with a file system policy that only allows
each role via its access point:
```json
{"Version":"2012-10-17","Statement":[
 {"Effect":"Allow","Principal":{"AWS":"arn:aws:iam::<ACCOUNT_ID>:role/app1"},
  "Action":["elasticfilesystem:ClientMount","elasticfilesystem:ClientWrite"],
  "Resource":"arn:aws:elasticfilesystem:<REGION>:<ACCOUNT_ID>:file-system/fs-0abc",
  "Condition":{"StringEquals":{"elasticfilesystem:AccessPointArn":"arn:aws:elasticfilesystem:<REGION>:<ACCOUNT_ID>:access-point/fsap-0abc"}}},
 {"Effect":"Deny","Principal":{"AWS":"*"},"Action":"*","Resource":"arn:aws:elasticfilesystem:<REGION>:<ACCOUNT_ID>:file-system/fs-0abc",
  "Condition":{"Bool":{"aws:SecureTransport":"false"}}}]}
```
The Deny on `aws:SecureTransport` forces `tls`. Set a file system policy in production.

## 5. From Lambda, ECS/Fargate, EKS
EFS is accessible from EC2, ECS, EKS, Lambda and Fargate. Use an access point per workload and a role with `ClientMount`/`ClientWrite`. For EKS use the `aws-efs-csi-driver`. Look up the exact Lambda, ECS task-definition and CSI settings in each service's EFS page.

## 6. Performance tuning
- Throughput scales with parallelism and large I/O; single small-file ops are ~ms.
  Many small files: run parallel workers.
- Regional Bursting file systems in General Purpose mode: maximum 35,000 read and 7,000 write IOPS;
  Provisioned 55,000 / 25,000. Regional Elastic reaches 900,000-2,500,000 read and 500,000 write IOPS
  and 20-60 GiBps read, 1-5 GiBps write (varies by Region). Per-client limit: 1,500 MiBps with Elastic and
  efs-utils 2.0 or later, else 500 MiBps.
- Watch `PercentIOLimit` (General Purpose IOPS limit), `MeteredIOBytes` (elastic cost driver).

## 7. Cost and lifecycle
See the EFS pricing page for storage-class prices. Lifecycle rules move files not accessed for N
days (`TransitionToIA` accepts AFTER_1_DAY to AFTER_365_DAYS values, `TransitionToArchive` the same from
AFTER_1_DAY, at most 3 policies); `TransitionToPrimaryStorageClass: AFTER_1_ACCESS` pulls hot files back.
Writes to IA or Archive files go to Standard first and become eligible to transition after 24 hours.
**EFS Replication** (`create-replication-configuration`) copies a file system to another Region or AZ.

## Gotchas
- Mount hangs forever → check that the mount-target security group allows NFS 2049 from the client.
- Unmount before deleting mount targets.
- Maximum throughput depends on the Region; exceeding it needs a quota increase.

## Verify
- [ ] Mount from an instance in each AZ succeeds via the DNS name with `tls,iam`; a mount without `tls` is denied by the policy.
- [ ] A parallel `fio` run shows throughput within the mode's limits above.
- [ ] Files written via access point A are invisible/unwritable via access point B.
- [ ] `describe-file-systems` shows IA size growing after the lifecycle period.
- [ ] AWS Backup recovery point exists and a restore to a new FS reproduces a sample tree.

## Checked
2026-10-31. Confirmed against the EFS performance and lifecycle-management pages and the botocore `efs` model
(CreateFileSystem and PutLifecycleConfiguration shapes and enums): performance and throughput modes, bursting
rates (50 KiBps per GiB base, 1 MiBps minimum without credits), IOPS and throughput table, Max I/O legacy note,
lifecycle enums, 3-policy maximum and the 24-hour rule. Removed: prices, the Provisioned 24 h wait, 128 KiB tier
rule, Lambda/ECS/Fargate/CSI settings, mount options, DNS and stunnel details and other unconfirmed specifics.
Method: documentation only; no commands were run.
