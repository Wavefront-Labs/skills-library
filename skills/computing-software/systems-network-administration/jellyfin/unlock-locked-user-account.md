---
id: computing-software.systems-network-administration.jellyfin.unlock-locked-user-account
name: unlock-locked-user-account
category: computing-software
field: systems-network-administration
product: jellyfin
tags: [jellyfin, locked-account, sqlite, jellyfin-db, invalid-login-attempt, admin-recovery]
level: advanced
status: docs-checked
description: "Unlock a locked-out Jellyfin user by resetting InvalidLoginAttemptCount and a permission row in jellyfin.db with sqlite3."
sources: ["https://jellyfin.org/docs/general/administration/troubleshooting/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Unlocking a locked user account

Use this when the admin account is locked and Forgot Password does not work. You edit the database directly, so copy `jellyfin.db` first; manual changes can destroy an instance beyond repair.

1. Find `jellyfin.db`. On Linux the default is `/var/lib/jellyfin/data/`; other platforms are in `computing-software.systems-network-administration.jellyfin.server-path-precedence`.
2. Make sure `sqlite3` is installed (`apt install sqlite3` on Debian-based systems).
3. Open the database and run the two statements from the docs:

```bash
sqlite3 /PATH/TO/JELLYFIN/DB/jellyfin.db
```

```sql
UPDATE Users SET InvalidLoginAttemptCount = 0 WHERE Username = 'LockedUserName';
UPDATE Permissions SET Value = 0 WHERE Kind = 2 AND UserId IN (SELECT Id FROM Users WHERE Username = 'LockedUserName');
.exit
```

The first clears the failed-login counter; the second sets the value of permission kind 2 to 0 for that user.

On a desktop, SQLiteBrowser can run the same two UPDATE statements from its Execute SQL tab (omit `.exit`).

Replace `LockedUserName` with the real username. If the account still cannot do admin tasks, see `computing-software.systems-network-administration.jellyfin.repair-admin-permissions`.

## Checked

2026-11-03. Confirmed against the Jellyfin Troubleshooting page, Unlock locked user account section: default Linux location, sqlite3 install, both UPDATE statements, SQLiteBrowser alternative, and the backup caution in the permissions section. Removed: stop-the-server and restart steps that the page does not give.

Method: documentation only; no commands were run.
