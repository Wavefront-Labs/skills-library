---
id: computing-software.systems-network-administration.virtualisation.hyper-v-event-logs-and-vmms-troubleshooting
name: hyper-v-event-logs-and-vmms-troubleshooting
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [hyper-v, vmms, hyper-v-event-logs, vmwp, troubleshooting, stuck-vm, windows-server]
level: advanced
status: docs-checked
description: "Troubleshoot Hyper-V with its event logs: finding the VMMS-Admin and related logs, hard power-off of a stuck VM, and fixing VM permission and low-memory start errors."
sources:
  - https://learn.microsoft.com/en-us/troubleshoot/windows-server/virtualization/error-not-enough-memory-system-start-virtual-machine
  - https://learn.microsoft.com/en-us/troubleshoot/windows-server/virtualization/hyper-v-installation-configuration-operational-failure
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Hyper-V event logs and VMMS troubleshooting

## Where to look
List the Hyper-V logs present on the host rather than assuming names:
```powershell
Get-WinEvent -ListLog *Hyper-V* | Where-Object RecordCount | Select-Object LogName, RecordCount
Get-WinEvent -LogName 'Microsoft-Windows-Hyper-V-VMMS-Admin' -MaxEvents 50
```
`Microsoft-Windows-Hyper-V-VMMS-Admin` is the Virtual Machine Management service log; it records VM start failures
such as insufficient memory. Open the other `Microsoft-Windows-Hyper-V-*` logs that `-ListLog` returns for worker
process, hypervisor and high-availability events, and read the Admin channel first.

## Hard power-off of a stuck VM
```powershell
Stop-VM -Name app01 -TurnOff
```
This is the equivalent of pulling the power; use it only after a normal shutdown fails.

## Common start failures
- **Access denied (0x80070005)**: the VM cannot read its files. Microsoft's guidance is full access for
  Administrators, Hyper-V Administrators and `NT VIRTUAL MACHINE\Virtual Machines` on VM folders and VHDs, for
  example after files were copied manually.
- **Not enough memory**: the VMMS-Admin log records the failure; compare the VM's startup memory with the host's
  available memory (the `Hyper-V Dynamic Memory Balancer\Available Memory` counter depends on what the host and
  `vmwp.exe` processes use).
- Frequent SPN registration failures appear as Event ID 14050 from `Microsoft-Windows-Hyper-V-VMMS`.

## Verify
After the fix, the VM starts and the VMMS-Admin log shows no new errors for it.

## Checked

Date checked: 2026-10-27. Documentation: Microsoft Support articles "Not enough memory in the system to start the virtual machine" and "Hyper-V installation, configuration and operational failures" (SupportArticles-docs, 2026).
Confirmed: VMMS-Admin log name and its use for start failures; Event ID 14050 for SPN registration failures; recommended permissions for NT VIRTUAL MACHINE\Virtual Machines; memory-start-failure guidance. Other log names are left to Get-WinEvent -ListLog because the documentation pages read do not enumerate them.

Method: documentation only; no commands were run.
