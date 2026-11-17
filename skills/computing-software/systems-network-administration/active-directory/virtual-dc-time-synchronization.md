---
id: computing-software.systems-network-administration.active-directory.virtual-dc-time-synchronization
name: virtual-dc-time-synchronization
category: computing-software
field: systems-network-administration
product: active-directory
tags: [active-directory, virtualized-domain-controller, hyper-v-time-sync, virtual-dc-time, vmictimeprovider, vmware-tools-time-sync, w32time, time-drift, pdc-emulator]
level: practitioner
status: docs-checked
description: "Stop hypervisor time sync from fighting AD time on virtual DCs: disable or partially disable VMICTimeProvider, VMware Tools settings, and checks."
sources:
  - https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/get-started/virtual-dc/virtualized-domain-controllers-hyper-v
  - https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/manage/understand-fsmo-roles
  - https://learn.microsoft.com/en-us/powershell/module/hyper-v/disable-vmintegrationservice
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Time sync on virtual DCs

**Problem:** hypervisor integration services can push the host's clock into the guest. On a DC that bypasses the
domain time hierarchy.

## Hyper-V
Microsoft's guidance for VMs that are DCs: disable time synchronization between the host and the guest, so the guest
DC synchronizes with the domain hierarchy instead. Turn the VM off, open the VM settings, choose **Integration
Services** and clear **Time synchronization**. The Hyper-V module also has `Disable-VMIntegrationService -Name <service name> -VMName <vm>`
(the cmdlet reference shows `-Name Shutdown,VSS -VMName Test1`); use the service name as the Integration Services list shows it.

## Other hypervisors
Follow the hypervisor vendor's guidance for disabling guest time synchronization on a DC; those settings are outside
Microsoft's documentation.

## Domain hierarchy
In a default Windows Time hierarchy, a DC synchronizes with another DC, with the PDC emulator at the top. The PDC
emulator of the forest root domain is the authoritative time source for the forest; configure its external time
source there (see the PDC time skill).

## Verify
- [ ] The Time synchronization integration service is off for every virtual DC.
- [ ] Each DC's time source is another DC (or, for the forest-root PDC emulator, the configured external source).

## Checked

Documentation: Microsoft Learn "Virtualized domain controllers on Hyper-V" (time service section), understand-FSMO-roles
and the Disable-VMIntegrationService reference, from MicrosoftDocs/windowsserverdocs and MicrosoftDocs/windows-powershell-docs, main branch (latest commits 2026-10-23).
Confirmed: recommendation to disable host-guest time synchronization on DC VMs and to use the domain hierarchy, the
Integration Services check box path, the forest-root PDC emulator as the authoritative time source, and the cmdlet's
`-VMName`/`-Name` parameters (the exact service name for time sync was not shown in the reference). The earlier advice to prefer a registry change to VMICTimeProvider over disabling the
service contradicted Microsoft's guidance and was removed, along with VMware keys, Azure behaviour, `w32tm` checks
(not covered in the docs repo) and the 1 s offset target.

Method: documentation only; no commands were run.
