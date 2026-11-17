---
id: computing-software.digital-forensics-incident-response.disk-memory-forensics.password-spraying-and-brute-force-evidence
name: password-spraying-and-brute-force-evidence
category: computing-software
field: digital-forensics-incident-response
product: disk-memory-forensics
tags: [password-spraying, credential-theft, windows-event-logs, sign-in-logs, dfir]
level: practitioner
status: draft
description: "Distinguish password spraying from brute force in AD and Entra logs: 4625/4771/4776 patterns, status codes, smart lockout, sources, and the successful hit."
sources: ["https://attack.mitre.org/techniques/T1110/003/", "https://learn.microsoft.com/en-us/windows/security/threat-protection/auditing/event-4625", "https://learn.microsoft.com/en-us/entra/identity/authentication/howto-password-smart-lockout"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Password spraying and brute force evidence

**Goal:** spraying tries a few common passwords against many accounts (staying under lockout);
brute force tries many passwords against one account. Find the source, the targets, and above all
any success.

## Active Directory
| Event | Where | Use |
|---|---|---|
| 4625 | Member/DC (NTLM/interactive) | Failed logon: Status/SubStatus `0xC000006A` bad password, `0xC0000064` no such user, `0xC0000234` locked out |
| 4771 | DC (Kerberos pre-auth) | Failure code `0x18` bad password; `0x6` unknown user |
| 4776 | DC (NTLM validation) | Error `0xC000006A` |
| 4740 | DC | Account locked out (caller computer name) |
| 4624 / 4768 | | The success you are looking for |

Spray signature: one source IP/workstation, many distinct `TargetUserName`, 1-3 attempts each,
in a burst, repeated every lockout window (e.g. 30-60 min).
```kusto
SecurityEvent | where EventID in (4625, 4771)
| summarize users=dcount(TargetUserName), attempts=count(), first=min(TimeGenerated) by IpAddress, bin(TimeGenerated, 30m)
| where users > 20
```
Then search for 4624/4768 successes for the targeted users from the same source shortly after.

## Entra ID / Microsoft 365
- Sign-in logs: `ResultType 50126` (invalid username or password), `50053` (smart lockout /
  malicious IP), `50055` expired password, success `0`. Spray via legacy auth (`ClientAppUsed` = IMAP/SMTP/Exchange ActiveSync) bypasses MFA in tenants without legacy-auth blocking.
- Identity Protection "Password spray" risk detection.
- Many sprays rotate IPs (residential proxies, cloud functions); group by user agent and time pattern instead of IP.

## Response
- Reset passwords of accounts that had a successful sign-in from the spray infrastructure and review their activity.
- Block legacy authentication; enforce MFA; ban common passwords (Entra Password Protection on-prem too).

## Gotchas
- Kerberos pre-auth failures appear only on DCs; collect all DCs' logs.
- Event 4625 from a server shows the server as the source when it proxies authentication (e.g. Exchange, ADFS); look at its own logs for the real client IP.

## Verify
List of targeted accounts, success/failure per account, and actions taken for each success.
