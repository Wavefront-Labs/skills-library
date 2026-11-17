---
id: computing-software.digital-privacy-hygiene.vpn-tools.openpgp-keys-for-email
name: openpgp-keys-for-email
category: computing-software
field: digital-privacy-hygiene
product: vpn-tools
tags: [digital-privacy-hygiene, vpn-tools, openpgp, gpg, email-encryption, thunderbird-openpgp, keys-openpgp-org, wkd, key-fingerprint, revocation-certificate, email-privacy]
level: advanced
status: gated
description: "Generate an OpenPGP key, publish it (keys.openpgp.org, WKD), encrypt email with Thunderbird or gpg, verify fingerprints, and keep a revocation certificate."
sources:
  - "https://support.mozilla.org/en-US/kb/openpgp-thunderbird-howto-and-faq"
  - "https://www.gnupg.org/gph/en/manual.html"
  - "https://keys.openpgp.org/about/usage"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# OpenPGP keys for email

**Goal:** end-to-end encrypt email with someone who requires PGP (journalists, security
teams, bug bounty programmes), without the classic mistakes.

## Generate (GnuPG)
```bash
gpg --quick-generate-key "Alice Example <alice@example.org>" ed25519 sign,cert 2y
gpg --quick-add-key <FINGERPRINT> cv25519 encr 2y
gpg --list-keys --fingerprint alice@example.org
gpg --output alice-revoke.asc --gen-revoke alice@example.org   # store offline
```
(GnuPG 2.1+ creates a revocation certificate automatically in `openpgp-revocs.d/`.)
Back up the secret key: `gpg --export-secret-keys --armor alice@example.org > secret.asc`
into an encrypted container or onto paper/hardware token.

## Thunderbird (built-in OpenPGP, no Enigmail)
Account Settings > End-To-End Encryption > Add Key > create or import. Compose window:
Security > Require Encryption; Digitally Sign.

## Publish and find keys
- Upload to **keys.openpgp.org** and confirm the email verification so others can find it
  by address: `gpg --keyserver hkps://keys.openpgp.org --send-keys <FINGERPRINT>`.
- If you own the domain, **WKD** (Web Key Directory) lets clients fetch the key from
  your site.

## Verify fingerprints
Compare the full fingerprint with the person over another channel (call, in person,
their verified website). Mark as accepted (Thunderbird: Key Manager > Key Properties >
"Yes, I've verified in person").

## Limits
- Subject lines and metadata aren't encrypted (some clients hide subjects).
- One plaintext reply breaks it; agree on discipline.
- Losing the private key means old encrypted mail is unreadable.

## Verify
- [ ] Encrypted test email exchanged and decrypted both ways.
- [ ] Revocation cert and key backup stored offline.

## Checked

- Date: 2026-11-02.
- Confirmed against: gpg --gen-revoke, --list-keys, --fingerprint, --send-keys (GnuPG manual); keys.openpgp.org supports WKD (keys.openpgp.org usage page).
- Not confirmed: the quick-generate-key syntax, openpgp-revocs.d behaviour and the Thunderbird menu paths (Mozilla support page blocked) (gated: unconfirmed, source is paywalled or blocked). Treat as unverified and check the current vendor documentation.

Method: documentation only; no commands were run.
