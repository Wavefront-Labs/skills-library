---
id: computing-software.cybersecurity-defensive.identity-access-management.entra-id-protection-risk-policies
name: entra-id-protection-risk-policies
category: computing-software
field: cybersecurity-defensive
product: identity-access-management
tags: [entra-id, entra-id-protection, user-risk, sign-in-risk, risk-based-conditional-access, risky-users, self-remediation]
level: practitioner
status: docs-checked
description: "Use Entra ID Protection well: user vs sign-in risk detections, risk-based Conditional Access with self-remediation, investigating risky users, and dismiss vs confirm compromised."
sources: ["https://learn.microsoft.com/en-us/entra/id-protection/overview-identity-protection", "https://learn.microsoft.com/en-us/entra/id-protection/concept-identity-protection-risks", "https://learn.microsoft.com/en-us/entra/id-protection/howto-identity-protection-configure-risk-policies"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Entra ID Protection risk policies

Full detections require Entra ID P2 (some are available without it). Two risk types:
- **Sign-in risk**: this authentication looks suspicious (anonymous IP/Tor, atypical travel,
  unfamiliar sign-in properties, malicious IP, password spray, AiTM-related token anomalies).
- **User risk**: the account is likely compromised (leaked credentials found by Microsoft, anomalous
  user activity, Microsoft threat intel, admin confirmed compromised).

## Policies (configure in Conditional Access, not the legacy ID Protection policies)
1. **Sign-in risk medium and above** -> Require MFA (authentication strength), sign-in frequency
   every time. Users satisfy MFA and the risk is remediated.
2. **User risk high** -> Require password change (with MFA). Self-remediation for password-hash-synced
   or cloud users; for federated/on-prem password users check the risk policy article for the
   on-premises remediation requirements.
3. Admins: stricter thresholds (low+), or block on high sign-in risk.
Exclude break-glass accounts; start in report-only.

## Investigating
- Risky users / Risky sign-ins / Risk detections reports, or the Graph `riskyUsers` API.
- For a risky user: review detections (type, IP, location, app), sign-in logs around them, MFA method
  changes, mailbox rules, OAuth consents, new devices.
- With logs in Sentinel/Log Analytics, query the risk and sign-in tables for risky users and sign-ins.

## Actions
- **Confirm user compromised**: sets user risk high (triggers policy) and feeds Microsoft's models;
  then revoke sessions, reset password, review MFA methods.
- **Dismiss user risk**: when investigation shows benign (e.g. travel). Dismissal is not remediation;
  do not dismiss to make noise go away without checking.
- **Confirm sign-in safe / compromised** to tune detections.

## Gotchas
- Self-remediation by password change does not evict an attacker who already registered MFA or
  holds refresh tokens/OAuth grants; for confirmed compromise do the full response.
- Workload identities have separate risk (ID Protection for workload identities, premium).
- Offline detections are calculated after the sign-in; user risk can rise after the sign-in succeeded.
- VPN/egress IP changes generate atypical travel noise; mark trusted named locations.

## Verify
Sign in from Tor in a test account: sign-in risk recorded and MFA required; mark a test user
compromised: forced secure password change at next sign-in.

## Checked

2026-10-28. Confirmed against the ID Protection overview, risk detections and risk policy pages: P2 for full detections, riskyUsers API, Anomalous Token, Token issuer anomaly, Attacker in the Middle, Leaked credentials, Password spray detections, offline detections. Removed: on-premises password change setting name, riskDetections API name, KQL table names, 'hours later' offline claim.

Method: documentation only; no commands were run.
