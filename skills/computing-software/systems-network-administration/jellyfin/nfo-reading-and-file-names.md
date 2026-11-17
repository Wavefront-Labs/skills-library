---
id: computing-software.systems-network-administration.jellyfin.nfo-reading-and-file-names
name: nfo-reading-and-file-names
category: computing-software
field: systems-network-administration
product: jellyfin
tags: [jellyfin, nfo, local-metadata, kodi, tvshow-nfo, uniqueid, metadata-priority]
level: practitioner
status: docs-checked
description: "Name .nfo files so Jellyfin finds them, and understand which tags it reads, tag precedence and user data import."
sources: ["https://jellyfin.org/docs/general/server/metadata/nfo/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Reading local .nfo metadata

Jellyfin can read and write local `.nfo` files to exchange metadata with other tools.

**File names**

| Media | File name |
| --- | --- |
| Movies | `movie.nfo`, `VIDEO_TS.nfo`, or for DVDs `<filename of the movie>.nfo` |
| TV show | `tvshow.nfo` |
| Season | `season.nfo` |
| Episode | `<filename of the episode>.nfo` |
| Music artist | `artist.nfo` |
| Music album | `album.nfo` |
| Music video | as movies |

**Behaviour to know**
- Tags read include `title`/`name`, `originaltitle`, `sortname`, `plot` (also `biography`, `review`), `tagline`, `mpaa`, `runtime`, `year`, `premiered`, `releasedate`, `genre`, `tag`, `studio`, `director`, `writer`, `actor`, `uniqueid`, `thumb`, `fanart` and `lockdata`. The docs say the list may not be exhaustive.
- When several tags map to the same internal field, such as `plot` and `review`, the last one in the file wins.
- NFO metadata cannot currently be disabled: local metadata is always fetched and has priority over remote providers such as TMDb.
- `watched`, `playcount` and `lastplayed` import user data for a single user only, chosen in the NFO settings.
- Provider id tags follow `<PROVIDER_NAME>id`. You can also give an IMDb, TMDb or TVDb link to identify media.

Kodi's NFO file documentation applies to the format. Rescan after adding or editing files.

## Checked

2026-11-08. Confirmed against the Jellyfin Local .nfo metadata page: file name table, tag list, last-tag-wins rule, NFO cannot be disabled and has priority over TMDb, single-user import, provider id tags and links, Kodi wiki pointer. Page read in full.

Method: documentation only; no commands were run.
