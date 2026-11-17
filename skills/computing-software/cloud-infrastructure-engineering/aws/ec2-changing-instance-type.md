---
id: computing-software.cloud-infrastructure-engineering.aws.ec2-changing-instance-type
name: ec2-changing-instance-type
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, ec2, change-instance-type, resize-instance, nitro-migration, ena-driver, nvme-driver, graviton]
level: practitioner
status: docs-checked
description: "Resize an EC2 instance safely: compatibility checks (architecture, virtualization, ENA/NVMe drivers, instance store), stop/modify/start, capacity errors and rollback."
sources: ["https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-instance-resize.html", "https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/resize-limitations.html", "https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/change-instance-type-of-ebs-backed-instance.html", "https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/enhanced-networking-ena.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Changing an EC2 instance type

## 1. Compatibility checks before stopping anything
| Check | How | Blocks |
|---|---|---|
| Architecture | `aws ec2 describe-images --image-ids <ami> --query 'Images[].Architecture'` vs target | x86_64 to arm64 (Graviton) **cannot** be resized; rebuild from an arm64 AMI |
| Virtualization | `VirtualizationType` | PV instances cannot move to HVM types |
| ENA driver | `aws ec2 describe-instances --query 'Reservations[].Instances[].EnaSupport'`; on Linux `modinfo ena` | Nitro-based types require EBS-backed AMIs with the ENA driver installed; install ENA (or ixgbevf) first when moving to a type with enhanced networking |
| NVMe driver | Linux `lsmod | grep nvme`; Windows AWS NVMe driver | Nitro exposes EBS as NVMe (`/dev/nvme0n1`); fstab with `/dev/xvdf` breaks |
| Instance store | data on ephemeral disks | **lost** on stop |
| Availability | `aws ec2 describe-instance-type-offerings --location-type availability-zone --filters Name=instance-type,Values=m7i.large` | type not offered in the instance's AZ |
Other documented blockers: Spot Instances cannot change type; the new type must support at least as many attached
EBS volumes as are attached now; a NitroTPM instance can move only to a NitroTPM-capable type; with ENA Express
enabled the new type must support it. For Linux Xen-to-Nitro moves, AWS provides the Systems Manager Automation
runbook `AWSSupport-MigrateXenToNitroLinux`.

## 2. Make fstab survive NVMe
Use UUIDs or labels, never device names:
```bash
sudo blkid                     # get UUIDs
# /etc/fstab
UUID=1b2c... /data xfs defaults,nofail 0 2
```
`nofail` lets the instance boot even if a volume is missing.

## 3. The resize (EBS-backed)
```bash
aws ec2 stop-instances --instance-ids i-0abc
aws ec2 wait instance-stopped --instance-ids i-0abc
aws ec2 modify-instance-attribute --instance-id i-0abc --instance-type '{"Value":"m7i.xlarge"}'
aws ec2 start-instances --instance-ids i-0abc
aws ec2 wait instance-status-ok --instance-ids i-0abc
```
- Stopping and starting moves the instance to new hardware; a public IPv4 address that is not an Elastic IP is
  released and replaced. NVMe instance store data is lost on stop.
- Instances in an ASG: Auto Scaling marks a stopped instance unhealthy and may replace it. Suspend the group's
  scaling processes while you change the type, or change the launch template version and run an instance refresh.
- Instance store-backed instances (and EBS-backed instances whose configuration is incompatible) cannot be
  resized; migrate to a new instance.
- When you change type, EC2 applies the existing CPU option settings to the new type if it supports them;
  otherwise they reset to the new type's defaults.

## 4. Capacity errors
`InsufficientInstanceCapacity` on start: AWS has no capacity of that type in that AZ right
now. Options: retry later, choose a similar type (m7i to m6i), or change AZ (requires a new
instance; snapshots/AMI).

## 5. After the change
- Verify the OS sees the CPUs/memory (`nproc`, `free -g`), network driver
  (`ethtool -i eth0` shows `ena`), and volumes mounted.
- Licensing: software licensed per vCPU or per core can be affected by the new type; check the licence terms.
- EBS optimization and network bandwidth change with type; check workloads at peak.
- Windows with EC2Launch v1 (Server 2016/2019) may need `InitializeInstance.ps1 -Schedule`, which resets the
  administrator password unless disabled in the settings.

## Rollback
Stop, modify back to the original type, start. Keep the original type noted in a tag
(`previous-instance-type`). Take a snapshot or AMI before the first Nitro migration of an
old instance in case drivers fail.

## Verify
- [ ] Pre-checks recorded: architecture, ENA, NVMe, boot mode, AZ availability.
- [ ] Instance reaches `2/2 checks passed` after start; application health checks green.
- [ ] fstab uses UUIDs and all volumes mount after reboot.

## Checked

Date: 2026-10-27. Sources: EC2 User Guide pages "Amazon EC2 instance type changes", "Compatibility for changing the instance type" and "Change the instance type for your Amazon EC2 instance".
Confirmed: instance must be stopped; same processor architecture required; PV cannot move to HVM-only types; Nitro needs ENA-enabled EBS-backed AMIs; EBS volumes appear as NVMe devices and fstab should use UUID or label; volume-count, NitroTPM and ENA Express constraints; Spot Instances cannot be changed; ASG marks stopped instances unhealthy; public IPv4 changes unless Elastic IP; instance store-backed instances must migrate.
Corrected: CPU options are applied to the new type when possible (the skill said they can be set only at launch); the Systems Manager runbook name is AWSSupport-MigrateXenToNitroLinux.
Removed (not in the pages): UEFI-only note for Graviton, NitroInstanceChecks, the Savings Plans and Reserved Instance statement, hibernation remark and SQL Server reactivation claim.

Method: documentation only; no commands were run.
