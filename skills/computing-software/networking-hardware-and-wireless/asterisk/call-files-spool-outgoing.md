---
id: computing-software.networking-hardware-and-wireless.asterisk.call-files-spool-outgoing
name: call-files-spool-outgoing
category: computing-software
field: networking-hardware-and-wireless
product: asterisk
tags: [networking-hardware-and-wireless, asterisk, call-files, pbx-spool, outgoing, spool, originate, waittime, maxretries, callfile]
level: practitioner
status: docs-checked
description: "Originate calls by dropping a call file in the outgoing spool: Channel, Callerid, WaitTime, MaxRetries, RetryTime, Application or Context/Extension/Priority, Setvar, Archive."
sources:
  - https://docs.asterisk.org/Configuration/Interfaces/Asterisk-Call-Files/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# call files
A call file starts a call outside the dialplan, AMI or ARI. Create the file, then place it in the `outgoing` spool directory (location configurable in `asterisk.conf`); `pbx_spool.so` watches it using inotify or kqueue, or polls every second otherwise. On an NFS-mounted spool, inotify does not work; build with `--without-inotify` to force polling.

**Never create the file directly in `outgoing`.** Write it elsewhere on the same filesystem and move it in, or Asterisk may read a partial file.

Format: one `Key: value` per line; `#` or `;` start comments (no `;----;` blocks).

Setup keys:
- `Channel: technology/resource` (required)
- `Callerid`, `Account` (becomes `CDR(accountcode)`)
- `WaitTime` (default 45 s), `MaxRetries` (default 0), `RetryTime` (default 300 s)

On answer, either:
- `Application` plus `Data`, or
- `Context`, `Extension`, `Priority` (number or label), with any number of `Setvar: var=value`.

End of processing: `Archive: yes` moves the file to `outgoing_done` (default is deletion) and Asterisk appends `Status:` of Expired, Completed or Failed. Asterisk also appends retry counters while retrying.

## Checked
2026-11-04: read the cited Asterisk documentation pages (Asterisk-Call-Files) and confirmed the commands, options, defaults and names stated above. Nothing removed; every claim was confirmed.

Method: documentation only; no commands were run.
