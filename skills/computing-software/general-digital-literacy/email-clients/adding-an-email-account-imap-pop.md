---
id: computing-software.general-digital-literacy.email-clients.adding-an-email-account-imap-pop
name: adding-an-email-account-imap-pop
category: computing-software
field: general-digital-literacy
product: email-clients
tags: [email-clients, email-account-setup, add-email-account, imap, pop3, smtp, server-settings, app-password, outlook-add-account, thunderbird]
level: intro
status: docs-checked
description: "Choose IMAP over POP and enter server settings when auto-setup fails, using Outlook.com and Gmail as worked examples, with app passwords for 2-Step Verification."
sources:
  - https://support.google.com/mail/answer/7126229
  - https://support.google.com/mail/answer/7104828
  - https://support.microsoft.com/en-us/outlook/pop-imap-and-smtp-settings-for-outlook-com
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Adding an email account (IMAP vs POP)

**Goal:** your mailbox in your mail app, staying in sync with phone and webmail.

## IMAP vs POP (Gmail's own description)
- IMAP can be used across several devices and keeps mail synced in real time.
- POP suits a single computer: mail is downloaded and you choose how often to fetch it; it is not synced in real time.
- For personal Gmail accounts IMAP access is always on (the Enable/Disable IMAP option was removed from January 2025).

## Manual settings: use your provider's page
Server names and ports are provider-specific; take them from the provider's help page. Two published examples:
- **Outlook.com:** IMAP outlook.office365.com port 993 SSL/TLS; POP outlook.office365.com port 995 SSL/TLS; SMTP smtp-mail.outlook.com port 587 STARTTLS; authentication method OAuth2 (modern authentication).
- **Gmail POP:** pop.gmail.com port 995 with SSL; SMTP smtp.gmail.com port 587 with TLS/STARTTLS, SSL and authentication required. Work or school Gmail accounts: ask the administrator for the SMTP configuration.

## Gotchas
- Gmail says that if you use 2-Step Verification and your client cannot sign in, try an **app password**.
- If you change your Gmail password, you may need to re-enter the account details or repeat setup in the other client.
- Gmail POP in recent mode (prefix the username with `recent:`) shows only the last 30 days of mail; remove that prefix from SMTP settings.
- Gmail is retiring "Check mail from other accounts" (POP fetch) and Gmailify: no new users after the first quarter of 2026, existing users until January 2027. The Gmail mobile apps keep supporting other accounts over IMAP.

## Verify
- [ ] Send a test to yourself; read it on the phone, then see it marked read in the desktop app.

## Checked
2026-10-27. Google Help "Add Gmail to another email client", "Read Gmail messages on other email clients using POP", "Learn about upcoming changes to Gmailify and POP", Microsoft Support "POP, IMAP and SMTP settings for Outlook.com". Confirmed: IMAP vs POP behaviour, the listed hosts and ports, app password advice, recent mode, retirement dates. Removed unconfirmed Outlook, Apple Mail and Thunderbird menu paths, generic `imap.provider.com` ports and port 25 claims.
Method: documentation only; no commands were run.
