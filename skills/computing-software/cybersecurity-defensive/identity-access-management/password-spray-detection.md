---
id: computing-software.cybersecurity-defensive.identity-access-management.password-spray-detection
name: password-spray-detection
category: computing-software
field: cybersecurity-defensive
product: identity-access-management
tags: [password-policy, password-spray-detection, brute-force, entra-sign-in-logs, event-4625, smart-lockout, legacy-authentication, t1110-003]
level: practitioner
status: gated
description: "Detect password spraying against Entra ID and AD: many users few attempts patterns, error codes and 4625/4771 fields, distributed sources, and the follow-up on any success."
sources: ["https://learn.microsoft.com/en-us/security/operations/incident-response-playbook-password-spray", "https://attack.mitre.org/techniques/T1110/003/", "https://learn.microsoft.com/en-us/entra/identity-platform/reference-error-codes"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Password spray detection

Spraying tries a few common passwords against many accounts to stay under lockout thresholds.
Signature: **one source (or a set of sources) -> many users -> few attempts each**.

## Entra ID (SigninLogs) (gated: unconfirmed, source is paywalled or blocked)
Useful error codes: 50126 (invalid username or password), 50053 (locked / smart lockout or malicious IP),
50055 (expired password), 50076/50074 (MFA required: password was correct!), 50057 (disabled account).
```kql
SigninLogs
| where TimeGenerated > ago(1d) and ResultType in ("50126","50053")
| summarize users=dcount(UserPrincipalName), attempts=count(), apps=make_set(AppDisplayName,5)
    by IPAddress, bin(TimeGenerated, 1h)
| where users > 20
```
Then the key follow-up: did any sprayed user succeed or reach MFA (50074/50076/0) from the same IPs?
```kql
let sprayIPs = SigninLogs | where ResultType == "50126" | summarize u=dcount(UserPrincipalName) by IPAddress | where u > 20 | project IPAddress;
SigninLogs | where IPAddress in (sprayIPs) and ResultType in ("0","50074","50076")
```
Distributed sprays rotate IPs (residential proxies): aggregate by user agent, ASN, or by the password
attempt time pattern across many IPs. Entra ID Protection raises a "Password spray" detection too.

## On-prem AD
- DCs: 4771 (Kerberos pre-auth failed, failure code 0x18) and 4625 (NTLM, status 0xC000006A bad password)
  with many distinct target account names per source IP in a window.
- AD FS / Web Application Proxy: extranet lockout settings and AD FS audit events.
- VPN, OWA, legacy endpoints are typical targets.

## Response
1. Block the sources (Conditional Access named location block, WAF, firewall) while investigating.
2. For any account with a success: treat as compromised (revoke sessions, reset password, review MFA
   and mailbox rules).
3. Check whether legacy authentication (IMAP/POP/SMTP AUTH, basic auth) was the target: block it.
4. Ban the sprayed passwords (Entra Password Protection custom banned list).

## Prevention
Phishing-resistant or at least number-matching MFA everywhere, smart lockout tuned, block legacy auth,
banned password list, and alerts above.

## Gotchas
- Users behind a single corporate egress IP make "many users per IP" noisy; exclude known egress or
  look at failure ratios.
- 50126 with usernames that do not exist in your tenant indicates enumeration lists, not your users.

## Verify
Run the queries over a known spray in the past (or a sanctioned test with a handful of test accounts)
and confirm detection and the success follow-up both return results.

## Checked

2026-10-28. Confirmed against the Entra error code reference, the Microsoft password spray playbook, event 4771 and 4625 pages and MITRE T1110.003: Entra codes 50126, 50053, 50055, 50057, 50074, 50076; 4771 failure code 0x18; 4625 status 0xC000006A; Entra ID Protection password spray detection. Gated: the KQL queries (table and column names not in the fetched pages). Removed: AD FS event ids 411/342, TargetUserName field name.

Method: documentation only; no commands were run.
