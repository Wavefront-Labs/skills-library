---
id: computing-software.cybersecurity-defensive.application-security.authentication-failures
name: authentication-failures
category: computing-software
field: cybersecurity-defensive
product: application-security
tags: [authentication-failures, owasp-a07, credential-stuffing, mfa, password-policy, brute-force-protection]
level: practitioner
status: gated
description: "Fix OWASP A07 identification and authentication failures: credential stuffing defences, NIST 800-63B password rules, MFA, lockout vs throttling, and session handling."
sources: ["https://owasp.org/Top10/A07_2021-Identification_and_Authentication_Failures/", "https://pages.nist.gov/800-63-4/sp800-63b.html", "https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html", "https://cheatsheetseries.owasp.org/cheatsheets/Credential_Stuffing_Prevention_Cheat_Sheet.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Identification and authentication failures (OWASP A07:2021) (gated: unconfirmed, source is paywalled or blocked)

## Weaknesses in this category
Permitting credential stuffing and brute force; default or weak passwords; weak recovery (knowledge
questions); plaintext or weakly hashed passwords; missing or bypassable MFA; session IDs in URLs; session not
rotated on login or not invalidated on logout.

## Password rules (NIST SP 800-63B)
- NIST SP 800-63-4: a password used as the only factor must be at least 15 characters; one used only as part of MFA may be shorter but at least 8. Allow a maximum of at least 64 characters, and accept Unicode and the space character.
- **No composition rules** (forced symbols) and **no periodic forced rotation**; force change only on evidence
  of compromise.
- Reject passwords on a blocklist of commonly used, expected or compromised values (NIST SP 800-63-4) and require a different choice.

## Credential stuffing and brute force
- Throttle by account and by source (IP, device fingerprint); weigh hard account lockout (see the OWASP Authentication Cheat Sheet, Account Lockout) against the denial of service it enables against users.
- Bot detection / CAPTCHA only after risk signals.
- MFA, preferably phishing-resistant (NIST requires phishing resistance at AAL3 and recommends it at AAL2).
- Monitor: spikes of failed logins across many accounts, logins from known proxy/hosting ranges.

## Login flow details
- Same response and similar timing for unknown user vs wrong password (see account enumeration).
- Rotate the session identifier on login and privilege change; invalidate server-side on logout; idle and
  absolute timeouts.
- Re-authenticate for sensitive actions (change email/password, add payee).
- Never put session tokens in URLs.

## Verify
Automated test: repeated rapid wrong passwords for one account are throttled; a password on the breached list is rejected at signup; session ID changes after login; MFA cannot be skipped by calling the
post-MFA endpoint directly.

## Checked

2026-10-28. Confirmed: NIST SP 800-63-4 63B (15-character single-factor and 8-character MFA minimums, 64-character maximum, no composition rules, no periodic rotation, blocklist, phishing resistance by level); OWASP Authentication Cheat Sheet (account lockout section, enumeration discrepancy, composition rules). Removed: the Have I Been Pwned k-anonymity API, the exponential-backoff wording, the WebAuthn/TOTP/SMS authenticator claims, the 20-attempt figure and the example password. The A07:2021 category name could not be confirmed because the OWASP Top 10 page returned a stub, so it is gated.
Method: documentation only; no commands were run.
