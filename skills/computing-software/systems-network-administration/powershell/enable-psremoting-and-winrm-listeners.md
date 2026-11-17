---
id: computing-software.systems-network-administration.powershell.enable-psremoting-and-winrm-listeners
name: enable-psremoting-and-winrm-listeners
category: computing-software
field: systems-network-administration
product: powershell
tags: [powershell, ps-remoting, winrm, enable-psremoting, winrm-listener, wsman, firewall, group-policy, powershell-7-endpoint]
level: practitioner
status: docs-checked
description: "Turn on PowerShell remoting with Enable-PSRemoting: what it configures, per-version endpoints, public-network firewall rules, who may connect, requirements."
sources:
  - https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/enable-psremoting
  - https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_remote_requirements
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Enable PS remoting and WinRM listeners

WS-Management based remoting is supported only on Windows. It is enabled by default on Windows Server 2012 and later. Run `Enable-PSRemoting` (elevated) on computers that receive commands, once; sending computers need no setup. Because it starts listeners, run it only where needed.

## What it does
`Enable-PSRemoting [-Force] [-SkipNetworkProfileCheck]` runs `Set-WSManQuickConfig`, then restarts WinRM:
- starts WinRM and sets it to Automatic;
- creates a listener on any IP address;
- enables a firewall exception for WS-Management;
- creates the simple-name and long-name endpoint configurations if needed, enables all session configurations and sets their security descriptors to allow remote access.

## Versions and endpoints
- It configures the endpoint for the PowerShell version you run it in. Running in PowerShell 6.2 creates `PowerShell.6` and `PowerShell.6.2.2`. Connect with `-ConfigurationName` on `Invoke-Command`, `New-PSSession` or `Enter-PSSession`.
- It does not affect endpoints hosted by Windows PowerShell (it only affects PowerShell 6+). Run it from Windows PowerShell to enable those; running it in PowerShell 7 prints a warning to that effect.

## Network locations and firewall
- Server Windows: private and domain get unrestricted rules; a Public rule allows only the local subnet (on by default, reapplied by the cmdlet).
- Client Windows: private and domain get unrestricted rules. Public networks are disallowed unless `-SkipNetworkProfileCheck` is used, which creates a local-subnet-only rule.
- To allow all locations: `Set-NetFirewallRule -Name "WINRM-HTTP-In-TCP-PUBLIC" -RemoteAddress Any`. Rule names vary by Windows version; check `Get-NetFirewallRule` and review the rule first.

## Who can connect
Members of Administrators or Remote Management Users on the remote computer, subject to the session configuration's security descriptor. The default `Microsoft.PowerShell` and `Microsoft.PowerShell32` configurations allow only Administrators.

## Requirements
Windows PowerShell 3.0+, .NET Framework 4+ and WinRM 3.0+ on both ends (WMF 5.1 recommended for full support). PowerShell 7+ also supports remoting over SSH to Windows, macOS or Linux. Administrator elevation is needed for loopback connections, managing session configurations and viewing or changing local WSMan settings, even for Administrators group members. Policies on the local computer apply while connecting; remote policies apply during the session.

## Verify (page's own test)
`New-PSSession` with no parameters creates a session on the local computer if remoting is configured; if it fails, see the remoting troubleshooting skill.

## Checked
Method: 2026-11-08 docs-only read of the Enable-PSRemoting reference and about_Remote_Requirements (MicrosoftDocs/PowerShell-Docs markdown). Dropped the unsupported GPO policy paths, Test-WSMan steps, AllowUnencrypted and Disable-PSRemoting claims. Unchanged: the elevation requirement and firewall rule name.
