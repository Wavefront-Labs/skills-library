---
id: computing-software.systems-network-administration.audiobookshelf.collections-vs-playlists
name: collections-vs-playlists
category: computing-software
field: systems-network-administration
product: audiobookshelf
tags: [collections, playlists, rss, library, organisation]
level: intro
status: docs-checked
description: "Pick between Audiobookshelf collections (public, books only, RSS-able) and playlists (private, books or podcast episodes)."
sources:
  - https://github.com/audiobookshelf/audiobookshelf-docs/blob/master/docs/documentation/libraries/common-content/3.playlists.md
  - https://github.com/audiobookshelf/audiobookshelf-docs/blob/master/docs/documentation/libraries/common-content/1.overview.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Both are library-specific, track listening progress per user, have a description field, can be reordered, cannot contain groups (other collections, series, playlists), and have a Play button that acts as Play All.

| Feature | Collection | Playlist |
| --- | --- | --- |
| Visibility | Public to anyone with library access | Private to its creator |
| RSS feed | Yes | No |
| Contents | Books only | Books or podcast episodes |

Create one from an individual book, either in the library view or the book's details (in newer versions the button is in the three-dot menu). The Playlists tab only shows once a playlist exists. For podcasts, add an episode to a playlist with the episode-row icon. To add to an existing one, repeat the steps and click the existing entry.

Edit: items show in the order added; drag the three-line handle to reorder; mark as read, edit details or remove from the same row. Edit the description with the pencil icon.

## Checked

Method: docs-checked 2026-11-09 against the Collections and Playlists page and the Library Overview page (library-specific scope) of the Audiobookshelf docs repo, both read in full from raw markdown.
