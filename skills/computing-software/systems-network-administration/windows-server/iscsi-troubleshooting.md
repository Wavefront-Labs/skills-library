---
id: computing-software.systems-network-administration.windows-server.iscsi-troubleshooting
name: iscsi-troubleshooting
category: computing-software
field: systems-network-administration
product: windows-server
tags: [iscsi, iscsi-troubleshooting, iscsi-initiator, mpio, event-logs]
level: practitioner
status: docs-checked
description: "Troubleshoot iSCSI on Windows: session drops, iScsiPrt events 9, 20, 39, 129, login failures, slow boots waiting for disks and MPIO path loss."
sources:
  - https://learn.microsoft.com/en-us/powershell/module/iscsi/get-iscsisession
  - https://learn.microsoft.com/en-us/powershell/module/iscsi/
  - https://learn.microsoft.com/en-us/powershell/module/mpio/set-mpiosetting
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# iSCSI troubleshooting

## State
```powershell
Get-IscsiSession | Select TargetNodeAddress,InitiatorPortalAddress,IsConnected,IsPersistent,NumberOfConnections
Get-IscsiConnection
Get-IscsiTarget | Select NodeAddress,IsConnected
```
For MPIO path counts use the MPIO tooling you have (the `mpclaim` utility or the MPIO properties dialog); `mpclaim` is not covered in the current Microsoft Learn reference.

## What to check by symptom
| Symptom | Look at |
|---|---|
| Initiator cannot connect | target IP and portal port, firewall, target initiator ids (IQN allowed) |
| Login fails | CHAP secrets and usernames on both sides, mutual CHAP configuration |
| Connection drops | NIC and switch flaps, target failover or reboot, storage latency on the array |
| Disk missing after reboot | session not persistent (`-IsPersistent $true`) |

Read the System log entries from the iSCSI initiator source for exact event ids on your build; the event id list is not given in Microsoft's cmdlet references.

## Persistent and boot issues
- Services that depend on iSCSI volumes must start after the disks arrive; the iSCSI initiator's Volumes and Devices tab handles volume binding.
- Favorites (persistent targets) missing after reboot: connect with `-IsPersistent $true`.

## Timeouts
Storage vendors often specify initiator timeout values; follow the array's guide. With MPIO, `Get-MPIOSetting` and `Set-MPIOSetting` (`-NewPDORemovePeriod`, `-NewDiskTimeout`, `-NewRetryCount`, `-NewRetryInterval`) control path and disk timers; changes may prompt for a restart.

## Network checks
A do-not-fragment ping at your jumbo size; `Get-NetAdapterStatistics` discards; switch port errors.

## Verify
- [ ] Sessions persistent on all paths; no new iSCSI or disk reset errors in the System log after a failover test (pull one cable).

## Checked
Release checked: windowsserverdocs and windows-powershell-docs (Windows Server 2025 docset), GitHub main as of 2026-10-23.
- Get-IscsiSession / Get-IscsiConnection / Get-IscsiTarget reference pages; Set-MPIOSetting parameters (-NewPDORemovePeriod, -NewDiskTimeout, -NewRetryCount, -NewRetryInterval, -NewPathVerificationPeriod; restart may be required).
- Wrong claim fixed: `Set-IscsiBoundVolume` does not exist in the iSCSI module (the module lists Connect, Disconnect, Get, New, Register, Remove, Set-IscsiChapSecret, Unregister and Update cmdlets only).
- Removed unconfirmed details: the iScsiPrt event-id table, the registry timeout names and defaults (MaxRequestHoldTime 60 s, LinkDownTime 15 s), the mpclaim command, and the exact jumbo ping size.

Method: documentation only; no commands were run.
