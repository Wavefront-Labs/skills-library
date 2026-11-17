---
id: computing-software.systems-network-administration.jellyfin.repair-admin-permissions
name: repair-admin-permissions
category: computing-software
field: systems-network-administration
product: jellyfin
tags: [jellyfin, permissions, sqlite, admin-user, permissionkind, jellyfin-db]
level: sme
status: docs-checked
description: "Inspect and restore a broken admin account's permission rows in jellyfin.db using the SQL given in the Jellyfin troubleshooting guide."
sources: ["https://jellyfin.org/docs/general/administration/troubleshooting/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Repairing admin user permissions

If your admin account's permissions break, restore them with SQL. Manual database changes can destroy the instance, so copy the file first:

```sh
cp /PATH/TO/JELLYFIN/DB/jellyfin.db /PATH/TO/JELLYFIN/DB/jellyfin.db.bck
```

Open it with `sqlite3 /PATH/TO/JELLYFIN/DB/jellyfin.db`.

**Overview of all users**

```sql
SELECT Permissions.Value,Permissions.Kind,Users.Username FROM Permissions INNER JOIN Users ON Permissions.UserID = Users.Id;
```

**One account** (change `AdminUsername`):

```sql
SELECT Value,Kind FROM Permissions WHERE UserId IN (SELECT Id FROM Users WHERE Username = 'AdminUsername');
```

`Value` is 1 or 0 for assigned or not; `Kind` is the permission type. The meaning of each Kind is the `PermissionKind` enumeration in the Jellyfin source code, so look it up there before editing.

**Repair.** The docs set kinds 0 and 3 to 21 to 1 (kinds 1 and 2 are left out; kind 2 is the one the locked-account procedure resets):

```sql
UPDATE Permissions SET Value = 1 WHERE (Kind = 0 OR Kind = 3 OR Kind = 4 OR Kind = 5 OR Kind = 6 OR Kind = 7 OR Kind = 8 OR Kind = 9 OR Kind = 10 OR Kind = 11 OR Kind = 12 OR Kind = 13 OR Kind = 14 OR Kind = 15 OR Kind = 16 OR Kind = 17 OR Kind = 18 OR Kind = 19 OR Kind = 20 OR Kind = 21) AND UserId IN (SELECT Id FROM Users WHERE Username = 'AdminUsername');
.exit
```

Not every permission is needed; remove the unnecessary ones afterwards in the web UI.

## Checked

2026-11-03. Confirmed against the Jellyfin Troubleshooting page, Fix Admin User Permissions section: backup caution and cp command, both SELECT queries, the Kind list in the UPDATE, PermissionKind pointer. Removed: stop-the-server step the page does not give.

Method: documentation only; no commands were run.
