---
id: computing-software.systems-network-administration.powershell.constrained-language-mode
name: constrained-language-mode
category: computing-software
field: systems-network-administration
product: powershell
tags: [powershell, powershell-security, constrained-language-mode, language-modes, wdac, applocker, languagemode, application-control]
level: advanced
status: gated
description: "Enforce PowerShell constrained language mode properly with WDAC or AppLocker, understand what it blocks, test scripts against it, and avoid the __PSLockdownPolicy trap."
sources:
  - https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_language_modes
  - https://learn.microsoft.com/en-us/powershell/scripting/security/app-control/application-control
  - https://devblogs.microsoft.com/powershell/powershell-constrained-language-mode/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Constrained language mode (CLM)

CLM lets users run cmdlets and approved scripts but blocks the language features attackers
use to reach arbitrary .NET and Win32 APIs.

```powershell
$ExecutionContext.SessionState.LanguageMode     # FullLanguage | ConstrainedLanguage | RestrictedLanguage | NoLanguage
```

## What CLM blocks
- `Add-Type` of new C#, arbitrary .NET method calls and `New-Object` except a list of core allowed
  types (the about_Language_Modes page lists `[string]`, `[int]`, `[datetime]`, `[hashtable]`, `[regex]`, `[pscustomobject]`...).
  `[math]::Round`, `[System.IO.Path]::GetTempFileName()`, `[System.Net.Dns]` calls and `New-Object System.Net.WebClient`
  all failed with "Method invocation is supported only on core types" / "Only core types are supported".
- COM objects outside an allowed list (no `WScript.Shell`, `Shell.Application`).
- Creating instances of PowerShell classes (the `class` block parses, but `[Foo]::new()` and `[Foo]@{}` fail),
  `[scriptblock]::Create(...)`, setting properties on most .NET objects (`$p.Name = 'x'` on a process object fails), and
  type conversions to unapproved types.
- Dot-sourcing and module import across language modes get extra restrictions under a policy (about_Language_Modes).

Cmdlets themselves still work, which is why JEA and normal admin commands keep functioning.

## Enforce it the right way: application control
CLM is reliable only when **WDAC (App Control for Business) or AppLocker script rules are in
enforce mode**. PowerShell then:
- runs scripts/modules **allowed** by policy (signed by your trusted cert, or matching hash/path
  rules) in **FullLanguage**;
- runs everything else, including interactive prompts, in **ConstrainedLanguage**.

Steps:
1. Sign your admin scripts and modules (see the code-signing skill).
2. WDAC: add a signer rule for your code-signing certificate and enable `Enabled:UMCI`
   (user mode code integrity). Audit mode first; check CodeIntegrity and
   `Microsoft-Windows-PowerShell/Operational` events, then enforce.
   AppLocker: Script Rules allowing your publisher plus default rules, enforced, with the
   Application Identity service running (gated: unconfirmed, source is paywalled or blocked). No application-control
   policy was applied on the test machine, so the signing, WDAC audit/enforce and AppLocker steps were not exercised.
3. Remove or block Windows PowerShell 2.0 where it still exists: it predates CLM, so it can serve as a downgrade path
   (gated: unconfirmed, source is paywalled or blocked). No Microsoft page was fetched for the bypass itself. Microsoft's removed-features page
   says Windows 11 24H2 and Windows Server 2025 no longer include it; on this Windows 11 build `Get-WindowsOptionalFeature`
   returned nothing for either `MicrosoftWindowsPowerShellV2` (the name Microsoft's 2017 deprecation post uses for the
   check) or `MicrosoftWindowsPowerShellV2Root`. On older builds, disable the optional feature and re-check its state.

## The __PSLockdownPolicy trap
The `__PSLockdownPolicy` environment variable was added for debugging and unit testing; the PowerShell team's
Constrained Language blog post calls treating it as enforcement "unwise" because an attacker can simply change it.
It is a **debugging aid, not a security feature**. Do not use it as your control.

## Write and test scripts that survive CLM
```powershell
# simulate in a test session (not a security boundary)
$ExecutionContext.SessionState.LanguageMode = 'ConstrainedLanguage'
.\MyScript.ps1
```
The docs say this assignment is "only useful for experimenting". It may differ from policy-driven CLM: `[pscustomobject]@{a=1}` threw "Only core types are supported" in 5.1 and 7.6.7 even though the docs list
`[pscustomobject]` as allowed, so confirm such failures under a real policy before rewriting code.
- Replace `Add-Type`/.NET calls with cmdlets, or sign the module so it runs in FullLanguage.
- Hashtables, `[regex]`, `[datetime]`, `[string]::new()` and `[int]::Parse()` ran in simulation; `New-Object System.Net.WebClient` did not.

## Verify
- [ ] An interactive prompt on a managed host reports `ConstrainedLanguage`.
- [ ] Your signed admin module runs its full feature set; an unsigned copy fails on `Add-Type`.
- [ ] Where Windows PowerShell 2.0 exists, its optional feature shows Disabled (and `powershell -Version 2` fails).

## Checked
Ran in-process CLM simulation on 5.1.26100 and 7.6.7: Add-Type, New-Object WebClient, COM, .NET static calls,
`[math]`, class instantiation, property set, `[scriptblock]::Create`, `[hashtable]`, `[string]::new`, `[int]::Parse`,
`[regex]` and the `[pscustomobject]` surprise. The allowed-type list, "Add-Type can load signed assemblies", the
application-control behaviour, and the note that the assignment is only for experimenting come from the
about_Language_Modes reference (PowerShell-Docs, 7.5). `__PSLockdownPolicy` wording is from the PowerShell team blog
(devblogs.microsoft.com/powershell/powershell-constrained-language-mode/); the `Enabled:UMCI` option name is from the
App Control for Business policy-rule table on Microsoft Learn; PowerShell 2.0 removal from the Windows removed-features
page. WDAC/AppLocker enforcement and the signed-versus-unsigned module behaviour were not run (no policy was applied to
this machine).
