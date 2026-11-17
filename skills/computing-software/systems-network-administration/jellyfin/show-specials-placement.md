---
id: computing-software.systems-network-administration.jellyfin.show-specials-placement
name: show-specials-placement
category: computing-software
field: systems-network-administration
product: jellyfin
tags: [jellyfin, shows, specials, season-00, airsbefore-season, airsafter-season, nfo]
level: practitioner
status: docs-checked
description: "Add specials in Season 00 and make them play inside a season using the display setting and Airs before/after metadata."
sources: ["https://jellyfin.org/docs/general/server/media/shows/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Show specials

Put specials in the `Season 00` folder. If your metadata provider knows them they are matched. If it does not, name the file for what it contains instead of `Series Name S00Exy.mkv`, so wrong metadata is not pulled. Special numbering varies between providers.

**Show a special inside a season** (useful when it belongs to the storyline) with two requirements:

1. Enable `Display specials within their series they aired in` under `Dashboard -> Library -> Display`.
2. Set the season and episode it aired before or after in the metadata, either in the metadata editor or an NFO using `airsbefore_season`, `airsafter_season` and `airsbefore_episode`.

Behaviour:
- `Airs before season` alone puts the special at the start of that season, before the first episode.
- Add `Airs before episode` for a mid-season position: season 2 and episode 7 plays it between S02E06 and S02E07.
- `Airs after series` places it at the end of the specified season and takes priority over the before fields.
- Specials with the same position play in the order stored in the specials season; with S00E01 and S00E03 both before S03E07, the order is S03E06, S00E01, S00E03, S03E07.

The special then shows in both the `Specials` season and the chosen season.

Check by playing the preceding episode with autoplay and confirming the special follows.

## Checked

2026-11-08. Confirmed against the Jellyfin TV Shows page: Season 00 placement, name advice, display setting path, airsbefore_season, airsafter_season and airsbefore_episode tags, positioning rules and the S03E06 ordering example. Partial read: through the Theme media example, which covers the Show Specials section in full.

Method: documentation only; no commands were run.
