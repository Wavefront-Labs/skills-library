---
id: computing-software.web-development.responsive-design.responsive-video-and-iframe-embeds
name: responsive-video-and-iframe-embeds
category: computing-software
field: web-development
product: responsive-design
tags: [responsive-embed, responsive-video, aspect-ratio, iframe-embeds, facade-pattern]
level: practitioner
status: gated
description: "Responsive video and iframe embeds: aspect-ratio instead of padding hacks, intrinsic sizing of third-party widgets, lite-embed facades, lazy loading and auto-resizing iframes."
sources:
  - https://developer.mozilla.org/en-US/docs/Web/CSS/aspect-ratio
  - https://web.dev/articles/iframe-lazy-loading
  - https://github.com/paulirish/lite-youtube-embed
  - https://developer.chrome.com/docs/lighthouse/performance/third-party-facades
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Responsive video and iframe embeds

## 1. aspect-ratio
```css
.embed iframe, .embed video { inline-size: 100%; block-size: auto; aspect-ratio: 16 / 9; border: 0; }
.embed--vertical iframe { aspect-ratio: 9 / 16; max-block-size: 80dvh; inline-size: auto; margin-inline: auto; }
```
- Replaces the old `padding-top: 56.25%` wrapper hack (aspect-ratio: Chrome 88, Firefox 89, Safari 15; run: a 640px-wide iframe rendered 640x360 and the 9/16 variant 270x480 with `max-block-size: 80dvh` in a 600px window).
- `<video width="1280" height="720">` already reserves the right ratio with `height: auto` (run: 640x360 at 640px wide); iframes have no intrinsic ratio (a raw 640px iframe rendered 644x154: default 150px height plus 2px borders), so set it in CSS.
- CMS content: target `iframe[src*="youtube"], iframe[src*="vimeo"]` in prose styles, or wrap embeds server-side.

## 2. Third-party widgets with unknown height
Tweets, Instagram posts and forms change height after load. Options:
- Reserve a typical `min-height` to limit layout shift.
- Use the provider's postMessage resize protocol, or for your own iframes, post the height from inside:
```js
// inside the iframe
new ResizeObserver(() => parent.postMessage({ type: "h", h: document.documentElement.scrollHeight }, "https://host.example")).observe(document.body);
// host: validate e.origin, then iframe.style.height = e.data.h + "px"
```

## 3. Facades for heavy players
A YouTube embed costs on the order of 500 KB on initial load (web.dev's iframe lazy-loading article says lazy-loading saves around 500 KB). Show a thumbnail + play button and swap in the iframe on click: `lite-youtube-embed`, `lite-vimeo-embed`, or a `<button>` with the poster. Use `youtube-nocookie.com` for privacy. Mobile Safari may need a second tap to play after swapping; pass `autoplay=1` (gated: unconfirmed, source is paywalled or blocked).

## 4. Lazy loading
`<iframe loading="lazy" title="Product demo video" ...>` defers offscreen embeds (iframe `loading`: Chrome 77, Firefox 121, Safari 16.4 per MDN compat data). Every iframe needs a `title`.

## 5. Video sizing
Serve multiple renditions or HLS for long videos; `object-fit: cover` for background video in a fixed-ratio box; always add `playsinline muted` for autoplaying hero video on iOS (gated: unconfirmed, source is paywalled or blocked), and a pause control.

## Verify
- [ ] Embeds fill the column at all widths without black bars or overflow; no CLS when they load; facades load the real player only on interaction; every iframe has a title.
