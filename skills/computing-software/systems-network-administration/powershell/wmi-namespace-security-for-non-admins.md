---
id: computing-software.systems-network-administration.powershell.wmi-namespace-security-for-non-admins
name: wmi-namespace-security-for-non-admins
category: computing-software
field: systems-network-administration
product: powershell
tags: [powershell, cim, wmi-namespace-security, least-privilege]
level: advanced
status: docs-checked
description: "Grant non-admin monitoring accounts remote WMI access: DCOM launch and activation rights, namespace Remote Enable, firewall, and how to test as the account."
sources:
  - https://learn.microsoft.com/en-us/windows/win32/wmisdk/securing-a-remote-wmi-connection
  - https://learn.microsoft.com/en-us/troubleshoot/windows-server/system-management-components/scenario-guide-troubleshoot-wmi-connectivity-access-issues
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# WMI namespace security for non-admins

Monitoring tools often run as Domain Admin because "WMI needs admin". By default only members of
Administrators can connect to WMI remotely, but a non-admin account can be granted the specific
rights below on the target computer.

## 1. DCOM remote launch and access
WMI uses DCOM for remote calls; failure here shows as `0x80070005` ("DCOM Access Denied").
On the target (Computer B), run `dcomcnfg` > Component Services > Computers > My Computer >
Properties > COM Security tab:
- Launch and Activation Permissions > Edit Limits: add the user or group and allow **Remote
  Launch** and **Remote Activation**.
- Access Permissions > Edit Limits: allow **Remote Access** for ANONYMOUS LOGON (as Microsoft's
  procedure states).
- Alternative: add the user to the local **Distributed COM Users** group, which by default has all
  permissions to access COM/DCOM.

## 2. Namespace permission
Remote Enable on the namespace is enabled only for administrators by default. A user without it
gets `0x80041003` (WBEM_E_ACCESS_DENIED).
- `wmimgmt.msc`, connect to the target, right-click WMI Control > Properties > Security tab,
  select the namespace (root\cimv2 is the default) > Security, find the account and check
  **Remote Enable** and **Read Security**.
- To inherit to child namespaces: Advanced, pick the user, and set Applies to "This namespace and
  subnamespaces".

## 3. Firewall
The target's firewall must allow incoming WMI: enable the Windows Management Instrumentation
(WMI) rule group. WMI remote connections are also affected by User Account Control.

## Test as the account
```powershell
$s = New-CimSession -ComputerName <SERVER> -Credential <DOMAIN>\<ACCOUNT>
Get-CimInstance -CimSession $s Win32_OperatingSystem
```
Connection errors such as `0x800706BA` or `0x80041015` point to the network or firewall;
`0x80070005` to DCOM; `0x80041003` to the namespace permission. Per-class extra rights (services,
event logs, performance counters) are not covered by the cited pages: look them up for the
specific class before relying on them.

## Verify
- [ ] The monitoring account is not an administrator and collects every class you need.

## Checked
2026-11-09. Read in full: "Securing a Remote WMI Connection" and "Scenario guide: Troubleshoot
WMI connectivity and access issues" (Microsoft Learn). Confirmed the default administrators-only
access, DCOM Launch/Activation and Access permission steps, the Distributed COM Users note,
Remote Enable and Read Security steps, the 0x80041003 and 0x80070005 errors and the WMI firewall
rule group. Removed as unconfirmed: Remote Management Users and WinRM guidance, default rights
of Authenticated Users, Enable Account, the Set-WmiNamespaceSecurity script and SetSecurityDescriptor
approach, service control manager, Event Log Readers and Performance Monitor Users advice, port
numbers, and the GPO and DSC statements.

Method: documentation only; no commands were run.
