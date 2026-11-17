---
id: computing-software.cybersecurity-defensive.network-defence.mail-flow-rules
name: mail-flow-rules
category: computing-software
field: cybersecurity-defensive
product: network-defence
tags: [mail-flow-rules, exchange-transport-rules, external-sender-banner, mail-flow, email-security, data-loss-prevention, rule-abuse-detection]
level: practitioner
status: docs-checked
description: "Use Exchange mail flow (transport) rules for security: external tagging, blocking risky attachments, auto-forward controls, rule hygiene and detecting malicious rule changes."
sources: ["https://learn.microsoft.com/en-us/exchange/security-and-compliance/mail-flow-rules/mail-flow-rules", "https://learn.microsoft.com/en-us/exchange/security-and-compliance/mail-flow-rules/mail-flow-rule-actions", "https://learn.microsoft.com/en-us/powershell/module/exchange/set-externalinoutlook"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Mail flow rules

## Useful security rules
| Rule | Notes |
|---|---|
| External sender identification | Prefer native `Set-ExternalInOutlook -Enabled $true` (Outlook "External" tag) over body banners that break DKIM/S/MIME signatures and clutter replies |
| Block risky attachments | Transport rule with `AttachmentExtensionMatchesWords` for extra file types |
| Block auto-forwarding externally | Transport rule using the `MessageTypeMatches` and `SentToScope` conditions |

## Create (PowerShell)
```
New-TransportRule -Name "Block risky attachment types" -Priority 0 `
  -AttachmentExtensionMatchesWords exe,js,hta,iso,img,vhd,one `
  -RejectMessageReasonText "Attachment type blocked" -RejectMessageEnhancedStatusCode 5.7.1 `
  -Mode Enforce -SetAuditSeverity High
```
Test in `-Mode AuditAndNotify` first; rule priority order matters (see `-StopRuleProcessing`).

## Hygiene and monitoring
- Rules that bypass filtering (`SetSCL -1`, skip spam filtering by sender domain or IP) are a phishing hole; review them and prefer connectors/allow lists with authentication checks.
- Rules that BCC or redirect mail (`BlindCopyTo`, `RedirectMessageTo`, `AddToRecipients`) can be abused by an attacker with Exchange admin rights; review rule changes.
- Export your rules regularly so changes can be compared.

## Verify
- [ ] Test message with a blocked attachment rejected with the custom NDR.
- [ ] No rule sets SCL -1 based on sender domain alone.
- [ ] Alert on transport rule changes tested.

## Checked

2026-10-28. Confirmed against: Microsoft Learn mail flow rules, mail flow rule actions, New-TransportRule reference (parameters in the example, SetSCL, BlindCopyTo, RedirectMessageTo, AddToRecipients), Set-ExternalInOutlook.

Removed as unconfirmed: anti-malware filter advice, outbound spam policy setting name, impersonation/DLP/encryption rows, Unified Audit Log alerting, Get-TransportRule export command.

Method: documentation only; no commands were run.
