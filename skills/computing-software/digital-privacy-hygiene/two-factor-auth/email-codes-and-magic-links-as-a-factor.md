---
id: computing-software.digital-privacy-hygiene.two-factor-auth.email-codes-and-magic-links-as-a-factor
name: email-codes-and-magic-links-as-a-factor
category: computing-software
field: digital-privacy-hygiene
product: two-factor-auth
tags: [digital-privacy-hygiene, two-factor-auth, email-otp, mfa-strength-ranking, primary-email-security]
level: practitioner
status: draft
description: "Judge email one-time codes and magic links as an authentication factor: why NIST excludes email for out-of-band, and how to harden accounts that rely on it."
sources:
  - "https://pages.nist.gov/800-63-4/sp800-63b.html"
  - "https://www.privacyguides.org/en/basics/multi-factor-authentication/"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Email codes and magic links as a factor

**Goal:** know what you're getting when a site offers "we'll email you a code" and compensate when that's the only
option.

## What NIST says
SP 800-63B-4 out-of-band rules: methods that don't prove possession of a specific device, such as **email** or
VoIP, SHALL NOT be used as out-of-band authenticators. Email codes prove you can read the mailbox, which is
whoever has your email password or session.

## Practical ranking
Passkey/security key > authenticator app > push with number matching > SMS > **email code** ~ magic link.
Email-only login means **your email account is the real lock** for that site.

## Where it shows up
- "Passwordless" sign-in via magic link (Slack, Medium, many shops).
- Login verification codes on new devices (Steam, retailers).
- Password reset links (every site).

## Hardening when email is the factor
1. Protect the mailbox: passkey or security key, no SMS recovery, no forwarding rules you didn't create.
2. Use a dedicated email address/alias for high-value sites so phished/leaked addresses don't map.
3. If the site offers TOTP or passkey, add it and see if email login can be disabled.
4. Don't click magic links in emails you didn't request; request fresh from the site.

## Gotchas
- Magic links opened on another device can log in **that** device; some phishing kits trick you into requesting
  and forwarding a code.
- Email codes in the same inbox as the password reset mean one compromise defeats both.
