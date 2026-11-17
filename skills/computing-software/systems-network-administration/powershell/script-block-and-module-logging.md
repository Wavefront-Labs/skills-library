---
id: computing-software.systems-network-administration.powershell.script-block-and-module-logging
name: script-block-and-module-logging
category: computing-software
field: systems-network-administration
product: powershell
tags: [powershell, powershell-security, script-block-logging, module-logging, transcription, event-4104, protected-event-logging, siem]
level: advanced
status: docs-checked
description: "Turn on PowerShell script block logging, module logging and system-wide transcription by GPO, read 4104 events, protect logs with Protected Event Logging, and forward them."
sources:
  - https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_logging_windows
  - https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_group_policy_settings
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Script block and module logging

| Feature | Records | Where |
|---|---|---|
| Script block logging | the processing of commands, scriptblocks, functions and scripts, invoked interactively or by automation | event 4104; PowerShell 7 writes to the `PowerShellCore/Operational` log, and the Group Policy page names `Microsoft-Windows-PowerShell/Operational` |
| Module logging | pipeline execution events for members of the specified modules | Windows PowerShell log in Event Viewer (per the Group Policy page); controlled by the module's `LogPipelineExecutionDetails` property, `$false` by default |
| Transcription | input and output of PowerShell commands as text | text files; default is each user's My Documents folder, named `PowerShell_transcript...` |

On Windows the PowerShell event provider must be registered first (`$PSHOME\RegisterManifest.ps1`, elevated) before PowerShell 7 events are written.

## Enable by GPO
PowerShell 7 reads its own policies: install the templates with `InstallPSCorePolicyDefinitions.ps1` (in `$PSHOME`), then use Computer Configuration > Administrative Templates > PowerShell Core:
- Turn on PowerShell Script Block Logging. Enabling Script Block Invocation Logging also logs start/stop of invocations and generates a high volume of events.
- Turn on Module Logging, with the module names to log.
- Turn on PowerShell Transcription. When the output directory is a shared location, limit access so users cannot view other users' or computers' transcripts.

Each PowerShell Core policy has a "Use Windows PowerShell Policy setting" field that inherits the matching Windows PowerShell policy under Administrative Templates > Windows Components > Windows PowerShell. Computer Configuration takes precedence over User Configuration.

Registry equivalent for PowerShell 7 (from about_Logging_Windows):
```powershell
$k = 'HKLM:\Software\Policies\Microsoft\PowerShellCore\ScriptBlockLogging'
New-Item $k -Force | Out-Null
Set-ItemProperty $k -Name EnableScriptBlockLogging -Value "1"
```
Script block logging can also be set in `powershell.config.json` (see about_PowerShell_Config). The Windows PowerShell 5.1 policy locations are in about_Logging for 5.1 (not covered by these sources).

## Protect the logs
- Logged script content can include credentials or other sensitive data. Microsoft recommends enabling Protected Event Logging when using script block logging for anything beyond diagnostics.
- Group Policy: Administrative Templates > Windows Components > Event Logging > Enable Protected Event Logging. It needs an encryption certificate with the Document Encryption enhanced key usage and Data Encipherment or Key Encipherment key usage. Keep the private key off the logging machines.
- Content is encrypted with CMS (public key); decrypt centrally, for example `Get-WinEvent Microsoft-Windows-PowerShell/Operational | Where-Object Id -EQ 4104 | Unprotect-CmsMessage`.
- Forward events to a central collector or SIEM so a compromised host cannot be the only copy; sizing the log and forwarding method are covered by your platform's Event Log and WEF documentation.

## Verify
- [ ] Run a harmless command in a new session (script block logging applies to new sessions) and find it in a 4104 event.
- [ ] Events arrive in the SIEM within the expected delay.
- [ ] Transcript files land on the share and users cannot read others' files.

## Checked
Date: 2026-11-02. Confirmed against about_Logging_Windows (event 4104, PowerShellCore/Operational, provider registration, registry path, Protected Event Logging, CMS, certificate requirements, Unprotect-CmsMessage example) and about_Group_Policy_Settings (PowerShell Core policy path, ADMX script, Use Windows PowerShell Policy setting, invocation logging volume, transcription defaults and share ACL advice, module logging default). Removed: event IDs 4103/4105/4106, suspicious-keyword Warning 4104 behaviour for PS 5+, 15 MB default log size and the wevtutil command, event Properties[] reassembly, the Windows PowerShell 5.1 registry path and the specific hunt keywords (none stated in the sources).
Method: documentation only; no commands were run.
