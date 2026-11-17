---
id: creative-arts.animation.blender.clip-proxies-prefetch
name: clip-proxies-prefetch
category: creative-arts
field: animation
product: blender
tags: [blender, motion-tracking, clip-proxies, prefetch, clip-cache, movie-clip-editor]
level: practitioner
status: docs-checked
description: "Speed up the Movie Clip Editor on heavy footage: Proxy panel sizes and Build Proxy, Proxy Size display, Prefetch (P) and the Preferences Memory Cache Limit."
sources:
  - https://docs.blender.org/manual/en/latest/movie_clip/tracking/clip/editing/clip.html
  - https://docs.blender.org/manual/en/latest/editors/preferences/system.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# clip-proxies-prefetch

Goal: real-time playback and quick tracking on heavy footage (4K, long-GOP video).

## Proxies (Sidebar > Footage tab > Proxy panel)

- The panel header checkbox enables proxies for the clip.
- **Build Original**: toggle 25, 50, 75 or 100 percent. **Build Undistorted**: the same sizes for undistorted proxies.
- **Quality** sets the proxy image quality. **Custom Directory** stores proxies elsewhere (the default is the movie location).
- **Build Proxy** creates them. **Proxy Size** chooses which size the editor displays.
- Tracking on a proxy size works from reduced images; switch back to the original size for final accuracy and check that tracks still sit on their features (practice, not from the manual).

## Prefetch and cache

- **Prefetch** (Clip menu, or P in the editor) fills the cache with as many frames as fit from the drive. The manual notes it keeps CPU and drive busy while the editor is open, so use it when you are about to track.
- **Preferences > System > Memory & Limits > Memory Cache Limit** is the upper limit, in megabytes, of the Video Sequencer and Movie Clip Editor memory cache.
- **Set Scene Frames** (Clip menu) sets the scene end frame to match the clip duration.

## Verify

After prefetch, play the clip: playback is smooth. Toggle Proxy Size and confirm tracks still sit on their features.

## Checked

Checked 2026-10-27 against the Blender 5.2 manual (blender-v5.2-release branch: movie_clip/tracking/clip/editing/clip, editors/preferences/system) and the 5.2 source (space_clip.py Proxy panel, rna_movieclip.cc proxy properties, blender_default keymap P). Fixed: the Proxy panel is in the Footage tab and has Build Original and Build Undistorted rows. Removed unconfirmed claims: timecode index options, the BL_proxy folder name, JPEG or video proxy format, suggested cache sizes, codec advice, and that timecode mismatch shifts tracks.
Method: documentation only; no commands were run.
