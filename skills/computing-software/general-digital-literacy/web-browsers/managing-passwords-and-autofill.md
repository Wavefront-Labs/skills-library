---
id: computing-software.general-digital-literacy.web-browsers.managing-passwords-and-autofill
name: managing-passwords-and-autofill
category: computing-software
field: general-digital-literacy
product: web-browsers
tags: [web-browsers, password-manager, autofill, saved-passwords, breach-alert, password-checkup, passkeys, weak-password-warning, autofill-addresses, autofill-payment-methods, syncing-passwords]
level: intro
status: docs-checked
description: "Set up the browser's built-in password manager and autofill correctly, respond to breach/weak-password alerts, and know when to use a dedicated manager instead."
sources:
  - https://support.google.com/chrome/answer/95606
  - https://support.google.com/chrome/answer/142893
  - https://support.google.com/chrome/answer/13168025
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Managing passwords and autofill — let the browser remember, correctly

**Goal:** use the password manager already built into the browser properly — generating
unique passwords, saving them, autofilling safely — and act on breach/weak-password
warnings instead of dismissing them. The steps below are for Chrome; other browsers have
equivalents under their own settings, so check that browser's help.

## 1. Turning it on and where it lives
- Chrome (desktop): More › Passwords and autofill › Google Password Manager. Saved
  Google Account passwords are also at passwords.google.com.
- When you enter a new password on a site, Chrome offers to save it. The offer can be
  switched on or off under Google Password Manager › Settings › "Offer to save passwords
  and passkeys".

## 2. Generating unique passwords
- In a password field on a sign-up form choose "Use strong password"; if it does not
  appear, right-click the field › "Generate password". Review the preview, then "Use
  suggested password". The generated password is saved to your Google Account.
- The point is **one unique password per site** — a password reused across accounts
  means one breached site compromises every account using it.

## 3. Autofill beyond passwords
- Chrome: More › Passwords and autofill. Addresses are under Contact info, cards under
  Payments. Addresses are saved in your Google Account when signed in; payment methods
  added in Chrome are saved in Google Wallet.
- Chrome partly hides sensitive info and requires a screen lock or similar verification
  before filling it into forms. Still rely on your device lock as the real boundary:
  anyone who can unlock your device can reach what is saved.
- Review saved cards periodically and remove old or cancelled ones.

## 4. Breach alerts and weak-password warnings
- In Google Password Manager, select **Checkup** for details on passwords exposed in a
  data breach and on weak, easy-to-guess passwords.
- To get alerts, open Settings › Privacy and security › Security and turn on "Warn you
  if a password was compromised in a data breach" (requires Safe Browsing on).
- **Act on a breach alert**: change that password at the site, and anywhere else you
  reused it. Replace a weak password with a generated one.

## 5. Passkeys
- A passkey is an alternative to a password, unique for each site and app. Chrome can
  save them in Google Password Manager (Windows 10 or later, Chromebook, Mac, Linux),
  stored in your Google Account and synced across devices signed in to the same account.
- Passkeys saved to Windows Hello or a security key are not synced: Windows Hello ones
  cannot be recovered if the computer is lost, and security-key ones cannot be recovered
  if the key is lost or reset. Where a site offers a passkey, consider setting one up.

## 6. When to use a dedicated password manager instead
Consider a dedicated manager if you use several browsers or ecosystems daily, or want a
shared household vault; otherwise the built-in manager is a reasonable default. Check a
product's own documentation for its features.

## Verify
- [ ] The browser's password manager is turned on and actively saving logins.
- [ ] New accounts use a generated password, not a reused or memorised one.
- [ ] Any breach-checkup alert has been acted on (password changed), not just seen.
- [ ] Passkeys are set up on the accounts that matter most where offered, and you know
      where each is stored.

## Checked
2026-11-01. Confirmed from Chrome Help pages on passwords (menu path, save offer, strong
password option, Checkup, breach warning setting), autofill (Contact info, Payments,
Google Wallet, screen-lock verification) and passkeys (Google Password Manager, sync,
Windows Hello and security-key limits). Removed: chrome:// URLs, Edge, Firefox and Safari
paths, tokenised-card and privacy-preserving-check claims, reused-password check, the
named dedicated managers, and the breach-list wording.
Method: documentation only; no commands were run.
