---
id: computing-software.systems-network-administration.audiobookshelf.migrate-fix-library-folder-paths
name: migrate-fix-library-folder-paths
category: computing-software
field: systems-network-administration
product: audiobookshelf
tags: [migration, sqlite, libraryfolders, sql, paths]
level: sme
status: docs-checked
description: "Fix stale library folder paths after a migration by editing the libraryFolders table in an unpacked Audiobookshelf backup."
sources:
  - https://github.com/audiobookshelf/audiobookshelf-docs/blob/master/docs/documentation/server-management/migration-os.md
  - https://github.com/audiobookshelf/audiobookshelf-docs/blob/master/docs/documentation/server-management/backups.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
If library folder paths are still wrong after running the migration tooling, edit the database manually. The docs' sequence:

1. Create a backup first.
2. Before restoring it on the new server, unpack the backup file.
3. Open the `database.sqlite` file inside with an SQLite editor (several web-based editors exist).
4. List current paths:

```sql
SELECT * FROM libraryFolders;
```

These will likely still show the old, incorrect paths.

5. Update a path, replacing `path` and `id` with your values:

```sql
UPDATE libraryFolders
SET
  path = '/new/path/to/library'
WHERE
  id = '56798b97-b544-4e85-96e7-27497f519a5c';
```

6. Restore the edited backup on the new server.

Note the page names the file `database.sqlite`, while the standard restore procedure on the backups page names the database `audiobookshelf.sqlite`; check which name appears in your unpacked backup. If stuck, read the Windows to Docker migration discussion thread before posting.

## Checked

Method: docs-checked 2026-11-09 against the Migrating an OS or File Paths page and the Backups page (file name comparison) of the Audiobookshelf docs repo, both read in full from raw markdown.
