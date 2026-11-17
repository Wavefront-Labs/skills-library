---
id: computing-software.email-administration.mail-server-administration.postsuper-operations
name: postsuper-operations
category: computing-software
field: email-administration
product: mail-server-administration
tags: [postsuper-operations, postsuper, hold-release, delete-queue]
level: practitioner
status: draft
description: "Hold, release, requeue and delete queued mail with postsuper, including bulk deletes by sender or domain."
sources:
  - https://www.postfix.org/documentation.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Postsuper operations

**Goal:** act on queue entries safely.
## Commands
- `postsuper -h <id>` hold; `postsuper -H <id>` release; `postsuper -r <id>` requeue; `postsuper -d <id>` delete one.
- Delete all deferred: `postsuper -d ALL deferred`.
- Delete by sender: `postqueue -p | awk` to collect ids, then `postsuper -d -` (reads ids on stdin).
- `postsuper -p` purges stale temp files; `postsuper -s` structure check.
## Failure modes
- `postsuper -d ALL` removes legitimate mail; review `qshape` first.
- Deleting does not notify senders; for abuse spam that is intended, for real mail send a notice.
## Verify
- `postqueue -p | tail -1` shows the new total ("-- N Kbytes in M Requests").

## Notes
- Written from the cited documentation; not run end to end here, so confirm option names against your Postfix/Dovecot version.
- Change one thing at a time in staging and keep a copy of the previous config.
