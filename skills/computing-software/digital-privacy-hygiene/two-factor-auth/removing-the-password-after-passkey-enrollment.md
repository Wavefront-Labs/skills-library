---
id: computing-software.digital-privacy-hygiene.two-factor-auth.removing-the-password-after-passkey-enrollment
name: removing-the-password-after-passkey-enrollment
category: computing-software
field: digital-privacy-hygiene
product: two-factor-auth
tags: [digital-privacy-hygiene, two-factor-auth, passwordless-account, passkey-enrollment, passkeys, skip-password, remove-password, fallback-methods, account-recovery]
level: practitioner
status: draft
description: "Go fully passwordless on an account once passkeys are in place: remove or randomise the password, disable weak fallbacks, and keep a tested recovery path."
sources:
  - "https://support.google.com/accounts/answer/13548313"
  - "https://support.microsoft.com/en-us/account-billing/how-to-go-passwordless-with-your-microsoft-account-674ce301-3574-4387-a93d-916751764c43"
  - "https://pages.nist.gov/800-63-4/sp800-63b.html"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Removing the password after passkey enrollment

**Goal:** a passkey only stops phishing if the attacker can't just use the password
instead.

## Three levels
1. **Passkey preferred, password kept** (default on most sites): convenience only;
   phishing of the password+OTP still works.
2. **Password randomised and forgotten**: set a 30+ char generated password stored
   only in the vault. It still exists as a fallback, but you never type it, so it
   can't be phished from you.
3. **Password removed**: sites that support it (Microsoft "passwordless account",
   Google "Skip password when possible", some others). The account can't be logged into
   with a password at all.

## Procedure
1. Register **at least two** passkeys/keys on different platforms (e.g. iPhone + YubiKey).
2. Confirm each works from a clean browser.
3. Download/print recovery codes if offered.
4. Choose level 2 or 3:
   - Google: myaccount.google.com > Security > "Skip password when possible" on.
   - Microsoft: see
     `computing-software.digital-privacy-hygiene.two-factor-auth.going-passwordless-on-a-microsoft-account`.
   - Others: change the password to a random 32+ char value in the vault.
5. Remove weaker MFA options (SMS) that still allow password-plus-code login.

## Gotchas
- Some old clients (IMAP mail apps, TVs, game consoles) need a password or app
  password; plan for device-code sign-in or app passwords before removing it.
- "Skip password" still allows password login in some flows; it's level 1.5, not 3.
- Account recovery by email/SMS remains; that's now the weakest path.

## Verify
- [ ] Fresh browser: sign-in offers passkey first; password route either absent or needs
      a password you never typed.
