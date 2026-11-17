---
id: computing-software.systems-network-administration.virtualisation.hyper-v-hypervisor-scheduler-types
name: hyper-v-hypervisor-scheduler-types
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [hyper-v, hypervisor-scheduler, core-scheduler, classic-scheduler, root-scheduler, smt, hwthreadcountpercore, bcdedit, windows-server]
level: advanced
status: docs-checked
description: "Choose and set the Hyper-V hypervisor scheduler (classic, core, root) with bcdedit, confirm it from the event log, and set guest SMT with HwThreadCountPerCore."
sources:
  - https://learn.microsoft.com/en-us/windows-server/virtualization/hyper-v/manage/manage-hyper-v-scheduler-types
  - https://learn.microsoft.com/en-us/windows-server/virtualization/hyper-v/manage/about-hyper-v-scheduler-type-selection
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Hyper-V hypervisor scheduler types

**Goal:** run the scheduler that matches your security and density needs, and know which one is active.

## The three schedulers
| Scheduler | Behaviour | Default on |
|---|---|---|
| Classic | Fair-share, preemptive, round-robin for guest virtual processors | Versions earlier than Windows Server 2019 |
| Core | Guest virtual processors run only on physical core pairs; a core is never shared between VMs (side-channel isolation) | Windows Server 2019 and later (optional on 2016) |
| Root | The root partition OS schedules the work with the NT scheduler | Windows client systems only; not supported for Hyper-V on Windows Server |

The core scheduler reduces exposure to side-channel attacks from guest VMs and can reduce performance, for example when only one virtual processor of a core pair can run. If host SMT is disabled or absent, Hyper-V uses classic scheduler behaviour whatever the setting.

## Check the active scheduler
```powershell
Get-WinEvent -FilterHashtable @{ProviderName='Microsoft-Windows-Hyper-V-Hypervisor'; Id=2} -MaxEvents 1 |
  Select-Object TimeCreated, Message
# "Hypervisor scheduler type is 0x3"  -> 1 classic (SMT off), 2 classic, 3 core, 4 root
```

## Change it (reboot required)
```powershell
bcdedit /set hypervisorschedulertype core     # or classic / root
Restart-Computer
```

## Guest SMT topology
With the core scheduler, expose SMT to guests so they can use sibling threads:
```powershell
Get-VMProcessor -VMName app01 | Select-Object Count, HwThreadCountPerCore
Set-VMProcessor -VMName app01 -HwThreadCountPerCore 0   # 0 = use the host's SMT thread count per core
```
In Windows Server 2019 and later, new VMs inherit the host SMT topology by default; in Windows Server 2016 guest SMT is not configured by default and `0` is not supported. Use `-HwThreadCountPerCore <n>` to set a specific number of threads per core.

## Gotchas
- Do not configure the root scheduler on Windows Server; and do not override the default scheduler on Windows client systems.
- Review the scheduler selection guidance before overriding the default.

## Verify
Event ID 2 reports the expected type after reboot, and `Get-VMProcessor` shows the intended `HwThreadCountPerCore` on SMT-aware guests.

## Checked
2026-10-26, Windows Server 2025 documentation (MicrosoftDocs windowsserverdocs and windows-powershell-docs, current as of 2026-10-23). Confirmed: three scheduler types and their defaults, bcdedit /set hypervisorschedulertype Classic, Core or Root with a restart, Event ID 2 values 1 to 4 from Microsoft-Windows-Hyper-V-Hypervisor, the Get-WinEvent query, HwThreadCountPerCore 0 behaviour and Windows Server 2016 differences, root scheduler unsupported on Windows Server. Removed as unconfirmed: named side-channel vulnerabilities, mixed-scheduler cluster claim, even vCPU count advice and the firmware SMT remark.

Method: documentation only; no commands were run.
