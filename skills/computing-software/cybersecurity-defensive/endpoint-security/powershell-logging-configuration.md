---
id: computing-software.cybersecurity-defensive.endpoint-security.powershell-logging-configuration
name: powershell-logging-configuration
category: computing-software
field: cybersecurity-defensive
product: endpoint-security
tags: [windows-security-features, powershell-logging, script-block-logging, module-logging, transcription, event-4104, protected-event-logging]
level: practitioner
status: draft
description: "Turn on PowerShell script block, module logging and transcription centrally, protect logs, forward event 4104, and know what each captures."
sources: ["Microsoft Learn - about_Logging_Windows (script block and module logging)", "NSA/CISA Keep PowerShell: Security Measures to Use and Embrace (2022)", "MITRE ATT&CK T1059.001 PowerShell (detection)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# PowerShell logging

**Goal:** every PowerShell command run on your Windows estate is recorded in deobfuscated form
and forwarded, because PowerShell is the most common post-exploitation tool on Windows.

## Settings (GPO: Administrative Templates > Windows Components > Windows PowerShell; Intune settings catalog has the same)
| Setting | What it records | Where |
|---|---|---|
| Turn on PowerShell Script Block Logging | Script blocks as executed, after deobfuscation (event **4104**); "log invocation start/stop" is very noisy, leave off | `Microsoft-Windows-PowerShell/Operational` |
| Turn on Module Logging (module names `*`) | Pipeline execution details (event 4103) | Same log |
| Turn on PowerShell Transcription | Full input/output text to files | Transcript directory (send to a write-only share) |
PowerShell 7 has its own policies (`PowerShellCore` ADMX) and logs to `PowerShellCore/Operational`; configure both.

Even without the policy, Windows logs script blocks it deems suspicious as warning-level 4104.

## Protect and forward
- Increase `Microsoft-Windows-PowerShell/Operational` log size (e.g. 1 GB).
- Forward 4104 (and 4103 if budget allows) to the SIEM.
- **Protected Event Logging** encrypts logged content with a certificate so local attackers cannot read secrets from logs; the SIEM side needs the private key to decrypt.
- Transcripts: a share where computers can write but not read/modify others' files.
- Remove PowerShell v2 (no logging, no AMSI): `Disable-WindowsOptionalFeature -Online -FeatureName MicrosoftWindowsPowerShellV2Root`.

## Detection ideas
4104 containing: `FromBase64String` with `IEX`, `Net.WebClient`/`DownloadString`, `Invoke-Mimikatz`,
`AmsiUtils`, `-bxor` loops, `Reflection.Assembly]::Load`. Correlate with parent process (Office spawning PowerShell).

## Gotchas
- Script block logs can contain passwords in admin scripts; restrict SIEM access and consider protected event logging.
- Very large scripts are split across multiple 4104 events (`MessageNumber`/`MessageTotal`); reassemble by `ScriptBlockId`.
- Volume: Desired State Configuration and management agents generate heavy logs; filter known benign script blocks at the forwarder by hash, carefully.

## Verify
- [ ] Running `Write-Output 'logtest-12345'` on a sample host produces a 4104 event visible in the SIEM.
- [ ] PowerShell v2 feature removed fleet-wide.
