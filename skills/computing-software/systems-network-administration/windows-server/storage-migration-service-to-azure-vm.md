---
id: computing-software.systems-network-administration.windows-server.storage-migration-service-to-azure-vm
name: storage-migration-service-to-azure-vm
category: computing-software
field: systems-network-administration
product: windows-server
tags: [windows-server, storage-migration-service, sms-azure-vm, windows-admin-center, cutover, azure-migration]
level: advanced
status: docs-checked
description: "Use Storage Migration Service in Windows Admin Center to migrate file servers to new Azure VMs it creates for you, then transfer data and cut over identity."
sources:
  - https://learn.microsoft.com/en-us/windows-server/storage/storage-migration-service/migrate-data
  - https://learn.microsoft.com/en-us/windows-server/storage/storage-migration-service/overview
  - https://learn.microsoft.com/en-us/windows-server/storage/storage-migration-service/faq
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Storage Migration Service to Azure VMs

Storage Migration Service (SMS) can create the destination as an Azure VM during the transfer step, then run the
normal inventory, transfer and cutover.

## Prerequisites
- Orchestrator: Windows Server 2019 or later, managed from Windows Admin Center.
- A valid Azure subscription, an existing Azure Compute resource group where you have Create rights, and an existing Azure virtual network and subnet.
- An ExpressRoute circuit or Azure VPN solution tied to that network, allowing connectivity from the VM to on-premises clients, domain controllers, the orchestrator, the WAC computer and the source computer.
- Source servers inventoried (see sms-inventory-source-servers).

## Create the Azure VM from the job
In the SMS job's **Transfer data** step, on the Add a destination device and mappings page choose **Create a new Azure VM** and use the wizard. It sizes the VM automatically, provisions storage, formats disks, joins the domain and adds the Storage Migration Service proxy (Windows Server 2019 or later). You can choose Windows Server 2025 (recommended), 2022, 2019 or 2016 VMs of any size with managed disks.

## Transfer and cutover
- Map source volumes and shares to the new VM's volumes, select Validate, then Start transfer; transfer again to copy files updated since the last pass.
- Cutover moves the source's computer name and IP address information to the destination, as for any destination; confirm the addressing you want in the cutover configuration.

## Gotchas
- The migration must keep the VM joined to the same domain as the source for the source's domain name to be transferred.
- SMS does not support Azure Files as a destination; it does support servers running the Azure File Sync agent with cloud tiering.
- To lift and shift VMs to Azure without a newer operating system, Microsoft suggests Azure Migrate.

## Verify
- [ ] Clients reach shares on the old name after cutover; shares and data match the inventory.

## Checked
Release checked: windowsserverdocs (storage-migration-service folder) and windows-powershell-docs (Windows Server 2025 docset), GitHub main as of 2026-10-23.
- migrate-data page: Create a new Azure VM prerequisites (subscription, resource group with Create rights, virtual network and subnet, ExpressRoute or VPN connectivity to clients, DCs, orchestrator, WAC and source), what the wizard automates, Windows Server versions offered; overview page: Azure VM section, Azure Migrate alternative; faq page: no Azure Files destination, Azure File Sync with cloud tiering supported.
- Removed unconfirmed details: that WAC must be registered with Azure, the region and VM size picker wording, per-volume disk type choice, and the claim that cutover assigns new Azure IPs and migrates local accounts.

Method: documentation only; no commands were run.
