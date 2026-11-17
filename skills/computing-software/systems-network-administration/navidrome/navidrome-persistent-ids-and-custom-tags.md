---
id: computing-software.systems-network-administration.navidrome.navidrome-persistent-ids-and-custom-tags
name: navidrome-persistent-ids-and-custom-tags
category: computing-software
field: systems-network-administration
product: navidrome
tags: [navidrome, pid, persistent-ids, custom-tags, tags-config, musicbrainz, discogs, tag-split, album-version]
level: advanced
status: docs-checked
description: "Configure Navidrome PID.Album, PID.Track and custom Tags: default MusicBrainz-first IDs, folder or Discogs IDs, legacy IDs, multi-value Split, disabling tags, full-scan rule."
sources: ["https://www.navidrome.org/docs/usage/configuration/persistent-ids/", "https://www.navidrome.org/docs/usage/configuration/custom-tags/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Navidrome persistent IDs and custom tags

PIDs give tracks and albums stable identities so moved or retagged files keep history. Defaults:

```toml
PID.Track = "musicbrainz_trackid|albumid,discnumber,tracknumber,title"
PID.Album = "musicbrainz_albumid|albumartistid,album,albumversion,releasedate"
```
The `|` means: use the first if present, else combine the second list. Alternatives:
- `PID.Album = "folder"` groups by folder.
- Discogs: `Tags.discogs_release_id.Aliases = ['discogs_release_id']`, `Tags.discogs_release_id.Album = true`, `PID.Album = 'discogs_release_id|albumartistid,album,albumversion,releasedate'`.
- Pre-0.55 behaviour: `PID.Album = "album_legacy"`, `PID.Track = "track_legacy"`.
Artist PIDs use only the name and are not configurable.

Changing PIDs triggers a full rescan that keeps playlists, stars, ratings, shares and play counts. Back up first. Retagging and moving files cannot happen in the same scan.

Custom tags (config file only, not env vars) under `Tags`:
- `Aliases` (required, case-insensitive), `Type` (`int`, `float`, `date`, `uuid`; default string), `MaxLength` (default 1024), `Album` (true includes it in album PID), `Split` (delimiters), `Ignore`.

```toml
Tags.MyCustomTag.Aliases = ["mycustomtag", "customtag"]
Tags.MyCustomTag.Split = ["; ", " / "]
Tags.Subtitle.Ignore = true
Tags.Genre.Split = []
Tags.Artist.Split = ['\', '; ']
```
Prefer multiple values written by your tag editor; splitting on `/` or `&` breaks names like AC/DC or Simon & Garfunkel. Any tag change needs `navidrome scan --full`. Tags not listed in `Tags` or the default set are ignored.

## Checked

2026-11-04. Confirmed against the Navidrome Persistent IDs and Custom Tags pages: default PIDs, `folder`, Discogs, legacy values, full-rescan rule, backup advice, retag/move rule, artist PIDs, custom tag properties and defaults, Split examples, Ignore, full scan after tag changes. Nothing removed.

Method: documentation only; no commands were run.
