---
id: computing-software.digital-privacy-hygiene.two-factor-auth.setting-up-mfa-and-backup-methods
name: setting-up-mfa-and-backup-methods
category: computing-software
field: digital-privacy-hygiene
product: two-factor-auth
tags: [digital-privacy-hygiene, two-factor-auth, 2fa, mfa, multi-factor-authentication, passkeys, fido2, webauthn, security-keys, yubikey, totp, authenticator-app, aegis, ente-auth, google-authenticator, authy, microsoft-authenticator, push-notifications, number-matching, sms-2fa, backup-codes, recovery-codes, sim-swap, port-out-pin, mfa-fatigue, account-recovery]
level: practitioner
status: draft
description: "Turn on the strongest MFA each account supports (passkeys, security keys, TOTP), register backups, store recovery codes and block SIM-swap so you are never locked out."
sources:
  - "https://pages.nist.gov/800-63-4/sp800-63b.html"
  - "https://fidoalliance.org/passkeys/"
  - "https://support.google.com/accounts/answer/185839"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Setting up MFA and backup methods — strong second factors, no lockouts

**Goal:** every important account has a phishing-resistant or app-based second factor,
at least two independent ways in, and printed recovery codes, so neither an attacker
with your password nor a lost phone can take the account.

## 1. The strength ladder — use the highest rung offered
1. **Passkeys / FIDO2 security keys** — the credential is bound to the real site's
   domain, so a lookalike page cannot use it. Phishing-resistant.
2. **TOTP authenticator app** (6-digit codes every 30 s) — strong against password
   reuse, but a real-time phishing proxy can relay the code.
3. **Push approval with number matching** — fine if you type the number shown on the
   login screen; plain "Approve?" prompts invite fatigue attacks.
4. **SMS or voice codes** — better than nothing, weakest: SIM swap, port-out fraud,
   SS7 interception. Keep only where nothing else is offered.
Email-link codes rank roughly with SMS and depend entirely on the email account.

## 2. Order of work
1. **Primary email** first — it resets everything else.
2. Password manager account.
3. Phone carrier account (see section 5).
4. Banking, payments, brokerage.
5. Apple/Google/Microsoft account (cloud backups, device find/wipe).
6. Social, work, shopping, everything else.

## 3. Hardware keys and passkeys
- Buy **two** keys (e.g. YubiKey or another FIDO2-certified key). Register both on
  every account; keep one on your keyring and one at home or with someone trusted.
- Set a **FIDO2 PIN** on each key when first prompted.
- Apple Account requires at least two keys when you add security keys. Google
  offers Advanced Protection for high-risk users (journalists, activists, officials).
- Passkeys synced by Apple/Google/a password manager are convenient; a hardware key
  is a separate device-bound backup. Having both is ideal.

## 4. Authenticator apps
- **Aegis** (Android, open source, encrypted local vault and export) and **Ente Auth**
  (cross-platform, end-to-end encrypted sync) are good choices; 2FAS is similar.
- **Google Authenticator** now offers cloud sync to your Google account — convenient,
  but it puts your codes behind that account; decide deliberately.
- **Authy** retired its desktop apps in 2024 and makes exporting hard; if you depend
  on it, migrate account-by-account by re-enrolling (I can't confirm current export
  options — check before relying on any).
- Some password managers store TOTP too. Convenient, but it collapses two factors
  into one vault; keep email and the manager itself on a separate app or key.
- When enrolling, **save the setup QR/secret** in an encrypted backup (Aegis/Ente
  export) — not a screenshot in your camera roll.

## 5. SIM-swap defence
- Set a **port-out / number-transfer PIN** or "number lock" with your carrier (names
  vary: account PIN, transfer PIN, number lock). In the UK, a number transfer needs
  a code texted to the handset, but still set an account password with the carrier.
- Set a **SIM PIN** on the phone so a stolen SIM can't be used in another handset.
- Remove the phone number as a recovery or 2FA option wherever a stronger method exists.

## 6. Backup codes and recovery planning
- Download the **backup/recovery codes** for each account at setup. Print them, or
  store them in your password manager **and** on paper for email and the manager
  itself. Each code works once; regenerate after use.
- Confirm recovery email and phone are current and are themselves protected.
- Note which accounts have no recovery path beyond support tickets (some won't help
  at all) and make sure you have two working factors on those.
- When replacing a phone, move authenticators **before** wiping the old one.

## 7. MFA fatigue
An unexpected push prompt, call or code means **someone has your password**. Deny it,
never approve "to make it stop", then change the password and review sessions. Real
support never asks you to read out a code.

## Gotchas
- Turning on 2FA without saving backup codes is the most common self-lockout.
- Some sites silently keep SMS as a fallback after you add a key; remove it if allowed.
- Time drift breaks TOTP: keep automatic time enabled on the phone.

## Verify
- [ ] Email, password manager and carrier have MFA above SMS.
- [ ] Two security keys (or a key plus a passkey) registered on critical accounts.
- [ ] Backup codes for each critical account exist on paper or offline, and you know where.
- [ ] Authenticator app has an encrypted backup you have restored once.
- [ ] Carrier port-out PIN and SIM PIN set.
- [ ] You signed in once using only a backup method to prove it works.
