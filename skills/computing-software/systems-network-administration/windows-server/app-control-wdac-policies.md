---
id: computing-software.systems-network-administration.windows-server.app-control-wdac-policies
name: app-control-wdac-policies
category: computing-software
field: systems-network-administration
product: windows-server
tags: [windows-server, os-hardening, windows-server-hardening, wdac, app-control-for-business, code-integrity, new-cipolicy, convertfrom-cipolicy, audit-mode, citool]
level: advanced
status: draft
description: "Deploy App Control for Business (WDAC) on servers: base policy from template, audit mode, merging allow rules from audit events, enforcement and safe rollback."
sources:
  - https://learn.microsoft.com/en-us/windows/security/application-security/application-control/app-control-for-business/design/appcontrol-design-guide
  - https://learn.microsoft.com/en-us/windows/security/application-security/application-control/app-control-for-business/deployment/appcontrol-deployment-guide
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# App Control for Business (WDAC) policies on servers

Kernel-enforced allow-listing (stronger than AppLocker; applies to drivers and admins).

## Start from a template
Templates are in `%windir%\schemas\CodeIntegrity\ExamplePolicies`:
`DefaultWindows_Audit.xml` (Windows + WHQL + Store), `AllowMicrosoft.xml`.
```powershell
$p = "$env:TEMP\ServerBase.xml"
Copy-Item "$env:windir\schemas\CodeIntegrity\ExamplePolicies\DefaultWindows_Audit.xml" $p
# add rules for installed software by scanning a reference server
New-CIPolicy -Level Publisher -Fallback Hash -ScanPath "$env:ProgramFiles" -UserPEs -FilePath "$env:TEMP\Apps.xml"
Merge-CIPolicy -PolicyPaths $p,"$env:TEMP\Apps.xml" -OutputFilePath "$env:TEMP\Merged.xml"
Set-RuleOption -FilePath "$env:TEMP\Merged.xml" -Option 3          # 3 = Audit Mode
Set-CIPolicyIdInfo -FilePath "$env:TEMP\Merged.xml" -PolicyName 'Server Base' -ResetPolicyID
```

## Deploy in audit mode
```powershell
ConvertFrom-CIPolicy -XmlFilePath "$env:TEMP\Merged.xml" -BinaryFilePath "$env:TEMP\policy.cip"
CiTool --update-policy "$env:TEMP\policy.cip"     # Server 2025 / Win11 22H2+, no reboot
# older: copy <PolicyId>.cip to %windir%\System32\CodeIntegrity\CiPolicies\Active and reboot
CiTool --list-policies
```
Or GPO (Device Guard > Deploy App Control), Intune, or Configuration Manager.

## Learn from audit events
Event log `Microsoft-Windows-CodeIntegrity/Operational` event 3076 (would have been
blocked), MSI/script events 8028 in `AppLocker/MSI and Script`. Build supplemental rules:
```powershell
New-CIPolicy -Audit -Level Publisher -Fallback Hash -FilePath "$env:TEMP\FromAudit.xml" -UserPEs
```
Run audit for a full business cycle (month-end, patch day).

## Enforce
Remove option 3, add option 9 (Advanced Boot Options menu) and 10 (Boot Audit on
Failure) for recovery, redeploy. Enforced blocks log event 3077.

## Gotchas
- Keep base policies signed for tamper resistance only after you have a process: a signed
  policy cannot be removed without the signing cert and a reboot dance.
- Use supplemental policies per application team instead of editing the base.
- Managed installer (ConfigMgr) and ISG options reduce rule churn on admin-heavy servers.

## Verify
- [ ] `CiTool --list-policies` shows the policy Is Currently Enforced = true.
- [ ] No unexpected 3077 events after a patch cycle.
