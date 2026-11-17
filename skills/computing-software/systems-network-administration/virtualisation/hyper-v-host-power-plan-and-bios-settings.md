---
id: computing-software.systems-network-administration.virtualisation.hyper-v-host-power-plan-and-bios-settings
name: hyper-v-host-power-plan-and-bios-settings
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [high-performance-power-plan, hyper-v, power-management, bios, performance-tuning]
level: practitioner
status: docs-checked
description: "Set the Hyper-V host power plan and firmware power settings for consistent VM performance: Balanced versus High Performance, OS-controlled power management, and verification."
sources:
  - https://learn.microsoft.com/en-us/windows-server/administration/performance-tuning/role/hyper-v-server/configuration
  - https://learn.microsoft.com/en-us/windows-server/administration/performance-tuning/hardware/power/power-performance-tuning
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Host power plan and BIOS power settings

**Goal:** VMs get consistent CPU frequency and low latency instead of power-saving behaviour that makes performance
uneven.

## Windows power plan
Windows Server uses and recommends the **Balanced** plan by default, which scales processor performance with CPU
utilisation. On a mostly idle host this can lead to moderate power draw and tenant workloads running more slowly
than they could. Microsoft says to consider the **High Performance** plan when you want maximum performance for
virtualised workloads; it locks processors at the highest performance state (including turbo) and unparks all cores,
at the cost of higher energy use and heat.
Choose the plan in Power Options (or with `powercfg -setactive <scheme GUID>`). After changing plan settings run
`powercfg -setactive`; no reboot is needed.

For ultra-low-latency or repeatable-performance hosts the tuning page also shows raising the minimum processor
state: `powercfg -setacvalueindex scheme_current sub_processor PROCTHROTTLEMIN 100` followed by
`powercfg -setactive scheme_current`.

## Firmware (BIOS/UEFI)
Some server manufacturers provide their own power management options in BIOS settings. If the operating system does
not have control over power management, changing the Windows power plan will not affect system power and
performance: check the vendor's power profile (for example OS controlled versus a fixed performance profile) and the
vendor management controller settings as well.

## Verify
Windows exposes the processor frequency state as a counter: use the **% of maximum frequency** counter in the
**Processor** group in Performance Monitor to see whether frequency caps are applied. For CPU load use the
`Hyper-V Hypervisor Logical Processor(_Total)\% Total Run Time` counter, not Task Manager in the root partition.

## Gotchas
- A firmware update or a vendor tool can change the power profile: include it in post-update checks.
- Measure host CPU with the Hyper-V Hypervisor Logical Processor counters; CPU counters in Task Manager and in
  the root or child partitions do not reflect actual physical CPU usage.

## Checked

Date checked: 2026-10-27. Documentation: Hyper-V server configuration considerations and "Processor power management tuning" pages (windowsserverdocs main branch, Windows Server 2025).
Confirmed: Balanced is the default and recommended plan; High Performance behaviour; vendor BIOS power options can override the OS; PROCTHROTTLEMIN example; % of maximum frequency counter; Hyper-V Hypervisor Logical Processor counters for real CPU use. powercfg -setactive applies changes without a reboot.

Method: documentation only; no commands were run.
