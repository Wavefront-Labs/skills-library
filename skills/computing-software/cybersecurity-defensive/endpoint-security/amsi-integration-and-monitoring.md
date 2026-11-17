---
id: computing-software.cybersecurity-defensive.endpoint-security.amsi-integration-and-monitoring
name: amsi-integration-and-monitoring
category: computing-software
field: cybersecurity-defensive
product: endpoint-security
tags: [antimalware, amsi, antimalware-scan-interface, script-scanning, powershell, vba, amsi-bypass-detection, office-macros, defender-antivirus, script-block-logging, powershell-v2-removal]
level: advanced
status: draft
description: "Use AMSI to scan scripts and macros at runtime: what feeds it, verifying it works, Defender logs, detecting AMSI tampering, PowerShell 2.0 removal and custom apps."
sources: ["https://learn.microsoft.com/en-us/windows/win32/amsi/antimalware-scan-interface-portal", "https://learn.microsoft.com/en-us/windows/win32/amsi/how-amsi-helps", "https://learn.microsoft.com/en-us/defender-endpoint/amsi-on-mdav", "https://support.microsoft.com/help/5065506", "https://attack.mitre.org/techniques/T1562/001/"]
aliases:
  - computing-software.systems-network-administration.powershell.amsi-and-powershell-script-scanning
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# AMSI (Antimalware Scan Interface)

**Goal:** malicious scripts are scanned after deobfuscation at runtime, and attempts to blind AMSI are detected.
This skill merges the earlier `systems-network-administration.powershell.amsi-and-powershell-script-scanning` skill (kept as an alias).

## What AMSI covers
Per Microsoft's AMSI portal page, the Windows components that submit content to the registered antimalware provider are: User Account Control (EXE, COM, MSI and ActiveX elevation), PowerShell (scripts, interactive use and dynamic code evaluation), Windows Script Host (wscript.exe, cscript.exe), JavaScript and VBScript, and Office VBA macros. For macros the VBA runtime logs Win32/COM/VBA calls in a circular buffer and, when a high-risk trigger API is seen, halts execution and sends the buffer to AMSI for a verdict. Microsoft Defender's AMSI page states AMSI does not currently support Python or Perl. (Other sources add .NET Framework 4.8 assembly loads and WMI; those are not on Microsoft's portal list and were not re-verified here.) Applications can call `AmsiInitialize`, `AmsiOpenSession` and `AmsiScanBuffer` themselves.

## How it works for PowerShell
1. PowerShell compiles a script block, including dynamic code from `Invoke-Expression`.
2. It calls `AmsiScanBuffer` with the deobfuscated text just before execution, so encoding and string-concatenation tricks that defeat file scanning are visible.
3. The provider (Defender or another registered AV/EDR) returns a verdict; malicious content raises "This script contains malicious content and has been blocked by your antivirus software".

## Verify it works
```powershell
# Use Microsoft's published AMSI test sample (see the AMSI demonstration page for Defender for Endpoint).
# The literal string is not reproduced here because antivirus quarantines any file that contains it.
Get-MpComputerStatus | Select-Object AMServiceEnabled, AntivirusEnabled, RealTimeProtectionEnabled
Get-ChildItem 'HKLM:\SOFTWARE\Microsoft\AMSI\Providers'     # registered AMSI providers
```
The sample should be blocked when pasted into a session. Third-party AV must register as an AMSI provider; with some products, or with Defender in passive mode, AMSI scanning may not be wired in, so test rather than assume.

## Logs
- Defender detections appear as event **1116** in the Microsoft-Windows-Windows Defender/Operational log (Microsoft's AMSI demo article points at 1116). 1117 is commonly read as the action taken, but sources disagree on its exact wording, and the field values that mark an AMSI-originated detection were not confirmed here.
- Pair with PowerShell script block logging (event **4104**) to see the exact code.

## Detect tampering
Attackers patch `AmsiScanBuffer` in memory, set `amsiInitFailed` through reflection, or downgrade to PowerShell 2.0 (no AMSI, no script block logging). Defend with:
- Alerts on 4104 events containing `AmsiUtils`, `amsiInitFailed`, `AmsiScanBuffer`, or `VirtualProtect` against amsi.dll; EDR alerts on amsi.dll memory modification.
- Removing PowerShell 2.0: `Disable-WindowsOptionalFeature -Online -FeatureName MicrosoftWindowsPowerShellV2Root`. Microsoft is removing it anyway (KB 5065506): from Windows 11 24H2 with an August 2025 update and from Windows Server 2025 with a September 2025 release; a script that requests version 2 now gets the default 5.1 engine. Older builds still need the feature disabled; alert on `powershell.exe -version 2`.
- App Control (WDAC) with Constrained Language Mode to limit reflection-based bypasses.
- Mapping to MITRE ATT&CK T1562.001 (Impair Defenses: Disable or Modify Tools).

## Gotchas
- AMSI is only as good as the provider.
- Bypass strings are themselves signatured, so attackers obfuscate the bypass; behavioural detection of memory patching is more durable.
- Office macro AMSI scanning depends on the Office version and the "Macro Runtime Scan Scope" policy.
- False positives on admin scripts containing offensive-looking strings: add narrow path or hash exclusions in Defender, never disable AMSI.

## Verify
- [ ] The Microsoft test sample is blocked on representative endpoints.
- [ ] Detection for AMSI tampering strings in 4104 exists and fires in a purple-team test.
- [ ] PowerShell 2.0 is absent or disabled on all supported builds.
