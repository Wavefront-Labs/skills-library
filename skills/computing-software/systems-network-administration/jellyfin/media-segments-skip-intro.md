---
id: computing-software.systems-network-administration.jellyfin.media-segments-skip-intro
name: media-segments-skip-intro
category: computing-software
field: systems-network-administration
product: jellyfin
tags: [jellyfin, media-segments, intro, outro, recap, commercial, skip-button, plugins]
level: practitioner
status: docs-checked
description: "Use Jellyfin media segments for skip-intro style actions via providers, the Media segment scan task and client playback settings."
sources: ["https://jellyfin.org/docs/general/server/metadata/media-segments/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Media segments

Media segments (introduced in 10.10) are typed time ranges stored with a media file. Unlike chapters, which have no type, segments carry a type so clients can act on them. A 16 minute video might have an `Intro` from 00:00:00 to 00:03:08, a `Commercial` from 00:08:03 to 00:08:59 and an `Outro` from 00:14:30 to 00:16:00.

Jellyfin stores the segments and provides them to clients; the client decides what to do, for example show a skip button.

**Types:** Commercial, Preview, Recap, Outro, Intro.

**Getting started**
1. Install one or more media segment provider plugins. Segments come from plugins, each giving a begin timestamp, an end timestamp and a type. The official `Chapter Segments Provider` plugin creates segments from chapters and chapter names.
2. Run the `Media segment scan` task in the dashboard to create segments immediately; it also runs automatically in the background.
3. Set actions for each segment type in the client. The location differs by client but is generally in playback settings.

This design means more platforms can be supported without custom per-client changes, since the segment data is generic.

## Checked

2026-11-03. Confirmed against the Jellyfin Media segments page: 10.10 introduction, example timestamps, five types, provider plugins, Chapter Segments Provider, Media segment scan task, client actions. Removed: invented check step.

Method: documentation only; no commands were run.
