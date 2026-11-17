---
id: media-communication.broadcasting.podcast-production.episode-edit-loudness-and-rss-publishing
name: episode-edit-loudness-and-rss-publishing
category: media-communication
field: broadcasting
product: podcast-production
tags: [podcast-production, podcast, podcasting, audio-editing, episode-editing, remote-recording, double-ender, riverside, zencastr, audacity, reaper, adobe-audition, descript, loudness, lufs, true-peak, ffmpeg, loudnorm, mp3, id3, rss, rss-feed, podcast-hosting, enclosure, guid, apple-podcasts, spotify, show-notes, chapters, broadcasting]
level: practitioner
status: docs-checked
description: "Take a podcast episode from recording to feed: record separate tracks, edit for pace, and publish via RSS without breaking subscribers (enclosure, GUID, feed moves)."
sources:
  - https://www.rssboard.org/rss-specification
  - https://podcasters.apple.com/support/837-change-the-rss-feed-url
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Episode edit, loudness and RSS publishing

**Goal:** a consistent-sounding episode that arrives in every podcast app, on time, with
correct metadata - and a feed you never accidentally break.

## 1. Record so the edit is easy
- **Separate tracks per speaker.** Remote: use a double-ender tool or have each guest
  record locally, so each voice is captured at source, not through call compression.
- Mics close, quiet soft room, headphones on everyone to prevent bleed.
- Record room tone and a clap/sync point at the start.

## 2. Edit for listeners, not completeness
- **Structure pass first:** cut whole sections that drag; move the strongest material earlier.
- **Line pass:** remove false starts, crosstalk, long ums (not all - over-cleaning sounds
  robotic). Cut on breaths or consonants; use short crossfades to avoid clicks.
- Fill gaps with room tone, never digital silence.
- Text-based editors speed this up; still listen through - transcripts hide clicks and bad joins.

## 3. Loudness
Pick the loudness target from your host or platform's current delivery spec and measure the
final file with a loudness meter rather than trusting a setting. Do not copy a number from
memory; this skill does not state one.

## 4. Publishing via RSS
Your host generates the RSS feed; podcast apps poll it.
- Each `<item>` carries an **enclosure** with three required attributes: `url` (where the
  file is), `length` (size in bytes) and `type` (a standard MIME type) (RSS 2.0 spec).
- The **`guid`** is a string that uniquely identifies the item; aggregators may use it to
  decide whether an item is new (RSS 2.0 spec). Apple: keep original GUIDs unchanged, even if
  title or enclosure URL change; changing them can create duplicate episodes and distort
  Analytics.
- **Moving a feed URL (Apple Podcasts):** serve an HTTP 301 redirect from the old feed URL
  and add the `itunes:new-feed-url` tag to the new feed, pointing at the new URL (not the
  Apple Podcasts Connect mirror URL). Keep both for at least four weeks. A third-party host
  can usually set up the redirect.
- Write show notes with links, guest names and timestamps.

## Verify
- [ ] Each speaker on a separate track, room tone recorded.
- [ ] Final file measured against your platform's loudness target.
- [ ] Enclosure has url, length in bytes and MIME type.
- [ ] No GUID or feed URL changed on existing episodes; any feed move uses 301 plus `itunes:new-feed-url`.

## Checked
2026-11-01. Confirmed: enclosure attributes and guid wording (RSS 2.0 specification, rssboard.org); 301 redirect, `itunes:new-feed-url`, four-week minimum and GUID stability (Apple Podcasts "Change the RSS feed URL" page). Removed: loudness figures, ffmpeg command, processing-chain settings, MP3 and ID3 bitrate and artwork sizes, sample-rate advice (Apple requirements pages did not state them and ffmpeg docs could not be fetched).
Method: documentation only; no commands were run.
