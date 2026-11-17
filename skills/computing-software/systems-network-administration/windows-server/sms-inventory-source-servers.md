---
id: computing-software.systems-network-administration.windows-server.sms-inventory-source-servers
name: sms-inventory-source-servers
category: computing-software
field: systems-network-administration
product: windows-server
tags: [windows-server, storage-migration-service, sms, sms-inventory, windows-admin-center, orchestrator, file-server-migration]
level: practitioner
status: docs-checked
description: "Set up Storage Migration Service and inventory source file servers: orchestrator, proxy, credentials, firewall rules and reading the inventory results in WAC."
sources:
  - https://learn.microsoft.com/en-us/windows-server/storage/storage-migration-service/overview
  - https://learn.microsoft.com/en-us/windows-server/storage/storage-migration-service/migrate-data
  - https://learn.microsoft.com/en-us/windows-server/storage/storage-migration-service/faq
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Storage Migration Service: inventory source servers

SMS migrates file servers (shares, data, permissions, and optionally the server
identity) from Windows Server 2003 and later, failover clusters, Linux Samba servers and NetApp FAS CIFS servers to newer Windows Server or
Azure VMs, driven from Windows Admin Center. Samba, NetApp and cluster sources need a Windows Server 2022 orchestrator, or 2019 with KB5001384.

## Components
- **Orchestrator**: Windows Server 2019 or later (can be the destination when migrating a single server); install Storage Migration Service from Windows Admin Center Server Manager. Install the Storage Migration Service Proxy on each destination running 2019 or later for faster transfers (Roles and features > Features).
- Windows Admin Center with the Storage Migration Service extension.

## Network and credentials
- Source and destination: File and Printer Sharing (SMB-In), Netlogon Service (NP-In),
  Windows Management Instrumentation (DCOM-In) and (WMI-In) rules enabled inbound.
- Migration account: administrator on the source (and orchestrator); domain or local account, except local only for computers not joined to a domain. Cutover may need AD credentials that can remove and re-add the computer.

## Inventory job
WAC > Storage Migration Service > New job > choose Windows servers and clusters, Linux servers that use Samba, or NetApp FAS array > enter credentials (SSH password or private key for Linux) > Install required tools > add devices > **Validate** > **Start scan**.
You can review the inventoried shares, configuration, network adapters and volumes for each server.

## What to look for
- Shares located in the Windows system folder produce warnings and must be skipped during transfer; SMS does not transfer files or folders that could interfere with Windows operation.
- Multiple server sources in one job are processed serially for inventory, transfer and cutover; create more jobs to run servers in parallel.
- Local users and groups: the default option renames same-named accounts and migrates them; NetApp CIFS sources cannot migrate local users and groups.

## Verify
- [ ] Validation passed for all servers and the scan completed with the share list and volumes you expect.

## Checked
Release checked: windowsserverdocs (storage-migration-service folder) and windows-powershell-docs (Windows Server 2025 docset), GitHub main as of 2026-10-23.
- overview page: supported source and destination OS lists, Samba/NetApp/cluster sources need Windows Server 2022 or 2019 with KB5001384, orchestrator and proxy requirements; migrate-data page: job types, credentials, install-required-tools, validate and scan steps, system-folder share warnings, local user options.
- faq page: serial processing of multiple sources in one job.
- Removed unconfirmed details: Install-WindowsFeature feature names, the per-source result list (DFS-N root status, file counts), the hidden admin share claim and the CSV export step.

Method: documentation only; no commands were run.
