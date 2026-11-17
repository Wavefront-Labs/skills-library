---
id: computing-software.cloud-infrastructure-engineering.aws.efs-cross-vpc-and-cross-account-mounts
name: efs-cross-vpc-and-cross-account-mounts
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, efs, efs-cross-vpc, cross-account, efs-utils, mount-target]
level: advanced
status: docs-checked
description: "Mount EFS from another VPC or account over peering or Transit Gateway using mount target IPs, efs-utils options, file system policies and same-AZ placement."
sources: ["https://docs.aws.amazon.com/efs/latest/ug/efs-different-vpc.html", "https://docs.aws.amazon.com/efs/latest/ug/mounting-fs-mount-helper-ec2-linux.html", "https://docs.aws.amazon.com/efs/latest/ug/iam-access-control-nfs-efs.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cross-VPC and cross-account EFS mounts

## 1. Network
- Peering or Transit Gateway between client VPC and the EFS VPC; routes both ways.
- Mount target security group allows inbound NFS from the client CIDRs.
- From another VPC, mount with a mount target IP address rather than the file system DNS name.

## 2. Mount by IP with efs-utils
```bash
aws efs describe-mount-targets --file-system-id fs-0abc \
  --query 'MountTargets[].{az:AvailabilityZoneId,ip:IpAddress}'
sudo mount -t efs -o tls,iam,mounttargetip=<MOUNT_TARGET_IP> fs-0abc /mnt/shared
```
- Pick the mount target in the **same AZ ID** as the client (AZ names can differ between accounts).
- fstab: `fs-0abc:/ /mnt/shared efs _netdev,tls,iam,mounttargetip=<MOUNT_TARGET_IP> 0 0`.

## 3. Cross-account authorization
File system policy in the owner account:
```json
{"Effect":"Allow","Principal":{"AWS":"arn:aws:iam::<CLIENT_ACCOUNT_ID>:role/app"},
 "Action":["elasticfilesystem:ClientMount","elasticfilesystem:ClientWrite"],
 "Resource":"arn:aws:elasticfilesystem:<REGION>:<OWNER_ACCOUNT_ID>:file-system/fs-0abc",
 "Condition":{"Bool":{"elasticfilesystem:AccessedViaMountTarget":"true"}}}
```
Mount with `iam` so the client's role is presented; combine with access points for POSIX identity.

## Verify
- [ ] `df -h /mnt/shared` shows the file system; writes succeed as the expected UID.
- [ ] Client and mount target share the AZ ID.

## Checked

2026-10-28

Confirmed: mounttargetip and tls,iam mount options, same Availability Zone ID requirement across accounts, _netdev for automatic mounts, ClientMount/ClientWrite actions, elasticfilesystem:AccessedViaMountTarget condition key, describe-mount-targets (EFS User Guide pages, check_commands).

Removed: TCP 2049 and security-group-reference claims, DNS-resolution claim, cross-AZ charge claim, Route 53 private zone alternative, efs-utils crossaccount option.

Method: documentation only; no commands were run.
