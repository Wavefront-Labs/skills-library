---
id: computing-software.web-development.frontend-development.html-video-and-audio-elements
name: html-video-and-audio-elements
category: computing-software
field: web-development
product: frontend-development
tags: [semantic-html, html-video-audio, media-tracks, video, audio, webvtt, html]
level: practitioner
status: docs-checked
description: "Using video and audio elements: multiple sources and codecs, track elements for captions, preload/poster, playsinline, autoplay policy, and range-request serving."
sources:
  - https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/video
  - https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/track
  - https://developer.mozilla.org/en-US/docs/Web/Media/Guides/Autoplay
  - https://developer.mozilla.org/en-US/docs/Web/Media/Guides/Formats/codecs_parameter
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Video and audio elements

## 1. Markup
```html
<video controls preload="metadata" poster="/media/intro.jpg" width="1280" height="720" playsinline>
  <source src="/media/intro.av1.mp4" type='video/mp4; codecs="av01.0.05M.08"'>
  <source src="/media/intro.h264.mp4" type="video/mp4">
  <track kind="captions" src="/media/intro.en.vtt" srclang="en" label="English" default>
  <track kind="captions" src="/media/intro.fr.vtt" srclang="fr" label="Français">
  <a href="/media/intro.h264.mp4">Download the video</a>
</video>
```
- Browser picks the first `<source>` whose `type` it can play - put the most efficient codec first, H.264 MP4 last as the universal fallback.
- `width`/`height` reserve space for the video.
- Fallback content inside is shown only by browsers without media support.

## 2. Attributes
- `preload="none|metadata|auto"` - a hint; `metadata` is a good default. `none` for many videos on a page.
- Browsers block autoplay of audible media; it is allowed when the media is muted or the user has interacted with the site. Always pair with `muted playsinline`, and still expose controls (WCAG 2.2.2 for >5s).
- `playsinline` plays the video within the element's playback area; its absence does not imply fullscreen.
- `crossorigin` is relevant for cross-origin `<track>` files - see the `crossorigin` attribute on the media element and `<track>`.

## 3. Tracks
- `kind`: `captions` (dialogue + sounds, for deaf users), `subtitles` (translation), `descriptions` (text audio description), `chapters`, `metadata`.
- `default` may be set on only one `<track>` per media element; the default `kind` is `subtitles`.

## 4. Serving
- For streaming and delivery options see the MDN audio and video delivery guide.

## 5. Scripting
`video.play()` returns a promise - catch the rejection (`NotAllowedError` means playback was not permitted, for example by autoplay policy) and show a play button. Listen for `loadedmetadata`, `ended`, `error`.

## Verify
- Captions appear in the player menu; the video plays inline on mobile.

## Checked
2026-10-26. MDN video and track pages, autoplay guide, codecs parameter page (main, 2026-10-26): confirmed preload none/metadata/auto is only a hint, autoplay is allowed for muted media or after user interaction, play() returns a promise rejected with NotAllowedError when blocked, track kind values subtitles/captions/descriptions/chapters/metadata, one default track per media element, the AV1 codecs string form, and playsinline semantics. Removed range-request, text/vtt, faststart, HLS and CLS claims that no fetched page confirms.
Method: documentation only; no commands were run.
