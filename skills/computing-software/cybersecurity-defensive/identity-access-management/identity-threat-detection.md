---
id: computing-software.cybersecurity-defensive.identity-access-management.identity-threat-detection
name: identity-threat-detection
category: computing-software
field: cybersecurity-defensive
product: identity-access-management
tags: [itdr, identity-threat-detection-and-response, impossible-travel, mfa-fatigue, token-theft, pass-the-hash, kerberoasting, golden-ticket, oauth-consent-phishing, conditional-access, azure-ad, entra-id, risky-sign-in]
level: advanced
status: draft
description: "Detect identity-layer attacks that bypass network/endpoint controls: impossible travel, MFA fatigue, token theft and replay, Kerberoasting, and malicious OAuth consent grants."
sources: ["Microsoft - Entra ID Identity Protection risk detections (public docs)", "MITRE ATT&CK Enterprise matrix (Credential Access, Persistence)", "CISA/NSA guidance on identity-based attacks (public advisories)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Identity threat detection — the attacks that look like a normal login

**Goal:** detect the identity-layer techniques that let an attacker operate using
valid credentials or tokens — these generate no malware alert and often no
endpoint alert, because from the system's point of view it's just someone logging
in; identity telemetry is the only place they show up.

## 1. Impossible travel and anomalous sign-in properties
Flag sign-ins from the same account from geographically implausible locations
within a time window too short for travel, from a new country/ASN never seen for
that user, from a known-malicious IP/Tor exit node, or with a device/browser
fingerprint that's never been seen for that account. Cloud identity providers
(Entra ID Identity Protection, Okta ThreatInsight, AWS IAM Access Analyzer-adjacent
signals) ship this as a built-in risk score — tune the risk-level-to-action mapping
(e.g. medium risk → require re-auth with MFA, high risk → block and force password
reset) rather than leaving default thresholds, which are tuned for a generic
population, not your user base's actual travel/remote-work patterns.

## 2. MFA fatigue and push-bombing
Repeated MFA push notifications sent to a user in a short window (the attacker has
the password and is hoping the user eventually approves one out of
annoyance/confusion) is a specific, detectable pattern: alert on N+ MFA prompts to
one user within a short window, especially outside normal working hours.
Mitigate at the control layer too: switch from simple approve/deny push to
number-matching MFA (user must enter a displayed number, not just tap approve),
which defeats blind push-bombing; and cap/rate-limit MFA prompt frequency per
account.

## 3. Token theft and replay
Modern SSO issues session/refresh tokens that, once stolen (adversary-in-the-middle
phishing kits, malware token theft, a compromised endpoint), let an attacker skip
the password and MFA prompt entirely by replaying a valid token — this is why
"MFA was enabled" doesn't guarantee an account wasn't compromised. Detect via
**token/session anomalies**: a session's claimed device/location suddenly
diverging mid-session, token use from an impossible second location while the
original session is still active, or a token issued on one device being used on
another without a corresponding new-device sign-in event. Mitigate with
Conditional Access policies that bind tokens to device compliance/location where
supported, and shorten token lifetimes for high-risk applications.

## 4. Kerberoasting and golden/silver ticket abuse (on-prem AD)
Kerberoasting (requesting service tickets for accounts with weak passwords to
crack offline) shows up as a spike in TGS (service ticket) requests, especially
for accounts with SPNs set and weak/old passwords, often from one source in a
short window — hunt for abnormal Event ID 4769 volume per account/source. Golden
ticket abuse (forged Kerberos tickets using a stolen KRBTGT hash) is harder to
detect directly but shows as tickets with implausible lifetimes or for accounts
that shouldn't have that access — this is a Tier 0 compromise signal; if
confirmed, the KRBTGT password must be rotated **twice** (AD keeps the previous
key valid) and treated as a full domain-compromise incident.

## 5. Malicious OAuth consent grants
A phishing page that asks the user to "sign in with Microsoft/Google" and then
requests broad OAuth scopes (mail read, file access) on a look-alike third-party
app gets persistent access *without ever learning the password*, and survives a
password reset. Monitor and restrict user consent to third-party apps (admin
consent workflow for anything beyond a safe scope allowlist), and periodically
audit granted app consents for scope creep and unfamiliar publishers.

## Gotchas
- Impossible-travel detection breaks for users behind corporate VPN egress points
  or CGNAT that make many users appear to share one exit IP — tune for your
  network topology, not a generic cloud default.
- A risk-based Conditional Access policy that only "recommends" MFA for risky
  sign-ins (report-only mode) blocks nothing — confirm policies are in enforce
  mode, not left in evaluation/report mode after initial rollout.
- Rotating KRBTGT only once after a suspected golden ticket leaves the second,
  still-valid key usable by the attacker.
- OAuth consent audits miss anything already granted before the monitoring was
  turned on — run a one-time historical audit, not just forward monitoring.

## Verify
- [ ] Risk-based sign-in policies are confirmed in enforce mode, not report-only.
- [ ] MFA uses number-matching or equivalent, with a rate limit on push frequency.
- [ ] TGS request volume per account/source is monitored for Kerberoasting signals.
- [ ] A suspected golden ticket event triggers a double KRBTGT rotation and
      full domain-compromise incident handling.
- [ ] Third-party OAuth app consents were audited historically, not just going forward.

Related: computing-software.cybersecurity-defensive.identity-access-management.sso-and-mfa-rollout,
computing-software.cybersecurity-defensive.identity-access-management.privileged-access-management,
computing-software.cybersecurity-defensive.threat-intelligence.attack-mapping-and-ioc-handling
