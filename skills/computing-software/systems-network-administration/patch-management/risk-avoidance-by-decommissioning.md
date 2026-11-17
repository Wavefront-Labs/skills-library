---
id: computing-software.systems-network-administration.patch-management.risk-avoidance-by-decommissioning
name: risk-avoidance-by-decommissioning
category: computing-software
field: systems-network-administration
product: patch-management
tags: [risk-avoidance, decommission, attack-surface-reduction, patch-risk-responses, asset-retirement, patch-management]
level: practitioner
status: draft
description: "Avoid vulnerability risk by removing software or decommissioning hosts: confirm no dependencies, scream test, retire cleanly from AD/DNS/CMDB/scanner, and close findings."
sources:
  - https://csrc.nist.gov/pubs/sp/800/39/final
  - https://csrc.nist.gov/pubs/sp/800/88/r1/final
  - https://csrc.nist.gov/pubs/sp/800/40/r4/final
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Risk avoidance by removal or decommission

The cheapest patch is uninstalling the thing. Use when software is unused, duplicated, or the host serves nothing that matters.

## Candidates
- Apps with no launches in 90 days (software metering, EDR process telemetry, `Get-WinEvent` app logs).
- Runtimes left behind by uninstalled apps (old Java, .NET Core runtimes, Python 2, Flash remnants).
- Servers with no inbound connections for 30+ days (NetFlow, firewall logs, `ss -tn` sampling).
- Features/roles enabled but unused (IIS on file servers, SMBv1, Telnet client).

## Confirm no dependency
```powershell
# Windows: who connects to this box
Get-NetTCPConnection -State Established | Group-Object RemoteAddress | Sort-Object Count -desc
```
```sh
ss -tnp state established
```
Check CMDB relationships, scheduled tasks/cron on other hosts referencing the name, DNS query logs for the hostname.

## Scream test
1. Announce with date. 2. Stop services / shut down VM (do not delete) for 2-4 weeks. 3. Watch for tickets. 4. Proceed or restore.

## Clean retirement
- Uninstall via the deployment tool so it does not get reinstalled (remove from baselines and app assignments).
- For hosts: disable then delete AD computer object, remove DNS records, DHCP reservations, monitoring, backup jobs, scanner assets, licences, CMDB status Retired.
- Sanitise or destroy disks per NIST SP 800-88.
- Close vulnerability findings by asset removal in the scanner (purge, not just stop scanning).

## Gotchas
- Month-end/quarter-end/year-end jobs: a 2-week scream test can miss them; check job schedules.
- Shared libraries: removing a runtime other apps load breaks them silently.
- Firewall rules and service accounts linger; remove them too.

## Verify
Software absent on rescan, findings closed by removal, no reinstall after next deployment cycle, and change record closed with the retirement checklist.
