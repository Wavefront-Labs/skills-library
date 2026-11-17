---
id: computing-software.digital-forensics-incident-response.log-analysis.ntlm-credential-validation-event-4776
name: ntlm-credential-validation-event-4776
category: computing-software
field: digital-forensics-incident-response
product: log-analysis
tags: [4776, ntlm-authentication, windows-event-logs, dfir]
level: practitioner
status: docs-checked
description: "Investigate NTLM credential validation with event 4776: where it is logged, fields, error codes, what to monitor, and the Restrict NTLM audit setting."
sources: ["https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-10/security/threat-protection/auditing/event-4776", "https://learn.microsoft.com/en-us/windows/security/threat-protection/security-policy-settings/network-security-restrict-ntlm-audit-ntlm-authentication-in-this-domain"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# NTLM credential validation (event 4776)

Event 4776 ("The computer attempted to validate the credentials for an account") is generated every time a credential validation occurs using NTLM. It is logged only on the computer that is authoritative for the credentials: the domain controller for domain accounts, the local computer for local accounts. Audit subcategory: Credential Validation. It records both successes and failures, and also fires when a workstation is unlocked. It is not generated when a domain account logs on locally to a domain controller.

On domain controllers the main advantage is that you can see all NTLM authentication attempts for domain accounts.

## Fields
- Authentication Package: always `MICROSOFT_AUTHENTICATION_PACKAGE_V1_0` for this event.
- `TargetUserName` (Logon Account): the account whose credentials were validated; can be a user, a computer account (for example `WIN81$`) or a well-known principal such as Local System.
- `Workstation` (Source Workstation): the name of the computer the attempt came from. Only the source computer name is shown; the destination computer (for example the server a user connected to) is not in the event.
- `Status` (Error Code): `0x0` means no error.

| Status | Meaning (per Microsoft) |
|---|---|
| 0xC0000064 | The username does not exist (bad username) |
| 0xC000006A | Misspelled or bad password |
| 0xC000006D | Generic logon failure (invalid username or password, or a LAN Manager authentication level mismatch between source and target) |
| 0xC000006F | Logon outside authorised hours |
| 0xC0000070 | Logon from an unauthorised workstation |
| 0xC0000071 | Expired password |
| 0xC0000072 | Account disabled by an administrator |
| 0xC0000193 | Expired account |
| 0xC0000224 | "Change password at next logon" flagged |
| 0xC0000234 | Account locked out |

## What Microsoft suggests monitoring
- High-value accounts (domain admins, built-in local administrator, service accounts, DC accounts): watch 4776 for their `TargetUserName`.
- Accounts that should never be used (disabled, guest, inactive): alert on any 4776 for them.
- Anomalies: watch `TargetUserName` plus `Workstation` pairs, for example use outside working hours or from a computer the person should not log on from.
- Rate of failures over a time window: many bad-username events can indicate account enumeration, many bad-password events or lockouts a brute-force attack, and disabled-account, expired-account, outside-hours or unauthorised-workstation failures a compromise attempt, especially for critical accounts.
- A local account that should be used only locally: look for events where `Workstation` differs from the computer that logged the event.
- Local logon always uses NTLM when the account logs on to the device that stores it, so local-account 4776 volume is expected.

For monitoring local account logons Microsoft recommends event 4624 instead, because it carries more detail.

## NTLM audit setting
"Network security: Restrict NTLM: Audit NTLM authentication in this domain" (Computer Configuration, Windows Settings, Security Settings, Local Policies, Security Options) makes a domain controller log NTLM sign-ins that would be denied by the matching "NTLM authentication in this domain" restriction, without blocking anything; "Enable all" logs all incoming NTLM traffic to that DC. Default is Not defined, and no restart is needed. The audit events go to the operational log under Applications and Services Log, Microsoft, Windows, NTLM, not to the Security log. Restrict access to those logs and watch their size during testing.

## Verify
Findings from 4776 are corroborated by other logs from the target systems or by the NTLM operational log, since 4776 does not name the destination.

## Checked
Checked 2026-11-09 against the Microsoft Learn pages for event 4776 (description, fields, error-code table, monitoring recommendations) and the Restrict NTLM audit policy page (values, location, defaults, log location). Removed: the claim that tools send blank or random workstation names, the spraying and pass-the-hash hunting heuristics, 4624 field values (LmPackageName, KeyLength), the KQL query, the 4771 Kerberos note and NTLM operational event IDs 8001-8004, none of which the pages state.
Method: documentation only; no commands were run.
