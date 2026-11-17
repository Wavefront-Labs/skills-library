---
id: computing-software.digital-privacy-hygiene.two-factor-auth.paypal-2fa-and-login-alerts
name: paypal-2fa-and-login-alerts
category: computing-software
field: digital-privacy-hygiene
product: two-factor-auth
tags: [digital-privacy-hygiene, two-factor-auth, paypal-2fa, paypal, two-step-verification, login-alerts]
level: practitioner
status: draft
description: "Turn on PayPal 2-step verification with an authenticator app or passkey, remove weak fallbacks, and set alerts for logins and payments."
sources:
  - "https://www.paypal.com/us/security"
  - "https://www.paypal.com/us/legalhub/useragreement-full"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# PayPal 2FA and login alerts

**Goal:** a PayPal account that a phished password or SIM swap cannot drain.

## Turn on 2-step verification
1. Settings (gear) > **Security** > 2-step verification > Set up.
2. Choose **authenticator app** over text message; scan the QR into your TOTP app and enter the code.
3. Add a passkey too (Security > Passkeys, or accept the prompt at login) for phishing-resistant sign-in.
4. Keep a second method enrolled so a lost phone is not a lockout.

## Tighten fallbacks
- Remove old phone numbers and email addresses under Settings > Account; each is a recovery path.
- Make the email on the account one with strong 2FA, since PayPal password resets go there.
- Review **Security > Manage your logins / devices** and log out unknown sessions.

## Alerts
Settings > **Notifications**: enable email and app notifications for money sent, payments received, and account
changes. In the app, allow push notifications so a strange payment pings you immediately.

## Connected access
Settings > Payments > **Automatic payments**: cancel merchants you no longer use; each is a standing debit
permission. Review "Connected apps" / Log in with PayPal and remove old sites.

## If something looks wrong
Report unauthorised transactions in the Resolution Center within 60 days of the statement (PayPal buyer
protection window), change the password, and check the linked bank and card for direct debits.

## Gotchas
- SMS codes are phishable and SIM-swappable; keep SMS only if no other method works.
- Phishers send fake "PayPal invoice" emails from real PayPal (callback phishing); check activity in the app, not via
  the email.
