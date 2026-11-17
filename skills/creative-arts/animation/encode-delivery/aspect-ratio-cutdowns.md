---
id: creative-arts.animation.encode-delivery.aspect-ratio-cutdowns
name: aspect-ratio-cutdowns
category: creative-arts
field: animation
product: encode-delivery
tags: [aspect-ratio-versions, platform-master, vertical-video, 9x16, 1x1, 4x5, reframing, social-cutdown, safe-zones, ffmpeg, crop]
level: practitioner
status: verified
description: "Make vertical, square and 4:5 social versions of 16:9 animation: reframing strategies, per-shot crop keys, safe zones for platform UI, ffmpeg crop/pad."
sources:
  - https://ffmpeg.org/ffmpeg-filters.html#crop
  - https://support.google.com/youtube/answer/10059070
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Aspect ratio versions and social cutdowns

**Goal:** 9:16 (Shorts/Reels/TikTok), 1:1 and 4:5 versions where characters stay in frame and
nothing important sits under the platform's buttons and captions.

## Strategy choice

| Method | When |
|---|---|
| Re-render with a new camera (best) | 3D/CG shots where the scene file exists: change resolution and reframe the camera per shot |
| Per-shot crop with keyframed offset | 2D or finished comps; action moves within frame |
| Centre crop | only if staging was protected for vertical from the start |
| Blurred-fill pillar (fit 16:9 inside 9:16 over a blurred copy) | fallback for wide shots that cannot be cropped |

Plan it at layout: mark a 9:16 protection area in the camera overlay for shows that will be cut
down, so the crop is designed rather than rescued.

## ffmpeg recipes (1920x1080 source)

```bash
# static centre-ish crop to 9:16 then scale to 1080x1920
ffmpeg -i shot.mov -vf "crop=608:1080:656:0,scale=1080:1920:flags=lanczos" -c:v libx264 -crf 18 v916.mp4
# moving crop: x from 400 to 900 over the shot (linear pan)
ffmpeg -i shot.mov -vf "crop=608:1080:'400+(900-400)*t/5':0,scale=1080:1920" v916_pan.mp4
# blurred fill
ffmpeg -i ep.mov -filter_complex "[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=20[bg];[0:v]scale=1080:-2[fg];[bg][fg]overlay=(W-w)/2:(H-h)/2" v916_fill.mp4
# 1:1 and 4:5
ffmpeg -i ep.mov -vf "crop=1080:1080,scale=1080:1080" sq.mp4
ffmpeg -i ep.mov -vf "crop=864:1080,scale=1080:1350" p45.mp4
```

For per-shot keys across an episode, keep a CSV of shot in/out and crop x per shot, and
generate one filter per shot (trim + crop) then concat, rather than one huge expression.

## Safe zones

Vertical platforms overlay their own UI (buttons, captions, account name): keep titles and faces
clear of the top, bottom and right-hand edges. Use each platform's current safe-zone guidance;
it changes with app redesigns.

## Gotchas

- Re-time for the platform: social cutdowns usually need a tighter edit and burned-in captions.
- Cropping a 1080p master to 9:16 gives 608 px of real width; upscaling to 1080 softens line
  art. Render vertical natively when quality matters.

## Verify

Preview each version on a phone with the platform UI (upload unlisted/private), check faces and
text clear of overlays.

## Checked

2026-10-28. Confirmed in the ffmpeg-filters manual: `crop` takes width, height, x and y; x and y are evaluated per frame and may use `t`; `scale` supports `force_original_aspect_ratio`; `boxblur` and `overlay` exist. Removed: platform safe-zone percentages, the muted-autoplay statement, and the Instagram help source (page not readable).

2026-11-01 run check: all five recipes (static crop, moving crop with a `t` expression, blurred fill, 1:1, 4:5) executed on a synthetic 1920x1080 source; outputs probed at 1080x1920, 1080x1920, 1080x1920, 1080x1080 and 1080x1350. 1080 x 9/16 = 607.5, so 608 px of real width is arithmetic.

Method: commands run with ffmpeg 8.0.1 (Windows build) on synthetic lavfi inputs, plus the ffmpeg manuals for the options above.
