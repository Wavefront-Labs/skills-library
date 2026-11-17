---
id: computing-software.digital-privacy-hygiene.vpn-tools.choosing-an-encrypted-email-provider
name: choosing-an-encrypted-email-provider
category: computing-software
field: digital-privacy-hygiene
product: vpn-tools
tags: [digital-privacy-hygiene, vpn-tools, encrypted-email-provider, email-privacy, email-encryption, proton-mail, tuta, mailbox-org, zero-access-encryption, email-migration]
level: intro
status: draft
description: "Choose a privacy-focused email provider (Proton Mail, Tuta, Mailbox.org), understand what 'encrypted email' covers, and migrate without losing access to old accounts."
sources:
  - "https://www.privacyguides.org/en/email/"
  - "https://www.privacyguides.org/en/basics/email-security/"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Choosing an encrypted email provider

**Goal:** move your primary email to a provider whose business isn't reading your mail
for ads, knowing email's limits.

## What "encrypted email" usually means
- **Zero-access storage**: mail at rest is encrypted with keys the provider doesn't hold
  (Proton, Tuta). Incoming mail from Gmail users arrives in plaintext and is encrypted on
  arrival; the provider saw it in transit.
- **End-to-end** only between users of the same service or with OpenPGP keys.
- **Subject lines and metadata** (From/To/time) are often not encrypted (Tuta encrypts
  subjects; Proton doesn't for standard interoperability).
Email is not a secure messenger; for sensitive conversations use Signal.

## Options (Privacy Guides list; verify current)
| Provider | Model | Notes |
|---|---|---|
| Proton Mail | OpenPGP-based, zero-access | Bridge for desktop clients (paid); custom domains paid |
| Tuta | Own encryption (incl. post-quantum), encrypts subject | No IMAP; own apps only |
| Mailbox.org | Standard IMAP + optional PGP and encrypted storage | Works with any client |

## Migration plan
1. Create the new account; secure it with 2FA/passkey.
2. Ideally use a **custom domain** so you can switch providers later (see
   `computing-software.digital-privacy-hygiene.vpn-tools.custom-domain-email-ownership`).
3. Import old mail (Proton Easy Switch, IMAP import).
4. Set auto-forward from old address; update accounts gradually, highest value first.
5. Keep the old account alive and secured for a year (password resets will still go
   there); don't delete it, or someone may re-register the address in some providers.

## Verify
- [ ] Top 20 accounts updated to the new address.
- [ ] Old account still 2FA-protected, forwarding active.
