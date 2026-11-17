---
id: computing-software.it-support-helpdesk.remote-support-tools.winrm-and-psremoting-configuration
name: winrm-and-psremoting-configuration
category: computing-software
field: it-support-helpdesk
product: remote-support-tools
tags: [it-support-helpdesk, remote-support-tools, winrm-configuration, enable-psremoting, trustedhosts, winrm-https, kerberos, powershell-remoting, invoke-command-fan-out]
level: advanced
status: docs-checked
description: "Enable and fix WinRM for PowerShell remoting: Enable-PSRemoting, network profile behaviour, ports, Kerberos vs TrustedHosts, HTTPS listeners and listener diagnosis."
sources:
  - "https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/enable-psremoting"
  - "https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_remote_troubleshooting"
  - "https://learn.microsoft.com/en-us/windows/win32/winrm/installation-and-configuration-for-windows-remote-management"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# winrm-and-psremoting-configuration

PowerShell remoting (`Enter-PSSession`, `Invoke-Command`) uses WinRM (WS-Management). The
default HTTP listener port is 5985 and HTTPS uses 5986. Remoting is enabled by default on
Windows Server; on other Windows versions run `Enable-PSRemoting`.

## Enable
- Elevated PowerShell on the target: `Enable-PSRemoting -Force`. It configures the endpoint,
  starts the service and creates firewall rules. On client Windows it creates rules for
  domain and private networks only; for a Public network profile, `-SkipNetworkProfileCheck`
  creates a rule that allows access from the same local subnet. That parameter does not
  change server versions, which already allow the local subnet on public networks.
- It must be run from the PowerShell version you want to remote into (each installation
  gets its own endpoint).
- The default endpoint security descriptor allows the built-in Remote Management Users
  group, so grant that group rather than local admin where it is enough.

## Authentication
- Kerberos gives mutual authentication but works only in domains, not workgroups. Where
  mutual authentication cannot be established (workgroup, or connecting by IP address),
  use an HTTPS listener or add the target to the client-side **TrustedHosts** list; keep
  that list narrow (the WinRM page gives workgroup best practice).
- Create the HTTPS listener as described in "Installation and Configuration for Windows
  Remote Management" (needs a certificate; open port 5986) and connect with SSL.

## Diagnose
- On the target: `winrm enumerate winrm/config/listener` lists listeners (transport and
  address).
- The `about_Remote_Troubleshooting` page covers further remoting errors and fixes.

## Gotchas
- Log remoting use (script block logging and transcription) for audit; this is policy
  advice, not a setting this page documents.

## Checked
2026-11-01. Confirmed against Microsoft Learn Enable-PSRemoting, "Installation and
Configuration for Windows Remote Management" and about_Remote_Troubleshooting: default ports,
server default, firewall profile behaviour and SkipNetworkProfileCheck, per-version endpoints,
Remote Management Users in the default descriptor, Kerberos domains only, TrustedHosts
purpose, HTTPS port, listener enumerate command. Removed: GPO menu path, Intune advice,
TrustedHosts/New-Item examples, error table, SPN check, second-hop advice, Test-WSMan and
Test-NetConnection checks.
Method: documentation only; no commands were run.
