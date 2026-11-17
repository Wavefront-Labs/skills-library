---
id: computing-software.systems-network-administration.navidrome.navidrome-artwork-resolution
name: navidrome-artwork-resolution
category: computing-software
field: systems-network-administration
product: navidrome
tags: [navidrome, artwork, cover-art, coverartpriority, artistartpriority, discartpriority, folder-jpg, embedded-art, artwork-cli]
level: practitioner
status: docs-checked
description: "Control how Navidrome picks album, artist and disc artwork with CoverArtPriority, ArtistArtPriority and DiscArtPriority, and inspect why an item got its image."
sources: ["https://www.navidrome.org/docs/usage/library/artwork/", "https://www.navidrome.org/docs/usage/admin/cli/artwork/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Navidrome artwork resolution

Lists are comma-separated and evaluated in order; options are in the config file or `ND_` variables.

- Albums: `CoverArtPriority`, default `cover.*, folder.*, front.*, embedded, external` (external is currently Last.fm). Placeholder is the blue record.
- Artists: `ArtistArtPriority`, default `artist.*, album/artist.*, external`. Placeholder is a grey star. Add `image-folder` to the list and set `ArtistImageFolder` for a central artist-image folder.
- Discs: `DiscArtPriority`, default `disc*.*, cd*.*, cover.*, folder.*, front.*, discsubtitle, embedded`. `discsubtitle` matches image files named after the disc subtitle. Set `DiscArtPriority = ""` to make every disc use the album cover.
- Media files (tracks): embedded image, then disc art, then album cover. This can be slow; `EnableMediaFileCoverArt=false` returns the album cover for songs.
- Playlists: resolved separately (see the docs order).

Related settings: `EnableArtworkPrecache`, `ImageCacheSize`, `CoverArtQuality`, `EnableWebPEncoding`, `MaxImageSize`, `EnableArtworkUpload`, `MaxImageUploadSize`.

The `navidrome artwork` command explains problems without touching the DB. Kind codes: `ar` artist, `al` album, `pl` playlist, `ra` radio, `mf` media file, `dc` disc. Subcommands include `status`, `explain`, `refresh`, `reprocess` and `cancel`; `explain` supports all kinds, `refresh` all except disc, `reprocess` skips media files because track art comes from embedded tags read at scan time or first view, and disc art has no stored state (resolved per request and cached by content).

Verify: `navidrome artwork explain` on an affected album shows which source in the priority chain won.

## Checked

2026-11-04. Confirmed against the Navidrome Artwork location resolution page and the `navidrome artwork` CLI page: default priority lists, placeholders, disc and media file order, playlist note, kind codes, subcommands and which kinds each accepts. Nothing removed.

Method: documentation only; no commands were run.
