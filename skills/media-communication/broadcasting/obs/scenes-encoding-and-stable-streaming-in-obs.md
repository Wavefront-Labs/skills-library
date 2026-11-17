---
id: media-communication.broadcasting.obs.scenes-encoding-and-stable-streaming-in-obs
name: scenes-encoding-and-stable-streaming-in-obs
category: media-communication
field: broadcasting
product: obs
tags: [obs, obs-studio, live-streaming, streaming, recording, scenes, sources, scene-collection, profiles, encoder, bitrate, stream-key, dropped-frames, mkv, remux, hybrid-mp4, broadcasting]
level: practitioner
status: docs-checked
description: "Set up OBS Studio for a stable stream and safe recording: profiles vs scene collections, bitrate headroom, dropped frames, GPU overload, and recording to a crash-safe format."
sources:
  - https://obsproject.com/kb/profiles
  - https://obsproject.com/kb/stream-connection-troubleshooting
  - https://obsproject.com/kb/encoding-performance-troubleshooting
  - https://obsproject.com/kb/audio-video-formats-guide
  - https://obsproject.com/kb/hybrid-mp4
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Scenes, encoding and stable streaming in OBS

**Goal:** a stream that doesn't drop frames and switches scenes smoothly, plus a safe local
recording in case the stream fails.

## 1. Organise: profiles and scene collections
- A **profile** stores stream settings (including the connected account), video settings
  and output settings. Profiles do not store scenes.
- A **scene collection** holds your scenes and sources. Keep them separate so changing a
  platform does not wreck your layout.

## 2. Scenes and sources
- Build one scene per shot (starting soon, main, screen share, BRB, ending).
- Check the OBS KB for stream layout tutorials (game screen, alerts and chat, BRB).

## 3. Bitrate and dropped frames
- Dropped frames mean the connection to the server is not stable or you cannot keep up
  with your set bitrate; too many can disconnect you from the server.
- The KB suggests starting at 75% of your total upload speed. The right value also depends
  on your stable upload and the service's limits: check the platform's current guidance
  rather than a remembered number.
- If frames drop, lower the bitrate to what your connection holds steadily.

## 4. GPU overload
- Choppy output or "encoding overloaded" messages mean the machine is short of resources:
  free some up for OBS.
- On Windows, GPU overload can often be resolved by running OBS Studio as administrator.
- Hardware encoding runs on the GPU, so GPU load matters for it too.

## 5. Recording
- For recording, the OBS guide recommends the best hardware encoder available
  (AV1, then HEVC, then H.264).
- MKV is the default and recommended for most uses; it is failsafe (a recording interrupted
  by power loss stays recoverable) and can be remuxed into a more compatible format.
- Do not record directly to MP4 or MOV; Hybrid MP4 (OBS 30.2) and Hybrid MOV (OBS 32.0) are
  the recoverable alternatives. Chapter markers are written only on finalisation, so a
  crash loses them.

## 6. Stream key
The stream key is a secret: keep the settings window off screen and reset the key if it
was exposed.

## Verify
- [ ] Separate profile and scene collection per use.
- [ ] Bitrate set below your measured stable upload.
- [ ] Test stream shows no sustained dropped frames.
- [ ] Recording plays back with audio in sync.

## Checked
2026-11-01. Confirmed against the OBS Knowledge Base pages listed in sources: what profiles
and scene collections store, dropped-frame meaning, the 75% of upload starting point, run
as administrator for GPU overload, MKV default and failsafe, remuxing, Hybrid MP4/MOV
versions. Removed as not stated on those pages: specific bitrates, keyframe interval,
CBR, encoder menu paths, shortcuts, filter chain and levels, multistream plugins, Stats
dock table, sample rate, transition times, scene nesting and source locking. Stream layout tutorials listed in the
KB category were seen by title only.
Method: documentation only; no commands were run.
