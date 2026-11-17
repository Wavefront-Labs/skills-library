---
id: computing-software.cybersecurity-defensive.identity-access-management.token-protection
name: token-protection
category: computing-software
field: cybersecurity-defensive
product: identity-access-management
tags: [token-protection, token-binding, primary-refresh-token, aitm-phishing, session-hijacking, conditional-access, cloud-identity, token-binding-and-protection]
level: advanced
status: docs-checked
description: "Reduce token theft and replay: Entra token protection (sign-in session binding), compliant-device CA, CAE, phishing-resistant MFA against AiTM, and detecting replayed tokens."
sources: ["https://learn.microsoft.com/en-us/entra/identity/conditional-access/concept-token-protection", "https://learn.microsoft.com/en-us/entra/identity/devices/concept-primary-refresh-token", "https://www.microsoft.com/en-us/security/blog/2022/11/16/token-tactics-how-to-prevent-detect-and-respond-to-cloud-token-theft/"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Token protection

After MFA, the session is a bearer token or cookie. Adversary-in-the-middle phishing, infostealer
malware and pass-the-cookie bypass MFA entirely by stealing it.

## Controls (Entra)
1. **Token protection** Conditional Access session control: requires sign-in session tokens to be cryptographically bound to the device (PRT-bound) for supported clients and resources (see the token protection page for the current list). Start in report-only, scope to supported platforms/apps, exclude unsupported clients or they are blocked.
2. **Require compliant or hybrid-joined device** for sensitive apps: a stolen cookie replayed from an attacker's machine fails the device check.
3. **Phishing-resistant MFA** (FIDO2/passkeys, WHfB, CBA): AiTM proxies cannot relay origin-bound WebAuthn.
4. **CAE** (continuous access evaluation): access is re-evaluated during active sessions.
5. Short sign-in frequency for unmanaged devices; disable persistent browser sessions.

## Detection
- Entra ID Protection risk detections: "Anomalous token", "Token issuer anomaly", "Attacker in the middle", "Unfamiliar sign-in properties".
- Sign-ins where the session ID appears from two distant IPs/ASNs; non-interactive sign-ins from hosting providers.

## Response
Revoke sign-in sessions, reset password, review mailbox rules and MFA methods
added, remove malicious OAuth grants; the infected device (infostealer) must be reimaged.

## Gotchas
- Token protection coverage is limited to certain clients/platforms; check current support before enforcing broadly.
- Browser cookies on unmanaged devices are not bindable; compliant-device requirements are the stronger control.

## Verify
- [ ] Report-only results show no unexpected blocks before enforcing.
- [ ] Replay test: cookie exported from a managed device fails on an unmanaged one.

## Checked

2026-10-28. Confirmed against the Entra token protection, PRT and ID Protection pages: token protection is a Conditional Access session control accepting only device-bound sign-in session tokens (PRTs), report-only mode, continuous access evaluation, detections Anomalous Token, Token issuer anomaly and Attacker in the Middle. Removed: named supported client list, Revoke-MgUserSignInSession name, Defender XDR cookie alerts, Global Secure Access bullet, strict location enforcement wording.

Method: documentation only; no commands were run.
