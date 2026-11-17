---
id: computing-software.systems-network-administration.windows-server.sms-cutover-identity
name: sms-cutover-identity
category: computing-software
field: systems-network-administration
product: windows-server
tags: [windows-server, storage-migration-service, sms, sms-cutover, identity-migration, rename-computer, ip-migration, file-server-migration]
level: advanced
status: docs-checked
description: "Cut over a file server with Storage Migration Service: move name and IPs to the destination, rename the source, AD account handling and rollback considerations."
sources:
  - https://learn.microsoft.com/en-us/windows-server/storage/storage-migration-service/cutover
  - https://learn.microsoft.com/en-us/windows-server/storage/storage-migration-service/migrate-data
  - https://learn.microsoft.com/en-us/windows-server/storage/storage-migration-service/overview
  - https://learn.microsoft.com/en-us/powershell/module/storagemigrationservice/new-smscutover
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Storage Migration Service: cut over

Cutover makes the destination **become** the source: it takes the source computer name
and (optionally) IP addresses, so users and apps keep using `\\FS01\share` with no
change.

## Configure
WAC > job > Cut over to the new servers:
1. AD credentials, if the migration credentials cannot remove the computer from the domain and add it back with a new name.
2. Map source network adapters to destination adapters; the source gets a new DHCP or static address (a static address must be in the same subnet as the old one or cutover fails; NetApp sources use NetApp subnets), and a random or chosen new name.
3. Validate, then start. (`New-SmsCutover` has a `-CutoverTimeout` parameter.)

## What happens
SMS connects to both computers, creates a temporary local account on each (domain-joined: `MsftSmsStorMigratSvc`), removes the source from the domain, maps its interfaces, renames it and rejoins it, removes the destination from the domain, applies the source's IP information and name to the destination, and rejoins it using the source's original AD computer account (preserving group memberships and ACLs). The servers restart several times; the duration depends on restarts and AD and DNS replication.

## Planning
- Do a transfer shortly before cutover so the final delta is small.
- Communicate the outage window: users and apps may see an interruption while names and addresses move and servers restart.
- File server cluster resources are supported as sources and destinations; Windows Server 2008 R2 clusters support inventory and transfer but not cutover; domain controllers cannot be cut over.
- Apps referencing the server by IP keep working only if IPs are migrated.

## Rollback and manual cutover
SMS does not alter the contents of the source; keep it online for at least two weeks after cutover. If cutover fails because of the environment, run `Stop-SmsTransfer -Name <job>` on the orchestrator and finish the remaining steps manually following the documented stages (including re-enabling the local account token filter policy where cutover disabled it). After cutover, review certificates on the destination: renaming does not reissue certificates that carry the old name.

## Common issues
- Stuck waiting for the source to respond after the first restart: likely when the source is not in a DHCP subnet but DHCP was selected.
- Destination fails to join with the source's AD object: the account is not a Domain Admin and has no admin rights on that object; supply alternate AD credentials.

## Verify
- [ ] `\\FS01\share` resolves to the new server; `Get-SmbShare` there lists all shares;
  old server reachable under its new name.

## Checked
Release checked: windowsserverdocs (storage-migration-service folder) and windows-powershell-docs (Windows Server 2025 docset), GitHub main as of 2026-10-23.
- cutover page: the twelve-step sequence, temporary account name, stage table (including steps that apply only to Linux sources), manual cutover with `Stop-SmsTransfer -Name`, 2008 R2 and domain controller limits from the overview page.
- migrate-data page: network adapter mapping, static address must be in the same subnet, AD credentials only if the migration credentials lack rights, keep the source two weeks, reissue certificates; New-SmsCutover has -CutoverTimeout.
- Removed unconfirmed details: the 30 minutes per step default, the 30 to 60 minute outage estimate, the troubleshooting causes for WinRM and WMI, and the manual rollback procedure. SMS does not offer an automatic rollback in the documentation reviewed.

Method: documentation only; no commands were run.
