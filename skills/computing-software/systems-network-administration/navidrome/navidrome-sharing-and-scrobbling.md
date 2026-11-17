---
id: computing-software.systems-network-administration.navidrome.navidrome-sharing-and-scrobbling
name: navidrome-sharing-and-scrobbling
category: computing-software
field: systems-network-administration
product: navidrome
tags: [navidrome, sharing, share-link, scrobble, lastfm, listenbrainz, scrobble-filter, defaultshareexpiration, shareurl]
level: practitioner
status: docs-checked
description: "Configure Navidrome share links (expiry, ShareURL, proxy path) and per-user scrobbling to Last.fm and ListenBrainz, including the 0.64 scrobble filter JSON rules."
sources: ["https://www.navidrome.org/docs/usage/features/sharing/", "https://www.navidrome.org/docs/usage/features/scrobbling/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Navidrome sharing and scrobbling

Sharing:
- Enabled by default; turn off with `EnableSharing=false`. It is one server-wide switch, so there is no per-user control.
- Any user can create shares and manages their own; admins manage all. Shared content is limited to the owner's libraries.
- Default expiry is one year (`DefaultShareExpiration = "8760h"`); accepts `24h`, `1h30m`. `DefaultDownloadableShare` sets the default download state.
- Links look like `http://yourserver.com/share/XXXXXXXXXX`. Behind a reverse proxy, allow `/share`. Set `ShareURL` when the server address is not public (for example over Tailscale).
- Subsonic share endpoints are implemented, and HTML meta tags give previews in chat apps.

Scrobbling:
- Last.fm: set `LastFM.ApiKey` and `LastFM.Secret` first, then each user toggles Scrobble to Last.fm in Personal Settings and approves access on Last.fm.
- ListenBrainz: toggle Scrobble to ListenBrainz, create or copy the token on the ListenBrainz site, paste it in Navidrome. Self-hosted compatible servers (for example Maloja) use `ListenBrainz.BaseURL`.
- Scrobble filter (0.64.0+): edit the user's Scrobble filter field with smart-playlist JSON rules. Matching songs are not sent to Last.fm, ListenBrainz or scrobbler plugins but still count locally. Examples: `{"all":[{"is":{"genre":"Christmas"}}]}`, `{"all":[{"lt":{"rating":4}}]}` (unrated count as 0), `{"all":[{"is":{"library_id":3}}]}`. `limit`, `limitPercent`, `offset`, `refreshDelay` and unknown fields are rejected. Users can set their own filter only if `EnableUserEditing` is on.
- Scrobble history is stored natively from 0.59.0; earlier plays are not backfilled, so totals may differ from play counts.

## Checked

2026-11-04. Confirmed against the Navidrome Sharing and Scrobbling pages: enable switch, ownership and library limits, default expiry, link format, `/share` proxy note, Subsonic endpoints, meta tags, Last.fm and ListenBrainz setup, scrobble filter rules (0.64.0), history (0.59.0). Nothing removed.

Method: documentation only; no commands were run.
