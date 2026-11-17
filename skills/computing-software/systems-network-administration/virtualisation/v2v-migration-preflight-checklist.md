---
id: computing-software.systems-network-administration.virtualisation.v2v-migration-preflight-checklist
name: v2v-migration-preflight-checklist
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [migration-preflight, v2v, vmware-to-hyper-v, virt-v2v, migration-cutover, proxmox, hyper-v]
level: practitioner
status: docs-checked
description: "Pre-migration checklist for moving VMs between hypervisors: inventory, snapshots, drivers, BIOS vs UEFI, static IPs and MACs, licensing, app owners, rollback, and cutover plan."
sources:
  - https://libguestfs.org/virt-v2v.1.html
  - https://libguestfs.org/virt-v2v-support.1.html
  - https://github.com/proxmox/pve-docs/blob/master/qm.adoc
  - https://learn.microsoft.com/en-us/windows-server/virtualization/hyper-v/plan/should-i-create-a-generation-1-or-2-virtual-machine-in-hyper-v
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# V2V migration pre-flight checklist

Do this per VM (script the inventory) before any conversion run.

## Inventory and blockers
- [ ] **Firmware**: BIOS or UEFI (target VM must match: Hyper-V Gen 1/Gen 2, PVE SeaBIOS/OVMF).
- [ ] **Disks**: count, sizes, controllers; RDMs/pass-through or shared disks (WSFC) need a
  separate plan.
- [ ] **Snapshots**: consolidate/delete first; virt-v2v's manual says converting from a snapshot is only for a throwaway test.
- [ ] **Guest OS support** on target hypervisor: check the tool's support list (for virt-v2v, its support page).
- [ ] **Windows power state**: virt-v2v cannot convert guests that use Fast Startup or are hibernated.
- [ ] **Encryption**: if a BitLocker key is held in the source vTPM it cannot be moved; the guest will
  ask for the recovery key at first boot on the target (virt-v2v manual), so escrow the keys.
- [ ] **Network**: static IPs per NIC, VLANs, MAC-dependent licences or DHCP reservations
  (decide: keep MAC or update reservations).
- [ ] **Drivers on target**: VirtIO (PVE/KVM) or Hyper-V drivers present in the guest before
  cutover for Windows (install virtio-win guest tools in advance); Linux initramfs includes
  target storage drivers.
- [ ] **Agents**: VMware Tools to remove; backup, monitoring, AV agents that bind to the
  hypervisor.
- [ ] **Licensing**: Windows activation may require reactivation; per-host licensed apps
  (Oracle, SQL per core) on the new cluster.
- [ ] **Dependencies**: app tiers moving together, firewall rules referencing host groups,
  DNS TTLs lowered.

## Plan
- Method per VM: tool (virt-v2v, PVE ESXi import, SCVMM/Windows Admin Center, Veeam
  restore-to-other-hypervisor, Azure Migrate), offline vs incremental sync.
- Downtime window agreed with app owner; communication sent.
- **Rollback**: keep the source VM powered off, not deleted, for N days; document how to
  power it back on (and revert DNS/IP).
- Test conversion of one representative VM per OS family first.

## Day-of checks
- Fresh backup of the source.
- Shut down guest cleanly (not suspend) before final copy.
- After boot on target: drivers, IPs, services, app smoke test, time sync, backups enrolled.

## Verify
Checklist signed per VM; pilot VMs ran a full business cycle on the target before bulk waves.

## Checked

Checked 2026-10-27 against the virt-v2v manual, the Proxmox VE qm manual (proxmox/pve-docs) and Microsoft's Hyper-V generation 1 versus 2 article (MicrosoftDocs/windowsserverdocs). Confirmed: Hyper-V generation 1 is legacy BIOS and generation 2 is UEFI, Proxmox VE VMs use SeaBIOS by default with OVMF for UEFI, virt-v2v refuses Fast Startup and hibernated Windows guests, a vTPM-held BitLocker key cannot be moved and triggers a recovery-key prompt, and conversion from a snapshot is only for testing. Removed the unconfirmed remark that some tools skip independent disks and the unconfirmed mention of specific legacy operating systems. The remaining items are planning prompts for the migrating team rather than product facts.

Method: documentation only; no commands were run.
