---
id: computing-software.it-support-helpdesk.user-support-communication.verifying-ai-suggested-fixes
name: verifying-ai-suggested-fixes
category: computing-software
field: it-support-helpdesk
product: user-support-communication
tags: [it-support-helpdesk, user-support-communication, ai-in-support, ai-hallucination, verification, generative-ai, script-review, source-checking, comptia-a-plus, ai-limitations]
level: practitioner
status: draft
description: "Treat AI troubleshooting answers as hypotheses: spot invented cmdlets, keys and flags, check vendor docs, sandbox-test first, and record verified sources."
sources:
  - "https://www.comptia.org/certifications/a"
  - "https://www.nist.gov/itl/ai-risk-management-framework"
  - "https://learn.microsoft.com/en-us/powershell/scripting/learn/ps101/02-help-system"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# verifying-ai-suggested-fixes

Goal: use AI to think faster without running a confidently invented command
on a user's machine (A+ 220-1202 4.10: AI limitations, hallucinations,
bias, accuracy).

## Typical hallucinations in IT answers
- PowerShell cmdlets or parameters that don't exist (`Repair-WindowsProfile`).
- Plausible registry paths/values with no effect, or the wrong hive.
- Wrong menu paths for the current Windows/Office version.
- Made-up error-code meanings and KB numbers.
- Commands that exist but do something broader (e.g. "reset network stack"
  that wipes VPN adapters).

## Verify before running
1. **Does it exist?** `Get-Command <cmdlet>`, `Get-Help <cmdlet> -Parameter
   <name>`, `<tool> /?`, `man <cmd>`. Registry: does the key exist on a test
   machine; is it documented by the vendor?
2. **Check the source**: find the vendor doc (Microsoft Learn, Apple
   Support, vendor KB) that states it. No doc = treat as untested.
3. **Understand every line** of any script — what changes, what's
   destructive (`Remove-`, `del /s`, `format`, `reg delete`), what runs as
   SYSTEM.
4. **Test** in Windows Sandbox / a VM / a test device first; take a restore
   point or backup if it touches the registry or system files.
5. **Least change**: apply the smallest step that tests the theory (A+
   method — one change at a time).

## Using AI well
Good uses: summarising long logs (after redaction), explaining an error code
you then confirm, drafting a KB article or user email you edit, generating
a script skeleton you review. Poor uses: final authority on security
settings, legal/licensing interpretation, anything you can't verify.

## In the ticket
Record the fix as verified fact with its documented source — not "AI said
so". If AI drafted a reply, you're accountable for every word.

## Verify
Every command you ran from an AI suggestion is traceable to vendor docs or
a successful sandbox test noted in the ticket.
