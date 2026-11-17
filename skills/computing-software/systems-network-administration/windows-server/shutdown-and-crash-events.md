---
id: computing-software.systems-network-administration.windows-server.shutdown-and-crash-events
name: shutdown-and-crash-events
category: computing-software
field: systems-network-administration
product: windows-server
tags: [event-logs, event-1074, unexpected-shutdown, event-41, bugcheck]
level: practitioner
status: docs-checked
description: "Work out why a server restarted: events 1074 (who/what initiated), 6006/6005, 6008 unexpected shutdown, Kernel-Power 41 and BugCheck 1001."
sources:
  - https://learn.microsoft.com/en-us/troubleshoot/windows-client/performance/event-id-41-restart
  - https://learn.microsoft.com/en-us/troubleshoot/windows-server/performance/troubleshoot-unexpected-reboots-system-event-logs
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Shutdown and crash events

## The timeline query
```powershell
Get-WinEvent -FilterHashtable @{LogName='System';Id=1074,6006,6008,41,6009} -MaxEvents 50 |
  Select TimeCreated,Id,ProviderName,@{n='Msg';e={$_.Message.Split("`n")[0]}} | Format-Table -Wrap
```

## Event meanings
| ID | Meaning |
|---|---|
| 1074 | an application is responsible for a shutdown or restart |
| 6006 | the event log service stopped: Windows was shut down cleanly |
| 6008 | the previous shutdown was unexpected |
| 41 | Kernel-Power: the system rebooted without cleanly shutting down first |
| 6009 | logged at boot with OS version information |

## Reading
Event 41 data includes a BugcheckCode; review events 13, 41, 1074, 6008 and 6009 together to classify the reboot type (see the unexpected-reboot troubleshooting page).

## Hypervisor-initiated
A Hyper-V host can restart a clustered VM through the Hyper-V heartbeat feature when it stops receiving heartbeats.

## Verify
- [ ] Root cause recorded (who/what/why) for each unplanned reboot.

## Checked
2026-10-28: Confirmed on Learn pages event-id-41-restart and troubleshoot-unexpected-reboots-system-event-logs: events 1074, 6006, 6008, 41 (Kernel-Power), 6009, BugcheckCode in event 41, and the Hyper-V heartbeat restart. Removed: events 1076, 6005 and 1001 meanings, source names for 1074/6006, example process names, bugcheck-zero interpretation, vmicshutdown clean-shutdown claim.
Method: documentation only; no commands were run.
