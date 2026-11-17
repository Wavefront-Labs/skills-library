---
id: computing-software.digital-privacy-hygiene.two-factor-auth.hotp-counter-tokens-and-resync
name: hotp-counter-tokens-and-resync
category: computing-software
field: digital-privacy-hygiene
product: two-factor-auth
tags: [digital-privacy-hygiene, two-factor-auth, hotp, rfc-4226, oath-hotp, counter-desync, look-ahead-window, yubikey-oath, hardware-token, mfa]
level: practitioner
status: docs-checked
description: "Use event-based HOTP tokens (hardware tokens, YubiKey OATH accounts) and understand the counter desync and look-ahead resync that follow extra button presses."
sources:
  - "https://datatracker.ietf.org/doc/html/rfc4226"
  - "https://datatracker.ietf.org/doc/html/rfc6238"
  - "https://docs.yubico.com/software/yubikey/tools/ykman/OATH_Commands.html"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# HOTP counter tokens

**Goal:** understand and fix the one quirk of counter-based codes.

## How HOTP works
HOTP(K, C) = Truncate(HMAC-SHA-1(K, C)) where K is the shared secret and C the counter
(RFC 4226). TOTP (RFC 6238) is the same algorithm with the counter replaced by a value
derived from time; its default time step is 30 seconds and it MAY use HMAC-SHA-256 or
HMAC-SHA-512.

## Where the counter lives
- The token increments its counter every time a new HOTP is requested.
- The server increments its counter only after a successful validation (by one).
- So extra presses leave the two counters out of step.

## Desync and resync (RFC 4226 section 7.4)
- Pressing the button without using the code pushes the token ahead of the server.
- The server SHOULD use a **look-ahead window** of size s: it computes the next s values
  and checks the submitted code against them. s should be as low as possible while
  keeping usability, so a token pressed too many times falls outside it.
- The server MAY require two or three consecutive HOTP values to resynchronise, because
  forging a consecutive sequence is harder than guessing one value.
- Servers should throttle or lock out after a maximum number of failed attempts
  (section 7.3), so repeated guesses while desynced can lock the account.
- The window size is a server setting: ask the issuer for the resync procedure; the RFC
  gives no number to rely on.

## Adding an HOTP account to a YubiKey
`ykman oath accounts add --oath-type HOTP --counter <n> <name> <secret>` where `--oath-type`
is `HOTP` or `TOTP` (default `TOTP`), `--counter` is the initial counter for HOTP accounts,
and the secret is base32-encoded. Codes from HOTP accounts need a single account match
and are triggered when you request them.

## Pros and cons vs TOTP
- HOTP needs no clock, so it works on devices without accurate time.
- A counter-based code is not tied to a time step. Treat written-down or unused codes as
  sensitive.
- Both are OTP schemes, not phishing resistant.

## Verify
- [ ] After a few stray presses, a fresh code is still accepted (within the window).
- [ ] You know the issuer's resync procedure before you need it.

## Checked
Checked 2026-11-08 against RFC 4226 (sections 7.2 to 7.4), RFC 6238 (sections 1 and 4)
and the ykman OATH commands page. Removed: the "commonly 10-50 counts" window figure,
the claim that the server rejects counters at or below the last accepted one, specific
device examples, Yubico Authenticator mention and the NIST 800-63B comparison (the
NIST page was not read for this claim).

Method: docs-only read of cited pages, 2026-11-08
