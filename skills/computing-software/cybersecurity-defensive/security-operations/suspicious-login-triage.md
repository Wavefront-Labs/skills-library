---
id: computing-software.cybersecurity-defensive.security-operations.suspicious-login-triage
name: suspicious-login-triage
category: computing-software
field: cybersecurity-defensive
product: security-operations
tags: [alert-triage, suspicious-login-triage, impossible-travel, identity-protection, sign-in-logs, session-revocation, soc]
level: practitioner
status: docs-checked
description: "Triage suspicious sign-in alerts: impossible travel, unfamiliar location, MFA fatigue and token theft, using sign-in logs, device and user context to reach a verdict."
sources: ["https://learn.microsoft.com/en-us/entra/id-protection/concept-identity-protection-risks", "https://learn.microsoft.com/en-us/entra/identity/monitoring-health/concept-sign-ins", "https://learn.microsoft.com/en-us/azure/azure-monitor/reference/tables/signinlogs", "https://learn.microsoft.com/en-us/powershell/module/microsoft.graph.users.actions/revoke-mgusersigninsession"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Suspicious sign-in alert triage

**Goal:** decide whether a flagged sign-in is the user, a known benign pattern (VPN,
travel, mobile carrier), or an account takeover, and act before the attacker settles in.

## 1. Gather context for the sign-in
From sign-in logs (Entra `SigninLogs` table, or your identity provider's equivalent):
- IP, ASN/ISP, country; is the ASN a hosting provider or anonymiser (VPS, Tor, residential
  proxy)? Corporate VPN egress and known SASE IPs explain many "impossible travel" alerts.
- Result: success, MFA required/satisfied, which MFA method, failure codes.
- Client app and user agent: legacy authentication clients, unusual browsers, scripting user agents.
- Device: compliant/joined device ID present or not.
- Session/token details: whether Entra ID Protection flagged Anomalous Token or Token issuer
  anomaly, and whether a token was replayed from a new IP.
- Entra ID Protection risk detections worth matching to the alert: Atypical travel, Impossible
  travel, Anonymous IP address, Unfamiliar sign-in properties, Password spray.

## 2. Compare with baseline
User's usual countries, devices, working hours; recent travel (calendar or HR travel
system); new MFA method registered just before.

## 3. Patterns
- **Impossible travel** between corporate VPN and home ISP: benign if both IPs are known.
- **MFA fatigue:** many push denials then an approval at odd hours; treat approval as compromise.
- **AiTM phishing:** successful sign-in with MFA from a hosting IP shortly after the user
  clicked a link; often followed by new inbox rules or MFA method registration.
- **Password spray:** many users, few attempts each, same IP range; check if any succeeded.
- **Legacy auth success** where blocked by policy: find the gap in Conditional Access.

## 4. Act on likely compromise
1. Revoke sessions/refresh tokens (`Revoke-MgUserSignInSession` or portal), reset password,
   require re-registration of MFA if methods were added.
2. Check post-login activity: mailbox rules, forwarding, OAuth app consents, file downloads,
   MFA changes, new devices.
3. Block the IP/ASN temporarily if used in a spray.
4. Contact the user out-of-band (phone, not email/Teams which may be controlled).

## Gotchas
- Confirming with the user through the compromised channel tells the attacker.
- Mobile carriers geolocate to odd cities; geo alone is weak evidence.
- Revoke sessions as well as resetting the password, so existing refresh tokens stop working.

## Verify
Case notes record the evidence for the verdict, actions with timestamps, and a check that no
new sign-ins from the bad IPs occurred after containment.

## Checked
2026-11-09. Read: Entra ID Protection risk detections page (Atypical and Impossible travel, Anonymous
IP, Anomalous Token, Token issuer anomaly, Unfamiliar sign-in properties, Password spray), the
SigninLogs table reference and the Revoke-MgUserSignInSession cmdlet page. Removed: Okta and Google
log names, `python-requests`/`axios` user agents, IMAP/SMTP basic-auth wording, and the CISA source
(blocked, 403). Attack-pattern descriptions and response order are practitioner judgement, not
sourced figures.
Method: documentation only; no commands were run.
