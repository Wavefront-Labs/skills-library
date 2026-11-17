---
id: computing-software.networking-hardware-and-wireless.asterisk.directory-dial-by-name
name: directory-dial-by-name
category: computing-software
field: networking-hardware-and-wireless
product: asterisk
tags: [networking-hardware-and-wireless, asterisk, directory, dial-by-name, voicemail-conf, dialplan, ivr]
level: intro
status: docs-checked
description: "Offer a dial-by-name directory with Directory(voicemail_context,dialplan_context,options), including the f and e options and how entries come from voicemail.conf."
sources:
  - https://docs.asterisk.org/Configuration/Applications/Directory-Application/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# directory dial-by-name
`Directory([voicemail_context,[dialplan_context,[options]]])` asks the caller to enter the first few digits of a name and searches the named context in `voicemail.conf`.

- `voicemail_context`: context in `voicemail.conf` to search; `default` if omitted.
- `dialplan_context`: when the caller picks an entry, Asterisk dials the extension matching that mailbox in this context.
- `options`: `f` searches by first name instead of last name; `e` also reads the extension number. The full list is in `core show application Directory`.

Example from the page: `exten => 6501,1,Directory(vm-demo,users,ef)`.

## Checked
2026-11-04: read the cited Asterisk documentation pages (Directory-Application) and confirmed the commands, options, defaults and names stated above. Nothing removed; every claim was confirmed.

Method: documentation only; no commands were run.
