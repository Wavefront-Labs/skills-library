---
id: computing-software.systems-network-administration.jellyfin.migrating-from-other-servers
name: migrating-from-other-servers
category: computing-software
field: systems-network-administration
product: jellyfin
tags: [jellyfin, migration, emby, plex, watched-status, fresh-database]
level: intro
status: draft
description: "Know what can and cannot be migrated into Jellyfin from Emby, Plex or another Jellyfin: watched status via scripts, never the database."
sources: ["https://jellyfin.org/docs/general/administration/migrate/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Migrating to Jellyfin from Emby or Plex

Jellyfin's internal databases cannot be copied or adjusted easily, so migration is limited.

**Watched status and users**: third-party scripts use the API to copy watched status and users from Plex, Emby or another Jellyfin instance. The docs link an Emby/Jellyfin to Jellyfin script (Emby2Jelly) and a Plex to Jellyfin script (migrate-plex-to-jellyfin). They are community tools, not part of the server.

**Emby database**: direct database migration from Emby of any version is not supported. The docs report many subtle bugs from inconsistent schemas and strongly recommend a fresh database and library scan. A legacy procedure exists for Emby 3.5.2 or earlier only; Emby 3.5.3 and 3.6+ cannot be migrated, and the project cannot support or guarantee the old procedure. It involved moving `/var/lib/emby`, installing the `jellyfin` package, copying files over and marking the startup wizard complete in `/etc/jellyfin/system.xml` so an open wizard does not become a security risk.

**Practical plan**
1. Keep media paths stable where possible.
2. Install Jellyfin fresh and add libraries.
3. Run a watched-status script against the new server.
4. Retire the old server only after checking users and play states.
