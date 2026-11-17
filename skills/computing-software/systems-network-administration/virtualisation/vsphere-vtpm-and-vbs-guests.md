---
id: computing-software.systems-network-administration.virtualisation.vsphere-vtpm-and-vbs-guests
name: vsphere-vtpm-and-vbs-guests
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [vtpm, virtualization-based-security, vbs, credential-guard, windows-11, secure-boot, efi, native-key-provider, vsphere-security, vmware, vsphere]
level: practitioner
status: docs-checked
description: "Give vSphere guests a vTPM and VBS: key provider prerequisite, EFI and hardware version needs, privileges, clone Replace option, backup nvram rule, removal impact, VBS CPU rules."
sources:
  - https://techdocs.broadcom.com/us/en/vmware-cis/vsphere/vsphere/8-0/vsphere-security-8-0/securing-virtual-machines-with-virtual-trusted-platform-module.html
  - https://techdocs.broadcom.com/us/en/vmware-cis/vsphere/vsphere/8-0/vsphere-security/securing-virtual-machines-with-virtual-trusted-platform-module/vtpm-overview.html
  - https://techdocs.broadcom.com/us/en/vmware-cis/vsphere/vsphere/8-0/vsphere-security/securing-virtual-machines-with-virtual-trusted-platform-module/add-a-virtual-trusted-platform-module-to-a-virtual-machine.html
  - https://techdocs.broadcom.com/us/en/vmware-cis/vsphere/vsphere/8-0/vsphere-security/securing-virtual-machines-with-virtual-trusted-platform-module/enable-vtpm-for-an-existing-virtual-machine.html
  - https://techdocs.broadcom.com/us/en/vmware-cis/vsphere/vsphere/8-0/vsphere-security/securing-virtual-machines-with-virtual-trusted-platform-module/remove-vtpm-from-a-virtual-machine.html
  - https://techdocs.broadcom.com/us/en/vmware-cis/vsphere/vsphere/8-0/vsphere-security-8-0/securing-windows-guest-operating-systems-with-virtual-based-security.html
  - https://techdocs.broadcom.com/us/en/vmware-cis/vsphere/vsphere/8-0/vsphere-security/securing-windows-guest-operating-systems-with-virtual-based-security/enable-virtualization-based-security-on-a-virtual-machine.html
  - https://techdocs.broadcom.com/us/en/vmware-cis/vsphere/vsphere/8-0/vsphere-security/securing-windows-guest-operating-systems-with-virtual-based-security/enable-virtualization-based-security-on-an-existing-virtual-machine.html
  - https://techdocs.broadcom.com/us/en/vmware-cis/vsphere/vsphere/8-0/vsphere-security/securing-windows-guest-operating-systems-with-virtual-based-security/disable-virtualization-based-security.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# vTPM and Virtualization-based Security for vSphere guests

**Goal:** guests that need a TPM 2.0 or VBS get one, without making the VM unrecoverable.

## vTPM prerequisites
- A **key provider** must exist first; a vTPM relies on VM encryption to protect its data. With a vTPM only the VM home files (including the `.nvram` file that holds vTPM state) are encrypted, not the disks, unless you add encryption explicitly.
- VM firmware **EFI** and hardware version 14 or later.
- vCenter Server 6.7+ for Windows guests, 7.0 Update 2+ for Linux guests; ESXi hosts 6.7+ (Windows guest) or 7.0 Update 2+ (Linux guest). Guest OS: Windows Server 2008 and later, Windows 7 and later, or Linux.
- Privileges: Cryptographic operations (Clone, Encrypt, Encrypt new, Migrate, Register VM), plus Virtual machine -> Change Configuration -> Add or remove device when adding to an existing VM. Opening a console afterwards also needs Cryptographic operations -> Direct Access.

## Add a vTPM
New VM: the vTPM is added in the creation wizard. Existing VM: power it off, Edit Settings -> Add New Device -> Trusted Platform Module -> OK. The VM details then show encryption applied.

## VBS (Windows guests)
Enable it in two steps: first on the VM, then inside Windows.
- Intel CPUs: vSphere 6.7+, hardware version 14+, Windows 10 (64-bit) or later or Windows Server 2016 (64-bit) or later.
- AMD CPUs: vSphere 7.0 Update 2+, hardware version 19+, Windows 10 (64-bit) 1809 or later or Windows Server 2019 (64-bit) or later.
- Apply the latest patches for Windows 10 1809 and Windows Server 2019 first.
- New VM: tick "Enable Windows Virtualization Based Security" on the guest OS page. Existing VM: Edit Settings -> VM Options -> tick Enable for Virtualization Based Security.
- Changing firmware from Legacy BIOS to UEFI on an existing Windows VM requires reinstalling the guest OS.
- To disable: power off, turn off VBS options inside Windows first (they stay on otherwise and can cause performance problems), then clear the Enable box under VM Options.

## Cloning
In vSphere 8.0 and later, cloning a vTPM VM with the **Replace** option starts with a new blank vTPM that has its own secrets and identity. All keys, including workload keys, are replaced, so ensure workloads no longer depend on the old vTPM first.

## Backup and DR
- Backups of a vTPM VM must include all VM data including the `*.nvram` file; without it the VM cannot be restored.
- The VM home files are encrypted, so the encryption keys must be available at restore time.

## Gotchas
- Removing a vTPM makes all encrypted information on the VM unrecoverable. Deactivate guest uses such as BitLocker first or the VM may not boot. The VM must be powered off, must have no snapshots, and you need Cryptographic operations -> Decrypt.
- The vTPM endorsement key is issued by VMCA or a third-party CA; changing it invalidates data stored in the vTPM.

## Checked
Date: 2026-11-08. Confirmed against the vSphere 8.0 Security pages for vTPM (overview, create, add to existing, remove) and VBS (overview, activate on new and existing VM, deactivate). Removed because those pages do not state them: Native Key Provider specifics, the Windows 11 Secure Boot step, the PowerCLI `New-VTpm` command, `msinfo32` and `Get-Tpm` checks, GPO/Intune enablement, restore-to-another-vCenter key provider advice, backup-product caveats and the nested virtualization and CPU overhead remarks.
Method: documentation only; no commands were run.
