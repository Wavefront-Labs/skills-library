---
id: computing-software.systems-network-administration.powershell.winrm-https-and-trustedhosts
name: winrm-https-and-trustedhosts
category: computing-software
field: systems-network-administration
product: powershell
tags: [powershell, ps-remoting, winrm, winrm-https, trustedhosts, workgroup-remoting, port-5986, certificate, ntlm]
level: practitioner
status: docs-checked
description: "Remote into workgroup or cross-domain machines safely: a WinRM HTTPS listener on 5986 with a proper certificate, and when (not) to use TrustedHosts."
sources:
  - https://learn.microsoft.com/en-us/troubleshoot/windows-client/system-management-components/configure-winrm-for-https
  - https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_remote_troubleshooting
  - https://learn.microsoft.com/en-us/powershell/scripting/security/remoting/winrm-security
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# WinRM over HTTPS and TrustedHosts

Inside a domain, Kerberos authenticates both user and server. Outside it (workgroup, DMZ, other untrusted domain, or
connecting by IP address, which makes PowerShell fall back to NTLM) the client gets the error that HTTPS transport
must be used or the destination must be added to TrustedHosts. NTLM is disabled by default; you enable it either by
configuring SSL on the target or by setting TrustedHosts on the client.

## HTTPS listener (preferred)
The target needs a local-computer Server Authentication certificate whose CN matches the hostname (or an exact SAN
match), not expired, revoked or self-signed. View it under Certificates (Local computer) > Personal.
```cmd
winrm quickconfig -transport:https
winrm enumerate winrm/config/listener
```
HTTP uses port 5985 and HTTPS uses 5986 on Windows 7 and later. If listener creation fails with "does not have an
appropriate certificate", check the dates, that the hostname matches Issued to or a SAN exactly, that Enhanced Key
Usage contains Server authentication, and that the certification path is OK. With several certificates installed,
confirm the thumbprint in the listener output matches the intended certificate.

Client:
```powershell
Enter-PSSession -ComputerName dmz-web01.example.net -UseSSL -Credential (Get-Credential)
```
WinRM encrypts PowerShell remoting traffic after initial authentication over HTTP or HTTPS; over HTTPS it uses TLS.
Basic authentication provides no encryption.

## TrustedHosts (when you accept NTLM to that host)
```powershell
Get-Item WSMan:\localhost\Client\TrustedHosts
$cur = (Get-Item WSMan:\localhost\Client\TrustedHosts).Value
Set-Item WSMan:\localhost\Client\TrustedHosts -Value "$cur, dmz-web01"
```
- It is a client-side, comma-separated list of names, IP addresses and FQDNs. Wildcards are permitted, so avoid them.
  The value affects all users of the computer.
- Local administrator accounts connecting over the network get a filtered token. The `LocalAccountTokenFilterPolicy`
  registry value set to 1 disables UAC remote restrictions for all users of all affected computers; consider the
  implications before changing it.

## Verify
- [ ] `winrm enumerate winrm/config/listener` shows the HTTPS listener with the right thumbprint.

## Checked
2026-11-09. Read the Learn WinRM-for-HTTPS troubleshooting page, about_Remote_Troubleshooting and the WinRM security
page. Confirmed: certificate requirements, quickconfig command, ports, listener error and checks, TrustedHosts
semantics and commands, LocalAccountTokenFilterPolicy, NTLM and encryption statements. Removed as unconfirmed: the
New-Item WSMan listener syntax, firewall rule, SkipCACheck/SkipCNCheck options, Test-WSMan check, the
pass-the-hash remark, certificate renewal advice, and the CA-trust requirement.
Method: documentation only; no commands were run.
