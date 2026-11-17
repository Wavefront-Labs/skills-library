---
id: computing-software.digital-privacy-hygiene.vpn-tools.password-protected-and-expiring-email
name: password-protected-and-expiring-email
category: computing-software
field: digital-privacy-hygiene
product: vpn-tools
tags: [digital-privacy-hygiene, vpn-tools, expiring-email, proton-mail, gmail-confidential-mode, email-encryption]
level: practitioner
status: draft
description: "Send password-protected, expiring emails to non-users with Proton or Tuta, and know why Gmail confidential mode is not end-to-end encryption."
sources:
  - "https://proton.me/support/password-protected-emails"
  - "https://support.google.com/mail/answer/7674059"
  - "https://tuta.com/support#encrypt-email"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Password-protected and expiring messages

**Goal:** send something sensitive by email to someone without an encrypted mail account, and limit how long it
lives.

## Proton Mail
1. Compose > lock icon (**Password protection**); set a password and an optional hint.
2. Clock icon: **expiration** (up to 28 days); the message becomes unreadable after.
3. The recipient gets a link to read and reply securely in a browser.
4. Share the password through a different channel (Signal, phone), never in the same email.

## Tuta
Compose > toggle confidential with a password for external recipients; they read in Tuta's web page.

## Gmail confidential mode
Sets expiry, disables forwarding/copy/print, and can require an SMS code. It is **not** end-to-end encrypted: Google
stores and can read the message, and the recipient can still screenshot it. Useful only to reduce accidental
forwarding.

## Outlook / Microsoft 365
Encrypt or Do Not Forward (Microsoft Purview Message Encryption) protects in transit and controls forwarding, but
Microsoft can access it; requires a qualifying plan.

## Good practice
- Expiry stops future reading, not screenshots or saved copies.
- For files, a one-time encrypted link (Bitwarden Send, Proton Drive share with password and expiry) is often better.
- Phishers mimic "secure message" emails; tell the recipient to expect it.
