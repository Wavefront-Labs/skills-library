---
id: computing-software.cybersecurity-defensive.endpoint-security.script-enforcement
name: script-enforcement
category: computing-software
field: cybersecurity-defensive
product: endpoint-security
tags: [script-enforcement, wdac-script-enforcement, constrained-language-mode, msi-script-control, app-control-for-business, application-control]
level: advanced
status: draft
description: "Enforce script control with App Control for Business: PowerShell CLM for unsigned scripts, WSH/MSHTA/MSI enforcement, signing internal scripts and handling exceptions."
sources: ["https://learn.microsoft.com/en-us/windows/security/application-security/application-control/app-control-for-business/design/script-enforcement", "https://learn.microsoft.com/en-us/powershell/scripting/learn/security-features", "https://learn.microsoft.com/en-us/windows/security/application-security/application-control/app-control-for-business/design/microsoft-recommended-block-rules"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Script enforcement

When an App Control for Business (WDAC) policy is enforced and **script enforcement** is on (default -
not disabled by policy option 11 "Disabled:Script Enforcement"), Windows hosts treat scripts as follows:

| Host | Behaviour for scripts not allowed by policy |
|---|---|
| PowerShell | Runs in **Constrained Language Mode** (no arbitrary .NET/COM/Add-Type) |
| Windows Script Host (cscript/wscript: VBScript, JScript) | Scripts not allowed by policy are blocked; COM object creation restricted |
| MSHTA | Blocked (HTA files) |
| MSI (msiexec) | Installers must be allowed by policy (signer/hash) |
| cmd/batch | **Not** enforced |

## Allow internal scripts
- Sign PowerShell scripts with an internal code-signing certificate (`Set-AuthenticodeSignature -FilePath x.ps1 -Certificate $cert -TimestampServer http://timestamp.digicert.com`) and add the signer to the policy (`New-CIPolicyRule -Level Publisher`), or allow by hash for a few stable scripts.
- Configuration management agents (SCCM, Intune) run scripts in contexts that may need signer rules (Intune Management Extension scripts run as allowed if the IME is a managed installer/trusted signer).

## Detect impact first
Audit mode: event 8028/8029 (script would be blocked) in `Microsoft-Windows-CodeIntegrity/Operational` and
PowerShell event 4104 indicates CLM when enforced. Query `DeviceEvents` `ActionType startswith "AppControlCodeIntegrityScriptAudited"` in Defender advanced hunting.

## Block bypass paths
Apply the Microsoft recommended block rules (MSBuild, InstallUtil and other LOLBins that can run code
outside script enforcement) and remove the PowerShell 2.0 engine.

## Gotchas
- CLM breaks admin scripts that call .NET types; sign them rather than disabling enforcement.
- Remove Windows PowerShell 2.0 (`Disable-WindowsOptionalFeature -Online -FeatureName MicrosoftWindowsPowerShellV2Root`) - it bypasses CLM.

## Verify
- [ ] `$ExecutionContext.SessionState.LanguageMode` shows ConstrainedLanguage for an unsigned interactive session on enforced devices, FullLanguage for signed scripts.
- [ ] No 8029 events for business scripts after rollout.
