---
id: computing-software.it-support-helpdesk.intune-mdm.attack-surface-reduction-rules
name: attack-surface-reduction-rules
category: computing-software
field: it-support-helpdesk
product: intune-mdm
tags: [it-support-helpdesk, intune-mdm, attack-surface-reduction, asr, defender-antivirus, endpoint-security, audit-mode, exclusions, intune]
level: advanced
status: docs-checked
description: "Roll out Defender attack surface reduction rules from Intune: audit before block, standard protection rules, per-rule exclusions, merge behavior, rules that block business apps."
sources:
  - "https://learn.microsoft.com/en-us/defender-endpoint/attack-surface-reduction-rules-reference"
  - "https://learn.microsoft.com/en-us/defender-endpoint/attack-surface-reduction-rules-deployment"
  - "https://learn.microsoft.com/en-us/mem/intune/protect/endpoint-security-asr-policy"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# attack-surface-reduction-rules

ASR rules target risky software behaviour that malware commonly uses (scripts that
download files, obfuscated scripts, code injection). They are a Microsoft Defender
Antivirus feature available on any Windows edition that includes it (for example
Windows 11 Home), configurable locally with PowerShell or Group Policy. Defender for
Endpoint adds centralized management, reporting and alerting through Intune,
Configuration Manager and the Defender portal.

## Intune prerequisites
Windows devices with Defender Antivirus as the primary antivirus. Policies live in the
Intune admin center under Endpoint security > Attack surface reduction (platform
Windows, profile **Attack Surface Reduction Rules**). Windows Server is supported through
the Defender for Endpoint security settings management scenario, where only the ASR
rules profile is supported.

## Rule modes
Not configured, **Audit** (log only), **Block**, and **Warn** (not every rule supports it:
the LSASS credential rule and "Block Office applications from injecting code into other
processes" do not).

## Deployment sequence
1. Standard protection rules can normally be enabled in Block or Warn without testing.
   Test the other rules in Audit mode first (the deployment guide splits this into plan,
   test, enable, manage and monitor, using deployment rings).
2. Standard protection rules: **Block abuse of exploited vulnerable signed drivers
   (Device)**, **Block credential stealing from the Windows local security authority
   subsystem**, **Block persistence through WMI event subscription**.
3. Review audit results in the Defender portal's ASR rules report or advanced hunting.
   Hunting action types follow the pattern `AsrOfficeChildProcessAudited` /
   `AsrOfficeChildProcessBlocked` (each rule has its own pair in the reference page).
4. Add exclusions only for confirmed business needs, then move to Block in rings.

## Rules that commonly need attention
- **Block all Office applications from creating child processes** (GUID
  d4f940ab-401b-4efc-aadc-ad5f3c50688a): some legitimate line-of-business apps spawn
  child processes such as Command Prompt or PowerShell; enforced only when Office is
  installed under %ProgramFiles% or %ProgramFiles(x86)%.
- **Block executable files from running unless they meet a prevalence, age, or trusted
  list criterion** (01443614-cd74-433a-b99e-2ecdc07bfc25): needs cloud-delivered protection.
- **Block process creations originating from PSExec and WMI commands**
  (d1e49aac-8f56-4280-b9ba-993a6d77406c): if you use Configuration Manager, do not
  enable this rule with other deployment methods; the ConfigMgr client relies heavily on WMI.
- **Block persistence through WMI event subscription**: test extensively in Audit with ConfigMgr.
- **Block credential stealing from LSASS**: very large volume of audit events, almost all
  safe to ignore; Microsoft allows skipping Audit and starting Block on a small device
  set. Not needed if LSA protection is enabled. No Warn mode.
- **Block use of copied or impersonated system tools**: can also block legitimate
  third-party executables run from nondefault paths; the block does not prove malice.
- **Use advanced protection against ransomware**: errs on the side of caution and blocks
  files without a positive reputation; add a per-rule exclusion if blocks do not resolve.

## Supporting a blocked user
1. Get the time and the app name.
2. Identify the rule: the reference page lists each rule's Intune name, GUID and
   advanced hunting action types. Decide: legitimate, then request an exclusion for the
   specific file or folder; suspicious, then treat as a security incident.
3. Some rules show notifications or EDR alerts only at certain cloud protection levels
   (Adobe Reader, email executable content and JavaScript/VBScript rules: EDR alerts need
   High plus or Zero tolerance; pop-ups need High, High plus or Zero tolerance).

## Gotchas
- Intune offers two exclusion settings: global **Attack Surface Reduction Only
  Exclusions** (applies to every ASR rule on the device, because devices receive a
  superset of settings from all policies) and **ASR Only Per Rule Exclusions** (per rule;
  default Not configured). Prefer per-rule.
- Some rules have only limited exclusion support (see "File and folder exclusions for ASR rules").
- Intune merges ASR settings from Endpoint security ASR policy, endpoint protection
  profiles and the Defender for Endpoint baseline: non-conflicting settings are merged;
  conflicting settings are held back, not deployed.
- Office rules that require restart: "Block Office applications from injecting code into
  other processes" needs Microsoft 365 Apps restarted.

## Verify
In the Intune policy status the device reports the ASR policy as successful, and a test
trigger of a rule in Audit mode produces the rule's `...Audited` hunting action type.

## Checked
Date: 2026-11-07. Read in full: the ASR rules reference (OS support, deployment method,
alerts and per-rule details), the ASR deployment guide, and the Intune ASR policy article.
Not opened: the linked ASR test, enable and report articles, and the Defender CSP.
Removed as unconfirmed: the 24-hour Warn bypass, "2-4 weeks" pilot, the KQL query and
Defender portal menu path, event IDs 1121/1122/1129, the Windows Security toast text,
the `Get-MpPreference` check, "wildcard path" exclusion advice, the "Conflict" status
wording (page describes merge behaviour instead), and the Microsoft test page
Verify step. Corrected: PSExec/WMI note (page says do not enable with other methods
under ConfigMgr, not that it "breaks" ConfigMgr).
Method: documentation only; no commands were run.
