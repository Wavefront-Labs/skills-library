---
id: computing-software.systems-network-administration.jellyfin.nfo-writing-and-images
name: nfo-writing-and-images
category: computing-software
field: systems-network-administration
product: jellyfin
tags: [jellyfin, nfo, nfo-saver, metadata-export, artwork, save-image-paths]
level: advanced
status: docs-checked
description: "Make Jellyfin write .nfo files with the Nfo saver and understand exported tags and how nfo image paths take priority."
sources: ["https://jellyfin.org/docs/general/server/metadata/nfo/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Writing .nfo files and nfo images

To export metadata, select the **Nfo saver** in the library's settings. Jellyfin then writes `.nfo` files using these tags (selection from the docs):

- General: `title`, `originaltitle`, `sorttitle`, `year`, `premiered`, `releasedate`, `enddate`, `rating`, `criticrating`, `mpaa`, `runtime`, `aspectratio`, `language`, `countrycode`.
- New tag per item: `director`, `writer`, `credits`, `country`, `genre`, `studio`.
- `dateadded` in UTC; `set` is the collection name (movies only) and `collectionnumber` the TMDb collection id.
- Ids: `id` (IMDb for movies, TVDb for shows), `imdbid` (all other media), `imdb_id` (TV shows only), `tvdbid`, `tmdbid`, `tvrageid`, `zap2itid`, and MusicBrainz and AudioDB ids for music. Other providers export as `<providernameid>`.
- Episodes: `showtitle`, `season`, `episode`, `aired`, `airsafter_season`, `airsbefore_season`, `airsbefore_episode`, `displayseason`, `displayepisode`. Seasons use `seasonnumber`.
- Music artists: `formed`, `disbanded`.
- `trailer` as a YouTube URL in the Kodi plugin format.
- `art` only when "save image paths" is enabled in NFO settings.

**Images in NFO files.** Jellyfin supports one image per artwork type, so only the first `thumb` tag for each type is used. Artwork defined by local path or URL in an NFO has priority over remote image providers and images in media folders.

Check by saving metadata for one item and opening the resulting file.

## Checked

2026-11-08. Confirmed against the Jellyfin Local .nfo metadata page: Nfo saver setting, writable tag list and notes, collection and id tags, episode tags, music tags, trailer format, art with save image paths, one image per type and priority of nfo artwork. Removed: the claim that lockdata is read only, which the page does not state. Page read in full.

Method: documentation only; no commands were run.
