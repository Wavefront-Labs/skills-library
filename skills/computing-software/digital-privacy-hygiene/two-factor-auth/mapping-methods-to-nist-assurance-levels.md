---
id: computing-software.digital-privacy-hygiene.two-factor-auth.mapping-methods-to-nist-assurance-levels
name: mapping-methods-to-nist-assurance-levels
category: computing-software
field: digital-privacy-hygiene
product: two-factor-auth
tags: [digital-privacy-hygiene, two-factor-auth, authenticator-assurance-level, mfa-strength-ranking, phishing-resistant-mfa]
level: practitioner
status: docs-checked
description: "Map authentication methods to NIST SP 800-63B-4 AAL1, AAL2 and AAL3, including syncable authenticators and biometrics, to set a target level per important account."
sources:
  - "https://pages.nist.gov/800-63-4/sp800-63b.html"
  - "https://www.cisa.gov/sites/default/files/publications/fact-sheet-implementing-phishing-resistant-mfa-508c.pdf"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Mapping methods to NIST assurance levels

**Goal:** use the federal standard's vocabulary to decide which accounts need which strength.

## The levels (SP 800-63B-4, section 2)
| AAL | Permitted | Key requirements |
|---|---|---|
| AAL1 | Password, look-up secret, out-of-band, single-factor OTP or cryptographic, or any AAL2/AAL3 type | Single or multi-factor; verifiers SHOULD offer multi-factor. Phishing resistance not required; key export permitted |
| AAL2 | Multi-factor cryptographic, out-of-band or OTP; or a physical authenticator (look-up secret, out-of-band, single-factor OTP or cryptographic) plus a password or biometric comparison | Replay resistance required; intent SHOULD be shown; verifiers SHALL offer at least one phishing-resistant option; key export permitted |
| AAL3 | Multi-factor cryptographic, or single-factor cryptographic plus a password or biometric comparison | Non-exportable private key, phishing resistance, replay resistance, intent, FIPS 140 Level 1 overall; key export prohibited |

Reauthentication: AAL1 SHOULD be at most 30 days; AAL2 at most 24 hours overall and 1 hour inactivity (SHOULD); AAL3 SHALL be at most 12 hours overall, inactivity 15 minutes (SHOULD).

## Notes from the standard
- Syncable authenticators need exportable keys: allowed at AAL1 and AAL2, SHALL NOT be used at AAL3. Appendix B conditions were not read in this review.
- PSTN (SMS/voice) out-of-band is "restricted"; email SHALL NOT be used for out-of-band authentication (recovery and validation codes are exempt).
- Biometrics only count as part of multi-factor with a physical authenticator, a non-biometric alternative must be offered, and local comparison is preferred.
- Phishing resistance means cryptographic authentication with channel binding (PIV/CAC-style TLS) or verifier name binding (WebAuthn/FIDO2); passwords, look-up secrets, out-of-band and OTPs are not phishing resistant. CISA agrees: FIDO/WebAuthn is the only widely available phishing-resistant option, with PKI-based MFA less widely available.

## Personal targets (judgement, not from the sources)
| Account | Target |
|---|---|
| Primary email, password manager, platform account | AAL3-like: hardware security keys |
| Bank, registrar, work SSO | AAL2 with a phishing-resistant method |
| Shopping, social | AAL2 |
| Low-value forums | AAL1 with a unique password |

## Gotchas
- AAL describes the authentication event; weak account recovery undermines any level.

## Checked
Method: 2026-11-08 read section 2 and parts of section 3 of the NIST page (first ~100k of ~289k characters; Appendix B not read) and the CISA fact sheet PDF. Removed as unsupported: the typical-methods examples (passkey alone, TPM device-bound passkey, FIDO2 key with PIN) as AAL assignments, and "warn users" about SMS.
