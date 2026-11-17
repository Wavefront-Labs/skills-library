---
id: computing-software.cybersecurity-defensive.network-defence.blocking-external-auto-forwarding
name: blocking-external-auto-forwarding
category: computing-software
field: cybersecurity-defensive
product: network-defence
tags: [email-security, external-forwarding, outbound-spam-policy, inbox-rules, exchange-online, data-exfiltration]
level: practitioner
status: docs-checked
description: "Control automatic external forwarding in Microsoft 365: outbound spam policy settings, remote domain and mail flow rule precedence, finding forwarders, and the blocked NDR."
sources: ["https://learn.microsoft.com/en-us/defender-office-365/outbound-spam-policies-external-email-forwarding"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Blocking external auto-forwarding

Automatic forwarding to external recipients can disclose information, and attackers can use that information against the organisation or its partners.

## Forwarding mechanisms (Microsoft 365)
- Users configure Inbox rules that forward to external recipients, deliberately or through a compromised account.
- Admins configure mailbox forwarding (SMTP forwarding), choosing whether to keep copies in the mailbox.
- On-premises mailboxes that forward through Microsoft 365 are subject to the same policy controls as cloud mailboxes.

## Outbound spam filter policy
Three values control automatic external forwarding:
- **Automatic - System-controlled** (the default). It originally equalled On; in 2021 it changed to Off for new organisations and for existing ones not actively using it, while organisations already using it can remain On. Behaviour differs by organisation, so set On or Off explicitly instead.
- **On - Forwarding is enabled**: external forwarding allowed, not restricted.
- **Off - Forwarding is disabled**: external forwarding is blocked and the sender gets an NDR.

Turning it off disables any Inbox rule or mailbox forwarding that redirects to external addresses. Forwarding between internal users is not affected.

## Other controls and precedence
- Remote domains can allow or block automatic forwarding to some or all external domains. Exchange mail flow (transport) rules can detect and block auto-forwarded messages from Inbox rules.
- When one setting allows forwarding and another blocks it, the block typically wins. Remote domains allowing plus policy Off: blocked. Policy On plus a blocking mail flow rule or remote domain: blocked for the affected recipients. Remote domains allowing plus policy Automatic: depends on the organisation, so avoid it.
- You can allow forwarding in the policy and use remote domains to limit which external domains users can forward to.

## Find who is forwarding
- Cloud accounts: the **Auto forwarded messages** report.
- On-premises users forwarding through Microsoft 365: create a mail flow rule in the Exchange admin center with condition message header `X-MS-Exchange-Inbox-Rules-Loop` matches `.`, an action such as setting header `X-Forwarded` to `True`, and a severity of Low, Medium or High so the transport rule report lists the users.

## Blocked-forward NDR
A blocked message returns an NDR containing: `5.7.520 Access denied, Your organization does not allow external forwarding. Please contact your administrator for further assistance.`

## Self-check
- [ ] The policy is set explicitly to Off (or On with remote domains or rules restricting it), not left on Automatic.

## Checked

Confirmed on the Microsoft Learn page on controlling automatic external email forwarding (updated 2026-08-18): mechanisms, three policy values and the 2021 change, notes, precedence table, report, mail flow rule, NDR text. The Get-InboxRule link resolved to the generic Exchange module index and the CISA PDF returned 403, so neither was used. Removed because the readable page does not state them: `Set-RemoteDomain` and Get-Mailbox/Get-InboxRule scripts, property names such as `ForwardingSmtpAddress` and `RedirectTo`, audit-log operation names, suspicious rule patterns, Power Automate and DLP notes, and quarterly exception review.

Method: docs-only read of cited pages, 2026-11-08
