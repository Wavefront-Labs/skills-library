---
id: computing-software.digital-privacy-hygiene.password-managers.delegated-access-instead-of-password-sharing
name: delegated-access-instead-of-password-sharing
category: computing-software
field: digital-privacy-hygiene
product: password-managers
tags: [digital-privacy-hygiene, password-managers, delegated-access, password-sharing, shared-accounts]
level: practitioner
status: draft
description: "Use account-level delegation (email delegates, family sharing, authorised users, profiles) instead of handing over a password and its 2FA."
sources:
  - "https://support.google.com/mail/answer/138350"
  - "https://support.apple.com/en-us/108380"
  - "https://ssd.eff.org/module/creating-strong-passwords"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Delegated access instead of password sharing

**Goal:** give someone the access they need with their own login, so you can revoke it, audit it, and keep
your MFA.

## Why
A shared password means shared 2FA codes, no audit trail, and rotation pain when someone leaves. Many services
have built-in delegation.

## Common built-ins
| Need | Use |
|---|---|
| Assistant reads/sends your Gmail | Gmail Settings > Accounts > Grant access to your account (delegate) |
| Shared calendar | Calendar sharing with "Make changes" permission |
| Family uses your Apple purchases/iCloud+ | Family Sharing |
| Kids on streaming | Separate profiles/managed accounts; household plans |
| Partner pays bills | Joint account or authorised user, bank's own online access for them |
| Accountant sees finances | Read-only accountant access in the accounting/bank platform |
| Parent's care | Power of attorney registered with the bank; carrier "authorised user" |
| Website/domain help | Registrar and host "team member" roles |
| Google Drive | Share folders, not the account |

## When delegation doesn't exist
Use the password manager's sharing (shared vault/collection), keep the 2FA on a device you control, and rotate
when access ends.

## Revoke
Review delegates quarterly: Gmail delegates, Google Drive sharing, Family Sharing members, registrar team.

## Gotchas
- Some services prohibit password sharing in their terms; delegation keeps you compliant.
- Delegated email access can send as you; give it only to people you'd trust with that.
