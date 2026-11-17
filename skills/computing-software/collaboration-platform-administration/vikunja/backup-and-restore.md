---
id: computing-software.collaboration-platform-administration.vikunja.backup-and-restore
name: backup-and-restore
category: computing-software
field: collaboration-platform-administration
product: vikunja
tags: [vikunja, mysqldump, pg-dump, sqlite-file-copy, attachments-backup]
level: practitioner
status: docs-checked
description: "Back up and restore a Vikunja instance: database dumps for MySQL and PostgreSQL, SQLite file copy and the attachments folder, plus the warning about permanent deletes."
sources:
  - https://raw.githubusercontent.com/go-vikunja/website/main/src/content/docs/setup/backups.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Back up two things: the database and the attachments folder (`files.basepath`). Copying the folder is enough for files.

Project deletion is permanent and irreversible: no trash, recycle bin or undo, so keep backups with suitable retention.

MySQL:

```
mysqldump -u <user> -p -h <db-host> <database> > vikunja-backup.sql
mysql -u <user> -p -h <db-host> <database> < vikunja-backup.sql
```

PostgreSQL:

```
pg_dump -U <user> -h <db-host> <database> > vikunja-backup.sql
psql -U <user> -h <db-host> <database> < vikunja-backup.sql
```

SQLite: copy the database file (`database.path`) elsewhere.

## Checked

2026-11-04. Confirmed against the Vikunja What to backup page (setup/backups): the two parts to back up, the permanent-deletion warning, mysqldump and mysql, pg_dump and psql, and SQLite file copy. Removed: the upgrade-migration advice and the container paths, which that page does not state.

Method: documentation only; no commands were run.
