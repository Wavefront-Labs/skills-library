---
id: computing-software.systems-network-administration.patch-management.compromise-assessment-during-emergency-patching
name: compromise-assessment-during-emergency-patching
category: computing-software
field: systems-network-administration
product: patch-management
tags: [compromise-assessment, indicators-of-compromise, threat-hunting, emergency-patching, incident-response]
level: practitioner
status: draft
description: "Check for compromise while emergency patching an exploited flaw: preserve evidence first, run vendor integrity tools, hunt IOCs, and decide when to rebuild instead of patch."
sources:
  - https://www.cisa.gov/news-events/directives
  - https://csrc.nist.gov/pubs/sp/800/61/r3/final
  - https://www.cisa.gov/known-exploited-vulnerabilities-catalog
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Compromise assessment alongside patching

If a vulnerability was exploited before you patched, the patch closes the door with the intruder inside. For any exploited-in-the-wild CVE on an exposed system, assess compromise in parallel.

## Order of operations
1. **Preserve** before changing: memory capture if feasible, VM snapshot (with memory), disk image of appliances where the vendor supports it, export logs (web, VPN, auth) which a reboot or upgrade may wipe.
2. **Run vendor integrity/IOC tools** (e.g. Ivanti Integrity Checker Tool, Citrix/Fortinet/Cisco published scripts, Microsoft Exchange `Test-ProxyLogon.ps1` style tools).
3. **Hunt** for published IOCs: webshells in web roots (recent `.aspx/.jsp/.php` files), new local/admin accounts, unusual scheduled tasks/cron, outbound connections to listed IPs/domains, suspicious processes spawned by web server processes (w3wp.exe -> cmd.exe).
4. **Patch or mitigate**.
5. **Re-check** after patching; some actors deploy persistence that survives upgrades.

## Quick hunts
```powershell
Get-ChildItem "$env:SystemDrive\inetpub","$env:ExchangeInstallPath" -Recurse -Include *.aspx,*.ashx -ErrorAction SilentlyContinue |
  Where-Object LastWriteTime -gt (Get-Date).AddDays(-30)
Get-ScheduledTask | Where-Object Date -gt (Get-Date).AddDays(-30)
```
```sh
find /var/www /opt -type f -newermt '30 days ago' \( -name '*.jsp' -o -name '*.php' \)
last -F | head; awk -F: '$3==0' /etc/passwd
```
EDR: query process trees from the service binary, and the CVE's specific exploitation telemetry if the vendor published detection rules.

## Decide
- No indicators, logs cover the exposure window -> patch, monitor.
- Indicators found or logs missing for the window -> incident response: isolate, rotate credentials/keys/certs reachable from the host, rebuild from known-good media, then patch.

## Gotchas
- Factory reset/upgrade on appliances can destroy evidence; image first if IR might need it.
- Integrity tools miss novel implants; absence of IOCs is not proof of clean.

## Verify
Assessment record per exposed host: evidence collected, tools run with results, decision and approver; IR ticket opened for any positives.
