---
id: computing-software.systems-network-administration.windows-server.hyper-v-powershell-direct-and-enhanced-session
name: hyper-v-powershell-direct-and-enhanced-session
category: computing-software
field: systems-network-administration
product: windows-server
tags: [windows-server, hyper-v-host, hyper-v-vm, powershell-direct, enhanced-session-mode, invoke-command-vmname]
level: practitioner
status: docs-checked
description: "Manage Hyper-V guests without network access using PowerShell Direct (-VMName, -VMId, sessions, file copy) and enhanced session mode in VMConnect."
sources:
  - https://learn.microsoft.com/en-us/virtualization/hyper-v-on-windows/user-guide/powershell-direct
  - https://learn.microsoft.com/en-us/windows-server/virtualization/hyper-v/learn-more/use-local-resources-on-hyper-v-virtual-machine-with-vmconnect
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# PowerShell Direct and enhanced session mode

## PowerShell Direct
Runs commands in a Windows guest from the Hyper-V host, with no network,
firewall or remoting configuration. Requires: host and guest Windows 10/Server 2016+, VM
running on **this** host, credentials **for the guest** (local or domain).
```powershell
$cred = Get-Credential '.\Administrator'
Invoke-Command -VMName app01 -Credential $cred -ScriptBlock { Get-NetIPAddress; hostname }
Enter-PSSession -VMName app01 -Credential $cred
$s = New-PSSession -VMName app01 -Credential $cred
Copy-Item .\setup.ps1 -ToSession $s -Destination '<GUEST_DIR>\'    # file copy over the same session
```
Typical uses: set the IP on a freshly deployed VM, rejoin a domain after a broken secure
channel, fix a firewall rule that locked you out. `-VMId` works when names are duplicated.

## Enhanced session mode
Enhanced session mode lets VMConnect use the local computer's resources in the VM (for example a USB flash drive or
a printer) and lets you resize the VMConnect window. See the cited VMConnect page for host and guest setup.

## Linux guests
PowerShell Direct targets Windows 10 or newer and Windows Server 2016 or newer guests; use SSH for Linux guests.

## Verify
- [ ] `Invoke-Command -VMName` works with the guest NIC disconnected.
- [ ] Enhanced session mode exposes local resources (for example a USB drive) in VMConnect.

## Checked

2026-10-28. Confirmed against: powershell-direct page (Windows 10 / Server 2016 guest requirement, -VMName and -VMId, Enter-PSSession, Invoke-Command, Copy-Item -ToSession) and the VMConnect local-resources page. Removed (not confirmable from the cited pages): Copy-VMFile / Guest Service Interface section, hvc ssh, Set-VMHost and Set-VM enhanced-session cmdlets, VMBus, RDP service requirements.

Method: documentation only; no commands were run.
