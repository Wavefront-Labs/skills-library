---
id: computing-software.digital-privacy-hygiene.two-factor-auth.ranking-mfa-methods-by-strength
name: ranking-mfa-methods-by-strength
category: computing-software
field: digital-privacy-hygiene
product: two-factor-auth
tags: [digital-privacy-hygiene, two-factor-auth, mfa-strength-ranking, mfa, 2fa, nist-800-63b, aal2, aal3, sms-2fa, totp, push-notifications, security-keys, passkeys]
level: intro
status: docs-checked
description: "Rank the second factors a site offers (SMS, email, push, TOTP, FIDO2 key) by what they stop, using CISA's table, NIST 800-63B-4 and Privacy Guides, and drop the weak ones."
sources:
  - "https://pages.nist.gov/800-63-4/sp800-63b.html"
  - "https://www.cisa.gov/sites/default/files/publications/fact-sheet-implementing-phishing-resistant-mfa-508c.pdf"
  - "https://www.privacyguides.org/en/basics/multi-factor-authentication/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Ranking MFA methods by strength

**Goal:** when a site offers several options, know which to choose and which to remove.

## CISA's order (strongest to weakest)
| Method | Phishing | Push bombing | SS7 / SIM swap |
|---|---|---|---|
| FIDO/WebAuthn, PKI-based | resistant | not applicable | not applicable |
| App OTP, token OTP, push with number matching | vulnerable | resistant | not applicable |
| Push without number matching | n/a | vulnerable (and user error) | not applicable |
| SMS or voice | vulnerable | n/a | vulnerable |
CISA calls SMS/voice a last resort and a temporary bridge, and phishing-resistant MFA the "gold standard"; any MFA still beats none. CISA says FIDO/WebAuthn is the only widely available phishing-resistant option.

## Privacy Guides order (weakest to strongest)
SMS, email codes, app push, TOTP, Yubico OTP, FIDO2/WebAuthn.
- SMS and email: SIM swapping or email takeover exposes codes.
- Push: risk of accidental approval; prompts often go to all devices.
- TOTP: reasonable, but a code captured by a fake site works until it expires (about 60 seconds).
- Yubico OTP: not phishing resistant; public ID reused across sites can enable profiling.
- FIDO2/WebAuthn: most secure and private; the signature includes the site's origin; keys are not linkable across sites.
- Your MFA is only as strong as the weakest method you leave enabled: with TOTP, disable SMS and email; with FIDO2, drop Yubico OTP and TOTP on that account. Keep backups (a pair of keys; TOTP recovery keys).

## NIST SP 800-63B-4 points
- Phishing resistance needs cryptographic authentication with channel binding (for example PIV/CAC) or verifier name binding (WebAuthn/FIDO2). Passwords, look-up secrets, out-of-band and OTPs are not phishing resistant.
- PSTN (SMS/voice) out-of-band is "restricted"; email SHALL NOT be used for out-of-band authentication (recovery and validation codes are exempt).
- Verifiers SHALL offer at least one phishing-resistant option at AAL2. AAL3 needs a non-exportable key and phishing resistance, so syncable authenticators SHALL NOT be used at AAL3.
- Compare-and-approve push is no longer acceptable; the secret must be transferred between device and primary channel.

## Picking per account
1. Use the strongest offered; remove weaker methods you do not need.
2. Keep a recovery path that does not depend on the same device.

## Verify
- [ ] Email, bank, vault and carrier accounts use the strongest available method.
- [ ] SMS and email removed where a stronger method plus backups exist.

## Checked
Method: 2026-11-08 read the CISA fact sheet (PDF) and Privacy Guides page in full; NIST SP 800-63B-4 was read via the first ~100k characters of a ~289k-character page (sections 2.2, 2.3, 3.1.2, 3.1.3, 3.2.5), the remainder not read. Removed: the seven-rank table, "AAL3-capable" claims for device-bound passkeys, "stops SIM swap" for email, and the "even SMS blocks the overwhelming majority" claim.
