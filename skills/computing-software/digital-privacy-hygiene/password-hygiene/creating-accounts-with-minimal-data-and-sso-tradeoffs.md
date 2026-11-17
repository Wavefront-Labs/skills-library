---
id: computing-software.digital-privacy-hygiene.password-hygiene.creating-accounts-with-minimal-data-and-sso-tradeoffs
name: creating-accounts-with-minimal-data-and-sso-tradeoffs
category: computing-software
field: digital-privacy-hygiene
product: password-hygiene
tags: [digital-privacy-hygiene, password-hygiene, social-login, data-minimization-signup, sign-in-with-apple, sign-in-with-google, oauth-scopes, email-aliases, account-creation, hide-my-email]
level: intro
status: draft
description: "Create new accounts with the least personal data, and decide between 'Sign in with Google/Apple' and email+password on lock-in, tracking and recovery grounds."
sources:
  - "https://www.privacyguides.org/en/basics/account-creation/"
  - "https://support.apple.com/en-us/102609"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Creating accounts with minimal data, and SSO trade-offs

**Goal:** every field you fill at signup ends up in a breach or a data broker eventually.

## Minimal-data signup checklist
- Read what's **required** (asterisks); skip optional fields.
- Email: unique alias (Hide My Email, SimpleLogin, Firefox Relay, own domain).
- Phone: skip unless required for 2FA; if required, consider a secondary number.
- Birthday: only if legally needed (age gates); otherwise any adult date you record in
  the vault.
- Name: real only where identity matters (banks, government, shipping).
- Uncheck marketing consent and "share with partners".
- Don't upload contacts when apps ask "find your friends".

## Sign in with Google / Apple / Facebook: trade-offs
| | SSO | Email + password (from vault) |
|---|---|---|
| Security | Inherits the provider's MFA/passkeys; no new password to leak | Depends on the site's storage; manager makes it unique |
| Privacy | Provider learns which services you use; Facebook/Google may share profile | Site only gets what you give |
| Lock-in/recovery | Lose the Google account = lose all linked accounts; site may not let you add a password later | Independent |
| Unlinkability | **Sign in with Apple** offers Hide My Email (relay address) | Alias gives same |
Practical rule: Sign in with Apple (hidden email) is reasonable; Google SSO for
low-stakes services is fine if your Google account is strongly protected; avoid Facebook
login. For important services, use email + password + MFA so they're independent.

## Check scopes
The consent screen lists what the site gets (name, email, contacts, Drive). Deny if it
asks for more than identity.

## Verify
- [ ] Last 5 new accounts used aliases and no optional data.
- [ ] SSO connections list reviewed for scope creep.
