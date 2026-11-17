---
id: computing-software.cloud-infrastructure-engineering.aws.efs-data-migration
name: efs-data-migration
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, efs, efs-migration, datasync, file-migration, metadata-preservation]
level: practitioner
status: docs-checked
description: "Migrate file data into EFS with DataSync (incremental, metadata-preserving), parallel rsync/fpsync, or EFS replication, and plan the final cutover sync."
sources: ["https://docs.aws.amazon.com/efs/latest/ug/trnsfr-data-using-datasync.html", "https://docs.aws.amazon.com/datasync/latest/userguide/create-efs-location.html", "https://docs.aws.amazon.com/efs/latest/ug/efs-replication.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Migrating data into EFS

## 1. Pick the tool
| Source | Tool |
|---|---|
| On-prem NFS/SMB | DataSync with an agent (VM or EC2) |
| Another EFS (Region/account) | EFS replication (cross-account needs an IAM role you provide; the service-linked role is not permitted) |
| EC2/EBS in AWS | DataSync |

## 2. DataSync
```bash
aws datasync create-location-nfs --server-hostname nas01.corp --subdirectory /export/projects \
  --on-prem-config AgentArns=<AGENT_ARN>
aws datasync create-location-efs --efs-filesystem-arn <EFS_ARN> \
  --ec2-config SubnetArn=<SUBNET_ARN>,SecurityGroupArns=<SG_ARN> --in-transit-encryption TLS1_2
aws datasync create-task --source-location-arn <SRC> --destination-location-arn <DST> --name projects \
  --options VerifyMode=ONLY_FILES_TRANSFERRED,PreserveDeletedFiles=REMOVE,PosixPermissions=PRESERVE,Uid=INT_VALUE,Gid=INT_VALUE,TransferMode=CHANGED
aws datasync start-task-execution --task-arn <TASK_ARN>
```
Run repeatedly: first full copy, then incrementals; final run during a short write freeze.

## 3. EFS settings during migration
- Use Elastic throughput mode: DataSync recommends it, and with Bursting mode the copy can
  affect the performance of the file system's applications and take longer.
- Enable backups, and have access points ready for the apps.

## Verify
- [ ] File counts and total bytes match (`find | wc -l`, `du -s --apparent-size`); DataSync verification passes.
- [ ] Ownership and permissions spot-checked on sample paths.

## Checked

2026-10-28. Confirmed against the EFS DataSync transfer page, the DataSync EFS location page and the EFS replication page: Elastic throughput recommended for DataSync (Bursting can slow the transfer and affect applications), --in-transit-encryption TLS1_2 option, replication roles (cross-account needs a provided IAM role). Removed (unconfirmed): agentless-DataSync-for-EFS-to-EFS claim, fpsync/rsync parallelism section, lifecycle IA charge advice. Read end to end.

Method: documentation only; no commands were run.
