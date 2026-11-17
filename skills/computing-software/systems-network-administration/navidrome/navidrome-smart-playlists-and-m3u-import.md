---
id: computing-software.systems-network-administration.navidrome.navidrome-smart-playlists-and-m3u-import
name: navidrome-smart-playlists-and-m3u-import
category: computing-software
field: systems-network-administration
product: navidrome
tags: [navidrome, smart-playlists, nsp, m3u, playlist-import, pls-export, autoimportplaylists, playlistspath]
level: advanced
status: docs-checked
description: "Write Navidrome smart playlists as .nsp JSON rules, understand where they come from, and list, export or import playlists with navidrome pls and M3U auto-import."
sources: ["https://www.navidrome.org/docs/usage/features/smart-playlists/", "https://www.navidrome.org/docs/usage/admin/cli/pls/", "https://www.navidrome.org/docs/faq/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Navidrome smart playlists and playlist CLI

Smart playlists (beta) are JSON rules; tracks matching are selected and updated as the library and history change. They come from `.nsp` files imported by the scan (the file is the source of truth) or from a client such as Feishin through the API (stored in the database, no `.nsp`). Refresh frequency: `SmartPlaylistRefreshDelay`.

```json
{
  "name": "80s top songs",
  "all": [
    { "any": [{ "is": { "loved": true } }, { "gt": { "rating": 3 } }] },
    { "inTheRange": { "year": [1981, 1990] } }
  ],
  "sort": "-year,title",
  "limit": 25
}
```
Other forms from the docs: `{ "inTheLast": { "lastPlayed": 30 } }`, `"sort": "random"`, multi-field sort `"-year,-rating,title"` (leading `-` is descending), `{ "is": { "library_id": 2 } }`, and `limitPercent` (1-100) instead of `limit`. The docs advise against an uncapped random list on large libraries.

M3U: scans import `.m3u` files automatically (`AutoImportPlaylists`, restrict with `PlaylistsPath`, `DefaultPlaylistPublicVisibility`). A playlist imported from M3U is read-only while its per-playlist Auto-import toggle is on (each scan replaces its tracks with the file's); edit the .m3u file, or turn the toggle off to edit in Navidrome (re-enabling later overwrites your edits).

CLI:
- `navidrome pls list [-u user] [-f csv|json]`
- `navidrome pls --playlist "Road Trip Mix" --output ./road-trip.m3u8` (file) or `pls export -o ./playlists` (folder, which must already exist; duplicate names get the first 6 characters of the ID appended). With `--playlist` and no output it prints to stdout; without `--playlist` `--output` is required, optionally with `--user`.
- `pls import [-u user] [--sync] <file>...` loads M3U files as playlists; the first admin owns them unless `--user` is given. `--sync` makes a playlist follow its file, so its tracks cannot be edited in Navidrome.

## Checked

2026-11-04. Confirmed against the Navidrome Smart Playlists page, the `pls` CLI page and the FAQ (M3U playlists): rule sources, example operators and sorting, `limitPercent`, refresh delay, M3U auto-import toggle behaviour, `pls` flags and export rules. Added the `pls import` flags from the CLI page; changed the random-list advice to the docs wording.

Method: documentation only; no commands were run.
