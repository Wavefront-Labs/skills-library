---
id: computing-software.it-support-helpdesk.user-support-communication.script-safety-and-review
name: script-safety-and-review
category: computing-software
field: it-support-helpdesk
product: user-support-communication
tags: [it-support-helpdesk, user-support-communication, scripting, script-safety, code-review, script-signing, test-before-deploy, rollback, malicious-scripts, comptia-a-plus, execution-policy-signing]
level: practitioner
status: draft
description: "Avoid the scripting risks A+ names (malware, system damage, resource exhaustion): review checklist, test rings, signing, a script repo, rollback, spotting malicious scripts."
sources:
  - "https://www.comptia.org/certifications/a"
  - "https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.security/set-authenticodesignature"
  - "https://learn.microsoft.com/en-us/powershell/scripting/learn/deep-dives/everything-about-shouldprocess"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# script-safety-and-review

Goal: scripts save time without becoming the outage (A+ 220-1202 4.8 other
considerations: unintentionally introducing malware, inadvertently changing
system settings, browser or system crashes due to mishandling of
resources).

## Review checklist (before any script touches more than one machine)
- [ ] Source known and trusted (your repo, vendor docs) — no copy-paste from
      random forums or AI without understanding every line.
- [ ] Destructive commands (`Remove-Item -Recurse`, `rd /s`, `rm -rf`,
      `format`, `reg delete`, `Clear-Disk`) have guards: variables
      validated non-empty, paths checked with `Test-Path`, `-WhatIf`
      dry run tested.
- [ ] Scope: targets exactly the intended devices/users.
- [ ] Context: runs as SYSTEM/root vs user — paths and permissions
      correct for that context.
- [ ] Resource use: loops bounded, no unbounded downloads/log growth,
      no tight polling; timeouts on network calls.
- [ ] Idempotent: running twice causes no harm.
- [ ] Logging and meaningful exit codes.
- [ ] No secrets in plain text (use managed credentials/secure stores).
- [ ] Rollback: how to undo (backup key/file first, uninstall step).

## Test and deploy
1. Your own test VM/sandbox.
2. IT pilot ring (5–10 devices), then a small business pilot.
3. Broad deployment in waves, watching success/failure counts in
   Intune/RMM.
Peer review by a second engineer for anything fleet-wide.

## Control
- Central **script repository** (Git) with history and review.
- **Code signing** for PowerShell where execution policy is AllSigned:
  `Set-AuthenticodeSignature .\fix.ps1 -Certificate $cert -TimestampServer http://timestamp.digicert.com`.
- Only approved tools run scripts at scale (Intune, RMM) with audit logs.

## Recognising malicious scripts (from tickets)
Encoded commands (`powershell -enc`), downloads from unknown URLs
(`iwr ... | iex`), scripts in `%TEMP%`/`AppData` launched by Office or
scheduled tasks, obfuscated variable soup — don't run; report to security.

## Verify
Every fleet script has a repo entry, review record, pilot results, and
rollback notes; failure rate in deployment reports under the agreed
threshold.
