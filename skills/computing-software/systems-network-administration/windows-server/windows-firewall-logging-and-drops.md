---
id: computing-software.systems-network-administration.windows-server.windows-firewall-logging-and-drops
name: windows-firewall-logging-and-drops
category: computing-software
field: systems-network-administration
product: windows-server
tags: [windows-server, windows-firewall, firewall-logging, pfirewall-log, wfp-auditing, event-5157, dropped-packets, troubleshooting, filtering-platform-auditing]
level: practitioner
status: docs-checked
description: "Troubleshoot Windows Firewall drops: enable pfirewall.log logging, WFP audit events 5152/5157, netsh wfp capture, and mapping a drop to the blocking filter."
sources:
  - https://learn.microsoft.com/en-us/windows/security/operating-system-security/network-security/windows-firewall/configure-logging
  - https://learn.microsoft.com/en-us/windows/security/operating-system-security/network-security/windows-firewall/troubleshooting-uwp-firewall
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Firewall logging and troubleshooting drops

## Enable the log
```powershell
Set-NetFirewallProfile -All -LogBlocked True -LogAllowed False -LogMaxSizeKilobytes 32767 `
  -LogFileName '%systemroot%\system32\LogFiles\Firewall\pfirewall.log'
```
- A custom log folder needs Modify rights for `NT SERVICE\mpssvc`.
- Read the log: `Get-Content $env:windir\System32\LogFiles\Firewall\pfirewall.log -Tail 50 -Wait`.

## WFP audit and filters
```powershell
auditpol /set /subcategory:"Filtering Platform Packet Drop" /failure:enable
auditpol /set /subcategory:"Filtering Platform Connection" /failure:enable
netsh wfp show filters file=filters.xml
```
Turn the audits off afterwards.

## Fast checks
- `netsh wfp capture start` / `stop` captures WFP state and drops.

## Verify
- [ ] Drop identified to a specific rule or profile, fix applied, log shows ALLOW/no DROP.

## Checked
2026-10-28: Confirmed on Learn pages set-netfirewallprofile, configure-logging, netsh-wfp and auditpol-set: -LogBlocked/-LogAllowed/-LogMaxSizeKilobytes, NT SERVICE\mpssvc rights, pfirewall.log, auditpol /subcategory, netsh wfp show filters and capture start. Removed: silent-failure claim, GPO override claim, log field list, event IDs 5157/5152 and filter-ID mapping, listening-port and Test-NetConnection checks. Replaced the auditpol subcategory names with a placeholder (names not on the fetched page).
Method: documentation only; no commands were run.
