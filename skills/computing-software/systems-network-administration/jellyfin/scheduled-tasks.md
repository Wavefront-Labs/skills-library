---
id: computing-software.systems-network-administration.jellyfin.scheduled-tasks
name: scheduled-tasks
category: computing-software
field: systems-network-administration
product: jellyfin
tags: [jellyfin, scheduled-tasks, maintenance, library-scan, cleanup-collections, optimize-database]
level: practitioner
status: docs-checked
description: "List Jellyfin's default scheduled tasks and the data-loss risk of the playlist and collection clean-up task."
sources: ["https://jellyfin.org/docs/general/server/tasks/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Scheduled tasks

Tasks are operations scheduled to run periodically, found in the Dashboard. Any task can also be run manually with the run button on its right.

**Default tasks**

| Group | Tasks |
| --- | --- |
| Libraries | Download Missing Subtitles, Refresh Users, Extract Chapter Images, Scan Library, Extract Key Frames |
| Application | Update Plugins |
| Maintenance | Optimize Database, Clear Log Folder, Clear Cache Folder, Clear Activity Logs, Clear Transcodes Folder, Clean up collections and playlists |

Plugins can add their own tasks, which also appear in the task settings for you to configure. The `Media segment scan` task is one used by segment providers.

**Warning.** If media files are unavailable when `Clean up collections and playlists` runs, for example a network share not yet mounted, your playlists will be lost. By default it runs at Jellyfin startup.

See `computing-software.systems-network-administration.jellyfin.network-storage-and-nfs` for the related caution about unavailable media storage.

## Checked

2026-11-03. Confirmed against the Jellyfin Tasks page (task list, run button, plugin tasks, playlist-loss note and startup default) and the Media segments page (Media segment scan task). Removed: unsupported scheduling advice, a scan-removal claim and the invented check.

Method: documentation only; no commands were run.
