---
id: creative-arts.music.dj-performance.live-streaming-dj-sets-and-copyright
name: live-streaming-dj-sets-and-copyright
category: creative-arts
field: music
product: dj-performance
tags: [dj-performance, rekordbox, serato, cdj, dj-live-stream, obs, twitch, youtube-live, audio-interface-routing, stream-audio-levels, copyright-takedown, content-id, licensed-streaming-platforms, camera-setup]
level: practitioner
status: draft
description: "Stream DJ sets: routing mixer audio into OBS, levels and AV sync, camera and lighting basics, and avoiding copyright takedowns under platform rules."
sources: ["https://obsproject.com/kb/ (OBS Studio knowledge base - audio sources and filters)", "https://support.google.com/youtube/answer/2797370 (YouTube Content ID)"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Live streaming DJ sets and copyright

**Goal:** a good-sounding, stable stream that doesn't get muted or taken down.

## 1. Audio routing
- Mixer master/REC OUT -> audio interface input (or the mixer's own USB audio as an input device) -> OBS **Audio Input Capture**.
- Mute desktop audio and other sources to avoid doubling; use OBS's audio mixer meters.
- Levels: peaks around **-6 dBFS** in OBS; add a limiter filter at -1 dB as safety. Bitrate 160-320 kbps AAC for music.
- Mic for talking on a separate input with a noise gate; duck music slightly while talking if desired.

## 2. Video
- One wide camera + one close camera on the hands/decks; capture card or USB webcams. Light the face and hands (soft key light).
- Sync audio and video: add a video delay or audio sync offset in OBS (Advanced Audio Properties) so beats match hand movements.
- Wired internet; test upload bandwidth (need roughly 1.5x the stream bitrate headroom).

## 3. Copyright
- Most mainstream platforms detect copyrighted recordings (Content ID, audible magic) and may mute, block or take down streams; repeated strikes can end accounts.
- Options: platforms or services with licensing arrangements for DJ streams (check current offerings; e.g. some partner programmes and DJ-specific streaming platforms), playing your own productions or tracks with explicit permission, or streaming only where the platform's music policy allows.
- Read the current music guidelines of the platform (Twitch, YouTube, Facebook/Instagram) before going live; policies change.

## 4. Run sheet
- Test stream (unlisted/private) before the show; check audio on a phone.
- Backup recording locally (OBS Record) at higher quality.

## Gotchas
- Stream audio clipping because the mixer master is in the red.
- OBS sample rate (48 kHz) different from the interface: drift/crackle.
- Assuming a short clip or "DJ mix" exemption protects you: it doesn't.

## Verify
- Private test stream: audio clean, in sync, no mutes over 30 minutes.
- Local recording saved after the show.
