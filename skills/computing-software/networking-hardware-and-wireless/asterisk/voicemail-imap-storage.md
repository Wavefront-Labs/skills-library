---
id: computing-software.networking-hardware-and-wireless.asterisk.voicemail-imap-storage
name: voicemail-imap-storage
category: computing-software
field: networking-hardware-and-wireless
product: asterisk
tags: [networking-hardware-and-wireless, asterisk, voicemail, imap, imap-storage, uidplus, folders, email]
level: advanced
status: docs-checked
description: "Plan IMAP voicemail storage for Asterisk: what integration provides, separate versus shared mailboxes and UIDPLUS expunge behaviour, required folders and server versions."
sources:
  - https://docs.asterisk.org/Configuration/Applications/Voicemail/IMAP-Voicemail-Storage/
  - https://docs.asterisk.org/Configuration/Applications/Voicemail/IMAP-Voicemail-Storage/Voicemail-and-IMAP-Folders/
  - https://docs.asterisk.org/Configuration/Applications/Voicemail/IMAP-Voicemail-Storage/Separate-vs.-Shared-E-mail-Accounts/
  - https://docs.asterisk.org/Configuration/Applications/Voicemail/IMAP-Voicemail-Storage/IMAP-Server-Implementations/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# voicemail imap storage
With IMAP storage, Asterisk stores voicemail in IMAP rather than the file structure. Benefits listed: listening on the phone marks the message read; deleting on the phone deletes it from the mailbox; opening or deleting the voicemail email clears MWI (deleting also removes it from the voicemail system).

- Folders: besides INBOX, create "Old", "Work", "Family" and "Friends" at the same hierarchy level to mimic file-based voicemail. Avoid the top-level folder where users keep lots of email, which can cause long delays.
- Account choice: a shared mailbox puts voicemail in the user INBOX, but if the server lacks UIDPLUS, Asterisk expunges all messages marked for deletion when the user leaves voicemail. A separate voicemail mailbox avoids expunging regular email.
- Servers: UW IMAP-2005 or earlier has no UIDPLUS; UW IMAP-2006 supports UIDPLUS; both are not recommended. UW IMAP-2007 is the recommended version. Cyrus IMAP 2.3.3 was tested with hierarchy delimiter `/`.

## Checked

2026-11-09. Confirmed against the four cited Asterisk IMAP voicemail storage pages: integration benefits, extra folders and the top-level folder warning, shared versus separate mailbox and UIDPLUS expunge behaviour, UW IMAP and Cyrus IMAP versions. Removed the quota bullet, description mention and tag because none of the cited pages states it.
Method: documentation only; no commands were run.
