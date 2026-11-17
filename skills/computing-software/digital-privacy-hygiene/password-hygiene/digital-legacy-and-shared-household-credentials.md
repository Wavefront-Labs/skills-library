---
id: computing-software.digital-privacy-hygiene.password-hygiene.digital-legacy-and-shared-household-credentials
name: digital-legacy-and-shared-household-credentials
category: computing-software
field: digital-privacy-hygiene
product: password-hygiene
tags: [digital-privacy-hygiene, password-hygiene, digital-legacy, inheritance, estate-planning, legacy-contact, shared-accounts, household-vault, joint-access, next-of-kin, google-inactive-account-manager, apple-legacy-contact, death-and-digital-assets, beneficiary-access]
level: practitioner
status: draft
description: "Plan who can reach your accounts if you die or are incapacitated, and run shared household credentials, without weakening day-to-day security or handing out your real password."
sources:
  - "https://support.apple.com/en-us/102631"
  - "https://support.google.com/accounts/answer/3036546"
  - "https://bitwarden.com/help/emergency-access/"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Digital legacy and shared household credentials

**Goal:** a partner, family member or executor can reach the accounts they
legitimately need — banking, photos, email, the password vault itself — if you die,
are incapacitated, or are simply unreachable, without anyone sharing a live
password day-to-day or weakening the account's normal protection.

## 1. Don't just "share the password" as the plan
Sharing your actual password with a partner for convenience means: it's now a
shared secret neither of you can rotate without telling the other, it can't be
distinguished from a compromise if it leaks, and it stops working the moment you
turn on passkeys or change it after a breach. Use the platform's actual
**legacy/emergency mechanisms** instead — they're built to hand over access on a
defined trigger, not to be an everyday login.

## 2. Platform legacy mechanisms
- **Apple**: Settings → [your name] → Password & Security → **Legacy Contact**.
  You nominate someone who, after your death, can request access with a death
  certificate; Apple issues them an access key to retrieve data without your
  password — it does not give them day-to-day access while you're alive.
- **Google**: **Inactive Account Manager** (myaccount.google.com) — set a timeout
  (e.g. 3, 6, 12, 18 months of inactivity), nominate up to 10 trusted contacts, and
  choose exactly what each gets (Gmail, Photos, Drive, etc.) and whether the account
  auto-deletes afterward. This also protects *you*: if you're incapacitated rather
  than dead, it triggers on inactivity regardless.
- **Facebook/Meta**: a **Legacy Contact** can be set (Settings → Memorialization
  Settings) to manage a memorialized profile; they cannot log in as you.
- **Password manager emergency access** (see
  `computing-software.digital-privacy-hygiene.password-managers.vault-setup-sharing-and-recovery`):
  Bitwarden Emergency Access and 1Password's family organiser recovery are the
  actual key to everything else, since the vault holds the rest. This is the single
  highest-leverage legacy setting — get it right and everything downstream follows.

## 3. What to leave behind (the practical document)
A single reference — not the passwords themselves — covering: which password
manager and account email it uses, where the physical recovery sheet/Emergency
Kit is kept, which accounts have legacy contacts already configured and where,
and any accounts that have **no** recovery path beyond a support ticket (note
these explicitly; they are the ones most likely to be permanently lost). Store this
reference with a solicitor/will, a safe, or a trusted person — not emailed in
plaintext.

## 4. Shared household/day-to-day accounts (not the legacy case)
For accounts a couple or family genuinely uses together day-to-day (streaming,
a joint utility login, a family calendar), use the password manager's actual
**sharing** feature — a shared Collection/vault in Bitwarden, a shared vault in
1Password — so each person has their own login to the manager and the shared item
updates for everyone at once, rather than a password written on a sticky note or
texted. Family password-manager plans (Bitwarden Families, 1Password Families)
are built for exactly this and include an organiser recovery option for forgotten
master passwords within the family.

## 5. Incapacity, not just death
Emergency Access/legacy contacts cover incapacity too if set with a waiting
period rather than only a death-certificate trigger — Bitwarden's Emergency
Access, for example, grants a nominated contact vault access automatically after
a wait time you choose if you don't deny the request, which is useful for
"unreachable and incapacitated," not only deceased.

## Gotchas
- A legacy contact set up once and never revisited can point at an email address
  or phone number that's since changed — review it yearly, same as a will.
- Writing passwords on paper "for the family" defeats MFA and rotation and is a
  physical-security risk of its own; use the vault's sharing/emergency features
  instead.
- Uncertain: exact legal recognition of these platform mechanisms (vs. a will or
  power of attorney) varies by jurisdiction — for anything with real financial
  stakes, also address it in estate planning documents; this is not legal advice.

## Verify
- [ ] Password manager's emergency access/family recovery is configured with a
      real, current trusted contact.
- [ ] Apple Legacy Contact / Google Inactive Account Manager (or equivalents) set
      with sensible timeouts and recipients.
- [ ] A written reference to "where the recovery sheet lives" exists outside the
      vault itself, without containing live passwords.
- [ ] Accounts with no recovery path beyond a support ticket are identified and
      noted.
- [ ] Shared day-to-day logins live in a shared vault/Collection, not a shared
      password typed from memory.
