---
id: computing-software.email-administration.dovecot.doveadm-exit-codes-and-http-api-warning
name: doveadm-exit-codes-and-http-api-warning
category: computing-software
field: email-administration
product: dovecot
tags: [doveadm, exit-codes, sysexits, doveadm-http-api, ex-tempfail, dsync-migration]
level: practitioner
status: docs-checked
description: "Interpret doveadm and dsync exit codes during migrations, which ones mean retry, and why the doveadm HTTP API must not face untrusted networks."
sources:
  - https://doc.dovecot.org/main/core/admin/doveadm.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Doveadm is Dovecot's administration tool. It can run from the command line, over the doveadm protocol, or through the doveadm HTTP API. doveadm and dovecot-lda mostly use sysexits.h compatible codes.

Codes relevant to dsync migrations:
- 2: success, but the mailbox changed during the sync. Safe to ignore in intermediate migrations since the next sync catches changes; for a final cut-over, re-run dsync.
- 64 EX_USAGE: wrong parameters; should never appear in production, barring a bug.
- 65 EX_DATAERR: should not happen; treat as a failed migration and report it.
- 67 EX_NOUSER: the user is gone from the userdb. Remove them from the migration list, or investigate the identity backend.
- 68 EX_NOHOST: source or destination hostname unknown.
- 71 and 72: operating system problems on the dsync host.
- 73 EX_CANTCREAT: out of quota, hinting at duplicate messages.
- 75 EX_TEMPFAIL: temporary failure. Re-run, with a maximum retry count after which the account is flagged.
- 77 EX_NOPERM: authentication failure; with master-user auth to the old backend this indicates a configuration bug, and all migrations should pause.
- 78 EX_CONFIG: invalid settings; suspend all migrations until fixed.
- 1003 DOVEADM_EX_EXPIRED (added 2.4.0): the requested contents are outdated.

dsync fixes invalid folder names; a too-long name becomes a generated GUID, and a renamed folder is not synced afterwards.

Security: never expose the doveadm HTTP API to untrusted networks, because it has dangerous features. Limit it to your integration layer, with TLS and a random password or API key.

## Checked

2026-11-03. Confirmed on the Doveadm admin page: the sysexits-compatible code table (2, 64, 65, 67, 68, 71, 72, 73, 75, 77, 78 and 1003 DOVEADM_EX_EXPIRED, added 2.4.0) with the retry versus suspend guidance for each, the folder-rename note (invalid names fixed, too-long names become a generated GUID, no incremental sync after a rename), and the HTTP API warning (never expose to untrusted networks; TLS, random password or API key, network restrictions). Nothing removed.

Method: documentation only; no commands were run.
