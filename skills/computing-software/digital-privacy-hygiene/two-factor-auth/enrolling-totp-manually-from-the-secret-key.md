---
id: computing-software.digital-privacy-hygiene.two-factor-auth.enrolling-totp-manually-from-the-secret-key
name: enrolling-totp-manually-from-the-secret-key
category: computing-software
field: digital-privacy-hygiene
product: two-factor-auth
tags: [digital-privacy-hygiene, two-factor-auth, totp-manual-entry, totp, otpauth-uri, base32-secret, cant-scan-qr, enrollment, multi-device-enrollment]
level: intro
status: docs-checked
description: "Enroll a TOTP authenticator when you can't scan the QR: enter the base32 secret, set digits, period and algorithm, and confirm before saving."
sources:
  - "https://github.com/google/google-authenticator/wiki/Key-Uri-Format"
  - "https://datatracker.ietf.org/doc/html/rfc6238"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Enrolling TOTP from the secret key text

**Goal:** add 2FA when the QR code is on the same phone screen you'd scan it with,
or when you want the same secret on two authenticators.

## Steps
1. On the site's 2FA setup page choose its "can't scan" or "enter a setup key" option. You
   will see a base32 string. (The RFC 3548 base32 padding is not required and is omitted
   in the URI.)
2. In the authenticator choose to add an account manually:
   - Name it so you will recognise it: an issuer (the service) and an account name.
   - Secret: the setup key. Remove spaces if the app complains.
   - Type: time-based (TOTP). Keep the defaults unless the site says otherwise: **6 digits**,
     **30 second period**, **SHA1**.
3. Type the current code into the site to confirm. Only after it is accepted is 2FA on.
4. Save the recovery codes the site shows next.

## The otpauth URI
QR codes encode `otpauth://TYPE/LABEL?PARAMETERS` where TYPE is `hotp` or `totp`. Example
with every optional parameter:
`otpauth://totp/ACME%20Co:john.doe@email.com?secret=HXDMVJECJJWSRB3HWIZR4IFUGFTMXBOZ&issuer=ACME%20Co&algorithm=SHA1&digits=6&period=30`
- `secret` is required and Base32-encoded.
- `issuer` is strongly recommended; use both the label prefix and the parameter, and make
  them equal.
- `algorithm` is `SHA1` (default), `SHA256` or `SHA512`; `digits` is 6 (default) or 8;
  `period` is in seconds (default 30); `counter` is required for `hotp`.
- Google Authenticator's own implementations ignore `algorithm` and `period`, and Android
  ignores `digits`. Accounts needing non-default values may therefore display wrong codes in
  that app; use an app that honours them.
- Some apps accept a pasted full URI, which keeps non-default parameters.

## Two authenticators, same secret
Add the secret to both apps (or devices) during enrolment, before confirming. They produce
identical codes. RFC 6238 requires the prover and verifier to use the same time step, and
TOTP is HOTP with a time-derived counter, so matching settings give matching codes.

## Gotchas
- Do not screenshot the QR or paste the secret into notes or chat; it is equivalent to the
  factor itself.
- Services using 8 digits or SHA256/SHA512 fail in apps that ignore those parameters.

## Verify
- [ ] The site accepted a code at enrolment.
- [ ] Clipboard cleared and no screenshot or copy of the secret left behind.

## Checked
Checked 2026-11-08 against the Google Authenticator Key Uri Format wiki and RFC 6238
(sections 1, 3 and 4). Removed: the example code `JBSW Y3DP...` spacing remark,
the Steam claim and exchange examples, the Yubico OATH example, and the "backup without
recovery codes" claim; none are stated by these pages.

Method: docs-only read of cited pages, 2026-11-08
