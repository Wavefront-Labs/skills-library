---
id: computing-software.digital-privacy-hygiene.privacy-configuration.revoking-google-third-party-access
name: revoking-google-third-party-access
category: computing-software
field: digital-privacy-hygiene
product: privacy-configuration
tags: [digital-privacy-hygiene, privacy-configuration, google-third-party-access, google, oauth, sign-in-with-google, app-passwords, security-checkup]
level: intro
status: draft
description: "Review and remove third-party apps with access to a Google account, Sign in with Google links, and app passwords, prioritising Gmail and Drive scopes."
sources:
  - "https://support.google.com/accounts"
  - "https://myaccount.google.com/connections"
  - "https://myaccount.google.com/security-checkup"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Revoking Google third-party access

**Goal:** an app you tried once years ago should not still be able to read your Gmail or Drive.

## Review
- Go to myaccount.google.com/connections (**Third-party apps & services**). Each entry shows:
  - **Sign in with Google** only (identity, low risk), or
  - **access to** specific data: Gmail, Drive, Calendar, Contacts, Photos, YouTube.
- Open each: it lists exact scopes ("Read, compose, send, and permanently delete all your email") and when access
  was granted.

## Remove
- Delete access for anything unused, unknown, or with broader scope than it needs. Mail-reading "unsubscribe"
  and "receipt tracker" services commonly sell data.
- Before removing a Sign in with Google link, make sure you can still log in to that service another way (or
  delete that account first).
- myaccount.google.com/apppasswords: revoke **app passwords** you no longer use; they bypass 2-Step Verification.

## Also check
- Security Checkup (myaccount.google.com/security-checkup): devices, recent security events, third-party access.
- Gmail > Settings > See all settings > **Forwarding and POP/IMAP** and **Filters**: attackers who got in often add
  a forwarding address or filter; remove unknown ones.
- Google Drive: Settings > **Manage apps** for Drive-connected apps.
- Workspace users: the admin may restrict which apps can be granted access.

## After a phishing incident
OAuth grants survive a password change. If you clicked "Allow" on a suspicious consent screen, remove that app
here immediately.

## Verify
- [ ] Only apps you use and trust have data access; no app passwords left unexplained; no unknown forwarding.
