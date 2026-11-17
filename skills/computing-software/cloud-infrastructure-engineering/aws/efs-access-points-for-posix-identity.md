---
id: computing-software.cloud-infrastructure-engineering.aws.efs-access-points-for-posix-identity
name: efs-access-points-for-posix-identity
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, efs, efs-access-point, access-point-posix, root-directory-enforcement, multi-tenant-storage, lambda-efs]
level: practitioner
status: docs-checked
description: "Use EFS access points to give each app or tenant an enforced POSIX user and root directory, with IAM and file system policies that require the access point."
sources: ["https://docs.aws.amazon.com/efs/latest/ug/efs-access-points.html", "https://docs.aws.amazon.com/efs/latest/ug/create-access-point.html", "https://docs.aws.amazon.com/efs/latest/ug/iam-access-control-nfs-efs.html", "https://docs.aws.amazon.com/efs/latest/ug/limits.html", "https://docs.aws.amazon.com/AmazonECS/latest/APIReference/API_EFSAuthorizationConfig.html", "https://docs.aws.amazon.com/lambda/latest/dg/configuration-filesystem-efs.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# EFS access points

An access point is an application-specific entry into an EFS file system that:
- **enforces a POSIX identity** (UID, GID, secondary GIDs) for every NFS request, ignoring
  what the client claims;
- **enforces a root directory**: the client sees that directory as `/` and cannot escape;
- **creates the root directory** with given owner and permissions if missing.

## 1. Create
```bash
aws efs create-access-point --file-system-id fs-0abc \
  --posix-user Uid=1001,Gid=1001 \
  --root-directory 'Path=/tenants/acme,CreationInfo={OwnerUid=1001,OwnerGid=1001,Permissions=0750}' \
  --tags Key=tenant,Value=acme
```
- Default quota: 10,000 access points per file system (adjustable through AWS Support; EFS quotas page). At least one mount target must exist in the VPC first.
- `CreationInfo` is applied only if the root path does not exist; if you give no ownership and
  permissions and the directory is missing, mounting through the access point fails. An existing
  directory keeps its own owner and mode, so a root-owned directory may be unwritable for UID 1001.

## 2. Mount through it
```bash
sudo mount -t efs -o tls,iam,accesspoint=fsap-0acme fs-0abc:/ /mnt/acme
```
ECS task definition `efsVolumeConfiguration` with `authorizationConfig.accessPointId` and
`iam: ENABLED` (with an access point, the volume's root directory must be omitted or `/`, and transit
encryption must be on); the EKS EFS CSI driver's dynamic provisioning creates an access point for each
PersistentVolume; Lambda connects to EFS through an access point.

## 3. Require access points with policy
File system policy (resource policy on EFS):
```json
{"Version": "2012-10-17",
 "Statement": [
  {"Sid": "DenyNonTLS", "Effect": "Deny", "Principal": {"AWS": "*"}, "Action": "*",
   "Resource": "arn:aws:elasticfilesystem:eu-west-1:111122223333:file-system/fs-0abc",
   "Condition": {"Bool": {"aws:SecureTransport": "false"}}},
  {"Sid": "AcmeOnlyViaItsAP", "Effect": "Allow",
   "Principal": {"AWS": "arn:aws:iam::111122223333:role/acme-app"},
   "Action": ["elasticfilesystem:ClientMount", "elasticfilesystem:ClientWrite"],
   "Resource": "arn:aws:elasticfilesystem:eu-west-1:111122223333:file-system/fs-0abc",
   "Condition": {"StringEquals": {"elasticfilesystem:AccessPointArn":
     "arn:aws:elasticfilesystem:eu-west-1:111122223333:access-point/fsap-0acme"}}}]}
```
Once a file system policy exists, clients without an allowing statement (and mounting
with `iam`) are denied; clients mounting without IAM are treated as anonymous and governed
by the policy's anonymous access (deny by default when any policy exists and you do not
allow `*`). Do not grant `ClientRootAccess` to tenant roles.
Identity-based alternative: IAM policy for the role with the same
`elasticfilesystem:AccessPointArn` condition.

## 4. Multi-tenant pattern
- One file system, one access point per tenant with distinct UID/GID and root path
  `/tenants/<id>`.
- Root access for everyone else: omit `ClientRootAccess` from file system policy statements (the console's
  "Prevent root access by default" preset removes it).
- Admin role with `ClientRootAccess` mounts the file system root for maintenance only.

## Gotchas
- Access point POSIX identity overrides client UIDs, so `ls -l` inside shows files owned by
  the AP's UID regardless of the local user; apps checking ownership may be confused.
- The EFS API has no operation to update an access point (botocore model), so to change its POSIX user or path create a new one.

## Verify
- [ ] Mount via the access point shows only the tenant directory as `/`.
- [ ] `touch` creates files owned by the configured UID/GID.
- [ ] The tenant role cannot mount the file system root or another tenant's access point (denied).

## Checked

Checked 2026-10-27 against the EFS User Guide pages Working with access points, Creating access points, Using IAM to control access to file systems, quotas, the ECS API reference for EFSAuthorizationConfig, the Lambda and EKS pages for EFS, and the botocore efs model.
Confirmed: access points enforce POSIX user and root directory; CreateAccessPoint PosixUser and RootDirectory.CreationInfo shape; mount command mount -t efs -o tls,iam,accesspoint=fsap-... ; default quota of 10,000 access points per file system; mounting fails if the root directory is missing and no creation info was given; actions elasticfilesystem:ClientMount (read-only), ClientWrite and ClientRootAccess and condition key elasticfilesystem:AccessPointArn; default file system policy grants anonymous access until a policy is set; ECS accessPointId and iam settings; the EFS CSI driver creates an access point per volume in dynamic provisioning; Lambda mounts EFS through an access point; there is no UpdateAccessPoint operation. Removed the unconfirmed root squash mapping, ABAC tag and backup claims.

Method: documentation only; no commands were run.
