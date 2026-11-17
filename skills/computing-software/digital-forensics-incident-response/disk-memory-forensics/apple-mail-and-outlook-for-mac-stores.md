---
id: computing-software.digital-forensics-incident-response.disk-memory-forensics.apple-mail-and-outlook-for-mac-stores
name: apple-mail-and-outlook-for-mac-stores
category: computing-software
field: digital-forensics-incident-response
product: disk-memory-forensics
tags: [apple-mail, outlook-for-mac, emlx, macos-forensics, email-forensics, dfir]
level: practitioner
status: draft
description: "Examine Apple Mail (.emlx, Envelope Index SQLite) and Outlook for Mac (olk15 profile store) on macOS: locations, parsing, attachments, deleted mail and account mapping."
sources: ["https://github.com/mac4n6/APOLLO", "https://forensicswiki.xyz/wiki/index.php?title=Apple_Mail"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Apple Mail and Outlook for Mac stores

macOS mail clients do not use PST. Apple Mail stores one file per message; new Outlook for Mac uses a profile database with message files alongside.

## Apple Mail
Location: `~/Library/Mail/V<n>/` (V10 on recent macOS; protected by TCC/Full Disk Access on a live system).
- `V<n>/<account-UUID>/<Mailbox>.mbox/<UUID>/Data/.../Messages/<id>.emlx`: each `.emlx` is a byte count line, the raw RFC 5322 message, then an XML plist with flags and dates. `.partial.emlx` means attachments were stored separately under `Attachments/<id>/`.
- `V<n>/MailData/Envelope Index` (SQLite): tables `messages`, `subjects`, `addresses`, `mailboxes`; gives date_received, date_sent, read/flag state, deleted flag and mailbox for every message, including ones whose `.emlx` is gone.
- `~/Library/Mail/V<n>/MailData/Accounts*.plist` and `~/Library/Accounts/Accounts4.sqlite` map account UUIDs to email addresses.
- Attachments opened by the user also appear in `~/Library/Containers/com.apple.mail/Data/Library/Mail Downloads/` and in quarantine events.

Parse: strip the first line and trailing plist from `.emlx` to get a standard `.eml`, then use normal email header analysis. Query Envelope Index:
```sql
SELECT m.ROWID, datetime(m.date_received,'unixepoch') AS received, s.subject, a.address AS sender, mb.url, m.deleted
FROM messages m LEFT JOIN subjects s ON m.subject=s.ROWID
LEFT JOIN addresses a ON m.sender=a.ROWID LEFT JOIN mailboxes mb ON m.mailbox=mb.ROWID
ORDER BY m.date_received;
```
(Column names vary by version; check `.schema messages`.)

## Outlook for Mac
- New Outlook (2016 and later): `~/Library/Group Containers/UBF8T346G9.Office/Outlook/Outlook 15 Profiles/<Profile>/Data/`. `Outlook.sqlite` indexes items; message bodies are `.olk15Message` files under `Messages/`, attachments as `.olk15MsgAttachment`.
- The newest "New Outlook for Mac" relies more on cloud sync; much content may only be in the server mailbox; collect from Exchange Online as well.
- Legacy Outlook 2011: `.olm` export files or the Microsoft User Data identity database.

## Gotchas
- IMAP/Exchange accounts cache only part of the mailbox; absence locally is not deletion.
- Apple Mail rebuilds Envelope Index; WAL files (`Envelope Index-wal`) may hold recent changes; collect them together.
- Spotlight indexes mail content; its store can show messages since removed.

## Verify
Message counts per mailbox from Envelope Index reconcile with `.emlx` files found, and every message cited has headers parsed from the raw file.
