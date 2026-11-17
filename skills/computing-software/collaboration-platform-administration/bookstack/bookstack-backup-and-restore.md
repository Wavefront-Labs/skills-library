---
id: computing-software.collaboration-platform-administration.bookstack.bookstack-backup-and-restore
name: bookstack-backup-and-restore
category: computing-software
field: collaboration-platform-administration
product: bookstack
tags: [bookstack, backup, restore, mysqldump, env, app-key, uploads, update-url]
level: practitioner
status: docs-checked
description: "Back up and restore BookStack by hand: database dump, .env, public and storage uploads, themes, restore ordering, preserving APP_KEY and handling a changed URL."
sources: ["https://www.bookstackapp.com/docs/admin/backup-restore/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# BookStack backup and restore

BookStack has no built-in backup. Back up:

- the database,
- `.env`,
- `public/uploads` (images),
- `storage/uploads` (page attachments),
- `themes` (custom themes).

```
mysqldump -u {mysql_user} -p {database_name} > bookstack.backup.sql
tar -czvf bookstack-files-backup.tar.gz .env public/uploads storage/uploads themes
```

Store backups on a different device. Page export and import are not a backup mechanism.

Restore:

1. Install a fresh instance following the install guide but skip `php artisan migrate` (for Docker, restore the database before starting the container).
2. `mysql -u {mysql_user} -p {database_name} < bookstack.backup.sql`
3. If the new BookStack version differs, run `php artisan migrate`.
4. Extract the file archive in the BookStack folder with `tar -xvzf`, then reset permissions so the server can write.
5. Merge `.env`: keep the old `APP_KEY` (changing it breaks features such as MFA); database settings may come from the new instance's file.
6. If the URL changed, set `APP_URL` exactly to the new base URL, run `php artisan bookstack:update-url <oldUrl> <newUrl>` to rewrite stored URLs, and adjust web server config.

## Checked

2026-11-03. Confirmed against the BookStack docs page(s) admin/backup-restore/ and user/export-import/ (under https://www.bookstackapp.com/docs/), including the prose, not only identifiers.
Removed or reworded: nothing.
Method: documentation only; no commands were run.
