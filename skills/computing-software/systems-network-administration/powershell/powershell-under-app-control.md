---
id: computing-software.systems-network-administration.powershell.powershell-under-app-control
name: powershell-under-app-control
category: computing-software
field: systems-network-administration
product: powershell
tags: [powershell, ps-security, powershell-wdac, app-control-for-business, constrained-language-mode, script-signing]
level: advanced
status: docs-checked
description: "How PowerShell behaves under App Control for Business script enforcement: Constrained Language for untrusted scripts, module rules, audit mode, and signing checks."
sources:
  - https://learn.microsoft.com/en-us/powershell/scripting/security/app-control/application-control
  - https://learn.microsoft.com/en-us/windows/security/application-security/application-control/app-control-for-business/design/script-enforcement
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# PowerShell under App Control script enforcement

## What PowerShell does
- Under an App Control policy, PowerShell runs scripts and modules the policy allows in `FullLanguage` mode. All other scripts and script blocks are untrusted and run in `ConstrainedLanguage` mode, and PowerShell throws errors when they attempt disallowed actions. The page admits it can be hard to tell why a script failed in that mode.
- PowerShell detects App Control and AppLocker system-wide policies. App Control puts the system into System Lockdown mode, which decides the language mode. AppLocker has no way to query enforcement, so PowerShell creates two temporary files (`__PSScriptPolicyTest_<random>.ps1` and `.psm1` in the temp folder) and tries to run them.
- Microsoft recommends App Control for Business over AppLocker; AppLocker only receives security fixes.
- Windows PowerShell 5.1 was the first version to support App Control.

## Script enforcement (the Windows side)
- Script enforcement is on in every policy unless option `11 Disabled:Script Enforcement` is set. It is a handshake: the script host (such as PowerShell) asks App Control, then the host does the actual blocking, allowing or mode change. Option 11 is not supported on Windows Server 2016 or Windows 10 1607 LTSB.
- Signed scripts are validated with the WinVerifyTrust API. The signature root must be in the device's trusted root store and the policy must allow it. This differs from executable files, which do not need the root certificate installed.
- PowerShell: the policy must allow all `.ps1`, `.psm1` and `.psd1` files for Full Language. It must also allow dependent modules loaded by an allowed module. Module functions must be exported explicitly by name; a module with no export list loads but exposes no functions, and wildcards in export names make the module fail to load.
- A script not allowed by policy still runs, but in Constrained Language Mode.
- Dot-sourcing is not recommended (use modules). Dot-sourced files must also pass the policy.
- Interactive PowerShell is put into Constrained Language Mode if any UMCI policy is enforced and any active policy enables script enforcement, even in audit mode. To get Full Language interactively you must disable script enforcement for all policies.
- Events are written to the *AppLocker - MSI and Script* log. A "blocked" event does not mean the host fully blocked the script, and some hosts change behaviour even in audit mode, so test thoroughly.
- Other hosts: wscript.exe and cscript.exe scripts must be allowed or they are blocked; mshta.exe and MSXML execution is blocked whenever any script-enforcing policy is active, even in audit mode; cmd.exe and .bat/.cmd files are not directly controlled (what they launch is); unenlightened hosts such as many third-party Java or Python engines are implicitly allowed if the host is allowed. COM object enforcement is unaffected by option 11.

## Audit mode (PowerShell 7.4 and later)
In audit mode PowerShell runs untrusted scripts in `ConstrainedLanguage` mode without errors and logs messages to the event log describing what restrictions would apply under Enforce.

## Accepting scripts
Per the script-enforcement page: sign every script, module, manifest and dependent file, not just the entry script; add authenticated signature metadata (original file name, product, version) so rules can identify scripts; verify the signature and trust chain before deployment; test install, import, dot-sourcing, updates and removal in audit mode; review events 8028, 8029, 8037 and 8038; require a new signature or catalog after any change.

## Version notes
- 7.2: AppLocker rules take precedence over `Set-ExecutionPolicy Bypass`; `Add-Type` disallowed in NoLanguage sessions on locked-down machines; scripts cannot use COM objects under AppLocker lockdown (cmdlets that use COM internally are unaffected).
- 7.3: block or allow script files through the App Control API.
- 7.7-preview.4: `FileOnlyEntry` AppSetting for a more restricted mode.

## Checked
Method: 2026-11-08, read the PowerShell application-control page (PowerShell-Docs markdown) and the learn.microsoft.com script-enforcement page in full. Rewritten to what they state. Removed unsupported claims from the earlier draft: event IDs 3076/3077 and the CodeIntegrity log, the Set-AuthenticodeSignature command and timestamp server, the list of CLM-blocked features, PowerShell 2.0 bypass, the `__PSLockdownPolicy` remark, and the Verify checklist. The linked how-app-control-works and how-to-use-app-control pages were not read. Not executed.
