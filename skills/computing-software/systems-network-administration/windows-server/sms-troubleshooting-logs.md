---
id: computing-software.systems-network-administration.windows-server.sms-troubleshooting-logs
name: sms-troubleshooting-logs
category: computing-software
field: systems-network-administration
product: windows-server
tags: [windows-server, storage-migration-service, sms, sms-troubleshooting, sms-logs, event-logs, get-smslogs, known-issues]
level: advanced
status: docs-checked
description: "Troubleshoot Storage Migration Service: event log channels, collecting debug logs with Get-SmsLogs, common errors, service restarts and known issues."
sources:
  - https://learn.microsoft.com/en-us/windows-server/storage/storage-migration-service/known-issues
  - https://learn.microsoft.com/en-us/windows-server/storage/storage-migration-service/faq
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Troubleshoot Storage Migration Service

## Logs
Event Viewer: `Applications and Services Logs\Microsoft\Windows\StorageMigrationService` on the orchestrator (it always holds both logs) and `StorageMigrationService-Proxy` on destinations with the proxy installed.
```powershell
Get-WinEvent -LogName 'Microsoft-Windows-StorageMigrationService/Admin' -MaxEvents 50 | fl TimeCreated,Id,Message
```
Collect logs for Microsoft Support with the open-source Storage Migration Service Helper script (https://aka.ms/smslogs); read its README for usage.

## Services
- Orchestrator service: Storage Migration Service (`NET STOP SMS`); proxy service: `SMSPROXY`.
- Several known issues are resolved by restarting the Storage Migration Service service on the orchestrator. Install the latest cumulative updates: several fixes ship that way.

## Common errors
| Symptom | Cause |
|---|---|
| Inventory fails to connect or access denied | firewall rules (SMB-In, Netlogon NP-In, WMI DCOM-In and WMI-In), wrong credential, `LocalAccountTokenFilterPolicy = 0` set by Group Policy on the source |
| Inventory reads source registry and is rejected | Remote Registry service stopped, firewall, or migration account lacks remote registry or read permission on the source |
| Transfer log download times out | very large transfer; raise `sendTimeout` in the orchestrator's `Microsoft.StorageMigration.Service.exe.config` (known-issues page) |
| Transfer slow | no proxy on destination, default thread counts (see sms-transfer-data) |
| Files skipped as in use | applications lock them exclusively; rerun the transfer |
| Cutover stalls after the first restart | source not in a DHCP subnet but DHCP selected |

## Database
Job state lives in an ESE database in the hidden `%programdata%\Microsoft\StorageMigrationService` folder on the orchestrator (the FAQ documents moving it with the service stopped, and the known-issues page documents recreating it by stopping SMS and SMSPROXY and starting the service, which creates a new database). Do not touch the database during an active migration.

## Verify
- [ ] Root cause tied to an event; job completes after fix.

## Checked
Release checked: windowsserverdocs (storage-migration-service folder) and windows-powershell-docs (Windows Server 2025 docset), GitHub main as of 2026-10-23.
- known-issues page: log locations on orchestrator and proxy, Storage Migration Service Helper script (aka.ms/smslogs), restarting the Storage Migration Service service, NET STOP SMS / SMSPROXY, LocalAccountTokenFilterPolicy, remote registry failure causes, sendTimeout workaround for transfer log download, TCP 28940 timeout message.
- faq page: ESE database in the hidden programdata folder and how to move it.
- Wrong claims fixed: the database is under programdata, not %SystemRoot%\SMS (which holds the service config file); the helper is a script from the GitHub link, not a module named SmsLogsModule.psm1. Removed unconfirmed details: SMSPS service, SMB1 advice for 2003 sources, antivirus and WinRM causes.

Method: documentation only; no commands were run.
