---
id: computing-software.digital-privacy-hygiene.two-factor-auth.account-recovery-after-losing-your-second-factor
name: account-recovery-after-losing-your-second-factor
category: computing-software
field: digital-privacy-hygiene
product: two-factor-auth
tags: [digital-privacy-hygiene, two-factor-auth, account-recovery, locked-out, lost-phone, lost-security-key, google-account-recovery, apple-account-recovery, microsoft-account-recovery, identity-verification, recovery-timeline, backup-codes-missing]
level: practitioner
status: draft
description: "Recover major platform accounts when every second factor and backup code is gone: the real per-platform process, realistic timelines, and what to pre-stage so it's never needed."
sources:
  - "https://support.google.com/accounts/answer/185834"
  - "https://support.apple.com/en-us/102560"
  - "https://support.microsoft.com/account-billing/"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Account recovery after losing your second factor

**Goal:** know the actual process and realistic timeline for getting back into
an account when every MFA method and backup code is gone — a lost phone, a
destroyed hardware key, a house fire — and understand that for some platforms
there genuinely is no fast path, which is the real argument for the
preventive setup in
`computing-software.digital-privacy-hygiene.two-factor-auth.setting-up-mfa-and-backup-methods`.

## 1. The honest premise
Strong MFA is deliberately designed so that losing *every* factor is hard to
recover from quickly — that's the same property that makes it resistant to an
attacker. Platforms balance this against locking out legitimate owners by
offering an identity-verification recovery path, but it is slower, more
intrusive, and sometimes unsuccessful compared to just having a backup method.
Expect this process to take anywhere from minutes to several days depending on
the platform and the account's security settings, and go in understanding you
may not get back in at all for an account with no alternate recovery info set.

## 2. Google
- **myaccount.google.com → account recovery flow**: asks for the last password
  you remember, an approximate account creation date, and recovery email/phone
  if any are on file. Being signed in on a **trusted device** (one that's
  previously accessed the account) significantly speeds this up or can bypass
  further checks entirely — this is why "stay signed in on at least one spare
  trusted device" is worth doing deliberately, not by accident.
- If **Advanced Protection** was enabled (the high-security mode for
  journalists/activists/officials), recovery is intentionally slower and
  stricter — a deliberate trade-off of that program; expect it to take longer by
  design, not as a bug.
- Without a recovery phone/email and no trusted device, Google's own guidance
  is that recovery can be difficult or impossible — this is the strongest
  argument in this entire topic for keeping recovery email/phone current.

## 3. Apple
- **iforgot.apple.com** or Settings → [name] → Password & Security → account
  recovery, with options depending on what's configured: another trusted
  device already signed in, a recovery key if one was set, or **Account
  Recovery Contacts** (people you pre-designated who can generate a recovery
  code for you) — this is the single most useful pre-staged option and, unlike
  the legacy security-questions path, doesn't rely on factual answers that may
  be publicly discoverable.
- If you'd previously enabled a **Recovery Key** (a 28-character code), Apple
  states it **cannot** bypass it with any other identity verification — losing
  both the recovery key and all devices/trusted numbers can mean permanent
  loss of account access under that configuration. Decide deliberately whether
  you want this maximum-security mode or the more recoverable default.

## 4. Microsoft
- account.live.com/acsr (Account Recovery) asks a series of questions about
  account usage history (recent subject lines, contacts, when it was created,
  devices used) rather than a single secret — a known, previously-used device
  or browser session speeds this considerably.
- For a **work/school (Microsoft 365) account**, recovery is controlled by your
  organisation's IT admin, not Microsoft support directly — the actual fast
  path there is contacting your admin, not the consumer self-service flow.

## 5. Everything else (banking, social, smaller services)
- **Banking**: call the number on a card/statement (never a number from an
  email) and expect an in-person or video identity check for a full lockout —
  typically the fastest of all categories because banks have mature identity
  verification infrastructure, but exact process varies by institution.
- **Social media**: often has the weakest and slowest recovery path of any
  category, sometimes with no live human support at all for free-tier accounts
  — this is a strong argument for treating social accounts' MFA backups
  (section 6 of the companion skill) especially seriously, since recovery
  support may simply not exist.
- A **password manager's own account** has no recovery path beyond what you
  staged in advance (Emergency Access, Emergency Kit, organiser recovery) — see
  `computing-software.digital-privacy-hygiene.password-managers.vault-setup-sharing-and-recovery`;
  there is no vendor override for a forgotten master password.

## 6. What to pre-stage now, specifically because this process is slow/uncertain
- A current recovery email **and** phone number on every tier-1 account.
- At least one device that stays signed in and trusted, kept somewhere safe,
  specifically as a recovery aid (not your daily device, which is the one
  likely to be the thing that's lost).
- Apple Account Recovery Contacts, or the equivalent trusted-contact mechanism
  where a platform offers one.
- Printed backup codes stored separately from the devices they'd be backing up.

## Gotchas
- "I'll just use account recovery if I lose everything" is not a backup plan —
  it's an acceptance that you may be locked out for days or permanently; use
  it as the exercise that convinces you to pre-stage section 6, not as a
  substitute for it.
- A recovery key with no override (Apple's model, by design) is safer against
  attackers and strictly riskier for you if every copy is lost — know which
  trade-off you've chosen.
- Uncertain: exact recovery timelines and required proof vary by account age,
  prior activity, and current platform policy — treat the above as the shape
  of each process, not a guaranteed turnaround time.

## Verify
- [ ] You know, per tier-1 account, whether recovery without any device/key
      would even be possible, and roughly how long it would take.
- [ ] Recovery email and phone are current on every tier-1 account, checked in
      the last six months.
- [ ] At least one trusted, already-signed-in device exists specifically as a
      recovery aid.
- [ ] Apple Account Recovery Contacts (or platform equivalent) are set where
      offered.
