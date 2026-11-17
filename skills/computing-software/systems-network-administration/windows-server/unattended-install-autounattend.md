---
id: computing-software.systems-network-administration.windows-server.unattended-install-autounattend
name: unattended-install-autounattend
category: computing-software
field: systems-network-administration
product: windows-server
tags: [windows-server, windows-server-installation, autounattend, unattended-install, unattend-xml, windows-system-image-manager, setupcomplete, sysprep, image-index, product-key]
level: practitioner
status: draft
description: "Fully unattended Windows Server installs: autounattend.xml passes (windowsPE, specialize, oobeSystem), image index selection, disk layout, SetupComplete and secrets handling."
sources:
  - https://learn.microsoft.com/en-us/windows-hardware/customize/desktop/unattend/
  - https://learn.microsoft.com/en-us/windows-hardware/manufacture/desktop/add-a-custom-script-to-windows-setup
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Unattended Windows Server install (autounattend.xml)

Place `autounattend.xml` at the root of the install media (USB/ISO) or a secondary virtual
CD; Setup picks it up automatically. Author it with **Windows System Image Manager** (WSIM,
from the Windows ADK) against the matching `install.wim` so element names validate.

## Passes that matter
| Pass | Typical components |
|---|---|
| windowsPE | `Microsoft-Windows-International-Core-WinPE` (language), `Microsoft-Windows-Setup`: DiskConfiguration, ImageInstall/OSImage/InstallFrom (`/IMAGE/INDEX` or `/IMAGE/NAME`), UserData (EULA accept, product key) |
| specialize | `Microsoft-Windows-Shell-Setup` (ComputerName, TimeZone), `Microsoft-Windows-TCPIP`/`DNS-Client` (static IP), `Microsoft-Windows-UnattendedJoin` (domain join) |
| oobeSystem | `Microsoft-Windows-Shell-Setup`: UserAccounts/AdministratorPassword, OOBE (HideEULAPage etc.), AutoLogon (count 1) + FirstLogonCommands |

Image selection: list indexes first
```powershell
Get-WindowsImage -ImagePath <MEDIA>\sources\install.wim | Select ImageIndex,ImageName
```
Index names: "Windows Server 2025 Standard" (Core) vs "... Standard (Desktop Experience)".

## Disk layout (UEFI)
EFI 100-260 MB FAT32, MSR 16 MB, Windows (rest) NTFS; optionally a WinRE partition at the end.
In windowsPE `DiskConfiguration` with `WillWipeDisk=true` on Disk 0, then
`InstallTo DiskID=0 PartitionID=3`.

## Post-install scripts
`%WINDIR%\Setup\Scripts\SetupComplete.cmd` runs as SYSTEM after setup, before first logon;
good for enabling remoting, installing agents, applying a DSC config. Put it on the media via
`$OEM$\$$\Setup\Scripts\` or inject into the image.

## Secrets
Passwords in unattend are only base64-obscured (`PlainText=false`), not encrypted. Use a
throwaway initial password rotated by LAPS after domain join, and delete
`%WINDIR%\Panther\unattend.xml` copies post-setup (Setup removes some, not all).

## Verify
- [ ] VM boots from media and reaches the logon screen with no prompts.
- [ ] `%WINDIR%\Panther\setupact.log` shows the answer file was used; no secret copies remain.
