---
id: computing-software.cybersecurity-defensive.endpoint-security.powershell-constrained-language-mode
name: powershell-constrained-language-mode
category: computing-software
field: cybersecurity-defensive
product: endpoint-security
tags: [windows-security-features, constrained-language-mode, powershell, language-mode, app-control-for-business, applocker-script-rules, jea]
level: advanced
status: docs-checked
description: "Enforce PowerShell Constrained Language Mode through App Control or AppLocker, keep trusted admin scripts in Full Language, and use JEA (NoLanguage) for delegated admin."
sources: ["https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_language_modes", "https://learn.microsoft.com/en-us/powershell/scripting/security/overview"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# PowerShell Constrained Language Mode

**Goal:** untrusted PowerShell cannot reach the .NET, COM or Win32 APIs that could be abused, while scripts
the application control policy trusts still run in FullLanguage.

## How CLM is enforced
- PowerShell runs in ConstrainedLanguage automatically when it detects a system application control policy:
  AppLocker or Windows Defender Application Control (App Control for Business) on Windows.
- Under a policy, interactive sessions and any script or script-based module not allowed by the policy run in
  ConstrainedLanguage; scripts and modules the policy allows run in FullLanguage without those constraints.
- Microsoft states you must use ConstrainedLanguage in System Lockdown mode with App Control for Business to
  ensure it cannot be bypassed. Assigning `$ExecutionContext.SessionState.LanguageMode` by hand is only useful
  for experimenting.

## What ConstrainedLanguage restricts
- Cmdlets and the scripting language stay available, but only an allowed list of .NET types can be used.
- `Add-Type` can load signed assemblies but not arbitrary C# code or Win32 APIs.
- `New-Object` works only on allowed types; only the COM types Scripting.Dictionary, Scripting.FileSystemObject
  and VBScript.RegExp are permitted.
- Additional restrictions apply to dot-sourcing and module importing under a policy.

## Steps
1. Deploy App Control (or AppLocker) in audit mode and see which admin scripts would fall into CLM.
2. Make the admin scripts you need in FullLanguage trusted by the policy (the policy decides; follow Microsoft's
   "Use App Control to secure PowerShell" guidance).
3. Enforce, then check an interactive session: `$ExecutionContext.SessionState.LanguageMode` should print
   `ConstrainedLanguage`.
4. For delegated tasks use Just Enough Administration (JEA): JEA configurations use NoLanguage mode, so users can
   only run a defined set of commands and cannot directly access APIs, the file system or other resources.

## Verify
- [ ] On enforced machines an interactive session reports ConstrainedLanguage.
- [ ] Policy-allowed admin scripts run in FullLanguage; others run constrained.

## Checked
2026-11-01. Confirmed against Microsoft Learn about_Language_Modes (AppLocker/WDAC detection, FullLanguage for allowed scripts, allowed types and COM list, Add-Type limits, JEA NoLanguage, System Lockdown note) and the PowerShell security overview page (JEA and App Control topics exist). Removed: the `__PSLockdownPolicy` claims, PowerShell v2 bypass, execution-policy remarks, the code-signing command and timestamp server, JEA virtual accounts, tamper protection, and the `[Reflection.Assembly]::Load` example.
Method: documentation only; no commands were run.
