---
id: computing-software.systems-network-administration.navidrome.navidrome-missing-files-and-remap
name: navidrome-missing-files-and-remap
category: computing-software
field: systems-network-administration
product: navidrome
tags: [navidrome, missing-files, ghost-tracks, missing-fix, purgemissing, play-count, remap, removable-drive]
level: advanced
status: docs-checked
description: "Handle missing (greyed-out) tracks in Navidrome: why they appear, preventing them, remapping history with navidrome missing fix, purge policy, and deleting them in the admin UI."
sources: ["https://www.navidrome.org/docs/usage/library/missing-files/", "https://www.navidrome.org/docs/usage/admin/cli/missing/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Navidrome missing files

Navidrome keeps files it no longer finds in the database, marked missing, so ratings, play counts and playlist entries are not lost. Only admins see them (greyed out), and the `?` icon shows path and time. Causes: a move or rename combined with a tag change in one step, or a network or removable drive that is not mounted (files return when it does).

Prevention: move or rename first, run a quick scan, then retag. Matching order on scan is exact tags, then the persistent ID, then the original path ignoring the extension (`01-track.mp3` to `01-track.flac`).

Manual remap:

```bash
navidrome backup create
navidrome missing list [-f csv|json]     # id, library id, title, album, artist, path
navidrome missing fix "Rock/Old Album/track01.mp3" "Rock/New Album/track01.mp3"
```
`fix` moves play count, rating, starred status and bookmarks from the missing file onto the target. Each argument may be a media file ID, a library-relative path or `libraryID:path` (use the latter when the path exists in multiple libraries, e.g. `2:"Podcasts/ep01.mp3"`). The target must already be scanned and not missing; the action cannot be undone.

Purge policy: `Scanner.PurgeMissing` is `never` (default), `always` (after every scan) or `full` (after full scans only). Purging permanently deletes ratings, play counts and playlist entries of those files.

Permanent removal: as admin open Settings, Missing Files, select entries and Remove; the list can be exported to CSV.

## Checked

2026-11-04. Confirmed against the Navidrome Missing Files page and the `navidrome missing` CLI page: why files go missing, admin-only visibility, prevention order, remap command and argument forms, `Scanner.PurgeMissing` values, the Missing Files admin screen. The matching order is on the Persistent IDs page. Nothing removed.

Method: documentation only; no commands were run.
