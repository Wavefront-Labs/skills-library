---
id: computing-software.cloud-infrastructure-engineering.azure.conditional-access-block-legacy-authentication
name: conditional-access-block-legacy-authentication
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, conditional-access, block-legacy-auth, legacy-authentication, smtp-auth, entra-id]
level: practitioner
status: docs-checked
description: "Find and block legacy authentication (POP, IMAP, SMTP AUTH, ActiveSync basic, old Office) with a Conditional Access policy, sign-in log analysis and SMTP AUTH controls."
sources: ["https://learn.microsoft.com/entra/identity/conditional-access/policy-block-legacy-authentication", "https://learn.microsoft.com/entra/identity/conditional-access/block-legacy-authentication", "https://learn.microsoft.com/exchange/clients-and-mobile-in-exchange-online/authenticated-client-smtp-submission"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Block legacy authentication

**Goal:** remove the protocols that cannot do MFA - they cannot do MFA.

## 1. Find who still uses it
Sign-in logs > add filter *Client app* = all "Legacy authentication clients" options. Or in Log Analytics:
```kusto
SigninLogs
| where TimeGenerated > ago(30d)
| where ClientAppUsed in ("Exchange ActiveSync","IMAP4","POP3","Authenticated SMTP","Other clients","Exchange Web Services","MAPI Over HTTP","Offline Address Book","Exchange Online PowerShell")
| summarize count() by UserPrincipalName, ClientAppUsed, AppDisplayName, ResultType
```
Typical survivors: printers/scanners using SMTP AUTH, old
line-of-business apps, service accounts.

## 2. Policy (report-only first)
- Users: All users; exclude break-glass accounts (and temporarily, a named exception group).
- Target resources: All resources.
- Conditions > Client apps: **Exchange ActiveSync clients** and **Other clients** only.
- Grant: **Block access**. Start in report-only, review the impact, then move the toggle to On.

## 3. SMTP AUTH (Exchange Online)
CA blocks SMTP AUTH sign-ins, but disable it at source too:
```powershell
Set-TransportConfig -SmtpClientAuthenticationDisabled $true
Set-CASMailbox -Identity scanner@contoso.com -SmtpClientAuthenticationDisabled $false  # per-mailbox exception
```
Move devices to OAuth SMTP, direct send, or an SMTP relay connector; or Azure Communication Services email.

## Gotchas
- "Other clients" can also catch older Office clients without modern auth; check sign-in logs before enforcing.
- Customers without Conditional Access licences can use security defaults to block legacy authentication; security defaults also disable SMTP AUTH in Exchange Online.
- Exceptions must be time-bound and documented; an exception group becomes the attacker's target.

## Verify
- [ ] Report-only results show only expected failures; after enforcement, legacy-client sign-ins are blocked.
- [ ] Exception group membership reviewed and empty or justified.

## Checked

2026-10-28. Confirmed on the Entra block-legacy-authentication page and the Exchange Online SMTP AUTH page: policy checks Exchange ActiveSync clients and Other clients only, starts in report-only, then On; security defaults block legacy authentication and disable SMTP AUTH; Set-TransportConfig and Set-CASMailbox SmtpClientAuthenticationDisabled syntax. Removed: the password-spray statistic, the non-interactive log table name, the Graph JSON enum values, the review duration, the Office version and the 53003 error code (not found in fetched pages).

Method: documentation only; no commands were run.
