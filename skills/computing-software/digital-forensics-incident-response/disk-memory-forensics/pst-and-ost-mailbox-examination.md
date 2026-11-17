---
id: computing-software.digital-forensics-incident-response.disk-memory-forensics.pst-and-ost-mailbox-examination
name: pst-and-ost-mailbox-examination
category: computing-software
field: digital-forensics-incident-response
product: disk-memory-forensics
tags: [pst-ost, email-forensics, outlook, libpff, mailbox-export, dfir]
level: practitioner
status: draft
description: "Examine Outlook PST and OST files: locating them, extracting with libpff or commercial tools, deleted items and recoverable data, attachments and metadata timestamps."
sources: ["https://github.com/libyal/libpff", "https://learn.microsoft.com/en-us/openspecs/office_file_formats/ms-pst/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# PST and OST mailbox examination

**Goal:** extract messages, attachments and metadata (including deleted items) from local
Outlook data files.

## Locations
- OST (cached Exchange/M365): `Users\<u>\AppData\Local\Microsoft\Outlook\<account>.ost`
- PST (archives, POP/IMAP): `Users\<u>\Documents\Outlook Files\*.pst` or anywhere; search
  all volumes for `*.pst` and the PST header magic `!BDN`.
- Attachment temp: `AppData\Local\Microsoft\Windows\INetCache\Content.Outlook\<random>\`
  (opened attachments; often holds the maldoc).

## Extraction
```bash
pffinfo mailbox.ost
pffexport -m all -f all -t /cases/014/pff mailbox.ost   # exports items, attachments, recovered
```
`-m all` includes recovered (deleted) items from the PST/OST internal structures. Also:
Kernel/Aid4Mail/AXIOM/Intella (commercial), or open a PST in Outlook in an isolated VM
(never on your analysis host with network).

## Metadata
- `PR_CLIENT_SUBMIT_TIME` (sent), `PR_MESSAGE_DELIVERY_TIME` (received),
  `PR_CREATION_TIME`, `PR_LAST_MODIFICATION_TIME`, transport headers (`PR_TRANSPORT_MESSAGE_HEADERS`).
- OSTs only contain what was synchronised (cache window: often 1 year by default for new
  profiles); the server mailbox may hold more.

## Deleted items
Deleted Items folder, Recoverable Items (server-side, not in OST), and orphaned blocks inside
the PST/OST recoverable by `pffexport -m all` or forensic tools.

## Gotchas
- OST is tied to the profile; tools can read it offline, Outlook cannot open a foreign OST.
- Large OSTs and Unicode vs ANSI PST formats; use current tool versions.

## Verify
Count of exported items per folder roughly matches the folder counts shown by pffinfo or the
mailbox server, and key emails' headers match server-side message trace.
