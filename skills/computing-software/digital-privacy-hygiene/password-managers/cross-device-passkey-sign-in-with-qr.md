---
id: computing-software.digital-privacy-hygiene.password-managers.cross-device-passkey-sign-in-with-qr
name: cross-device-passkey-sign-in-with-qr
category: computing-software
field: digital-privacy-hygiene
product: password-managers
tags: [digital-privacy-hygiene, password-managers, hybrid-transport, cross-device-authentication, passkeys, cable-protocol, bluetooth-proximity, qr-code, fido2, shared-computer]
level: practitioner
status: draft
description: "Sign in on a computer using a passkey on your phone via the QR code and Bluetooth hybrid flow, and know why it resists remote phishing."
sources:
  - "https://fidoalliance.org/specs/fido-v2.2-rd-20230321/fido-client-to-authenticator-protocol-v2.2-rd-20230321.html"
  - "https://support.google.com/accounts/answer/13548313"
  - "https://support.apple.com/en-us/102195"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Cross-device passkey sign-in (hybrid transport)

**Goal:** log in on a laptop or borrowed computer with the passkey on your phone,
without typing any password into that computer.

## The flow
1. On the computer's sign-in page choose "Use a passkey" > **Use a phone or tablet**
   / "Use another device". A QR code appears.
2. Scan with the phone's camera. The phone checks **Bluetooth proximity** to the
   computer, then shows the account; unlock with face/fingerprint/PIN.
3. The phone signs the challenge; the computer is logged in. The private key never
   leaves the phone.
4. Optionally the browser offers to remember the phone (linked device) for next time;
   decline on a computer that isn't yours.

## Why it resists phishing
The QR leads to a tunnel the phone only completes if it is physically near the
computer (Bluetooth advertisement), and the signed response is bound to the website's
origin. A phisher in another country sending you a QR code can't complete it.
(FIDO calls this "hybrid"; earlier drafts called it caBLE.)

## Requirements and troubleshooting
- Bluetooth on for **both** devices; the computer needs a working Bluetooth adapter.
  Desktops without Bluetooth can't do hybrid.
- Phone needs a provider that supports hybrid: iOS 16+, Android 9+ with Google Play
  services, or a password manager acting as provider on the phone.
- Corporate VPNs/firewalls can block the relay (tunnel service); try off VPN.
- Windows: if the QR option doesn't appear, update Windows and the browser; Windows
  Hello handles the dialog.

## Gotchas
- Never scan a passkey QR that came in an email or chat; the legitimate QR only appears
  on the screen in front of you when you started a sign-in.
- Remove "linked phone" entries on shared computers afterwards (browser passkey settings).

## Verify
- [ ] Logged into a test account on a second computer via QR, Bluetooth required.
