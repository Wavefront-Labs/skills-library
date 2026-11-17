---
id: computing-software.systems-network-administration.powershell.system-wide-powershell-transcription
name: system-wide-powershell-transcription
category: computing-software
field: systems-network-administration
product: powershell
tags: [powershell, ps-security, powershell-transcription, group-policy, script-block-logging, module-logging, auditing]
level: practitioner
status: docs-checked
description: "PowerShell 7 Group Policy settings for transcription, script block and module logging: policy paths, PSCore ADMX install, defaults, and protecting a shared output directory."
sources:
  - https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_group_policy_settings
  - https://learn.microsoft.com/en-us/powershell/scripting/security/security-features
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# System-wide PowerShell transcription and logging (Group Policy)

## Where the PowerShell 7 settings live
PowerShell 7 policies are under `Computer Configuration\Administrative Templates\PowerShell Core` and the same path under
`User Configuration`. Computer Configuration takes precedence over User Configuration.

Install the templates with `InstallPSCorePolicyDefinitions.ps1` from `$PSHOME` (it ships with the ADMX/ADML files
`PowerShellCoreExecutionPolicy.admx/.adml`), then edit with `gpedit.msc`. List them:
`Get-ChildItem -Path $PSHOME -Filter *Core*Policy*`.

Each PowerShell Core setting has a "Use Windows PowerShell Policy setting" field that reads the equivalent setting at
`Administrative Templates\Windows Components\Windows PowerShell`. The Core templates contain no settings for Windows
PowerShell itself (the page points to the Central Store article for acquiring other templates).

## Turn on PowerShell Transcription
- Captures input and output of PowerShell commands to text transcripts, for PowerShell and other applications that use the engine.
- Default: each user's `My Documents`, filename containing `PowerShell_transcript`, the computer name and start time.
- Same effect as calling `Start-Transcript` in every session.
- Disabled: no default transcripts, but `Start-Transcript` still works.
- If `OutputDirectory` is a shared location, limit access to it so users cannot view other users' or computers' transcripts.

## Related policies on the same page
- **Turn on PowerShell Script Block Logging**: logs script input (commands, script blocks, functions, scripts, interactive or automated) to
  the Microsoft-Windows-PowerShell/Operational event log. The optional Script Block Invocation Logging also logs start and stop of
  invocations and generates a high volume of events.
- **Turn on Module Logging**: records pipeline execution events for chosen modules in the Windows PowerShell event log. Not configured:
  each module's `LogPipelineExecutionDetails` decides (default `$false`). Per-session alternative: set it on the imported module.
- **Turn on Script Execution**: AllSigned / RemoteSigned / Unrestricted equivalents; disabled means Restricted.
- **Console session configuration**: names a configuration endpoint PowerShell runs in.

The security-features page describes module and script block logging as separate features and links to about_Logging_Windows.

## Not stated by the sources
Share and NTFS permission layouts, registry value names, per-command invocation headers, SIEM collection and transcript file
path patterns are not covered by the two pages; consult other documentation before relying on them.

## Checked
Method: 2026-11-08, read about_Group_Policy_Settings (7.5 markdown) in full and the security-features page up to its Application Control section (all logging-related text). Rewritten to what they state. Removed unsupported claims from the earlier draft: Windows PowerShell policy node name for transcription, write-only share ACLs, registry keys, invocation-header option, transcript path pattern, and the claim that attackers cannot read transcripts. Not executed.
