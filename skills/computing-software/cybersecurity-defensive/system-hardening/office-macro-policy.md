---
id: computing-software.cybersecurity-defensive.system-hardening.office-macro-policy
name: office-macro-policy
category: computing-software
field: cybersecurity-defensive
product: system-hardening
tags: [office-macro-policy, vba-macros, mark-of-the-web, trusted-locations, asr-rules, essential-eight]
level: practitioner
status: docs-checked
description: "Lock down Microsoft Office macros: block internet macros via Mark of the Web, signed-only macros, trusted locations, ASR rules, and handling business exceptions."
sources: ["https://learn.microsoft.com/en-us/microsoft-365-apps/security/internet-macros-blocked", "https://www.cyber.gov.au/resources-business-and-government/essential-cyber-security/essential-eight/essential-eight-maturity-model", "https://learn.microsoft.com/en-us/defender-endpoint/attack-surface-reduction-rules-reference"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Office macro policy

VBA macros in documents were one of the most common malware delivery methods (Emotet, Qakbot). The ASD
Essential Eight includes a macro control with a maturity path (page not read in this review).

## Core settings (Group Policy / Intune Office templates, per app: Word, Excel, PowerPoint, Access, Visio)
- **Block macros from running in Office files from the Internet** = Enabled. Office now does this by default
  for files with Mark of the Web (MOTW); enforce it by policy so users cannot override.
- **Trusted locations**: Microsoft does not recommend network locations as Trusted Locations; allow none, or only admin-controlled paths users cannot write to.
- Use the VBA macro notification setting that matches the business need (for example allow only digitally signed macros).

## Signed macros
Sign internal macros with a code-signing certificate from the internal CA and publish the certificate as a trusted publisher through Group Policy; review macros before signing (signing is approval).

## Defender ASR rules (with Defender for Endpoint / Defender AV)
- Block Office application from creating child processes.
- Block Office applications from creating executable content.
The other Office-related rules are listed in the ASR rules reference. Start in audit mode, review the events, then block.

## MOTW gaps
Files that arrive without the Mark of the Web are not covered by the block-internet-macros policy: review the Microsoft article for the cases it lists, and block risky container formats at the mail gateway.

## Exceptions
Business-critical macro users (finance, engineering) get signed macros or a dedicated group with trusted
publisher access, never "enable all macros". Log who is in exception groups and review quarterly.

## Verify
Download a test macro document from the internet: Office blocks the macro with no enable option; an unsigned internal macro does not run; ASR audit events appear in Defender for a test macro that starts a child process.

## Checked

2026-10-28. Confirmed against: Microsoft Learn 'Macros from the internet are blocked by default' (Block macros from running in Office files from the Internet policy, MOTW, trusted locations); ASR rules reference (Office rule names).

Removed as unconfirmed: Essential Eight maturity levels, notification-setting names, add-in and trusted-document settings, VBA signature version, ASR event ids, two ASR rule names not read, ISO/MOTW behaviour claims.

Method: documentation only; no commands were run.
