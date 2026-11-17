---
id: computing-software.systems-network-administration.virtualisation.hyper-v-vmconnect-and-enhanced-session
name: hyper-v-vmconnect-and-enhanced-session
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [vmconnect, enhanced-session-mode, hyper-v, vm-console]
level: intro
status: docs-checked
description: "Use VMConnect to reach Hyper-V VM consoles: launching it, enhanced session mode for Windows and Linux, required ports and permissions, and Grant-VMConnectAccess."
sources:
  - https://learn.microsoft.com/en-us/windows-server/virtualization/hyper-v/enhanced-session-mode
  - https://learn.microsoft.com/en-us/powershell/module/hyper-v/set-vmhost
  - https://learn.microsoft.com/en-us/powershell/module/hyper-v/grant-vmconnectaccess
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# VMConnect console access

**Goal:** console access to VMs for installs, recovery and troubleshooting, with clipboard and drive redirection when useful.

## Launch
- Hyper-V Manager -> *Connect*, or directly: `vmconnect.exe hv01 app01`.

## Basic vs enhanced session
- **Basic**: video and keyboard/mouse only.
- **Enhanced session mode**: connects with RDP, giving a shared clipboard, audio playback, drive and USB redirection and smart cards.
```powershell
Set-VMHost -EnableEnhancedSessionMode $true           # whether users can use enhanced mode on this server
```
The VM needs Remote Desktop turned on in the guest. Windows 10 (version 2004 and later) and Windows 11 guests also need the "require Windows Hello sign-in" option off for the VMConnect sign-in prompt to appear. By default enhanced mode shares the clipboard and audio playback; other devices are chosen under Show Options > Local Resources.

## Ports and permissions
- `Grant-VMConnectAccess` grants a user permission to connect to a VM's console:
```powershell
Grant-VMConnectAccess -VMName app01 -UserName 'CONTOSO\helpdesk1'
Get-VMConnectAccess -VMName app01
Revoke-VMConnectAccess -VMName app01 -UserName 'CONTOSO\helpdesk1'
```

## Gotchas
- Shielded VMs: console connections are enabled only on hosts from Windows Server version 1803 (see the shielded VM comparison).

## Verify
`vmconnect hv01 app01` opens; with enhanced session enabled, the resolution prompt and clipboard work.

## Checked

Checked 2026-10-26 against MicrosoftDocs/windowsserverdocs (Enhanced Session Mode page, latest commit 2026-10-23) and the Windows Server 2025 `Set-VMHost -EnableEnhancedSessionMode` and `Grant-VMConnectAccess` references. Confirmed: enhanced mode uses RDP, needs Remote Desktop enabled in the guest, default clipboard and audio, the Windows Hello note for Windows 10 2004+ and Windows 11, access grant cmdlets. Corrected: the claim that shielded VMs always refuse VMConnect (console is enabled on version 1803+ hosts). Removed as undocumented: TCP 2179, the Hyper-V Administrators statement, `Set-VM -EnhancedSessionTransportType` (not in the Set-VM reference), xrdp and Linux vsock steps, the Windows Admin Center remark, keyboard shortcuts, and the lock-state remark.

Method: documentation only; no commands were run.
