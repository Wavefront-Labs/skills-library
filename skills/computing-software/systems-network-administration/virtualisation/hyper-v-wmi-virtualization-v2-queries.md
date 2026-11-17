---
id: computing-software.systems-network-administration.virtualisation.hyper-v-wmi-virtualization-v2-queries
name: hyper-v-wmi-virtualization-v2-queries
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [virtualization-v2-wmi, wmi, cim, hyper-v, automation]
level: advanced
status: docs-checked
description: "Query and control Hyper-V through the root\virtualization\v2 WMI namespace with CIM: VM state, summary info, guest KVP data and state changes."
sources:
  - https://learn.microsoft.com/en-us/windows/win32/hyperv_v2/msvm-computersystem
  - https://learn.microsoft.com/en-us/windows/win32/hyperv_v2/getsummaryinformation-msvm-virtualsystemmanagementservice
  - https://learn.microsoft.com/en-us/windows/win32/hyperv_v2/msvm-kvpexchangecomponent
  - https://learn.microsoft.com/en-us/windows/win32/hyperv_v2/requeststatechange-msvm-computersystem
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# WMI root\virtualization\v2 queries

**Goal:** read and change Hyper-V state from monitoring tools, remote non-Windows systems or scripts where the Hyper-V PowerShell module is not available.

## VMs and state
```powershell
$ns = 'root\virtualization\v2'
Get-CimInstance -Namespace $ns -ClassName Msvm_ComputerSystem -Filter "Caption='Virtual Machine'" |
  Select ElementName, Name, EnabledState, OnTimeInMilliseconds
```
`EnabledState`: 2 Enabled (running), 3 Disabled (off), 6 Enabled but Offline (saved), 9 Quiesce (paused); in v2 32768 and 32769 mean Creating Snapshot and Applying Snapshot. `Caption` is `Virtual Machine` for VMs and `Hosting Computer System` for the host.

## Summary information (fast, one call)
```powershell
$vsms = Get-CimInstance -Namespace $ns -ClassName Msvm_VirtualSystemManagementService
Invoke-CimMethod -InputObject $vsms -MethodName GetSummaryInformation -Arguments @{RequestedInformation=[uint32[]](1,4,100,101,103,105)}
```
The numbers are ElementName (1), NumberOfProcessors (4), EnabledState (100), ProcessorLoad (101), MemoryUsage (103) and Uptime (105); properties you do not request come back Null.

## Guest data via KVP (IP addresses, OS)
```powershell
$vm = Get-CimInstance -Namespace $ns -ClassName Msvm_ComputerSystem -Filter "ElementName='app01'"
$kvp = Get-CimAssociatedInstance -InputObject $vm -ResultClassName Msvm_KvpExchangeComponent
$kvp.GuestIntrinsicExchangeItems | ForEach-Object {
  $x = [xml]$_; $n = $x.SelectSingleNode("//PROPERTY[@NAME='Name']/VALUE").InnerText
  $d = $x.SelectSingleNode("//PROPERTY[@NAME='Data']/VALUE").InnerText; "$n = $d" }
```
`GuestIntrinsicExchangeItems` holds the key-value pairs the guest operating system has pushed up; it needs the guest side of the key-value exchange service running.

## Change state
```powershell
Invoke-CimMethod -InputObject $vm -MethodName RequestStateChange -Arguments @{RequestedState=[uint16]2}   # start
```
`RequestStateChange` is asynchronous: it returns a job reference and the return value 4096 means the transition started; poll `Msvm_ConcreteJob` for completion.

## Remote access
`New-CimSession -ComputerName hv01` (WinRM) and pass `-CimSession` to the cmdlets above.

## Gotchas
- Some `RequestStateChange` values are valid in Hyper-V version 1 only; use the v2 namespace and its values.

## Checked

Checked 2026-10-26 against MicrosoftDocs/win32 Hyper-V WMI v2 pages (`Msvm_ComputerSystem` EnabledState and Caption values, `GetSummaryInformation` RequestedInformation numbers, `Msvm_KvpExchangeComponent.GuestIntrinsicExchangeItems`, `RequestStateChange` return code 4096). Corrected: the v1 explanatory note (in v2, 32768 and 32769 are snapshot states). Removed as undocumented: the "namespace gone since 2012 R2" statement, pywinrm and DCOM remarks and the required-rights claim. The `OnTimeInMilliseconds` property is documented on `Msvm_ComputerSystem`.

Method: documentation only; no commands were run.
