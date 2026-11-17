---
id: computing-software.web-development.web-performance.video-instead-of-gif-and-poster-preload
name: video-instead-of-gif-and-poster-preload
category: computing-software
field: web-development
product: web-performance
tags: [image-optimization, video-optimization, animated-gif, poster, preload, performance, gif-to-video]
level: practitioner
status: docs-checked
description: "Replacing animated GIFs with video and optimising video delivery: muted autoplay loops, poster images, preload values and lazy-loading video."
sources:
  - https://web.dev/articles/replace-gifs-with-videos
  - https://web.dev/articles/fast-playback-with-preload
  - https://developer.mozilla.org/en-US/docs/Web/HTML/Element/video
  - https://web.dev/articles/lazy-loading-video
licence: Apache-2.0
version: 5
updated: 2026-11-17
---

# Video as GIF replacement, poster and preload

## 1. Replace GIFs
Animated GIFs are significantly larger than equivalent video (web.dev). Convert with FFmpeg (command from web.dev):
```bash
ffmpeg -i my-animation.gif -b:v 0 -crf 25 -f mp4 -vcodec libx264 -pix_fmt yuv420p my-animation.mp4
```
ffmpeg 8.0.1 turned a 321x241 GIF into a 320x240 MP4 with no error and no audio stream; `yuv420p` needs even sizes, so check the output size.
```html
<video autoplay loop muted playsinline width="480" height="270">
  <source src="anim.webm" type="video/webm">
  <source src="anim.mp4" type="video/mp4">
</video>
```
web.dev's GIF-replacement pattern uses `autoplay muted loop playsinline` on a video with no audio track, and MDN notes that modern browsers block autoplay of videos with an unmuted audio track.

## 2. Poster
- For ordinary video, set `poster` (and `width`/`height`) so users see an image before playback; optimise it like any image.
- A `<video>` without a poster is not an LCP candidate, which is why web.dev's GIF-style example has none. For a video that is an LCP candidate, use a poster image and preload it with `<link rel="preload" as="image" href="poster.avif">` (web.dev).

## 3. preload
- `preload="none"`: nothing until play - best for many videos per page or below the fold.
- `preload="metadata"`: only video metadata (for example length) is fetched.
- `preload="auto"`: the whole video file may be downloaded - only for the primary video likely to be played.

## 4. Lazy-load
`loading="lazy"` is supported on `<video>` (MDN, web.dev): the media and poster are not loaded until the element is near the viewport. Videos that are the LCP element should not use it.

## 5. Encoding and delivery
- For GIF-style loops, produce video with no audio track (web.dev).

## Verify
Network panel: GIF replaced by a much smaller video; videos below the fold don't download until scrolled near; LCP unchanged or better.

## Checked

2026-10-28. Confirmed from web.dev (replace GIFs with video: FFmpeg command, GIFs significantly larger, videos without poster are not LCP candidates; lazy-loading video: `autoplay muted loop playsinline`, preload poster for LCP video, `loading="lazy"` on video) and MDN `<video>` (`preload` values, `loading`, autoplay blocking). Removed or corrected: the 5-20x figure, the WebM and `+faststart` commands, CRF values, AV1 advice, WCAG 2.2.2 reference, the claim that `loading="lazy"` is unsupported on video (it is supported), and the advice to always set a poster on GIF-style loops (web.dev advises against it).

Run 2026-11-01 with ffmpeg and ffprobe 8.0.1 on Windows (Git Bash), scripts in a scratch folder: the web.dev GIF-to-MP4 command (h264, yuv420p, no audio track). Not run: the HTML attributes, `loading="lazy"` on video and `preload` behaviour (no browser), so the skill stays docs-checked.

Method: documentation plus partial commands run (ffmpeg 8.0.1).
