---
id: computing-software.digital-forensics-incident-response.incident-response-process.investigating-malicious-inbox-rules-and-forwarding
name: investigating-malicious-inbox-rules-and-forwarding
category: computing-software
field: digital-forensics-incident-response
product: incident-response-process
tags: [inbox-rules, mail-forwarding-rules, outlook-forms, exchange-online, m365, dfir]
level: practitioner
status: docs-checked
description: "Find and remove malicious Outlook inbox rules and custom forms in Exchange mailboxes after account compromise, using Microsoft's documented PowerShell and indicators."
sources: ["https://learn.microsoft.com/en-us/defender-office-365/detect-and-remediate-outlook-rules-forms-attack", "https://learn.microsoft.com/en-us/security/operations/incident-response-playbook-phishing"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Investigating malicious inbox rules and forwarding

**Goal:** after an attacker has signed in to a mailbox, find rules and custom forms they
left as a foothold, capture evidence, and remove them.

## Why it matters
Microsoft describes Outlook rules and custom forms as two persistence mechanisms. A fresh
Outlook install or a new computer does not help: when Outlook reconnects to the mailbox, the
rules and forms synchronise from the cloud. In the documented attack a forwarding rule fires
when a trigger message arrives and its action launches an application on a remote (WebDAV)
server, which typically installs malware. Current Outlook client defaults block both
mechanisms, so patched clients are not vulnerable, but the rules still need finding and
removing.

## Indicators (from Microsoft's page)
- Rules: the action starts an application, or references an EXE, ZIP or URL; new process
  starts originate from the Outlook process ID on the local machine.
- Forms: custom forms saved as their own message class, a message class containing
  executable code, typically in the Personal Forms Library or Inbox folders, named
  IPM.Note.[custom name]. Custom forms are rare, so any at all deserve a look, especially
  hidden ones.

## Enumerate
Connect to Exchange Online PowerShell, then:
```powershell
Get-InboxRule -Mailbox laura@contoso.onmicrosoft.com
Get-InboxRule -Mailbox laura@contoso.onmicrosoft.com -Identity "Suspicious Rule Name" | Format-List
```
For the whole tenant, Microsoft points to the `Get-AllTenantRulesAndForms.ps1` script, which
writes `MailboxRulesExport-yyyy-MM-dd.csv` and `MailboxFormsExport-yyyy-MM-dd.csv`.
The page notes the script repository is archived and that lines 154 to 158 use a connection
method that no longer works, so remove them and connect to Exchange Online PowerShell
first. It needs Global Administrator or Organization Management; prefer the least
privileged role that works. In the rules CSV, treat a rule as likely malicious if
ActionType is ID_ACTION_CUSTOM, IsPotentiallyMalicious is TRUE, or ActionCommand holds an
application, an .exe or .zip file, or an unknown URL.

## Remediate
Export or record the rule first as evidence, then:
```powershell
Disable-InboxRule -Mailbox laura@contoso.onmicrosoft.com -Identity "Suspicious Rule Name"
Remove-InboxRule -Mailbox laura@contoso.onmicrosoft.com -Identity "Suspicious Rule Name"
```
Disable lets you stop a rule processing while you investigate. Microsoft also says:
identify every device the user has used Outlook on and clean them; do not let the user
sign in and use email until all devices are clean; once offline copies of the mailbox are
removed, reset the password to a high-quality value and turn on MFA if it is not already
on; install current Outlook versions.

## Context from the phishing playbook
Microsoft's phishing investigation playbook lists "reviewing mailbox rules and forwarding
settings" under recovery, and says mailbox auditing and the unified audit log should be
available to investigators before an incident. Revoke active sessions and tokens and
reset or disable the compromised account as part of containment.

## Verify
Re-run the enumeration after removal and confirm no suspicious rules or forms remain.

## Checked
Dated 2026-11-08. Confirmed against "Detect and remediate Outlook rules and custom forms
injection attacks" (attack pattern, indicators, CSV columns, script caveats, Get-, Disable-
and Remove-InboxRule, remediation steps) and the "Phishing investigation playbook" (rule
and forwarding review in recovery, auditing prerequisites, revoke sessions). Removed as not
stated by either page: -IncludeHidden, the Get-Mailbox forwarding properties, transport
rule queries, Search-UnifiedAuditLog operation names, AutoForwardingMode, and the
red-flag rule names and keywords.
Method: docs-only read of cited pages, 2026-11-08
