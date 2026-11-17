---
id: computing-software.digital-privacy-hygiene.password-hygiene.account-security-audit-and-breach-response
name: account-security-audit-and-breach-response
category: computing-software
field: digital-privacy-hygiene
product: password-hygiene
tags: [digital-privacy-hygiene, password-hygiene, account-audit, account-inventory, have-i-been-pwned, hibp, data-breach, breach-response, password-reuse, weak-passwords, watchtower, password-health-report, revoke-sessions, email-forwarding-rules, oauth-grants, app-passwords, recovery-email, credit-freeze, fraud-alert, identity-theft, nist-800-63b, password-rotation, account-takeover, credential-stuffing]
level: practitioner
status: draft
description: "Audit your accounts: inventory and prioritise, check Have I Been Pwned and vault health reports, then respond to a breach in the right order and freeze credit where available."
sources:
  - "https://haveibeenpwned.com/"
  - "https://pages.nist.gov/800-63-4/sp800-63b.html"
  - "https://www.identitytheft.gov/"
  - "https://myaccount.google.com/security-checkup"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Account security audit and breach response

**Goal:** know which accounts you have, fix the ones that matter most, and when a breach
happens, close every door an attacker could use — in the order that stops them fastest.

## 1. Inventory
Build the list from: your password manager, the browser's saved logins, a search of
your inbox for "welcome", "verify your email" and "your account", and "Sign in with
Google/Apple/Microsoft/Facebook" connections listed in those accounts. Close accounts
you no longer use (deleting beats securing).

## 2. Prioritise (tier 1 first)
1. **Primary email** — resets everything.
2. **Phone carrier** — controls SMS codes and your number.
3. **Banking, payments, brokerage, crypto.**
4. **Cloud/platform accounts** (Apple, Google, Microsoft) — backups, photos, device wipe.
5. **Password manager.**
6. Social media and messaging (impersonation risk), then work, shopping, the rest.

## 3. Find the problems
- **Have I Been Pwned** (haveibeenpwned.com): check each email address, and sign up
  for notifications. A hit means data from that site leaked, not necessarily the password.
- **Password-manager health reports**: Bitwarden Reports (exposed, reused, weak,
  missing 2FA), 1Password Watchtower, KeePassXC Database › Reports › Health Check /
  HIBP, Google Password Manager Checkup, Apple Passwords › Security recommendations.
  These check passwords against breach corpora using k-anonymity, so the password
  itself is not sent.
- Fix in tier order: any **reused** password on a tier-1 account is urgent, then
  exposed, then weak.

## 4. What good looks like (NIST SP 800-63B)
Current NIST guidance (revision 4, finalised 2025): **length beats complexity**
(minimum 15 characters when a password is the only factor, 8 with MFA; allow at
least 64), no arbitrary composition rules, check new passwords against breach
lists, allow paste and password managers, **no forced periodic rotation** — change
only on evidence of compromise — and no security questions. Practically: unique,
long, random, stored in a manager, plus MFA.

## 5. Breach response — in this order
Do it from a device you trust; if this device may be infected, use another.
1. **Change the password** to a new unique one (and anywhere you reused the old one).
2. **Sign out all other sessions** (Google: Security › Your devices; Microsoft:
   Security › sign out everywhere; Meta: Accounts Center › Password and security ›
   Where you're logged in — menu names vary).
3. **Check recovery email and phone** — attackers change these first. Remove anything
   unfamiliar.
4. **Check email forwarding and filter/rules** (Gmail Settings › Forwarding and
   POP/IMAP and Filters; Outlook › Rules). A hidden rule forwarding or deleting
   bank mail is a classic persistence trick.
5. **Revoke app passwords and OAuth grants** (Google: Security › Your connections to
   third-party apps; Microsoft: Privacy › Apps and services; GitHub etc.: Settings ›
   Applications).
6. **Enable or re-enrol MFA**, removing any method you don't recognise (see
   `computing-software.digital-privacy-hygiene.two-factor-auth.setting-up-mfa-and-backup-methods`).
7. **Look for damage**: sent mail, payments, new devices, posts made in your name.
   Warn contacts if the account sent scams.
8. For financial or identity data, contact the bank via the number on your card.

## 6. Credit and identity protection (region-dependent)
- **US**: credit freezes are free at Equifax, Experian and TransUnion — freeze all
  three; lift temporarily when applying for credit. Report identity theft at
  IdentityTheft.gov. Consider an IRS Identity Protection PIN.
- **UK**: no freeze equivalent; check your files with the credit reference agencies
  and consider Cifas Protective Registration (paid).
- **Elsewhere**: arrangements differ — check your national credit bureau or consumer
  protection agency. I can't confirm specifics for every country.

## 7. Recovery readiness
Backup codes stored, two MFA methods on tier-1 accounts, current recovery info, and
your password manager's emergency kit — test one recovery path per year.

## Gotchas
- Changing a password doesn't kill existing sessions or OAuth tokens on every service.
- Breach-notification emails are themselves a phishing favourite: navigate to the site
  yourself rather than clicking.
- A "pwned" hit for an old, deleted account needs no action beyond not reusing that password.

## Verify
- [ ] Written inventory exists, tier-1 accounts marked.
- [ ] HIBP checked for every address, notifications on.
- [ ] Health report shows zero reused passwords on tier-1 accounts.
- [ ] Recovery info, forwarding rules and third-party grants reviewed on email.
- [ ] Credit frozen (where available) or monitoring in place.
