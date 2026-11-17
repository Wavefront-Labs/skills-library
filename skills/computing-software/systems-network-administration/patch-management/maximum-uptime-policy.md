---
id: computing-software.systems-network-administration.patch-management.maximum-uptime-policy
name: maximum-uptime-policy
category: computing-software
field: systems-network-administration
product: patch-management
tags: [max-uptime-policy, uptime, reboot-compliance, patch-reboots, patch-management]
level: practitioner
status: docs-checked
description: "Enforce a maximum uptime policy so patched-but-not-rebooted systems get caught: thresholds, querying uptime on Windows and Linux, reporting and forced-reboot escalation."
sources:
  - https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-update
  - https://man7.org/linux/man-pages/man1/uptime.1.html
  - https://man7.org/linux/man-pages/man5/proc_uptime.5.html
  - https://learn.microsoft.com/en-us/windows/win32/cimwin32prov/win32-operatingsystem
  - https://learn.microsoft.com/en-us/powershell/module/cimcmdlets/get-ciminstance
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Maximum uptime policy

Installed but pending updates protect nothing. A max-uptime rule catches hosts that never reboot, regardless of what the patch tool thinks.

## Policy example (thresholds are your own policy, not vendor figures)
- Workstations: max 14 days uptime; warning at 10, forced reboot outside active hours at 14.
- Servers: max 35 days (one cycle plus buffer); exceptions only via an approved list (for example clustered legacy apps with their own schedule).
- Uptime is counted from last boot, not last logon. On Linux, `/proc/uptime` includes time spent in suspend, so a suspended host is not "recently rebooted".

## Query
```powershell
Get-CimInstance Win32_OperatingSystem -ComputerName (Get-Content servers.txt) |
  Select-Object PSComputerName, LastBootUpTime,
    @{n='UptimeDays';e={[int]((Get-Date) - $_.LastBootUpTime).TotalDays}} |
  Where-Object UptimeDays -gt 35
```
`LastBootUpTime` is a property of the `Win32_OperatingSystem` class and `Get-CimInstance` accepts `-ComputerName`.
```sh
uptime -s          # boot time, yyyy-mm-dd HH:MM:SS
cat /proc/uptime   # two numbers in seconds: uptime and idle time
```
Report the same value from whatever endpoint-management or monitoring tool you use.

## Enforce
- Windows Update deadlines with a grace period handle patch-driven restarts: policy CSP `Update/ConfigureDeadlineGracePeriod` is the minimum number of days from update installation until restarts occur automatically for quality updates. It takes effect only when `Update/ConfigureDeadlineForQualityUpdates` is configured; if the deadline is configured but the grace period is not, the default is 2 days.
- For uptime alone, use your own remediation: a scheduled restart with notification when uptime exceeds the threshold; servers get a ticket to the owner, then a reboot in the next window after N days.

## Gotchas
- Uptime alone does not prove patches applied; pair it with pending-reboot detection.
- `uptime -c` (or the `PROCPS_CONTAINER` variable) shows container uptime instead of system uptime, so check which one your tooling reports.

## Verify
Weekly report of hosts over threshold trending to zero; exceptions list reviewed monthly.

## Checked
Date: 2026-11-07. Read: uptime(1) in full (`-s`, `-c`, `PROCPS_CONTAINER`), proc_uptime(5) in full (two numbers, seconds, includes suspend), Win32_OperatingSystem (`LastBootUpTime` member; searched, not read end to end), Get-CimInstance (`-ComputerName` in syntax; searched), policy CSP Update (read the `ConfigureDeadlineForQualityUpdates` and `ConfigureDeadlineGracePeriod` entries including the 2-day default; searched in a 150k-character page, not read end to end). Removed as unconfirmed: Fast Startup claims (`powercfg /h off`, "Require use of fast startup" GPO), the Ansible `ansible_uptime_seconds` fact, Intune Endpoint Analytics and ConfigMgr `v_GS_OPERATING_SYSTEM` references, live-patch reboot claim, "VMs keep uptime" and "containers report host uptime" (uptime(1) documents `-c` to show container uptime, so the blanket statement was not safe).
Method: documentation only; no commands were run.
