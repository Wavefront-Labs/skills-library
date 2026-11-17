---
id: computing-software.cybersecurity-defensive.network-defence.dkim-signing-and-key-rotation
name: dkim-signing-and-key-rotation
category: computing-software
field: cybersecurity-defensive
product: network-defence
tags: [email-security, dkim, domainkeys-identified-mail, dkim-selector, key-rotation, 2048-bit-rsa, dkim-alignment, email-authentication]
level: practitioner
status: docs-checked
description: "Set up DKIM signing for every sending service with 2048-bit keys, per-service selectors, alignment with the From domain and regular key rotation."
sources: ["https://datatracker.ietf.org/doc/html/rfc6376", "https://learn.microsoft.com/en-us/defender-office-365/email-authentication-dkim-configure"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# DKIM signing and key rotation

**Goal:** every legitimate message carries a DKIM signature aligned with the visible From
domain, so it passes DMARC.

## Setup per sending service
1. Generate or enable keys in the service (Microsoft 365: Defender portal > Email authentication
   > DKIM; Google Workspace: Admin > Gmail > Authenticate email; ESPs give CNAMEs).
2. Publish the selector record:
```
s1._domainkey.example.com. TXT "v=DKIM1; k=rsa; p=MIIBIjANBgkqh..."
```
   or CNAMEs to the provider-hosted keys (Microsoft 365 uses `selector1` and `selector2` CNAMEs).
3. Enable signing and verify the Authentication-Results header shows a DKIM pass for your domain.

## Key and selector practice
- RFC 6376: signers MUST use RSA keys of at least 1024 bits; prefer larger keys such as 2048 bits where your DNS provider supports the record length.
- One selector per service, so a compromised vendor key can be revoked alone.
- **Signing domain** (`d=`) must align with the From domain (same organisational domain) for DMARC; vendors default to signing with their own domain unless you set up custom DKIM.

## Rotation
1. Publish a new selector with the new key.
2. Switch signing to the new selector.
3. Keep the old public key published while messages signed with it may still be in transit, then revoke it by publishing an empty `p=` value.
Rotate on a schedule you set, and immediately if a key may be exposed.

## Gotchas
- Mailing lists and gateways that modify subject/body break signatures; ARC helps receivers trust forwarded mail.
- `l=` (body length) tag allows appended content: avoid it.

## Verify
- [ ] A DNS TXT query for the selector name returns the key; message headers show an aligned DKIM pass.
- [ ] DMARC aggregate reports show DKIM pass for all legitimate sources.

## Checked

2026-10-28. Confirmed against: RFC 6376 (1024-bit minimum for signers, empty p= revocation, l= tag risk); Microsoft Learn 'Use DKIM for email in your custom domain' (selector1/selector2 CNAMEs, Defender portal).

Removed as unconfirmed: RFC 8301/8463 statements, 6-12 month rotation figure, 'few days' overlap, 255-character TXT note, 'survives forwarding' claim.

Method: documentation only; no commands were run.
