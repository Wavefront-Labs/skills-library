---
id: computing-software.systems-network-administration.jellyfin.database-locked-errors
name: database-locked-errors
category: computing-software
field: systems-network-administration
product: jellyfin
tags: [jellyfin, database-locked, locking-behavior, optimistic, pessimistic, lxc, parallel-scan]
level: advanced
status: docs-checked
description: "Resolve 'Database Locked' scan failures by lowering the parallel scan limit and changing LockingBehavior in database.xml."
sources: ["https://jellyfin.org/docs/general/administration/troubleshooting/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Fixing "Database Locked" errors

Symptoms are failed scans or inconsistent data, with "Database Locked" in the logs.

**Step 1: lower scan parallelism.** In the admin dashboard reduce the parallel scan task limit. If it is 0, set it to half your CPU cores.

**Step 2: change the locking mode.** `LockingBehavior` accepts three values:

- `NoLock`: the default, which works for most users.
- `Optimistic`: all writes are attempted and retried when they fail.
- `Pessimistic`: all reads are blocked while any write is in progress.

Stop the server, open the configuration directory and edit `database.xml`:

```xml
<?xml version="1.0" encoding="utf-8"?>
<DatabaseConfigurationOptions xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema">
  <DatabaseType>Jellyfin-SQLite</DatabaseType>
  <LockingBehavior>Optimistic</LockingBehavior>
</DatabaseConfigurationOptions>
```

Start Jellyfin again, keeping the scan task limit low.

Only if `Optimistic` does not help, try `Pessimistic`; it has a significant performance cost.

**LXC.** The team reports problems specifically with LXC. If errors persist on LXC after setting `Optimistic`, move to a full virtual machine or Docker; the project cannot support database-locked problems on LXC.

Other keys in the same file are covered by `computing-software.systems-network-administration.jellyfin.database-xml-tuning`.

## Checked

2026-11-03. Confirmed against the Jellyfin Troubleshooting page, Database Locked Errors section: parallel scan limit advice, the three LockingBehavior values and database.xml example, Pessimistic performance warning, LXC statement. Nothing removed.

Method: documentation only; no commands were run.
