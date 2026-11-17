---
id: computing-software.systems-network-administration.windows-server.wac-troubleshooting
name: wac-troubleshooting
category: computing-software
field: systems-network-administration
product: windows-server
tags: [windows-admin-center, wac, wac-troubleshooting, winrm, wac-certificate]
level: practitioner
status: docs-checked
description: "Troubleshoot Windows Admin Center: gateway service and certificate errors, WinRM connectivity to targets, CredSSP prompts and the WAC event and diagnostics logs."
sources:
  - https://learn.microsoft.com/en-us/windows-server/manage/windows-admin-center/support/troubleshooting
  - https://learn.microsoft.com/en-us/windows-server/manage/windows-admin-center/support/known-issues
  - https://learn.microsoft.com/en-us/windows-server/manage/windows-admin-center/configure/update-certificate
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Troubleshooting Windows Admin Center

## Gateway does not load
- Service: check that **ServerManagementGateway** or **Windows Admin Center** is running (`Get-Service WindowsAdminCenter` on the
  modernized gateway), and look in Event Viewer > Applications and Services > Microsoft-ServerManagementExperience.
- Test the gateway port: `Test-NetConnection -Port <port> -ComputerName <gateway> -InformationLevel Detailed`; for an Azure VM check the NSG inbound rule.
- Certificate expired or wrong: update it with `Set-WACCertificateSubjectName` / `Set-WACCertificateAcl` and restart the service, or re-run the installer
  and choose the pre-installed certificate (see the gateway deployment skill).
- Use a current Edge or Chrome; if the page cannot be reached on a desktop install, try a private window and check that the right certificate was chosen.
- TLS error about outdated settings: the browser machine may be restricted to HTTP/2, which does not support integrated Windows authentication; set the
  `EnableHttp2Cleartext` and `EnableHttp2Tls` DWORDs to 0 under `HKLM:\SYSTEM\CurrentControlSet\Services\Http\Parameters` on that machine.
- "You are not authorized to view this page": choose the **Windows Admin Center Client** certificate at first launch, restart the browser and refresh.

## Cannot connect to a target
Make sure the WinRM service is running and set to start automatically on both gateway and target. From the gateway, sign in locally and run
`Enter-PSSession -ComputerName <target>` in an elevated PowerShell window: if it connects, connectivity and permissions are probably fine; if not, look at WinRM, network or authorization.
- Different subnet: allow inbound TCP 5985 on the target (for example `Set-NetFirewallRule -Name WINRM-HTTP-In-TCP-PUBLIC -RemoteAddress Any` on Windows Server).
- Workgroup target: the account must be in the target's local Administrators group (sometimes also Remote Management Users); for a local account that is not the
  built-in Administrator set `LocalAccountTokenFilterPolicy` = 1 (DWORD) under `HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System`.
  Add the target to the gateway's TrustedHosts (`Set-Item WSMan:localhost\Client\TrustedHosts -Value 'server01,server02'`; this overwrites the existing value, so save it first).

## Constant credential prompts
- No Kerberos delegation from gateway to targets: configure RBCD.
- WinRM does not allow credential delegation by default, so WAC enables CredSSP temporarily when a tool needs delegation; for CredSSP errors follow the
  manual steps in the Azure Local CredSSP troubleshooting article.

## Extensions failing
If outbound access is restricted, make sure the documented network URLs are allowed; the default feed is `https://aka.ms/sme-extension-feed`.
Remote Desktop, Events and PowerShell tools need WebSockets, which proxies and firewalls often block.

## Diagnostics
Check the Microsoft-ServerManagementExperience event log on the gateway, and the known issues page for the tool you are using.

## Verify
- [ ] Gateway loads with a trusted certificate; target opens; event logs clear of repeated errors.

## Checked
Checked 2026-10-26 against Microsoft windowsserverdocs main, Windows Admin Center pages (troubleshooting ms.date 2025-06-24; Azure VM and Arc pages current in repo), Windows Admin Center 2410+.
Confirmed from support/troubleshooting (ms.date 2025-06-24): supported OS, ServerManagementGateway or Windows Admin Center service names, Test-NetConnection command, HTTP/2 registry values,
WebSocket tool dependency, client certificate error, Enter-PSSession check, port 5985 firewall rule, LocalAccountTokenFilterPolicy, TrustedHosts commands and overwrite warning, the Microsoft-ServerManagementExperience log,
plus configure/update-certificate and includes/ps-extensions (feed URL). Removed Test-WSMan, the PowerShell 5.1 and port 443/IIS claims, the Settings > Advanced > Diagnostics bundle and the HTTP status code mapping, which the pages do not state.
Method: documentation only; no commands were run.
