---
id: computing-software.digital-privacy-hygiene.two-factor-auth.github-two-factor-with-keys-and-recovery-codes
name: github-two-factor-with-keys-and-recovery-codes
category: computing-software
field: digital-privacy-hygiene
product: two-factor-auth
tags: [digital-privacy-hygiene, two-factor-auth, github-2fa, account-hardening-programs, passkeys, security-keys, recovery-codes, github-mobile, personal-access-tokens, sudo-mode]
level: practitioner
status: docs-checked
description: "Secure a GitHub account: two or more 2FA methods, passkeys, saved recovery codes, TOTP app backup and the SSH key, token and device recovery methods."
sources:
  - "https://docs.github.com/en/authentication/securing-your-account-with-two-factor-authentication-2fa"
  - "https://docs.github.com/en/authentication/authenticating-with-a-passkey"
  - "https://docs.github.com/en/authentication/securing-your-account-with-two-factor-authentication-2fa/configuring-two-factor-authentication-recovery-methods"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# GitHub 2FA

**Goal:** a GitHub account is a software supply-chain asset; protect it like one.

## Setup
1. Configure 2FA from your account settings. GitHub's 2FA docs cover several options for
   the second source of authentication, and SMS is supported only in certain countries.
2. Configure **two or more** authentication methods; GitHub strongly recommends this to
   avoid losing access.
3. Download your **recovery codes** and keep them in a password manager or printed copy.
   Do not share them.
4. Passkeys let you sign in without a password and without a separate 2FA step, and can be
   used for sensitive actions (sudo mode) and to authenticate a password reset. For 2FA
   users, eligible security keys can be upgraded to passkeys.
5. As of March 2023 GitHub requires users who contribute code on GitHub.com to enable 2FA.

## Recovery codes
- Settings > "Access" > Password and authentication > next to "Recovery codes" click
  View, then Download, Print or Copy.
- Each code works once. There are 16; if you use them all, "Generate new recovery codes"
  creates another set and **invalidates** the old ones.
- Disabling and re-enabling 2FA, or generating new codes, updates the codes in your
  settings; reconfiguring 2FA without disabling it does not.

## Other recovery methods
GitHub lists four: the recovery codes file, SSH keys, personal access tokens and
verified devices. Set them up before you need them:
- SSH key: add it with the key type "authentication".
- Personal access token: choose the `repo` scope.
- TOTP app: most apps support backups, so a lost device can be replaced from the backup
  (1Password, Google Authenticator and Microsoft Authenticator docs are linked by GitHub).

## Gotchas
- Disabling 2FA on a personal account may cost you access to organisations you belong to.
- If you lose your 2FA credentials, use a recovery code or another recovery option from
  GitHub's "Recovering your account" article.

## Verify
- [ ] At least two authentication methods are configured.
- [ ] Recovery codes are saved outside the device that holds your 2FA app.

## Checked
Checked 2026-11-08 against the three cited GitHub Docs pages. Removed: the file name
and a 28-day check-up claim, the statement that PATs and SSH keys bypass 2FA, Settings
paths for tokens, sessions and applications, the days-long recovery timing and the
fine-grained token advice, none of which the cited pages state.

Method: docs-only read of cited pages, 2026-11-08
