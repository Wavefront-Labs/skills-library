---
id: computing-software.cybersecurity-defensive.system-hardening.powerstig
name: powerstig
category: computing-software
field: cybersecurity-defensive
product: system-hardening
tags: [powerstig, dsc, desired-state-configuration, disa-stig, windows-hardening, powershell]
level: advanced
status: docs-checked
description: "Apply DISA STIGs with PowerSTIG DSC composite resources: choose the STIG, set org values, record exceptions and skipped rules, and find the module's STIG list."
sources: ["https://github.com/microsoft/PowerStig", "https://github.com/microsoft/PowerStig/wiki/WindowsServer"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# PowerSTIG

PowerSTIG (Microsoft, open source) provides PowerShell DSC composite resources generated from DISA STIG data. You declare which STIG applies per node and DSC applies and monitors the settings. The README lists resources for technologies including Windows Server and client, Windows Defender and Firewall, DNS Server, IIS, SQL Server, Office, browsers, .NET Framework, RHEL, Ubuntu and vSphere.

## Install and list
```powershell
Install-Module -Name PowerStig -Scope CurrentUser   # README recommends PowerShellGet
Get-Stig -ListAvailable                              # STIGs and versions in this module release
Update-Module -Name PowerStig
```

## Configuration (WindowsServer resource)
```powershell
WindowsServer BaseLine {
    OsVersion   = '2012R2'        # see the wiki page for the versions this module release supports
    OsRole      = 'MS'            # MS = member server, DC = domain controller
    StigVersion = '2.12'          # optional: newest available if omitted
    DomainName  = 'sample.test'   # optional FQDNs, used for security-group rules
    ForestName  = 'sample.test'
    Exception   = @{ 'V-1075' = @{ ValueData = '1' } }     # override one rule's value
    SkipRule    = 'V-1075'                                 # skip a rule
    SkipRuleType = 'AuditPolicyRule'                       # skip a whole rule type
    OrgSettings = @{ 'V-205909' = @{ OptionValue = 'xAdmin' } }   # or a path to an org-settings XML file
}
```
- **OrgSettings** supplies organisation-chosen values for rules that allow a range. Without it, default values are merged in; with an XML file (entries like `<OrganizationalSetting value="3" id="V-1090"/>`) your values replace the defaults.
- **Exception** and **SkipRule** are different: an exception overrides a STIG value (and the module documents it); a skipped rule is not managed, and its title is tagged "Skip" for central log collection.
- Record why each exception or skip exists in your own risk-acceptance records.

## Gotchas
- Check `Get-Stig -ListAvailable` before planning: only the STIG versions shipped in the installed module release can be used.
- The `PowerStig.Document` checklist module is described in the README as experimental.
- Test in a lab first; STIG settings can break applications.

## Verify
`Get-Stig -ListAvailable` shows the STIG version you intend to use, and each exception or skipped rule in the configuration has a written justification.

## Checked
2026-11-01. Confirmed in the PowerStig README and the WindowsServer wiki page: install command, `Get-Stig -ListAvailable`, `Update-Module`, supported technologies, parameters OsVersion, OsRole (MS/DC), StigVersion, DomainName, ForestName, Exception, OrgSettings (file or inline), SkipRule, SkipRuleType, org XML format, Document module is experimental.
Removed: Windows Server 2022 and version 2.1 example values, copying a default org file, DSC push/pull and LCM mode steps, `Test-DscConfiguration`, `New-StigCheckList`, Azure Automation and Machine Configuration, and the Group Policy and release-lag gotchas (not stated on these pages).
Method: documentation only; no commands were run.
