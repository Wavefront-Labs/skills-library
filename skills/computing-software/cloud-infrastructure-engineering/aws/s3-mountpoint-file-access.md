---
id: computing-software.cloud-infrastructure-engineering.aws.s3-mountpoint-file-access
name: s3-mountpoint-file-access
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, s3, mountpoint, mountpoint-for-s3, mount-s3, s3-csi-driver, file-interface, fuse, express-one-zone, ml-training-data, eks, posix-semantics]
level: practitioner
status: docs-checked
description: "Mount an S3 bucket as a local file system with Mountpoint for Amazon S3 on EC2 or EKS: flags, caching, the write and rename limits, IAM and when to use EFS/FSx instead."
sources: ["https://docs.aws.amazon.com/AmazonS3/latest/userguide/mountpoint.html", "https://github.com/awslabs/mountpoint-s3/blob/main/doc/CONFIGURATION.md", "https://github.com/awslabs/mountpoint-s3/blob/main/doc/SEMANTICS.md", "https://github.com/awslabs/mountpoint-s3-csi-driver", "https://docs.aws.amazon.com/eks/latest/userguide/s3-csi.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Mountpoint for Amazon S3

**Goal:** read-heavy jobs (ML training, genomics, rendering inputs, log analysis) read S3
objects through a path like `/mnt/data` at S3 throughput, without copying data to disk
first, and nobody is surprised by what file operations do not work.

## 1. Decide it fits
Mountpoint is a FUSE client that maps file calls to S3 API calls. It is good at
**large sequential reads and writing new files**. It is not a general POSIX file system:
| Works | Does not work |
|---|---|
| Read any object, random reads within a file | Modify an existing file in place (except append on S3 Express One Zone with `--incremental-upload`) |
| Write new files sequentially (uploaded on close) | Rename on general purpose buckets (files in S3 Express One Zone directory buckets in an Availability Zone can be renamed); rename any directory |
| Delete (with `--allow-delete`), overwrite whole file (with `--allow-overwrite`, truncate on open) | Hard/symlinks, chmod/chown persistence, file locking |
| List directories (prefixes) | Many-writer coordination |
If you need shared POSIX semantics, use EFS or FSx instead.

## 2. Install and mount (EC2)
```bash
sudo yum install -y ./mount-s3.rpm          # or the .deb; packages from the Mountpoint download page
mkdir -p /mnt/data
mount-s3 training-data /mnt/data --prefix datasets/v3/ --read-only \
  --cache /mnt/nvme/mp-cache --max-cache-size 200000 --metadata-ttl 300
# writable variant
mount-s3 job-output /mnt/out --allow-delete --allow-overwrite --uid $(id -u) --gid $(id -g)
umount /mnt/data
```
- Credentials: the standard chain (instance profile). The role needs `s3:ListBucket` on
  the bucket and `s3:GetObject` (+ `PutObject`, `AbortMultipartUpload`, `DeleteObject` if
  writing) on the prefix. SSE-KMS needs `kms:Decrypt` on the key to read, and `kms:Decrypt` plus `kms:GenerateDataKey` to write (SSE-C objects cannot be read).
- `--cache` on local NVMe makes repeated epochs read locally; `--metadata-ttl` (or
  `indefinite` for immutable data) cuts LIST/HEAD calls.
- `/etc/fstab`: `s3://training-data/datasets/v3/ /mnt/data mount-s3 _netdev,nosuid,nodev,nofail,rw 0 0`.

## 3. EKS
Install the Mountpoint for Amazon S3 CSI driver (available as an EKS add-on), give
it an IAM role (EKS Pod Identity or IRSA), then a static PV:
```yaml
apiVersion: v1
kind: PersistentVolume
metadata: {name: s3-pv}
spec:
  capacity: {storage: 1200Gi}          # ignored, required field
  accessModes: [ReadWriteMany]         # or ReadOnlyMany
  storageClassName: ""                 # required for static provisioning
  mountOptions: [allow-delete, region us-east-1, prefix datasets/v3/]
  csi: {driver: s3.csi.aws.com, volumeHandle: s3-csi-driver-volume, volumeAttributes: {bucketName: training-data}}
```
Bind with a PVC (`storageClassName: ""`, `volumeName: s3-pv`). Only static provisioning.

## Gotchas
- A write is invisible to other readers until the file is closed (uploaded).
- `rm -rf dir` without `--allow-delete` fails; with it, it
  issues one DELETE per object — on millions of objects use S3 Batch/lifecycle instead.
- Tools that write via temp file + rename (many editors, `rsync` default, some ML
  checkpoint savers) fail, because file rename is only supported for S3 Express One Zone objects. Write directly or save locally and copy.
- Throughput scales with parallel readers; one single-threaded `cat` is not representative.
- Directory listing of huge prefixes is many LIST calls; avoid `ls` of a 10M-object prefix.

## Verify
- [ ] `fio --rw=read --bs=1M --numjobs=16 --directory=/mnt/data` reaches expected GB/s for the instance.
- [ ] Second training epoch shows cache hits (lower S3 `GetRequests` in CloudWatch request metrics).
- [ ] A write job's outputs appear in S3 after the process closes files.
- [ ] Mount survives reboot via fstab/systemd and fails soft (`nofail`) when S3 is unreachable.

## Checked

Checked 2026-10-27 against the S3 User Guide Mountpoint page, the Mountpoint for Amazon S3 repository docs CONFIGURATION.md and SEMANTICS.md (main branch), the Mountpoint CSI driver README, configuration and static provisioning example, and the EKS User Guide page for the CSI driver.
Confirmed: flags --prefix (must end in /), --allow-delete, --allow-overwrite, --incremental-upload (append on S3 Express One Zone), --read-only, --uid and --gid, --cache, --max-cache-size in MiB, --metadata-ttl (seconds, indefinite or minimal); required fstab options _netdev, nosuid, nodev and the s3:// entry form; IAM actions s3:ListBucket, s3:GetObject, s3:PutObject, s3:AbortMultipartUpload, s3:DeleteObject; file rename only for S3 Express One Zone objects, no directory rename, no chmod/chown, locks, hard or symbolic links; files being written are unreadable until closed; CSI driver supports static provisioning only with driver s3.csi.aws.com and volumeAttributes.bucketName; Pod Identity or IRSA credentials. Corrected the rename row and removed the unconfirmed add-on name and error text.

Method: documentation only; no commands were run.
