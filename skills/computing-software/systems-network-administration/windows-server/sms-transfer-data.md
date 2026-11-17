---
id: computing-software.systems-network-administration.windows-server.sms-transfer-data
name: sms-transfer-data
category: computing-software
field: systems-network-administration
product: windows-server
tags: [windows-server, storage-migration-service, sms, sms-transfer, validate-transfer, delta-transfer, checksums, destination-mapping]
level: practitioner
status: docs-checked
description: "Transfer data with Storage Migration Service: map volumes to destinations, validate, run initial and re-run delta transfers, checksum options and transfer reports."
sources:
  - https://learn.microsoft.com/en-us/windows-server/storage/storage-migration-service/migrate-data
  - https://learn.microsoft.com/en-us/windows-server/storage/storage-migration-service/faq
  - https://learn.microsoft.com/en-us/powershell/module/storagemigrationservice/new-smstransfer
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Storage Migration Service: transfer data

## Configure the transfer
WAC > job > Transfer data:
1. Destination credentials and destination server (existing server, or create an Azure
   VM directly from the wizard).
2. Map each source volume to a destination volume; choose which shares to include.
3. Adjust settings: local users and groups handling (rename accounts with the same name (default), reuse accounts with the same name, or do not transfer users and groups). `New-SmsTransfer` also exposes `-ChecksumType`, `-FileRetryCount`, `-FileRetryIntervalInSec`, `-SkipMovePreExisting` and `-ExcludeLocalPrincipals`.
4. **Validate**, then Start transfer.

## Run
Start transfer. SMS migrates SMB share flags, settings and security and creates the shares on the destination.
- The first transfer moves existing destination files to a backup folder (not supported on destinations running Azure File Sync with cloud tiering); later transfers refresh the destination without a backup by default.
- Transfer again any time before cutover: only files updated since the last transfer are copied.
- Migrated local user accounts arrive disabled with a random 127-character password; enable them and set a new password.

## Throughput tuning
Registry value `FileTransferThreadCount` (REG_DWORD, decimal) under `HKEY_LOCAL_MACHINE\Software\Microsoft\SMSProxy` on every node running the proxy: default 8 simultaneous file copies, valid range 1 to 512; a new job picks it up without a service restart. `EndpointFileTransferTaskCount` under `HKEY_LOCAL_MACHINE\Software\Microsoft\SMS` sets parallel shares (default 8). Also install the Storage Migration Service Proxy on destinations running Windows Server 2019 or later, which doubles transfer speed.

## Reports
WAC: select **Error log only** or **Transfer log** to save a CSV. Each later transfer overwrites the database information of the previous run, so save the CSV if you need an audit trail; very large transfers may need the download timeout raised (known-issues page). Files exclusively locked by applications are not migrated: SMS retries three times with a sixty-second delay (adjustable) and you can rerun the transfer to copy skipped files.

## Verify
- [ ] Error log empty or every failure explained; shares match the inventory.

## Checked
Release checked: windowsserverdocs (storage-migration-service folder) and windows-powershell-docs (Windows Server 2025 docset), GitHub main as of 2026-10-23.
- migrate-data page: transfer steps, local user/group options, first-transfer backup behaviour and the Azure File Sync exception, disabled migrated accounts with 127-character passwords, transfer-again option, CSV log overwrite note; faq page: three retries at 60 seconds, FileTransferThreadCount and EndpointFileTransferTaskCount (default 8, range 1 to 512) and the proxy doubling speed.
- New-SmsTransfer parameter names (-ChecksumType, -FileRetryCount, -FileRetryIntervalInSec, -SkipMovePreExisting, -ExcludeLocalPrincipals) from the cmdlet reference (descriptions are blank there).
- Wrong claims fixed: the thread setting lives under SMSProxy (not SMSPowershell) and its maximum is 512, not 128. Removed unconfirmed details: destination capacity validation wording, backup-privilege and SYSTEM deny ACE remark, and the file attribute and timestamp list.

Method: documentation only; no commands were run.
