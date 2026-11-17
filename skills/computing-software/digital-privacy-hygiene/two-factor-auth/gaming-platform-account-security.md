---
id: computing-software.digital-privacy-hygiene.two-factor-auth.gaming-platform-account-security
name: gaming-platform-account-security
category: computing-software
field: digital-privacy-hygiene
product: two-factor-auth
tags: [digital-privacy-hygiene, two-factor-auth, steam-guard, gaming-accounts, playstation-2fa, nintendo-account-2fa]
level: practitioner
status: draft
description: "Secure Steam with the Steam Guard mobile authenticator and revocation code, and turn on 2-step for PlayStation, Xbox, Nintendo and Epic accounts."
sources:
  - "https://help.steampowered.com/"
  - "https://www.playstation.com/en-us/support/account/2sv-account-security/"
  - "https://accounts.nintendo.com/"
  - "https://www.epicgames.com/help/"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Gaming platform account security

**Goal:** game libraries and stored wallets are a top target for phishing and account resale; lock them down.

## Steam
1. In the Steam mobile app: Steam Guard > **Add authenticator**; confirm by SMS and email.
2. **Write down the revocation code** (R followed by digits). It removes the authenticator if you lose the phone;
   without it, recovery goes through Steam Support and can take days.
3. Use the app's QR sign-in or approval prompts; only approve logins you started.
4. Trade and Market: without the mobile authenticator for 7+ days, trades are held up to 15 days.
5. Check Account details > **Manage Steam Guard** > Deauthorize all other devices if you suspect compromise.
6. Never "log in with Steam" on a site reached through a Discord or chat link; fake Steam login pop-ups
   (browser-in-the-browser) are the classic account-theft lure.

## Consoles and launchers
| Platform | Where | Methods |
|---|---|---|
| PlayStation | Account > Security > 2-Step Verification | Authenticator app, SMS; passkey sign-in supported |
| Xbox | Microsoft account security page | Microsoft Authenticator, passkey, security key |
| Nintendo Account | accounts.nintendo.com > Sign-in and security > 2-Step Verification | Authenticator app plus backup codes |
| Epic Games | Account > Password & Security | Authenticator app, SMS, email |

Save each platform's backup codes with your other recovery codes.

## Payment hygiene
Remove stored cards you do not need, require a password for purchases on consoles, and set spending limits for
child accounts.

## Gotchas
- Free-skin, giveaway and "vote for my team" links lead to token stealers; infostealers grab session cookies and
  bypass 2FA, so treat cracked cheats and mods as malware.
