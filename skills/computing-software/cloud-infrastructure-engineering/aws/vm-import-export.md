---
id: computing-software.cloud-infrastructure-engineering.aws.vm-import-export
name: vm-import-export
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, vm-import, vm-export, ami-import, migration, vmimport-role]
level: advanced
status: docs-checked
description: "Import VMware, Hyper-V or raw disk images into EC2 as AMIs and export instances or AMIs back to VMDK/OVA with VM Import/Export, including the vmimport role."
sources: ["https://docs.aws.amazon.com/vm-import/latest/userguide/vmimport-image-import.html", "https://docs.aws.amazon.com/vm-import/latest/userguide/required-permissions.html", "https://docs.aws.amazon.com/vm-import/latest/userguide/vmexport.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# VM Import/Export

## 1. Service role `vmimport`
You must create a service role named `vmimport` whose trust policy lets `vmie.amazonaws.com` assume it with the
condition `sts:Externalid = vmimport`, and attach a policy. The documented policy covers S3 actions on the image
bucket (including `s3:GetBucketLocation`, `s3:GetBucketAcl` and `s3:PutObject`), `ec2:ModifySnapshotAttribute`,
`ec2:CopySnapshot`, `ec2:RegisterImage`, `kms:` grants (`CreateGrant`, `Decrypt`, `DescribeKey`, `Encrypt`, ...) when
encrypting, and optional License Manager permissions to attach license configurations. Users also need
`iam:PassRole` on the role. Copy the policy documents from the "Required permissions" page.

## 2. Prepare the VM
Check the VM Import/Export user guide for supported operating systems, image formats and prerequisites before
exporting a VM from your hypervisor.

## 3. Import
```bash
aws s3 cp app-vm.ova s3://vm-imports-<ACCOUNT_ID>/
aws ec2 import-image --description app-vm --disk-containers file://containers.json \
  --boot-mode uefi --license-type BYOL --encrypted --kms-key-id alias/ami
aws ec2 describe-import-image-tasks --import-task-ids import-ami-0abc --query 'ImportImageTasks[].{s:Status,p:Progress,msg:StatusMessage,ami:ImageId}'
```
`containers.json`:
```json
[{"Description":"app vm","Format":"ova","UserBucket":{"S3Bucket":"vm-imports-<ACCOUNT_ID>","S3Key":"app-vm.ova"}}]
```

## 4. Export
```bash
aws ec2 export-image --image-id ami-0abc --disk-image-format VMDK \
  --s3-export-location S3Bucket=vm-exports-<ACCOUNT_ID>,S3Prefix=exports/
aws ec2 create-instance-export-task --instance-id i-0abc --target-environment vmware \
  --export-to-s3-task DiskImageFormat=VMDK,ContainerFormat=ova,S3Bucket=vm-exports-<ACCOUNT_ID>
```
You can export most EC2 instances to Citrix Xen, Microsoft Hyper-V or VMware vSphere; check the VM Export
requirements for instances that cannot be exported.

## Verify
- [ ] Import task `completed`; an instance from the AMI boots and passes status checks.

## Checked

2026-10-28. Confirmed against the VM Import/Export User Guide pages required-permissions and vmexport: the `vmimport` role name, `vmie.amazonaws.com` trust with `sts:Externalid = vmimport`, permission actions, iam:PassRole, License Manager option, and export targets (Citrix Xen, Hyper-V, VMware vSphere).
Removed: the VM preparation checklist (ENA/NVMe, DHCP, VMware Tools, antivirus, boot-mode rules), the image-format list and import-snapshot note, and the Marketplace/licence-included export restriction (not on the fetched pages).
Method: documentation only; no commands were run.
