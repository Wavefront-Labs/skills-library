---
id: computing-software.web-development.web-performance.low-quality-image-placeholders-and-blurhash
name: low-quality-image-placeholders-and-blurhash
category: computing-software
field: web-development
product: web-performance
tags: [image-optimization, image-placeholders, blurhash, lqip, perceived-performance]
level: practitioner
status: verified
description: "Improving perceived image loading with placeholders: dominant colour, LQIP, BlurHash/ThumbHash, CSS blur-up, and keeping placeholders from hurting LCP or CLS."
sources:
  - https://chromium.googlesource.com/chromium/src/+/refs/heads/main/docs/speed/metrics_changelog/2023_04_lcp.md
  - https://blurha.sh/
  - https://evanw.github.io/thumbhash/
  - https://nextjs.org/docs/app/api-reference/components/image#placeholder
  - https://web.dev/articles/lcp-lazy-loading
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Low-quality placeholders and BlurHash

Placeholders improve *perceived* performance and reduce visual jank; they don't make the real image arrive sooner.

## 1. Options (smallest to richest)
| Technique | Size | Notes |
|---|---|---|
| Dominant colour background | a few bytes | `background-color` on the img/container; cheapest, no JS |
| CSS gradient of 2-4 colours | ~50 bytes | precomputed |
| BlurHash | 28 chars at the default 4x3 components (run; 9x9 gave 166) | decode to canvas/data URL; needs JS decode (or server-side to a tiny PNG) |
| ThumbHash | 25 bytes in a run (32x32 input) | better detail, encodes aspect ratio and alpha |
| LQIP (tiny 16-32px JPEG/WebP, inlined base64) | a 16px WebP at quality 40 was 406 bytes (544 as base64); expect hundreds of bytes | blurred via CSS `filter: blur()` or SVG filter |
| SQIP (SVG primitives) | larger than the hashes; measure | stylised |

## 2. Blur-up implementation
```html
<div class="img-wrap" style="background-image:url(data:image/webp;base64,UklGR...); aspect-ratio: 4/3">
  <img src="photo-800.avif" srcset="…" sizes="…" width="800" height="600" alt="…" loading="lazy" decoding="async"
       onload="this.classList.add('loaded')">
</div>
```
```css
.img-wrap { background-size: cover; overflow: hidden; }
.img-wrap img { opacity: 0; transition: opacity .3s; }
.img-wrap img.loaded { opacity: 1; }
@media (prefers-reduced-motion: reduce) { .img-wrap img { transition: none; } }
```
Next.js: `<Image placeholder="blur" blurDataURL=…>` (`blurDataURL` is added automatically for static imports of jpg, png, webp and avif that are not animated; dynamic or remote images need your own). Generate hashes at upload/build time and store them with image metadata (`sharp` + `blurhash`/`thumbhash` packages).

## 3. Don't hurt Core Web Vitals
- Reserve dimensions (wrapper `aspect-ratio` or width/height) - placeholders must be exactly the final size or they cause CLS.
- **LCP**: an image sitting at `opacity: 0` is not an LCP candidate until it becomes visible (run in Chromium: LCP reported at about 0.66 s for a visible image and about 3.1 s when it started at `opacity: 0` and was revealed by a delayed fade); for the hero image skip the fade (show immediately) or make the transition very short. Placeholder images themselves can be counted as LCP candidates in some cases (since Chrome 112, images below 0.05 bits of image data per displayed pixel are ignored for LCP, per the Chromium metrics changelog, so a very simple placeholder is skipped and the real image becomes the LCP).
- Don't block rendering on JS decoding of BlurHash for above-the-fold images - decode server-side to a data URL or use CSS colours.
- Keep inline base64 small; dozens of 1 KB LQIPs bloat HTML.

## Verify
Throttled load shows placeholders of the right size with no layout shift; LCP time unchanged or improved compared to no placeholder (measure, don't assume).
