---
id: computing-software.digital-privacy-hygiene.two-factor-auth.fixing-totp-codes-rejected-by-clock-drift
name: fixing-totp-codes-rejected-by-clock-drift
category: computing-software
field: digital-privacy-hygiene
product: two-factor-auth
tags: [digital-privacy-hygiene, two-factor-auth, totp-time-drift, totp, rfc-6238, automatic-time, time-step, troubleshooting, invalid-code]
level: intro
status: docs-checked
description: "Diagnose 'invalid code' from an authenticator app: check the device clock, the wrong account entry, late typing and digit/period mismatches."
sources:
  - "https://datatracker.ietf.org/doc/html/rfc6238"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# TOTP codes rejected: clock drift and other causes

**Goal:** fix "wrong code" in two minutes instead of starting an account recovery.

## Why time matters
A TOTP code is computed from Unix time (seconds since midnight UTC, 1 January 1970) divided into time steps; the
RFC 6238 default step is 30 seconds. The RFC recommends that a server allow at most one time step of
network delay, so a phone clock that is off by more than about a step can make every code fail even though the
app looks fine.

## Diagnose in order
1. **Clock**: compare the phone's time with an accurate reference on another device, and turn on the
   operating system's automatic date and time setting (the menu name varies by OS version; search Settings for
   "date"). Time zone does not matter to TOTP because it uses UTC; the real clock does.
2. **Right entry**: several entries for the same service (old enrolment, work vs personal) are common. A code from
   a stale entry always fails. Check the account label.
3. **Typing too late**: enter the code while it has time left, or wait for a new one.
4. **Parameters**: a service may use a different digit count or period than the default; the RFC's own examples
   use 8 digits. A manually entered secret with default settings then produces wrong codes. Re-enrol using the
   QR code, which carries the parameters.
5. **Repeated failures**: sites may throttle attempts; wait before more tries.

## Still failing
Use a recovery/backup code, then re-enrol the authenticator.

## Verify
- [ ] Phone clock matches an accurate reference to within a second or two.
- [ ] Code accepted on first attempt after the fix.

## Checked
2026-11-01. Confirmed against RFC 6238: default time step 30 seconds (4.1, 5.2), Unix time definition (3), at most
one time step of delay recommended (5.2), 8-digit examples (Appendix A/B). Removed as unconfirmed: per-OS menu
paths and commands, the NIST 800-63B throttling citation, "+/-30 s" acceptance as a rule, 60-second periods, and
the Google Account Help URL (page does not cover Authenticator time sync).
Method: documentation only; no commands were run.
