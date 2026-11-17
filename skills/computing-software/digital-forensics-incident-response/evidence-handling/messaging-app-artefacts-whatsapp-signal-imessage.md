---
id: computing-software.digital-forensics-incident-response.evidence-handling.messaging-app-artefacts-whatsapp-signal-imessage
name: messaging-app-artefacts-whatsapp-signal-imessage
category: computing-software
field: digital-forensics-incident-response
product: evidence-handling
tags: [messaging-app-forensics, whatsapp, signal, imessage, mobile-forensics, sqlite-forensics, dfir]
level: advanced
status: draft
description: "Locate and interpret messaging app artefacts for WhatsApp, Signal, iMessage and Telegram on iOS, Android and desktop, including databases, encryption and backups."
sources: ["https://www.sans.org/posters/ios-third-party-apps-forensics-reference-guide-poster/", "https://github.com/abrignoni/iLEAPP", "https://github.com/abrignoni/ALEAPP"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Messaging app artefacts: WhatsApp, Signal, iMessage

**Goal:** recover message content, contacts, attachments and timing from messaging apps in a
lawful, scoped collection.

## iOS (from full file system extraction or iTunes/Finder backup)
| App | Location / database |
|---|---|
| iMessage/SMS | `HomeDomain/Library/SMS/sms.db` (tables `message`, `handle`, `chat`, `attachment`); dates are seconds or nanoseconds since 2001-01-01 (Mac absolute time) |
| WhatsApp | `AppDomainGroup-group.net.whatsapp.WhatsApp.shared/ChatStorage.sqlite` (`ZWAMESSAGE`, `ZWACHATSESSION`), media in `Message/Media` |
| Signal | `grdb/signal.sqlite`, SQLCipher-encrypted; key in the keychain, needs full file system extraction with keychain |
| Telegram | `telegram-data/account-*/postbox/db/db_sqlite` (proprietary blobs) |
Backups exclude some data unless encrypted backups are used (encrypted backups include
more, e.g. keychain items).

## Android (full file system or app-specific extraction)
- WhatsApp: `/data/data/com.whatsapp/databases/msgstore.db` (`message` table) and
  `wa.db` (contacts); local backups `msgstore.db.crypt14/15` need the key file from
  `/data/data/com.whatsapp/files/key`.
- Signal: `/data/data/org.thoughtcrime.securesms/databases/signal.db`, SQLCipher with key
  in Android Keystore; usually only via device-level extraction by commercial tools.
- SMS: `mmssms.db` (`sms` table), timestamps in ms since 1970.

## Desktop
WhatsApp Desktop (`%LOCALAPPDATA%\Packages\5319275A.WhatsAppDesktop_*`), Signal Desktop
(`%APPDATA%\Signal\sql\db.sqlite`, SQLCipher with key in `config.json` / DPAPI-protected
`encryptedKey` in recent versions), iMessage on macOS `~/Library/Messages/chat.db`.

## Tools
iLEAPP/ALEAPP (open source parsers), commercial (Cellebrite, Magnet AXIOM, Oxygen). Validate
parser output by querying the SQLite directly for key messages.

## Gotchas
- Disappearing messages, deleted messages in SQLite freelists/WAL may be partially
  recoverable; examine `-wal` files before opening the DB (opening can checkpoint and
  overwrite).
- Time zones: convert epoch formats carefully and state UTC.

## Verify
For each key message reported, cite database, table, row ID, raw timestamp and converted
time, and confirm with a second tool or manual SQL query.
