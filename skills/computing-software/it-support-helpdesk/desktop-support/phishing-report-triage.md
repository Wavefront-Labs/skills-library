---
id: computing-software.it-support-helpdesk.desktop-support.phishing-report-triage
name: phishing-report-triage
category: computing-software
field: it-support-helpdesk
product: desktop-support
tags: [it-support-helpdesk, desktop-support, workstation-security, phishing-triage, report-phishing, message-headers, defender-for-office-365, credential-compromise, revoke-sessions, social-engineering, comptia-a-plus]
level: practitioner
status: draft
description: "Triage phishing reports: what the user did, header and URL checks, tenant-wide removal of the message, and containment steps for compromised accounts."
sources:
  - "https://learn.microsoft.com/en-us/defender-office-365/submissions-users-report-message-add-in-configure"
  - "https://learn.microsoft.com/en-us/defender-office-365/threat-explorer-real-time-detections-about"
  - "https://learn.microsoft.com/en-us/security/operations/incident-response-playbook-phishing"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# phishing-report-triage

Goal: every reported phish gets a fast, consistent answer, and the users who
did more than look at it get contained quickly.

## First question: what did the user do?
| Action | Risk | Desk response |
|---|---|---|
| Only received/reported | low | thank, confirm it's removed |
| Clicked link, entered nothing | medium | check URL; browser/EDR alert check |
| **Entered credentials** | high | reset password, revoke sessions, review MFA methods and inbox rules, sign-in logs — security incident |
| **Approved an unexpected MFA prompt** | high | same as above |
| Opened attachment / enabled macros | high | isolate device, EDR scan, security incident |
| Replied / sent money/gift cards/data | high | security + finance/legal per process |

## Reporting path
Users report with the built-in **Report** button (Outlook) → goes to
Microsoft Defender submissions and your security mailbox. Don't ask users to
forward as attachments to the desk unless that's the process.

## Analyse (desk level)
- Sender address vs display name; reply-to differs; lookalike domains.
- **Headers** (Message header analyzer): SPF/DKIM/DMARC results,
  originating IP.
- Links: hover/preview, check reputation in a safe tool (never click on a
  production machine); Safe Links rewritten URLs.
- Attachments: don't open; submit to sandbox/Defender.

## Containment for the tenant
- Threat Explorer/Real-time detections (Defender for Office 365): find all
  recipients of the same message → **soft delete / move to junk** for all
  (or Content search + purge where licensed and permitted).
- Block sender/domain/URL in the Tenant Allow/Block List.
- Check who clicked (URL click reports).

## Compromised account steps (escalate to security)
Reset password, **Revoke-MgUserSignInSession**, remove unknown MFA methods,
check inbox rules (forwarding to external, delete rules), check
OAuth app consents, review sign-ins/audit log, notify contacts if mail was
sent from the account.

## Gotchas
- Shaming users kills reporting; thank every report.
- Simulated phishing (training) emails: know how to recognise them so you
  don't purge or escalate the security team's own campaign.

## Verify
Message removed from all mailboxes, sender blocked, users who clicked/entered
credentials have documented containment actions.
