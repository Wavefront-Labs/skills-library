---
id: computing-software.systems-network-administration.paperless-ngx.trash-and-audit-log
name: trash-and-audit-log
category: computing-software
field: systems-network-administration
product: paperless-ngx
tags: [paperless-ngx, trash, empty-trash-delay, audit-log, document-history, prune-audit-logs]
level: practitioner
status: docs-checked
description: "Configure the document trash retention and optional off-site original copies, and keep the audit log trimmed."
sources:
  - "https://docs.paperless-ngx.com/usage/"
  - "https://docs.paperless-ngx.com/configuration/"
  - "https://docs.paperless-ngx.com/administration/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Trash and audit log

## Trash
A deleted document is moved to the trash until it is explicitly deleted or automatically removed after a set time. Until then, all files and database content remain intact and it can be restored. `PAPERLESS_EMPTY_TRASH_DELAY` is the retention in days: default 30, minimum 1. `PAPERLESS_EMPTY_TRASH_TASK_CRON` schedules emptying the trash of expired documents (default `0 1 * * *`, once per day).

To keep a last-chance copy, set `PAPERLESS_EMPTY_TRASH_DIR` to a directory that exists and is writeable by the user running Paperless (inside a permanent volume in Docker, such as `../media/trash`). Deleted files' originals are moved there when the trash is emptied. Only the original file is kept; the archive file and all database information are permanently removed.

Deleting a root document moves its versions to the trash as well. A workflow "Move to Trash" action moves the document to the trash, and it can be restored until the trash is emptied.

## Audit log
`PAPERLESS_AUDIT_LOG_ENABLED` defaults to true (as of 2.7) and enables the audit trail for documents, document types, correspondents and tags. Changes to documents appear under the "History" tab; some changes, such as those made by workflows, record the actor as "System".

Entries for deleted documents are removed automatically, but entries created before that functionality was added are not. Prune them with:
```bash
prune_audit_logs
```

## Related
- To create a superuser, run `createsuperuser`. Alternatively set `PAPERLESS_ADMIN_USER` (with `PAPERLESS_ADMIN_PASSWORD`) to create one at start; this never changes an existing user's password or recreates an existing user.

## Checked
Date: 2026-11-07
Pages read in full: usage, configuration, administration (docs/*.md).
Corrections: removed "fully deleted files cannot be recovered except from this directory or your backups" (backups are not mentioned on those pages); replaced the unconfirmed "last-chance copy" timing with the documented "when the trash is emptied"; added the cron default; kept the superuser note only as documented in administration and configuration.
Method: documentation only; no commands were run.
