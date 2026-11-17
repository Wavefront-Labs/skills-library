---
id: computing-software.cybersecurity-defensive.endpoint-security.applocker-policy
name: applocker-policy
category: computing-software
field: cybersecurity-defensive
product: endpoint-security
tags: [application-control, applocker, applocker-rules, publisher-rules, path-rules, audit-only, applocker-bypasses, srp]
level: practitioner
status: draft
description: "Configure AppLocker rules (executables, scripts, MSI, packaged apps, DLL) via GPO with audit-first rollout, safe path rules and known bypass mitigations."
sources: ["Microsoft Learn - AppLocker overview and design guide", "CIS Control 2.7 (allowlist authorized scripts)", "Microsoft recommended block rules (App Control)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# AppLocker policy

**Goal:** restrict which programs and scripts users can run on Windows where App Control for
Business is not yet feasible, or as a user-mode complement to it.

## Rule collections
Executable (.exe/.com), Windows Installer (.msi/.msp), Script (.ps1/.bat/.cmd/.vbs/.js),
Packaged apps (AppX), DLL (off by default; performance cost). Each collection is enforced only
if it has rules.

## Build
1. GPO: Computer Configuration > Windows Settings > Security Settings > Application Control Policies > AppLocker.
2. Create **default rules** per collection (Everyone may run from `%WINDIR%` and `%PROGRAMFILES%`; Administrators anything) - then tighten.
3. Prefer **publisher rules** (signed vendor, product, file name, version range) over path rules; hash rules for unsigned LOB apps.
4. Avoid path rules on user-writable locations. Default rules allow `%WINDIR%\*`, which contains user-writable folders (e.g. `%WINDIR%\Temp`, `%WINDIR%\Tasks`, some `System32` spool folders); add exceptions for writable subfolders (AccessChk can find them).
5. Start the **Application Identity** service (`AppIDSvc`, set to automatic via GPO) - AppLocker does nothing without it.
6. Set enforcement to **Audit only**; review events in `Applications and Services Logs/Microsoft/Windows/AppLocker` (8003/8006 would-block, 8004/8007 blocked).
7. Enforce collection by collection.

## Bypass mitigation
- Block LOLBins users do not need (`mshta.exe`, `wscript.exe`, `cscript.exe`, `regsvr32.exe`, `msbuild.exe`, `installutil.exe`) with deny rules for standard users.
- Script rules put PowerShell into Constrained Language Mode for non-allowed scripts.
- AppLocker is not a security boundary per Microsoft (admins and some techniques bypass it); use App Control for Business for stronger enforcement.

## Gotchas
- AppLocker on Windows Pro editions is not enforced for all collections (requires Enterprise/Education for full support in many versions).
- DLL rules double the event volume and slow logons; enable only with a clear need.
- Packaged apps rules missing = Store apps blocked once you enforce executable rules on some builds; add default packaged app rules.

## Verify
- [ ] `Get-AppLockerPolicy -Effective -Xml` on a client shows the intended rules.
- [ ] Test unsigned exe in `%USERPROFILE%\Downloads` is blocked for standard users.
