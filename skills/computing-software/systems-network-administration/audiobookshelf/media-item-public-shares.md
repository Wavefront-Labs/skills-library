---
id: computing-software.systems-network-administration.audiobookshelf.media-item-public-shares
name: media-item-public-shares
category: computing-software
field: systems-network-administration
product: audiobookshelf
tags: [public-share, sharing, timestamp, slug, no-auth, books]
level: practitioner
status: docs-checked
description: "Create an Audiobookshelf public share for a book with a time limit, a start timestamp, and understand its exposure and playback limits."
sources:
  - https://github.com/audiobookshelf/audiobookshelf-docs/blob/master/docs/documentation/libraries/common-content/4.public-shares.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Only books can be shared, and only admins can create shares. Use **Share** from the dropdown on a cover or on the details page, then set how long the share stays available.

URL: built from how you access the server when creating it, for example `http://192.168.0.5/share/[slug]`. You can replace the host manually: `https://mycooldomain.com/share/[slug]`. Append `?t=1234` to start at 1234 seconds.

Exposure: anyone with the link and network access to the server can open it without logging in, including anyone on the internet if the server is internet reachable.

Playback limits: progress is tracked only by the client, so the listener cannot resume on another device. No transcoding is provided, so the client must play the file's format and codec directly.

Admins can filter the library for items with an open share using the same dropdown as Genres and Tags.

## Checked

2026-11-04. Confirmed against the Audiobookshelf docs: Public Shares page (Media Item Shares).

Method: documentation only; no commands were run.
