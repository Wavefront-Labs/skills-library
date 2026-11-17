---
id: creative-arts.visual-art.procreate.exporting-animated-gif-mp4-and-png
name: exporting-animated-gif-mp4-and-png
category: creative-arts
field: visual-art
product: procreate
tags: [visual-art, procreate, animated-gif, animated-png, animated-mp4, procreate-animation-export, gif-export, web-ready, frame-rate]
level: practitioner
status: draft
description: "Export a Procreate Animation Assist project as animated GIF, PNG or MP4, set frame rate and loop, and keep file size workable for social and web."
sources: ["https://procreate.com/handbook"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Exporting animation from Procreate

**Goal:** turn an Animation Assist timeline into a shareable file. Menu names per the Handbook's Animation Assist and Share sections.

## Steps
1. Turn on **Actions > Canvas > Animation Assist** and finish your frames (see `creative-arts.visual-art.procreate.animation-assist-onion-skins-and-timing`).
2. Set **Frames per second** (the slider ranges from 1 to 60) and the playback style (Loop, Ping-Pong or One Shot) in the Animation Assist settings.
3. **Actions > Share** and in the animation section choose **Animated GIF**, **Animated PNG**, **Animated MP4** or **Animated HEVC** (the list is from the Handbook; check your version).
4. Use the **Web ready** option (where offered) to reduce size for web use; GIF is limited to 256 colours so gradients band.
5. Save to Files, Photos or share direct. Preview the result on the target platform.

## Which format
- **GIF:** universal but large and 256-colour; fine for flat colour loops.
- **Animated PNG:** full colour and alpha, supported by modern browsers but not by every messaging app.
- **MP4:** smallest and best for photographic or gradient animation; no alpha. Whether the HEVC option keeps transparency depends on the player; treat as unconfirmed and test.

## Gotchas
- Large canvases create huge GIFs; reduce canvas size or export MP4.
- Frame rate changes duration; a 24 fps drawing played at 12 fps looks slow.
- Social platforms may re-compress; test how a looped MP4 plays.

## Verify
- [ ] The exported file loops as intended on the target platform.
- [ ] Duration equals frames divided by fps (accounting for holds).
