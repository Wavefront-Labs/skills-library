---
id: computing-software.digital-privacy-hygiene.two-factor-auth.apple-account-two-factor-and-trusted-numbers
name: apple-account-two-factor-and-trusted-numbers
category: computing-software
field: digital-privacy-hygiene
product: two-factor-auth
tags: [digital-privacy-hygiene, two-factor-auth, apple-two-factor, mfa-rollout, multi-factor-authentication, apple-account, trusted-devices, trusted-phone-number, verification-code]
level: intro
status: docs-checked
description: "How Apple Account two-factor works: trusted devices, trusted phone numbers, getting a verification code, what happens when you lose both, and where to go next."
sources:
  - "https://support.apple.com/en-us/102660"
  - "https://support.apple.com/en-us/102606"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Apple Account two-factor and trusted numbers

**Goal:** Apple's two-factor is the default for most accounts; the work is keeping the
trusted devices and numbers it relies on usable and under your control.

## How it works
On a new device or the web you need your Apple Account password and a six-digit
verification code. The code is shown automatically on your **trusted devices** or sent to
a **trusted phone number**. After the first sign-in you are not asked again on that device
unless you sign out completely, erase the device or must change your password. Some
services, such as Apple Pay and Sign in with Apple, require two-factor authentication.

## Getting a code
- **Trusted device:** a sign-in notification appears; choose **Allow** to see the code,
  then enter it on the new device. The notification may show a map based on the new
  device's IP address, which can reflect the network rather than the exact place.
- **Text or call:** on the code screen choose "Didn't Get a Code?" or "Can't get to your
  devices?" and send it to a trusted phone number. If you filter Unknown Senders in
  Messages, check there; Settings > Apps > Messages > Unknown Senders lets you allow
  time-sensitive notifications.
- In some cases your trusted number is verified in the background on an iPhone and you
  are not asked for a code.

## Turning it on
Most accounts already have it. On a device: Settings (System Settings on Mac) > your
name > Sign-In & Security > turn on two-factor authentication. On the web: account.apple.com >
Upgrade Account Security. If the account was created with two-factor, it cannot be
removed; a recently enabled account can lower security within two weeks.

## If you lose access
- Temporarily without devices and number: Apple says the fastest route is to wait until
  you have access again, sign in, then add more trusted phone numbers.
- Permanently without both: choose "Can't use [phone number]" to start account
  recovery. It can take a few days or longer, and contacting Apple does not speed it up.

## Hardening next steps
Add more than one trusted number you control, keep trusted devices passcode-protected
(Apple recommends a passcode plus Face ID, Touch ID or Optic ID), and consider a
recovery contact or key
(`computing-software.digital-privacy-hygiene.two-factor-auth.apple-recovery-key-and-recovery-contact`)
and security keys
(`computing-software.digital-privacy-hygiene.two-factor-auth.security-keys-for-apple-account`).

## Verify
- [ ] At least one trusted phone number is current and controlled by you.
- [ ] A new-device sign-in shows the code on a trusted device you hold.

## Checked
Checked 2026-11-08 against the two cited Apple Support pages (102660, 102606). Removed:
the device-list and appleid.apple.com steps, the Don't Allow action, "Apple never calls"
and the sold-phone and Safety Check remarks, none of which these pages state.

Method: docs-only read of cited pages, 2026-11-08
