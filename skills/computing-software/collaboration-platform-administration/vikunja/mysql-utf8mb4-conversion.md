---
id: computing-software.collaboration-platform-administration.vikunja.mysql-utf8mb4-conversion
name: mysql-utf8mb4-conversion
category: computing-software
field: collaboration-platform-administration
product: vikunja
tags: [vikunja, utf8mb4, latin1-database, information-schema, emoji-support]
level: advanced
status: docs-checked
description: "Check whether a Vikunja MySQL database is latin1 and convert it to utf8mb4 so non-Latin text and emojis work, using a generated ALTER script."
sources:
  - https://raw.githubusercontent.com/go-vikunja/website/main/src/content/docs/setup/utf-8.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Vikunja handles UTF-8 itself; the database may not. PostgreSQL and SQLite are fine. MySQL defaults are not, and problems appear only once you store non-Latin characters or emojis.

Check (database named `vikunja`):

```
SELECT default_character_set_name FROM information_schema.SCHEMATA WHERE schema_name = 'vikunja';
```

`latin1` means conversion is needed.

Procedure:
0. Back up the database first.
1. Write `preAlterTables.sql`: queries against `information_schema` that generate `ALTER DATABASE` (to `utf8mb4` / `utf8mb4_unicode_ci`), `ALTER TABLE ... CONVERT TO CHARACTER SET` per table, and `ALTER TABLE ... CHANGE` statements for varchar/char and text-type columns. Replace `vikunja` with your database name throughout.
2. Generate the script: `mysql -uroot < preAlterTables.sql | egrep '^ALTER' > alterTables.sql`
3. Apply it: `mysql -uroot < alterTables.sql`
4. Re-run the check; it should return `utf8mb4`.

## Checked

2026-11-04. Confirmed against the Vikunja UTF-8 Settings page (setup/utf-8): PostgreSQL and SQLite statement, the character set check query, latin1 meaning, backup step, the preAlterTables.sql contents, both mysql commands and the expected utf8mb4 result. Removed: the closing advice about server flags for new installs, which that page does not state.

Method: documentation only; no commands were run.
