---
id: computing-software.systems-network-administration.windows-server.sms-orchestrator-and-proxy-setup
name: sms-orchestrator-and-proxy-setup
category: computing-software
field: systems-network-administration
product: windows-server
tags: [storage-migration-service, sms-orchestrator, sms-proxy, windows-admin-center, firewall-rules]
level: practitioner
status: docs-checked
description: "Set up the Storage Migration Service orchestrator and proxy: where to install, required ports and accounts, scaling with proxy service on destinations."
sources:
  - https://learn.microsoft.com/en-us/windows-server/storage/storage-migration-service/overview
  - https://learn.microsoft.com/en-us/windows-server/storage/storage-migration-service/migrate-data
  - https://learn.microsoft.com/en-us/windows-server/storage/storage-migration-service/faq
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SMS orchestrator and proxy setup

## Components
- **Orchestrator** (Storage Migration Service): Windows Server 2019 or later; runs jobs and keeps the job database. Use a separate
  server for multi-server migrations, or the destination when migrating only one server.
- **Proxy** (Storage Migration Service Proxy): install it on every destination running Windows Server 2019 or later; it doubles transfer speed
  and opens the needed firewall ports on that destination. A destination created as an Azure VM from the job gets the proxy added automatically.
- Windows Admin Center with the Storage Migration Service extension as the UI.

## Install
- Orchestrator: in Windows Admin Center connect to it, go to Server Manager > Storage Migration Service and select Install.
- Proxy: connect to each destination in Windows Admin Center, go to Server Manager > Roles and features > Features, select Storage Migration Service Proxy and Install.
- Migrating to or from failover clusters: install Failover Clustering Tools on the orchestrator (done automatically when you select Migrate from failover clusters in the inventory job settings). NetApp FAS sources need the NetApp PowerShell Toolkit installed manually on the orchestrator.

## Accounts
- A migration account that is an administrator on the source computers and the orchestrator, and one that is an administrator on the destination computers and the orchestrator. They can be domain or local accounts, except for a computer not joined to the domain, which needs a local user.
- For cutover, supply AD credentials with permission to remove the computer from the domain and add it back with a new name if the migration account lacks it; destination takeover can fail unless the account is a Domain Admin or has admin rights on the source computer's AD object.
- Computers in a domain should all be in the same forest; to transfer the source's domain name the destination must be in the same domain.

## Firewall (enable on sources and destinations)
- File and Printer Sharing (SMB-In) 445
- Netlogon Service (NP-In)
- Windows Management Instrumentation (DCOM-In, WMI-In)
- The orchestrator also needs File and Printer Sharing (SMB-In) enabled inbound.
- Third-party firewalls: TCP 445, TCP 135, TCP 1025-65535 (RPC/DCOM ephemeral); Storage Migration Service ports are TCP 28940 (orchestrator) and TCP 28941 (proxy).

## Scale and tuning
- Install the proxy on every destination.
- `FileTransferThreadCount` (REG_DWORD, decimal) under `HKEY_LOCAL_MACHINE\Software\Microsoft\SMSProxy` on every proxy node: default 8 simultaneous file copies, valid range 1 to 512. `EndpointFileTransferTaskCount` under `HKEY_LOCAL_MACHINE\Software\Microsoft\SMS` controls parallel shares (default 8, range 1 to 512). A new job picks them up without a service restart.
- Orchestrator and destinations should have at least two cores or vCPUs and 2 GB of memory.

## Verify
- [ ] WAC SMS extension connects to the orchestrator; inventory of a test source succeeds.

## Checked
Release checked: windowsserverdocs (storage-migration-service folder) and windows-powershell-docs (Windows Server 2025 docset), GitHub main as of 2026-10-23.
- overview and migrate-data pages: orchestrator on Windows Server 2019 or later, proxy install steps in Windows Admin Center, migration account rules, same-forest rule, firewall rules (SMB-In, Netlogon NP-In, WMI DCOM-In and WMI-In), TCP 28940 orchestrator and 28941 proxy, 2 cores and 2 GB recommendation.
- faq page: FileTransferThreadCount under SMSProxy and EndpointFileTransferTaskCount under SMS, defaults 8, valid range 1 to 512.
- Wrong claims fixed: thread maximum was 128 (docs say 512); the proxy is not auto-installed when you add a destination (it is installed manually, except for Azure VMs created from the job); proxy port was given as TCP 28940 (28940 is the orchestrator, 28941 the proxy).
- Removed unconfirmed details: Install-WindowsFeature names SMS and SMS-Proxy, the firewall display group command, and the WcfOperationTimeoutInMinutes tuning note.

Method: documentation only; no commands were run.
