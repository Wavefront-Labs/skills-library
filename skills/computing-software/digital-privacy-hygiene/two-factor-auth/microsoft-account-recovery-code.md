---
id: computing-software.digital-privacy-hygiene.two-factor-auth.microsoft-account-recovery-code
name: microsoft-account-recovery-code
category: computing-software
field: digital-privacy-hygiene
product: two-factor-auth
tags: [digital-privacy-hygiene, two-factor-auth, microsoft-recovery-code, recovery-codes, microsoft-account-2fa]
level: practitioner
status: draft
description: "Generate and store the single Microsoft account recovery code, know when it's needed (passwordless or 2SV lockout), and regenerate after use."
sources:
  - "https://support.microsoft.com/account-billing/using-recovery-codes-to-regain-access-to-your-microsoft-account-c6f6c3e9-7c35-4c2d-b2cd-8c9a8b0b2a67"
  - "https://account.microsoft.com/security"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Microsoft account recovery code

**Goal:** a way back into a Microsoft account (Outlook, Xbox, OneDrive, Windows sign-in) if you lose your phone
and authenticator.

## What it is
One 25-character code. Generating a new one invalidates the old one. Used when two-step verification or
passwordless is on and you can't use your other verification methods.

## Generate
account.microsoft.com > Security > **Manage how I sign in** (Advanced security options) > Recovery code >
**Generate a new code**. Verify identity, then copy the code.

## Store
- Password manager item "Microsoft account" (custom field `recovery code`).
- Paper emergency sheet.
Not in OneDrive or Outlook (locked out = can't read it).

## Using it
Sign-in > "I don't have any of these" / "Use a recovery code" > enter code. After use you receive a new code;
store it immediately.

## Also check
- At least two verification methods (authenticator + security key/passkey, alternate email).
- Remove old phone numbers.

## Gotchas
- Without a recovery code or any method, the account recovery form is slow and often fails for passwordless
  accounts.
- Child accounts in Family Safety: the organiser should hold their recovery info.
