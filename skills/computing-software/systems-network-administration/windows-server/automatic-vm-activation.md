---
id: computing-software.systems-network-administration.windows-server.automatic-vm-activation
name: automatic-vm-activation
category: computing-software
field: systems-network-administration
product: windows-server
tags: [windows-server, windows-activation, avma, automatic-virtual-machine-activation, hyper-v, datacenter-edition, avma-keys, data-exchange-integration-service, licensing]
level: practitioner
status: docs-checked
description: "Activate guest VMs on a licensed Datacenter Hyper-V host with AVMA keys: requirements, guest/host version matrix, data exchange service, and reporting."
sources:
  - https://learn.microsoft.com/en-us/windows-server/get-started/automatic-vm-activation
  - https://learn.microsoft.com/en-us/windows-server/virtualization/hyper-v/manage/manage-hyper-v-integration-services
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Automatic Virtual Machine Activation (AVMA)

**What:** guests running on an **activated Windows Server Datacenter** Hyper-V host activate
against the host itself, no KMS/ADBA or internet needed. Good for hosting providers, DMZ and
isolated environments.

## Requirements
- Host: Windows Server Datacenter with the Hyper-V role, activated. In a failover cluster every host must be
  activated. AVMA does not work with other virtualization technologies.
- Guests: a host activates guests of the same or older version back to Server 2012 R2 (a 2025 host covers 2025,
  2022, 2019, 2016 and 2012 R2 guests; a 2022 host starts at 2022), all editions of those versions.
- Hyper-V **Data Exchange** (Key-Value Pair Exchange) integration service enabled for the VM; it is on by default
  for new VMs:
```powershell
Enable-VMIntegrationService -VMName app01 -Name 'Key-Value Pair Exchange'
```

## Configure a guest
Install the edition-specific **AVMA key** (public list on Microsoft Learn) in the guest:
```cmd
slmgr /ipk <AVMA_KEY_FOR_GUEST_EDITION>
slmgr /dlv
```
The VM activates when it starts, provided the host is activated. The AVMA keys per version and edition are
listed on the Microsoft Learn AVMA page (Server 2025 Datacenter, Standard and Azure Edition keys exist, among others).
The keys can also go in an unattend setup file.

## Licensing reality
AVMA is a technical activation mechanism. Licensing is still determined by your agreement:
Datacenter licenses all cores of the host and permits unlimited Windows Server VMs on it.
AVMA needs a Datacenter host, so a Standard host cannot activate guests this way.

## Reporting
Activation data is exchanged by key-value pairs and stored in the VM's registry; historical data about AVMA
requests is logged in Event Viewer on the virtualization host.

## Verify
- [ ] Guest `slmgr /dlv` shows Licensed after the AVMA key is installed.
- [ ] Integration service enabled on all VM templates.

## Checked

2026-10-27. Documentation release: windowsserverdocs Automatic Virtual Machine Activation (dated 2025-07-14) and Manage Hyper-V integration services. Confirmed: Datacenter host requirement, cluster note, version matrix, Key-Value Pair Exchange (default on), slmgr /ipk install, unattend tip, reporting location. Removed Azure Stack HCI/Azure Local, the 7-day renewal, live-migration to Standard host behaviour, the SPP event source and the quoted slmgr output as unconfirmed.

Method: documentation only; no commands were run.
