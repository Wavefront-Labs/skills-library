---
id: computing-software.collaboration-platform-administration.mattermost.move-server-migration
name: move-server-migration
category: computing-software
field: collaboration-platform-administration
product: mattermost
tags: [server-migration, new-server, database-restore, config-json]
level: advanced
status: docs-checked
description: "Move Mattermost to a new server by restoring the database, config.json and local data, with version and database matching rules."
sources: ["https://docs.mattermost.com/administration-guide/onboard/migrating-to-mattermost.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Move Mattermost to a new server

SOURCE is the server you move from; DESTINATION is the new one. Steps from the migration guide:
1. Back up the SOURCE server (database, config.json, files).
2. Upgrade SOURCE to the latest major build.
3. Install the latest major build on DESTINATION, configured and tested. The database type (MySQL or PostgreSQL) and version must match SOURCE. Stop DESTINATION and back up its database and config.json.
4. Restore a backup of the SOURCE database in place of the database DESTINATION uses.
5. Copy config.json from SOURCE to DESTINATION.
6. If FileSettings.DriverName is local, copy the ./data directory (or whichever directory you use) from SOURCE to DESTINATION.
7. Start DESTINATION, open the System Console, make a minor change and save it so config.json is upgraded to the latest schema with defaults for new settings.
8. Test by opening the URL of an existing team; refresh the browser to pick up the upgrade.

After verification you can optionally upgrade Team Edition to Enterprise Edition using the upgrade guide.

Bitnami note: Bitnami installs on MySQL and lowercases table names (users instead of Users). Adjust by starting MySQL with the --lower-case-table-names=1 switch; the start script location depends on how MySQL was installed.

Moves from other chat platforms (Slack, Rocket.Chat, Jabber, Pidgin) are separate procedures covered by their own sections of the migration guide.

## Checked

2026-11-03. Confirmed against the Mattermost documentation page https://docs.mattermost.com/administration-guide/onboard/migrating-to-mattermost (new server steps, Bitnami note). Removed unsupported downtime and change-freeze advice.

Method: documentation only; no commands were run.
