---
id: computing-software.digital-privacy-hygiene.two-factor-auth.phishing-resistant-mfa-and-origin-binding
name: phishing-resistant-mfa-and-origin-binding
category: computing-software
field: digital-privacy-hygiene
product: two-factor-auth
tags: [digital-privacy-hygiene, two-factor-auth, phishing-resistant-mfa, origin-binding, verifier-name-binding, channel-binding, webauthn, fido2, passkeys, nist-800-63b]
level: practitioner
status: docs-checked
description: "Understand why FIDO2/WebAuthn resists phishing (origin and RP ID binding) when TOTP, SMS and push do not, and how CISA suggests prioritising a move to it."
sources:
  - "https://pages.nist.gov/800-63-4/sp800-63b.html"
  - "https://www.cisa.gov/sites/default/files/publications/fact-sheet-implementing-phishing-resistant-mfa-508c.pdf"
  - "https://www.w3.org/TR/webauthn-2/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Phishing-resistant MFA

**Goal:** stop the attack that defeats ordinary 2FA: a phishing site that collects your password and code (CISA's example: username, password and the 6-digit app code submitted to a lookalike portal).

## The mechanism
- NIST SP 800-63B-4 (3.2.5) recognises two ways: **channel binding** (for example client-authenticated TLS as used by PIV/CAC) and **verifier name binding** (WebAuthn/FIDO2). Passwords, look-up secrets, out-of-band authenticators and OTPs are not phishing resistant.
- WebAuthn: by default the RP ID is the caller's origin's effective domain (it may be set to a registrable domain suffix); the origin must be https. The full requester origin is included in attestation and assertions so they cannot be replayed against another origin. Credentials are scoped to the Relying Party, enforced by browsers and authenticators, and a Relying Party cannot see credentials scoped to others.
- User presence (touch) is not user verification (PIN or biometric); both appear in the spec as separate checks.

## What counts (CISA)
- FIDO/WebAuthn is the only widely available phishing-resistant method; PKI-based MFA (smart cards such as PIV/CAC) is less widely available and needs mature identity management.
- WebAuthn authenticators are either roaming (separate tokens over USB or NFC) or platform (built into laptops or phones). FIDO can add PIN or biometrics on top of possession.
- CISA rates it resistant to phishing, push bombing, SS7 and SIM swap attacks.

## Rollout (CISA's prioritisation questions)
1. What do you most want to protect: email, file servers, remote access, identity servers.
2. Which users are high-value (administrators, attorneys with e-discovery access, HR).
3. Start with services that already support it (most hosted mail and SSO systems support FIDO) and an initial group such as help desk and IT admins.

## Gotchas (judgement)
- Phishing resistance is only as good as the fallbacks left enabled; remove weaker methods where the site allows.
- Recovery flows and stolen session cookies are separate bypasses not covered by the cited pages.

## Verify
- [ ] High-value accounts list a security key or passkey as a sign-in method.
- [ ] On a lookalike page the authenticator prompt does not complete.

## Checked
Method: 2026-11-08 read the CISA fact sheet PDF in full and the first ~100k characters each of the NIST page (~289k) and WebAuthn Level 2 spec (~526k); later sections (including the spec's Security Considerations) were not read. Removed as unsupported: named hardware vendors and passkey providers, the numbered personal rollout order, example lookalike domains, and the 2-authenticators-then-remove-TOTP advice.
