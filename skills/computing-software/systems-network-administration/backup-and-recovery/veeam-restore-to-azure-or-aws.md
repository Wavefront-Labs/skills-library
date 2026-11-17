---
id: computing-software.systems-network-administration.backup-and-recovery.veeam-restore-to-azure-or-aws
name: veeam-restore-to-azure-or-aws
category: computing-software
field: systems-network-administration
product: backup-and-recovery
tags: [veeam, restore-to-cloud, direct-restore-to-azure, restore-to-amazon-ec2, cloud-dr, helper-appliance]
level: advanced
status: docs-checked
description: "Restore Veeam VM and agent backups directly to Azure VMs or Amazon EC2 for DR or migration: accounts, helper appliances, conversion, networking and cost control."
sources:
  - https://helpcenter.veeam.com/docs/backup/vsphere/restore_azure.html
  - https://helpcenter.veeam.com/docs/backup/vsphere/restore_amazon.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Restore to Azure or AWS (Veeam)

Veeam can restore workloads (VMs, Google VM instances, physical servers and so on) from backups to Microsoft Azure or to Amazon EC2 as EC2 instances.

## Uses
- Restore workloads from Veeam backups.
- Migrate workloads from on-premises to the cloud.
- Create a test environment in the cloud for troubleshooting, testing patches and updates.

## Supported source backups
Backups of vSphere, VMware Cloud Director and Hyper-V VMs made by Veeam Backup & Replication; Veeam Agent for Windows/Linux machines; Nutanix AHV, Amazon EC2, Azure, Google Compute Engine, oVirt, Proxmox VE, Scale Computing HyperCore, HPE Morpheus VM Essentials, Xen, Sangfor aSV and KubeVirt workloads made by the matching Veeam product or plug-in.

## Azure specifics
- Restore the latest or any earlier restore point in the chain.
- Uses the Azure Resource Manager deployment model; batch restore of several VMs at once is supported.
- Generation follows the boot loader of the backed-up VM: UEFI becomes Generation 2, BIOS becomes Generation 1, and if both are possible Generation 2.
- Limitations are on a separate "Limitations for Restore to Microsoft Azure" page.

## AWS specifics
The Amazon EC2 section lists "How Restore to Amazon EC2 Works", "AWS IAM User Permissions" and "Performing Restore to Amazon EC2"; use those pages for permissions and steps.

## Checked
Date: 2026-11-03. Confirmed against the Veeam Help Center pages "Restore to Microsoft Azure" and "Restore to Amazon EC2".
Removed (not on those pages): account and appliance preparation, helper appliance and proxy appliance advice, instance/disk type choices, Secure Restore, guest driver and RDP readiness, egress and cost notes, Verify section.
Method: documentation only; no commands were run.
