---
id: creative-arts.animation.sound-design.video-track-sync-in-the-daw
name: video-track-sync-in-the-daw
category: creative-arts
field: animation
product: sound-design
tags: [video-in-daw, daw-session, picture-sync, timecode, two-pop, pro-tools, reaper]
level: practitioner
status: draft
description: "Lock picture to a DAW session for sound work: session frame rate, start timecode, importing the reference video, 2-pop alignment and checking video-offset drift."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Video track sync in the DAW

Sound work only holds up if the picture in the DAW is the picture the editor locked. Set it up the same way each time.

## Session set-up
1. **Frame rate**: set the session timecode rate to match the picture (for example 24, 23.976, 25, 29.97 non-drop or drop; see `timecode-drop-frame.md`). Mismatch gives progressive drift.
2. **Start timecode**: set the session start to match the reel. A common convention is to start each reel at the hour of its reel number (01:00:00:00 for reel 1), but follow what editorial sent.
3. **Import the reference video** (a low-bitrate H.264 or an intraframe codec such as ProRes proxy or DNxHD/HR) with burned-in timecode if possible. Pro Tools and REAPER both import video onto a timeline track; REAPER shows a video window from its View menu, and Pro Tools uses a video track and a video engine.
4. **Align** the file to the session start (video start timecode) rather than dragging by eye.

## Verify sync with the 2-pop
- Editorial leaders include a "2-pop": a one-frame beep, usually exactly 2 seconds before first frame of action (FFOA). See `leaders-and-two-pops.md`.
- Find the pop in the audio and the frame where the leader shows "2" (or a flash) and check they coincide. Do this every time you receive picture or audio.
- If the offset is a constant number of frames, record it in the session notes and fix it rather than nudging individual clips.

## Latency
- Video output hardware, interface and monitor add delay. Run a flash-and-beep test (a clip with a visual flash and a click on the same frame) and measure the playback offset; most DAWs have a video offset setting in their preferences to compensate, and the name and location varies by DAW and version.
- Do not compensate for display delay by sliding audio clips; fix it in the DAW's settings or the monitoring chain.

## New picture versions
- When editorial sends a new cut, conform the session (see `editorial-change-lists.md`) rather than re-aligning by ear, then re-verify the 2-pop.

## Verify
- [ ] Frame rate and start timecode match the turnover notes.
- [ ] 2-pop and flash coincide on playback.
- [ ] Offset notes recorded in the session.
