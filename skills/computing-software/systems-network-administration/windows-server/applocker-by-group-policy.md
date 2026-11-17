---
id: computing-software.systems-network-administration.windows-server.applocker-by-group-policy
name: applocker-by-group-policy
category: computing-software
field: systems-network-administration
product: windows-server
tags: [windows-server, security-policy-settings, gpo-security-settings, applocker, application-control, appidsvc, audit-only, publisher-rules, path-rules, get-applockerfileinformation, new-applockerpolicy, allow-listing]
level: practitioner
status: docs-checked
description: "Deploy AppLocker via GPO: default rules, publisher over path rules, audit-only first, the Application Identity service, event review and moving to enforce."
sources:
  - https://learn.microsoft.com/en-us/windows/security/application-security/application-control/app-control-for-business/applocker/applocker-overview
  - https://learn.microsoft.com/en-us/powershell/module/applocker/new-applockerpolicy
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# AppLocker via Group Policy

**Position:** AppLocker is easier than App Control for Business (WDAC) and supports per-user
rules, but it is a defence-in-depth feature (bypassable by admins); WDAC is the stronger
control. AppLocker is still a fast win on RDS hosts and kiosks.

## Rule collections
AppLocker covers executables, scripts, Windows Installer files, DLLs, packaged apps and packaged app installers (the
overview page lists these rule collections; check each collection's file types there).

## Build
GPO: *Computer Configuration > Policies > Windows Settings > Security Settings > Application
Control Policies > AppLocker*.
1. In each collection, create the default rules (verify what they allow in the console before using them).
2. Add **publisher rules** for signed software in user-writable locations (e.g. Teams,
   approved tools), path rules only for admin-controlled folders.
3. Generate rules from a reference machine:
```powershell
Get-AppLockerFileInformation -Directory '<APPS_DIR>' -Recurse -FileType Exe |
  New-AppLockerPolicy -RuleType Publisher,Hash -User Everyone -Optimize -Xml | Out-File applocker.xml
Set-AppLockerPolicy -XmlPolicy applocker.xml -Merge -LDAP "LDAP://CN={GPO-GUID},CN=Policies,CN=System,DC=ad,DC=example,DC=com"
```
4. Enforcement: Properties of AppLocker > each collection **Audit only** first.
5. Start the **Application Identity** service (`appidsvc`) via GPO System Services = Automatic; Learn lists it as the
   required system service for AppLocker.

## Review audit events
`Applications and Services Logs > Microsoft > Windows > AppLocker > EXE and DLL` and
`MSI and Script`: audit-mode and enforce-mode events are logged there separately; read the event text to tell them apart.
```powershell
Get-AppLockerFileInformation -EventLog -EventType Audited | Group-Object Path | Sort Count -Desc
```

## Enforce
After a clean audit period switch collections to **Enforce rules**. Test with
`Test-AppLockerPolicy -XmlPolicy applocker.xml -Path <file> -User AD\jsmith`.

## Gotchas
- Enforcing script rules can change how PowerShell behaves for users; test admin tooling first.
- Path rules on user-writable locations are a classic bypass; allow those by publisher or hash instead.

## Verify
- [ ] AppIDSvc running on targets; audit log quiet for legit apps.
- [ ] An unsigned exe dropped in a user profile is blocked after enforcement.

## Checked
2026-10-28. Confirmed on the Learn AppLocker overview and PowerShell module pages: rule categories exist for executables, scripts,
installers, DLLs and packaged apps; Application Identity service (appidsvc) is required; Get-AppLockerFileInformation,
New-AppLockerPolicy (-RuleType Publisher,Hash, -Optimize, -User, -Xml), Set-AppLockerPolicy -LDAP, Test-AppLockerPolicy.
Removed as unconfirmed: per-collection file extensions and DLL default, event ID numbers, Constrained Language Mode claim.
Method: documentation only; no commands were run.
