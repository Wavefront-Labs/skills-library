---
id: computing-software.systems-network-administration.audiobookshelf.podcast-add-and-find-episodes
name: podcast-add-and-find-episodes
category: computing-software
field: systems-network-administration
product: audiobookshelf
tags: [podcasts, rss, opml, add-podcast, find-episodes]
level: practitioner
status: docs-checked
description: "Add a podcast to Audiobookshelf by name search, RSS link, OPML upload or filesystem, and download chosen episodes."
sources:
  - https://github.com/audiobookshelf/audiobookshelf-docs/blob/master/docs/documentation/libraries/podcast-library/1.podcast-directory-structure.md
  - https://github.com/audiobookshelf/audiobookshelf-docs/blob/master/docs/documentation/install/11.env-configuration.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Two ways to add: through the UI, or by placing episode files into the correct folder structure on disk (useful if you fetch episodes with another tool for more control).

UI: use the **Add** tab in the web interface or the app. Search by name (uses the region set in podcast settings), enter an RSS link (the feed is read directly without search), or upload an OPML file. Search terms are not stored. Fill in the podcast details and add it.

Local-IP feeds are blocked by the SSRF filter; set `DISABLE_SSRF_REQUEST_FILTER=1` if you self-host the feed.

Download specific episodes: click **Find Episodes** to list every episode in the RSS feed, downloaded or not, pick the ones to fetch. Episodes already downloaded and matched have a green check.

Only episodes downloaded to the server are visible and playable; Audiobookshelf is not a pass-through service. Downloads go to the download queue, reachable from the navigation bar.

## Checked

Method: docs-checked 2026-11-09 against the Podcast Library Structure page and the Environment Configuration page of the Audiobookshelf docs repo, both read in full from raw markdown.
