---
id: computing-software.digital-privacy-hygiene.phishing-awareness.oauth-consent-phishing
name: oauth-consent-phishing
category: computing-software
field: digital-privacy-hygiene
product: phishing-awareness
tags: [digital-privacy-hygiene, phishing-awareness, consent-phishing, credential-phishing, oauth-grants, illicit-consent-grant, third-party-app-access, google-connections, microsoft-app-permissions, device-code-phishing]
level: practitioner
status: draft
description: "Recognise phishing that asks you to grant an app access (not a password) to your mailbox or Drive, review the consent screen, and revoke malicious grants."
sources:
  - "https://learn.microsoft.com/en-us/entra/identity/enterprise-apps/protect-against-consent-phishing"
  - "https://support.google.com/accounts/answer/13533235"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# OAuth consent phishing

**Goal:** a link leads to the **real** Google or Microsoft sign-in, then asks you to grant
"Document Viewer" access to read your email and files. No password is stolen, MFA isn't
bypassed, and password changes don't remove the access.

## Recognise
- After signing in on the real domain, a **consent screen**: "<App> wants to access your
  Google Account: Read, compose, send and permanently delete all your email", "Access
  your files", "Maintain access to data you have given it access to" (offline access).
- App name mimics something expected (Docs, Adobe, "Secure Viewer", "Office 365 Update").
- Publisher "unverified" or unknown domain.
A related trick, **device code phishing**, asks you to enter a code at
`microsoft.com/devicelogin` "to view a document", granting the attacker a session token.
Only enter device codes for devices you are setting up yourself.

## Before clicking Allow
Ask: did I start this to use a known app? Do the permissions match what it needs? If in
doubt, Cancel.

## Revoke
- Google: `myaccount.google.com/connections` (Third-party apps & services) > remove access.
- Microsoft personal: `account.live.com/consent/Manage`; work accounts: My Apps / admin.
- GitHub, Slack, Dropbox: Settings > Applications / Connected apps.
Also check email forwarding rules the app may have created.

## Verify
- [ ] Connected apps lists reviewed; unknown grants removed.
