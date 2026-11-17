---
id: computing-software.systems-network-administration.pi-hole.backup-and-split-query-database
name: backup-and-split-query-database
category: computing-software
field: systems-network-administration
product: pi-hole
tags: [sqlite-online-backup, rotate-ftl-db, pihole-ftl-db-backup]
level: advanced
status: docs-checked
description: "Back up pihole-FTL.db while running with the SQLite online backup, or rotate it into monthly files with a cron job."
sources: ["https://docs.pi-hole.net/database/query-database/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Backup and rotate the query database

**Backup while FTL runs.** Use the SQLite3 online backup method:

```bash
sqlite3 /etc/pihole/pihole-FTL.db ".backup /media/backup/pihole-FTL.db.backup"
```

This creates a consistent copy of the long-term database.

**Split (rotate) the database.** You can split the long-term database by rotating the file periodically. Do this only while `pihole-FTL` is not running. Individual databases can be merged later. A monthly cron job could run:

```bash
sudo service pihole-FTL stop
sudo mv /etc/pihole/pihole-FTL.db /media/backup/pihole-FTL_$(date +"%m-%y").db
sudo service pihole-FTL start
```

DNS resolution is unavailable while `pihole-FTL` is stopped.

**Limit growth instead.** `database.maxDBdays` sets how old queries may be before periodic removal; `database.DBinterval` (default once per minute) controls how often queries are written, protecting against data loss on power failure. `database.DBimport` can be disabled if importing from a very large database delays FTL on startup.

**Checklist**

1. Pick backup or rotation.
2. Schedule it with cron.
3. Confirm FTL restarts and history repopulates.
4. Keep a copy on separate storage.

## Checked

2026-11-04. Confirmed against the official Pi-hole documentation: Query Database (database/query-database). Nothing needed removing. The page example writes the backup to a home directory; the backup path here is only an example. Note the two official pages disagree on the default for `database.maxDBdays` (365 on the query database page, 91 on the configuration reference), so this skill states no default.
Method: documentation only; no commands were run.
