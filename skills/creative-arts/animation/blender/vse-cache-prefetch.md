---
id: creative-arts.animation.blender.vse-cache-prefetch
name: vse-cache-prefetch
category: creative-arts
field: animation
product: blender
tags: [blender, vse, sequencer, vse-cache, sequencer-cache, prefetch, playback]
level: practitioner
status: docs-checked
description: "Speed up VSE playback: memory cache limit, Raw and Final cache, Prefetch Frames, the Show Cache overlay bars, and why Scene strips are not prefetched."
sources:
  - https://docs.blender.org/manual/en/latest/editors/video_sequencer/sequencer/sidebar/cache.html
  - https://docs.blender.org/manual/en/latest/editors/preferences/system.html#video-sequencer
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# vse-cache-prefetch

Goal: smooth playback of heavy edits with effects and modifiers.

## Memory cache limit

- Preferences > System > Video Sequencer > **Memory Cache Limit** (MB). This limit is shared by the Video Sequencer and the Movie Clip Editor. The manual recommends high values for best performance.

## Cache settings (Sidebar > Cache > Cache Settings)

These settings apply to all strips in the editor.

- **Prefetch Frames**: caches frames after the current frame in the background, for smoother playback. Prefetching is not supported for Scene strips.
- **Cache > Raw**: caches image data right after it is read from disk. Speeds up changes to strip parameters such as colour correction, at the cost of more memory.
- **Cache > Final**: caches the final composited image of each frame, for faster playback of fully processed strips.
- A readout at the bottom shows the current cache size and the Raw and Final usage.

## Seeing what is cached

Overlays > **Show Cache** (Timeline overlay). Under Display in the Cache panel: Raw shows a red bar under cached frames, Final shows a blue bar at the top of the timeline.

## Gotchas

- Scene strips (3D scenes in the edit) are not prefetched. Render them to image sequences and replace the strips when playback matters.
- Proxies reduce decoding cost for large footage (see vse-proxy-setup) and can be combined with the cache.
- If cached frames look stale after a source file changed, reload the strips (Strip > Inputs > Reload Strips, Alt R) or run the Refresh All operator.

## Verify

Play a section twice: with Final cache on, the second pass plays from cache and the blue bar covers the section.

## Checked

- Date: 2026-10-27. Documentation: Blender 5.2 manual (blender-v5.2-release branch of blender-manual).
- Confirmed: Memory Cache Limit location and scope (Preferences > System > Video Sequencer), Prefetch Frames location and Scene-strip exclusion, Raw and Final cache options only, red and blue overlay bars, Reload Strips (Alt R). Removed the Preprocessed and Composite levels, the Developer Extras note and the disk cache section, which the 5.2 manual does not document.
- Method: documentation only; no commands were run.
