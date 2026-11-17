---
id: computing-software.systems-network-administration.virtualisation.hyper-v-automatic-start-stop-actions
name: hyper-v-automatic-start-stop-actions
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [automatic-start-action, automatic-stop-action, hyper-v-vm, startup-order, hyper-v]
level: practitioner
status: docs-checked
description: "Set Hyper-V automatic start and stop actions with delays for standalone hosts, avoid the Save action disk reservation, and know why clusters ignore these settings."
sources:
  - https://learn.microsoft.com/en-us/powershell/module/hyper-v/set-vm
  - https://learn.microsoft.com/en-us/windows-server/virtualization/hyper-v/manage/integration-services
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Automatic start and stop actions

## Settings
```powershell
Set-VM -Name dc01  -AutomaticStartAction Start          -AutomaticStartDelay 0
Set-VM -Name sql01 -AutomaticStartAction StartIfRunning -AutomaticStartDelay 120
Set-VM -Name app01 -AutomaticStartAction StartIfRunning -AutomaticStartDelay 240
Set-VM -Name lab01 -AutomaticStartAction Nothing
Get-VM | Set-VM -AutomaticStopAction ShutDown
Get-VM | Select Name, AutomaticStartAction, AutomaticStartDelay, AutomaticStopAction
```
`-AutomaticStartDelay` is a number of seconds. Check the values currently set before changing a fleet.

| Start action | Meaning |
|---|---|
| Nothing | VM stays off when the host starts |
| StartIfRunning | starts if it was running when the host went down |
| Start | always starts |

| Stop action | Meaning at host shutdown |
|---|---|
| Save | saves the VM state |
| TurnOff | power cut |
| ShutDown | guest OS shutdown through the integration services |

## Recommendations
- Use **ShutDown** for servers so the guest stops cleanly. It needs the Hyper-V Guest Shutdown service (`vmicshutdown`) in the guest: when the service is disabled the host can only force a power-off, which can cause data loss.
- Stagger start delays so infrastructure (DNS, AD, DB) starts first and storage is not hit by a boot storm.
- The host's shutdown waits for guests: give the host enough time in UPS shutdown scripts.

## Clusters
For clustered VMs, check how the failover cluster starts roles before relying on these per-VM settings; for ordered start in a cluster use cluster group sets (see the VM groups skill).

## Verify
Reboot the host in a window: VMs start in the intended order and with the intended delays.

## Checked
2026-10-26, Windows Server 2025 documentation (MicrosoftDocs windowsserverdocs and windows-powershell-docs, current as of 2026-10-23). Confirmed in the Set-VM reference: -AutomaticStartAction accepts Nothing, StartIfRunning and Start; -AutomaticStopAction accepts TurnOff, Save and ShutDown; -AutomaticStartDelay is in seconds. Confirmed in the integration services page that without the guest shutdown service the host can only force a power-off. Removed as unconfirmed: which action is the default, the claim that changing the stop action needs the VM off, the RAM-sized placeholder file and Kerberos remarks, the cluster priority numbers and the statement that clustered VMs ignore the start action.

Method: documentation only; no commands were run.
