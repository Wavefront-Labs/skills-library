---
id: computing-software.it-support-helpdesk.intune-mdm.win32-detection-and-requirement-rules
name: win32-detection-and-requirement-rules
category: computing-software
field: it-support-helpdesk
product: intune-mdm
tags: [it-support-helpdesk, intune-mdm, win32-detection-rules, requirement-rules, detection-script, msi-product-code, app-deployment, win32-app]
level: practitioner
status: docs-checked
description: "Write Intune Win32 detection and requirement rules: MSI, file, registry and script rules, 32-bit context options, STDOUT and STDERR behaviour, and not-detected fixes."
sources:
  - "https://learn.microsoft.com/en-us/mem/intune/apps/apps-win32-add"
  - "https://learn.microsoft.com/en-us/troubleshoot/mem/intune/app-management/troubleshoot-app-install"
  - "https://learn.microsoft.com/en-us/mem/intune/apps/apps-win32-troubleshoot"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# win32-detection-and-requirement-rules

Detection rules tell Intune whether the app is present. You must configure at least one rule, and the conditions of **all**
rules must be met for the app to be detected. If Intune finds a Required-intent app not present, it offers the app again
within about 24 hours.

## Detection rule types (Detection rules page)
| Type | Settings | Notes |
|---|---|---|
| MSI | MSI product code; optional product version check | Can be added only once |
| File | Path, file or folder, detection method (existence, date, version or size) | Path must not contain special characters such as `,` or `"` |
| Registry | Key path (`HKEY_LOCAL_MACHINE\Software\WinRAR` or `HKLM\Software\WinRAR`), value name, detection method (key or value exists, string equals, integer, version) | Empty value name checks the key; the (default) value is used for non-existence methods |
| Custom script | PowerShell script file | See below |

File and registry rules have "Associated with a 32-bit app on 64-bit clients": Yes expands paths in the 32-bit context
(file rules) or searches the 32-bit registry (registry rules); No (default) uses the 64-bit context. 32-bit clients always
use 32-bit.

### Custom detection script
The app is detected when the script exits 0 **and** writes a string value to STDOUT; Intune does not look for a particular
string. A nonzero exit means not installed. Any data written to STDERR makes the result not installed, even with exit 0 and
STDOUT data. Options: "Run script as 32-bit process on 64-bit clients" (default No) and "Enforce script signature check"
(default No). Microsoft recommends encoding the script as UTF-8 BOM.

Example that detects a file version (the shape of Microsoft's own sample):
```powershell
$v = ([System.Diagnostics.FileVersionInfo]::GetVersionInfo("<path to binary>").FileVersion).Trim()
if ($v -eq "<expected version>") { $v; exit 0 }
exit 1
```
Use `[System.Diagnostics.FileVersionInfo]::GetVersionInfo("<path to binary>").FileVersion` on the device to see the real string.

## Requirement rules (Requirements page)
Choose OS architecture and minimum OS; optionally disk space (MB), physical memory (MB), minimum logical processors and
minimum CPU speed (MHz). Additional rules can be File, Registry or Script:
- File and Registry requirement rules have the same 32-bit option as detection rules.
- Script requirement: if the exit code is 0, Intune reads STDOUT more closely, for example as an integer with value 1; you
  choose the output data type used for the match. Options: 32-bit process, run with logged-on credentials, signature check.

## Fixing "installed but not detected"
1. Read `%ProgramData%\Microsoft\IntuneManagementExtension\Logs\AppWorkload.log` (main app log, includes app detection) and
   `AppActionProcessor.log` (detection and applicability checks).
2. Check the install location and version on the device against the rule, including 32-bit vs 64-bit context.
3. Win32 apps can be installed in System or User context; make sure the install behavior matches where the app lands.
4. For Entra registered devices, choose System install behavior.

## Verify
On a clean device the app is not detected before install and is detected after; the version column in Apps > All Apps shows
the app version.

## Checked
Date: 2026-11-08. Read in full: "Add, assign, and monitor a Win32 app" (Program, Requirements, Detection rules sections),
Win32 app troubleshooting (updated 2026-04-14) and "Troubleshooting Intune app installation issues". Removed as
unconfirmed: the 0x87D1041C error text and meaning, "detection runs before install to skip", the Uninstall-key registry
example, version comparison examples, the claim that product code changes per version, folder-exists leftovers, the
supersedence gotcha, and the "late-written file" cause.
Method: documentation only; no commands were run.
