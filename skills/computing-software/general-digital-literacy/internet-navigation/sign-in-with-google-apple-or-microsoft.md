---
id: computing-software.general-digital-literacy.internet-navigation.sign-in-with-google-apple-or-microsoft
name: sign-in-with-google-apple-or-microsoft
category: computing-software
field: general-digital-literacy
product: internet-navigation
tags: [internet-navigation, in-forms-accounts, sign-in-with-google, sign-in-with-apple, single-sign-on, social-login]
level: intro
status: docs-checked
description: "Decide when to use Sign in with Google, Apple, Microsoft or Facebook on websites, what data is shared, Hide My Email, and how to review and remove connected apps."
sources:
  - https://support.google.com/accounts/answer/12849458
  - https://support.google.com/accounts/answer/13533235
  - https://support.apple.com/en-us/102571
  - https://support.microsoft.com/en-gb/privacy/access-your-account-privacy-settings
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Sign in with Google, Apple or Microsoft

## Pros and cons
- **Pros:** no new password to reuse or leak; inherits your Google/Apple/Microsoft 2-step verification and passkeys; fewer phishing targets.
- **Cons:** if you lose that main account, you lose every site that relies on it; the site learns your name/email and the provider learns which sites you use.
- Good for low-stakes sites; for important accounts (banking, work) use a separate login with a password manager and 2FA, unless the site only offers SSO.

## What's shared
- The consent screen lists it: usually name, email, profile picture. Decline extra permissions (contacts, Drive, calendar) unless the app genuinely needs them.
- **Sign in with Apple** lets you hide your email address from the app (Hide My Email); you can turn off forwarding per app or developer in Settings › your name › iCloud › Hide My Email (iCloud+ Features section). Stopping it for one app applies to all apps from that developer.

## Review and remove
- **Google:** your Google Account's linked apps page › *Sign in with Google* › pick the app › See details › **Stop using Sign in with Google** › Confirm. This stops automatic sign-in; it does not delete your data in the app.
- **Apple:** iPhone/iPad Settings › your name › **Sign in with Apple** › pick the app › Delete; Mac System Settings › your name › Sign in with Apple; web: account.apple.com › Sign-In & Security › Sign in with Apple. You are signed out of the app; signing in with Apple again returns you to the same account.
- **Microsoft:** sign in at account.microsoft.com › Privacy › Other privacy settings › **Apps and services that can access your data** (per Microsoft's privacy-settings page).
- Removing the connection doesn't delete your account on the site; delete it there first.

## Gotchas
- Mixing methods creates duplicate accounts: if you signed up with Google, always choose Google.
- Fake SSO pop-ups exist; the real one opens a Google, Apple or Microsoft sign-in page, not a form inside the website itself; check the address bar.

## Verify
- [ ] Connected-apps list contains only sites you still use.

## Checked

Checked 2026-10-27 against Google Account Help (answers 12849458, 13533235), Apple Support 102571 (published 14 Sep 2026) and Microsoft Support (account privacy settings). Confirmed: Google linked-apps removal steps and that data in the app is not deleted; Apple Settings > your name > Sign in with Apple, Hide My Email forwarding path, same-account behaviour on re-sign-in, account.apple.com; Microsoft Apps and services entry under Privacy.

Method: documentation only; no commands were run.
