---
id: computing-software.general-digital-literacy.email-clients.mail-not-syncing-or-send-errors
name: mail-not-syncing-or-send-errors
category: computing-software
field: general-digital-literacy
product: email-clients
tags: [email-clients, email-account-setup, email-sync-error, smtp-error, outlook-not-syncing, mail-app-troubleshooting]
level: practitioner
status: draft
description: "Fix mail apps that stop syncing or fail to send: password changes, app passwords, SMTP settings, full mailboxes, offline mode and repairing profiles."
sources:
  - https://support.microsoft.com/en-us/outlook
  - https://support.google.com/mail
  - https://support.apple.com/guide/mail/welcome/mac
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Mail not syncing or send errors

## First checks
1. Does webmail work (gmail.com, outlook.com, icloud.com)? If not, it's the account/server, not the
   app: check status pages and mailbox storage.
2. Did you change the password, turn on 2-step verification, or get a security alert? The app needs
   re-signing in (or an app password for old IMAP apps).
3. Is the app offline? Outlook: **Send/Receive › Work Offline** off. Phone: mobile data allowed for the
   mail app, Low Data/Battery Saver not blocking background fetch.

## By symptom
- **Password prompt loops**: remove the account and add it again with modern sign-in (OAuth). Old
  "basic auth" with plain passwords is switched off at Microsoft and Google for most apps.
- **Send fails, receive works**: SMTP settings: port 587 STARTTLS (or 465 SSL), authentication on,
  same username/password as incoming. Some ISPs block port 25.
- **Mailbox full**: sends fail with "quota" bounces; free space.
- **Outlook classic stuck "Updating folder"**: File › Account Settings › Repair; rebuild the OST
  (close Outlook, rename the .ost in %LOCALAPPDATA%\Microsoft\Outlook, reopen) or create a new
  profile (Control Panel › Mail › Show Profiles › Add).
- **Apple Mail**: Mailbox › Take All Accounts Online; Window › Connection Doctor.
- **Phone shows old mail only**: Settings › Mail › Accounts › Fetch New Data: *Push*/*Fetch every 15
  minutes*; Outlook/Gmail apps: sign out/in.

## Verify
- [ ] Send and receive a test both ways; sent item appears in webmail's Sent folder.
