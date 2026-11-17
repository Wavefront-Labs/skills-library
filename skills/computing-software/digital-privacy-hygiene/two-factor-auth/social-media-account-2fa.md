---
id: computing-software.digital-privacy-hygiene.two-factor-auth.social-media-account-2fa
name: social-media-account-2fa
category: computing-software
field: digital-privacy-hygiene
product: two-factor-auth
tags: [digital-privacy-hygiene, two-factor-auth, social-media-2fa, mfa-rollout, facebook, instagram, whatsapp-two-step, tiktok, x-twitter, linkedin, accounts-center, login-alerts]
level: intro
status: draft
description: "Enable 2FA and login alerts on Facebook, Instagram, WhatsApp, TikTok, X and LinkedIn, where hijacked accounts are used to scam your contacts."
sources:
  - "https://www.facebook.com/help/148233965247823"
  - "https://faq.whatsapp.com/1920866721452534"
  - "https://help.x.com/en/managing-your-account/two-factor-authentication"
  - "https://www.linkedin.com/help/linkedin/answer/a1338780"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Social media account 2FA

**Goal:** hijacked social accounts are used to run "I'm stuck abroad, send money" and
crypto scams against your friends. 2FA plus login alerts stops most takeovers.

## Where to turn it on (paths change; search "two-factor" in settings if moved)
| Service | Path | Best method offered |
|---|---|---|
| Facebook / Instagram | Accounts Center > Password and security > **Two-factor authentication** | Authenticator app or security key (Facebook); authenticator (Instagram) |
| WhatsApp | Settings > Account > **Two-step verification** (6-digit PIN + email) and **Passkeys** | PIN + passkey |
| X | Settings > Security and account access > Security > Two-factor | Security key or authenticator (SMS 2FA is limited to paid accounts) |
| TikTok | Settings > Security & permissions > 2-step verification | Authenticator app |
| LinkedIn | Settings > Sign in & security > Two-step verification | Authenticator app |
| Snapchat | Settings > Two-Factor Authentication | Authenticator |

## Also on each
- **Login alerts** for unrecognised logins (Accounts Center > Security checks).
- **Where you're logged in**: end sessions you don't recognise.
- Recovery codes printed for Meta accounts (Recovery codes in 2FA settings).
- Remove old phone numbers.

## Gotchas
- Meta "your page will be disabled" messages with links are phishing; real notices
  appear in Accounts Center / Support Inbox.
- A friend asking you for "the code I accidentally sent to your phone" is a takeover in
  progress (WhatsApp/Instagram). Never forward codes.

## Verify
- [ ] Each social account shows 2FA on with an app or key.
- [ ] Active sessions list contains only your devices.
