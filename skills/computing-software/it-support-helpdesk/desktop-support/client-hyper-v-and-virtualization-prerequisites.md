---
id: computing-software.it-support-helpdesk.desktop-support.client-hyper-v-and-virtualization-prerequisites
name: client-hyper-v-and-virtualization-prerequisites
category: computing-software
field: it-support-helpdesk
product: desktop-support
tags: [it-support-helpdesk, desktop-support, virtualization, client-virtualization, client-hyper-v, vt-x, amd-v, slat, virtualization-based-security, hypervisorlaunchtype, virtualbox-conflict, comptia-a-plus, memory-integrity]
level: practitioner
status: docs-checked
description: "Enable client Hyper-V and other hypervisors on Windows: firmware VT-x/AMD-V, edition and RAM requirements, Hyper-V vs VirtualBox/VMware coexistence, and VBS side effects."
sources:
  - "https://learn.microsoft.com/en-us/windows-server/virtualization/hyper-v/get-started/Install-Hyper-V"
  - "https://learn.microsoft.com/en-us/windows-server/virtualization/hyper-v/host-hardware-requirements"
  - "https://learn.microsoft.com/en-us/windows-hardware/drivers/devtest/bcdedit--set"
licence: Apache-2.0
version: 4
updated: 2026-11-17
---
# client-hyper-v-and-virtualization-prerequisites

Goal: a developer or tester gets working local VMs without breaking the
security features or other hypervisors on the machine.

## Requirements check
```powershell
systeminfo | findstr /i "Hyper-V"
Get-CimInstance Win32_Processor | Select VirtualizationFirmwareEnabled, SecondLevelAddressTranslationExtensions
```
Microsoft's requirements for Hyper-V on Windows:
- Windows 10 or 11 **Pro or Enterprise**; the Hyper-V role cannot be installed
  on Windows 10 or 11 Home.
- A 64-bit processor with second-level address translation (SLAT) and VM
  Monitor Mode extensions, virtualization enabled in firmware.
- Hardware-enforced DEP available and enabled (Intel XD bit, AMD NX bit).
- At least 4 GB of RAM; more is better, since it must cover the host and all
  running VMs.
- If Control Panel shows "Windows Hypervisor Platform" instead of Hyper-V,
  the system may not be compatible.

## Enable
```powershell
Enable-WindowsOptionalFeature -Online -FeatureName Microsoft-Hyper-V -All
# or: DISM /Online /Enable-Feature /All /FeatureName:Microsoft-Hyper-V
```
Reboot. Tools: Hyper-V Manager and the Hyper-V PowerShell cmdlets.

## Coexistence with other hypervisors
To switch the Windows hypervisor off temporarily (anything that depends on
it stops working until you switch it back):
```cmd
bcdedit /set hypervisorlaunchtype off     :: reboot; 'auto' to restore
```
`hypervisorlaunchtype` accepts Off or Auto. Do not turn off security
features such as Memory Integrity or Credential Guard on managed devices
to satisfy a hypervisor; that is a security exception that needs approval.
For third-party hypervisor support on top of Windows, check the vendor's
current documentation.

## Gotchas
- Firmware updates or resets can disable virtualization settings.
- Nested virtualization (a VM inside a VM) needs the host VM's processor to
  expose the extensions: `Set-VMProcessor -VMName <VMName> -ExposeVirtualizationExtensions $true`.

## Verify
`Get-VM` lists your VMs and a test VM boots.


## Checked

Date 2026-10-27. Documentation release: Microsoft Learn Hyper-V enable and host hardware requirement pages, bcdedit /set reference, Windows Sandbox install page, as published October 2026. Confirmed: Pro/Enterprise only and no Home, SLAT, VM Monitor Mode extensions, DEP, 4 GB RAM minimum, the Windows Hypervisor Platform note, Enable-WindowsOptionalFeature and DISM commands, hypervisorlaunchtype Off/Auto, ExposeVirtualizationExtensions. Removed: Education edition, 16 GB advice, Task Manager check, Default Switch NAT and Quick Create notes, VMware 15.5.5 and VirtualBox 6 versions, Dynamic Memory and VHDX advice, licensing remarks, exam reference.

Method: documentation only; no commands were run.
