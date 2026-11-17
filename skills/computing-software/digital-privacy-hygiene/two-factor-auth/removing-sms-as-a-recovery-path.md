---
id: computing-software.digital-privacy-hygiene.two-factor-auth.removing-sms-as-a-recovery-path
name: removing-sms-as-a-recovery-path
category: computing-software
field: digital-privacy-hygiene
product: two-factor-auth
tags: [digital-privacy-hygiene, two-factor-auth, remove-sms-recovery, sim-swap, phone-number-security, sms-2fa, recovery-phone, account-recovery, nist-800-63b]
level: practitioner
status: draft
description: "Find every account where your phone number can reset the password or receive a code, and remove or demote it once stronger methods and recovery codes exist."
sources:
  - "https://pages.nist.gov/800-63-4/sp800-63b.html"
  - "https://www.fcc.gov/sim-swap-port-out-fraud"
  - "https://support.google.com/accounts/answer/183723"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Removing SMS as a recovery path

**Goal:** a SIM swap shouldn't hand an attacker your email, bank and social accounts.
Adding an authenticator often leaves SMS active as a "backup", which is the path an
attacker chooses.

## Inventory
For each important account check two places:
1. **2FA methods**: is "Text message" / "Phone" still listed?
2. **Recovery options**: is the phone number able to reset the password ("Forgot
   password? We'll text you a code")?
Typical offenders: Google (recovery phone + 2SV phone), Microsoft (security info),
Apple (trusted phone numbers are mandatory), X/Twitter, Instagram/Facebook, PayPal,
banks, mobile carrier account itself.

## Remove or demote
- **Google**: Security > 2-Step Verification > remove "Phone numbers" once passkeys/keys
  and backup codes exist. Recovery phone: keep only if you accept the risk; Advanced
  Protection reduces how it's used.
- **Microsoft**: Security > Advanced security options > remove phone from sign-in and
  verification methods; keep recovery code.
- **Apple**: requires at least one trusted number; mitigate with security keys and a
  recovery key instead.
- **Social/finance**: switch to authenticator/passkey; delete the number where allowed.
- Where SMS can't be removed, use a **number that's hard to swap** (see
  `computing-software.digital-privacy-hygiene.two-factor-auth.using-a-separate-number-for-account-recovery`)
  and carrier port-out protection.

## Gotchas
- Some services silently re-add your phone from your profile for "security alerts";
  recheck after changes.
- Removing the number from 2FA but leaving it as password-reset is the common mistake.
- Keep recovery codes before removing SMS, or you can lock yourself out.

## Verify
- [ ] Spreadsheet/note: per account, phone used for 2FA? for reset? both "no" or justified.
- [ ] "Forgot password" on email account does not offer SMS (or only with additional checks).
