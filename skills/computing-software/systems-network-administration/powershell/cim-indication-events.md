---
id: computing-software.systems-network-administration.powershell.cim-indication-events
name: cim-indication-events
category: computing-software
field: systems-network-administration
product: powershell
tags: [powershell, cim, register-cimindicationevent, wmi-events, event-subscription]
level: advanced
status: docs-checked
description: "Subscribe to WMI/CIM events with Register-CimIndicationEvent: class and query subscriptions, -Action, remote sessions, cleanup and permanent subscriptions."
sources:
  - https://learn.microsoft.com/en-us/powershell/module/cimcmdlets/register-cimindicationevent
  - https://learn.microsoft.com/en-us/windows/win32/wmisdk/receiving-a-wmi-event
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# CIM indication events

## Event types
A change in the standard WMI data model (for example `__InstanceCreationEvent`) is an intrinsic event; a change a
provider defines (registry, power management, Win32 provider events) is an extrinsic event.

## Subscribe by class
```powershell
Register-CimIndicationEvent -ClassName Win32_ProcessStartTrace -SourceIdentifier ProcessStarted
Get-Event -SourceIdentifier ProcessStarted
```
`Win32_ProcessStartTrace` raises an event whenever a process starts. The Learn example requires PowerShell run as
Administrator. `-SourceIdentifier` names the subscription.

## Subscribe by query, with an action
```powershell
$query = "SELECT * FROM CIM_InstModification WHERE TargetInstance ISA 'Win32_LocalTime'"
Register-CimIndicationEvent -Query $query -SourceIdentifier Timer
```
Add `-Action <scriptblock>` to react to each event; inside it the received event is in the `$Event` variable.

## Remote
The cmdlet takes `-ComputerName` or `-CimSession`, and `-Namespace` to pick the WMI namespace.

## Cleanup
```powershell
Get-EventSubscriber | Unregister-Event
```

## Permanent subscriptions
WMI can also run permanent event consumers using its standard consumer classes without provider code. Microsoft
recommends compiling permanent event subscriptions into the `root\subscription` namespace. Audit that namespace for
unexpected bindings, for example
`Get-CimInstance -Namespace root\subscription -ClassName __FilterToConsumerBinding`.

## Verify
- [ ] Subscription fires on a test event; unregistered at script end; no unexpected permanent bindings exist.

## Checked
2026-11-09. Read the Register-CimIndicationEvent reference and the WMI "Receiving a WMI event" page. Confirmed:
class and query parameter sets, SourceIdentifier, Action and `$Event`, ComputerName/CimSession/Namespace,
Win32_ProcessStartTrace, the Administrator note, intrinsic/extrinsic definitions, standard consumers, and the
root\subscription recommendation. Removed as unconfirmed: WITHIN polling guidance and CPU cost, Win32_ProcessStopTrace,
event property names, job cleanup, the persistence-attacker remark, CommandLineEventConsumer.
Method: documentation only; no commands were run.
