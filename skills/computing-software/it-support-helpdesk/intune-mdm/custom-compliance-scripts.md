---
id: computing-software.it-support-helpdesk.intune-mdm.custom-compliance-scripts
name: custom-compliance-scripts
category: computing-software
field: it-support-helpdesk
product: intune-mdm
tags: [it-support-helpdesk, intune-mdm, custom-compliance, compliance-scripts, discovery-script, json-rules, powershell, intune-management-extension, intune]
level: advanced
status: docs-checked
description: "Build Intune custom compliance: a discovery script (PowerShell, Bash, Linux) that emits settings, the rules JSON with operators and remediation text, limits, error codes."
sources:
  - "https://learn.microsoft.com/en-us/mem/intune/protect/compliance-use-custom-settings"
  - "https://learn.microsoft.com/en-us/mem/intune/protect/compliance-custom-script"
  - "https://learn.microsoft.com/en-us/mem/intune/protect/compliance-custom-json"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# custom-compliance-scripts

When built-in compliance settings do not cover a requirement, use **custom compliance**: a
discovery script plus a JSON rules file, both part of one compliance policy. Each policy
takes a single script (which can discover many settings), and each script can be used with
only one policy. Results can drive Conditional Access like built-in settings.

Platforms: Windows (not Home), macOS, Linux (Ubuntu Desktop 24.04 or 26.04 LTS, RHEL 9 or
10).

## 1. Discovery script
Upload it first: Intune admin center > Endpoint security > Device compliance > **Scripts** >
Add > choose platform. Intune does not validate syntax. A script cannot be deleted while
assigned to a policy. Adding scripts needs the default scope tag (no scope tags).
- **Windows**: PowerShell. Output must be compressed single-line JSON, so the last line is
  `return $hash | ConvertTo-Json -Compress`. Page sample:
  ```powershell
  $WMI_ComputerSystem = Get-WMIObject -class Win32_ComputerSystem
  $WMI_BIOS = Get-WMIObject -class Win32_BIOS
  $TPM = Get-Tpm
  $hash = @{ Manufacturer = $WMI_ComputerSystem.Manufacturer; BiosVersion = $WMI_BIOS.SMBIOSBIOSVersion; TPMChipPresent = $TPM.TPMPresent}
  return $hash | ConvertTo-Json -Compress
  ```
  Options: run with logged-on credentials (default is System context; falls back to System
  if nobody is logged on), enforce signature check, run in 64-bit host (default is 32-bit).
- **macOS**: Bash with a valid shebang, UTF-8 without BOM, exit 0 on success, non-zero on
  failure.
- **Linux**: any interpreter installed on the device, chosen with a shebang. Scripts run in
  the user's context, so they cannot check settings that need elevation.
- Limits: script max 1 MB, output max 1 MB; run time max 5 minutes on Linux, 10 minutes on
  macOS and Windows.

## 2. Rules JSON
Required per rule: `SettingName` (case-sensitive), `Operator`, `DataType`, `Operand`,
`MoreInfoUrl`, `RemediationStrings` (at least one `en_US` string; other languages
optional, `{ActualValue}` can appear in the Title). The file can be up to 100 KB and hold
100 rules.
```json
{"Rules":[
 {"SettingName":"TPMChipPresent","Operator":"IsEquals","DataType":"Boolean","Operand":true,
  "MoreInfoUrl":"https://example.com/kb/tpm",
  "RemediationStrings":[{"Language":"en_US","Title":"TPM chip must be enabled.",
   "Description":"TPM chip must be enabled. Please refer to the link above"}]},
 {"SettingName":"BiosVersion","Operator":"GreaterEquals","DataType":"Version","Operand":"2.3",
  "MoreInfoUrl":"https://example.com/kb/bios",
  "RemediationStrings":[{"Language":"en_US",
   "Title":"BIOS Version needs to be upgraded to at least 2.3. Value discovered was {ActualValue}.",
   "Description":"BIOS must be updated."}]}
]}
```
- Operators: IsEquals, NotEquals, GreaterThan, GreaterEquals, LessThan, LessEquals.
- DataTypes: Boolean, Int64, Double, String, DateTime, Version.

## 3. Policy
Create a compliance policy; on the Configuration settings page enable custom compliance,
select the script, then add the JSON. Pilot before wide assignment.

## How it runs and testing
- On Windows, the device installs the Intune Management Extension by MSI if missing. The
  extension checks for new or updated scripts every eight hours and runs discovery every
  eight hours; Check Compliance runs scripts but does not fetch new ones. Push
  notifications cannot trigger it on demand. A fix can take up to eight hours to show as
  compliant.
- Reports: Reports > Device compliance > Reports tab > Noncompliant devices and settings,
  choose a platform, Generate report.
- Error codes in the report: 65007 script returned failure, 65008 setting missing in the
  script result, 65009 invalid JSON for the discovered setting, 65010 invalid datatype.
- User refresh: Windows via Company Portal website sync; Linux via Refresh in the Intune
  app; macOS via Company Portal > Devices > the device > Check Status.

## Checked
Date: 2026-11-07. Read in full: "Custom compliance settings in Microsoft Intune", "Custom compliance discovery scripts" and
"Custom compliance JSON files". Removed as unconfirmed or contradicted: the operators Between, In and NotIn (page lists six
operators only); the "Devices > Compliance > Scripts" path (page says Endpoint security > Device compliance > Scripts); the
CrowdStrike service example and `psexec` testing; the log file names and the "after reboot" evaluation claim; the "Error counts
as not compliant" claim; and the Verify step. Added limits, error codes, rule/JSON size limits and platform requirements from the pages.
Method: documentation only; no commands were run.
