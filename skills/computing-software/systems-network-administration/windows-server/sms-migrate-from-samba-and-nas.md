---
id: computing-software.systems-network-administration.windows-server.sms-migrate-from-samba-and-nas
name: sms-migrate-from-samba-and-nas
category: computing-software
field: systems-network-administration
product: windows-server
tags: [storage-migration-service, sms-samba-source, sms-inventory, linux, netapp]
level: advanced
status: docs-checked
description: "Use Storage Migration Service to move shares from Linux Samba and NetApp CIFS sources to Windows Server, including credentials, limits and cutover differences."
sources:
  - https://learn.microsoft.com/en-us/windows-server/storage/storage-migration-service/overview
  - https://learn.microsoft.com/en-us/windows-server/storage/storage-migration-service/migrate-data
  - https://learn.microsoft.com/en-us/windows-server/storage/storage-migration-service/cutover
  - https://learn.microsoft.com/en-us/windows-server/storage/storage-migration-service/faq
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Migrating from Samba and NAS sources with SMS

Storage Migration Service can inventory and transfer from Linux Samba servers and NetApp FAS arrays when the orchestrator runs Windows Server 2022, or Windows Server 2019 with KB5001384.

## Linux Samba
- Tested by Microsoft: CentOS 7, Debian GNU/Linux 8, RedHat Enterprise Linux 7.6, SLES 11 SP4, Ubuntu 16.04 LTS and 12.04.5 LTS, with Samba 4.8, 4.7, 4.3, 4.2 and 3.6.
- In WAC: New job > choose **Linux servers that use Samba**; enter Samba credentials and Linux credentials (including an SSH password or private key).
- Cutover from Samba sources is supported: the cutover steps include Linux-specific stages (collecting source IP addresses and an extra restart), and the source can get DHCP or a new static address in the same subnet.
- The transfer destination must be Windows (SMS does not migrate to Samba, NetApp or Azure Files).

## NetApp FAS (2022, 2019 with updates)
- Source = NetApp FAS array hosting a NetApp CIFS server running ONTAP 9. Enter the array IP address and admin credentials, then credentials for the CIFS servers; Start scan lists the CIFS servers and you can uncheck any you do not want.
- Install the NetApp PowerShell Toolkit manually on the orchestrator (it needs a NetApp support agreement).
- Local users and groups cannot be migrated from NetApp CIFS servers; volumes show no drive letters and can be mapped to any destination volumes; a backup-privilege validation error from NetApp CIFS servers is expected and can be ignored; for cutover use NetApp subnets instead of DHCP.

## Other NAS
Only Windows, Linux Samba and NetApp FAS CIFS sources are documented as supported; for other NAS devices use a tool of your choice.

## Gotchas
- Transfer again (the second pass copies only updated files) and check the error log for skipped files.
- Cutover validation and manual cutover steps are in the cutover documentation.

## Verify
- [ ] Transfer reports zero unexpected errors; spot-check ACLs and file counts; DNS/alias switched.

## Checked
Release checked: windowsserverdocs (storage-migration-service folder) and windows-powershell-docs (Windows Server 2025 docset), GitHub main as of 2026-10-23.
- overview page: Samba and NetApp sources need Windows Server 2022 or 2019 with KB5001384; tested Samba distributions and versions; NetApp FAS with ONTAP 9; faq page: no migration to Samba, NetApp or Azure Files.
- migrate-data page: Samba and NetApp job steps, NetApp Toolkit, local users and groups limit, backup-privilege error, NetApp subnets for cutover.
- cutover page: Linux-specific stages (31% and 42%) show cutover from Linux sources is supported.
- Wrong claims fixed: "Samba 4.8+" (tested list is 4.8, 4.7, 4.3, 4.2, 3.6); KB4512534 gate (the overview page names KB5001384 for 2019); "cutover from Linux not supported" (it is supported). Removed unconfirmed details: sudo requirement, ACL mapping behaviour, other NAS vendors and robocopy advice.

Method: documentation only; no commands were run.
