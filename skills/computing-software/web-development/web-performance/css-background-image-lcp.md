---
id: computing-software.web-development.web-performance.css-background-image-lcp
name: css-background-image-lcp
category: computing-software
field: web-development
product: web-performance
tags: [background-image-lcp, lcp, css-background, image-preload, fetchpriority]
level: practitioner
status: docs-checked
description: "When a CSS background image is the LCP element: why it is discovered late, preloading with imagesrcset and image-set, and using an img element instead."
sources:
  - https://web.dev/articles/optimize-lcp#optimize-when-the-resource-is-discovered
  - https://web.dev/articles/preload-responsive-images
  - https://developer.mozilla.org/en-US/docs/Web/CSS/image/image-set
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# CSS background image as LCP

## 1. Why it is slow
For a good LCP the resource must be discoverable in the initial HTML response by the browser's preload scanner. web.dev lists the cases that are discoverable: an `<img>` with `src` or `srcset` in the initial markup, a CSS background image that is preloaded with `<link rel="preload">` (or a `Link` header), and a font preloaded the same way. A CSS background image that is not preloaded is not discoverable from the HTML, so it starts late; this shows up as a large resource load delay subpart of LCP (the time between TTFB and the browser starting to load the LCP resource).

## 2. Fix: use an img element
An `<img>` whose `src` or `srcset` is in the HTML is discoverable. Set `fetchpriority="high"` on the image likely to be the LCP element, but on no more than one or two images, since more makes priority unhelpful.
```html
<img src="hero-1200.avif" srcset="hero-640.avif 640w, hero-1200.avif 1200w, hero-2000.avif 2000w"
     sizes="100vw" alt="" fetchpriority="high" width="2000" height="900">
```

## 3. If it must stay a CSS background
Preload it in the HTML with a high fetch priority. Without `fetchpriority`, image preloads get the default (low) priority for `as="image"`.
```html
<link rel="preload" as="image" fetchpriority="high"
      imagesrcset="hero-640.avif 640w, hero-1200.avif 1200w, hero-2000.avif 2000w" imagesizes="100vw">
```
- `imagesrcset` and `imagesizes` take the same syntax as `srcset` and `sizes` on `<img>`.
- For CSS `image-set()` backgrounds (chosen by screen density), preload with `imagesrcset` and no `href`: browsers that lack `imagesrcset` on `<link>` but support `image-set` then download the right source (without the preload benefit).
- For art-directed backgrounds, use separate preload links with `media` attributes matching the CSS media queries.
- To preload a newer format as progressive enhancement, add `type="image/avif"`; browsers that support it benefit and others do not.
- `image-set()` accepts `type()` per candidate, for example `url("image1.avif") type("image/avif"), url("image2.jpg") type("image/jpeg")`.

## 4. Related render blocking
A large stylesheet that takes much longer to load than the LCP resource delays rendering the LCP element even after the resource has loaded. Remove unused CSS, defer non-critical CSS, and minify and compress critical CSS.

## Verify
- [ ] The network waterfall shows the hero image requested early (right after the HTML), and the resource load delay subpart is small.

## Checked
2026-11-09. Read the relevant sections of "Optimize Largest Contentful Paint" (discovery, fetch priority, render-blocking CSS), "Preload responsive images" (imagesrcset, image-set, media, type) and the MDN `image-set()` page. Removed (not on those pages): the claim that a mismatched preload downloads twice, the object-fit overlay CSS, the gradient-as-LCP note and the compression advice.
Method: documentation only; no commands were run.
