---
id: computing-software.web-development.nextjs.next-image-configuration
name: next-image-configuration
category: computing-software
field: web-development
product: nextjs
tags: [nextjs-optimization, nextjs-metadata, next-image, remotepatterns, image-optimization, sizes-attribute, priority-image, image-loader]
level: practitioner
status: verified
description: "Using next/image well: required sizing, sizes for responsive images, priority/preload for LCP, remotePatterns, custom loaders and self-hosted optimisation costs."
sources:
  - https://nextjs.org/docs/app/api-reference/components/image
  - https://nextjs.org/docs/app/getting-started/images
  - https://nextjs.org/docs/app/api-reference/config/next-config-js/images
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# next/image configuration

**Goal:** images served at the right size and format, LCP image loaded early, no layout shift, and no surprise optimisation bills or open proxies.

## 1. Sizing
```tsx
import Image from 'next/image';
import hero from './hero.jpg';                         // static import: width/height/blur known at build
<Image src={hero} alt="Team at work" placeholder="blur" priority sizes="100vw" />
<Image src={`https://cdn.example.com/p/${id}.jpg`} alt={name} width={640} height={480} sizes="(min-width: 768px) 33vw, 100vw" />
<div style={{ position: 'relative', aspectRatio: '16/9' }}><Image src={url} alt="" fill sizes="50vw" style={{ objectFit: 'cover' }} /></div>
```
- Remote images need `width`+`height` (intrinsic ratio) or `fill` with a positioned, sized parent.
- **`sizes` is essential** for responsive layouts: without it Next assumes the image is as wide as the viewport (`fill`) or generates only 1x/2x of `width`, over-downloading.

## 2. LCP image
In Next 16 `priority` is deprecated in favour of `preload` (image docs, v16.0.0 version history); `preload` inserts a `<link>` preload in the head. For most cases the docs recommend `loading="eager"` or `fetchPriority="high"` instead, and say not to combine `preload` with `loading`/`fetchPriority`. Use it on exactly the hero/LCP image per page; all others lazy-load by default. Also new in 16.0.0: the default `qualities` allowlist is `[75]`.

## 3. Remote sources
```js
// next.config.js
images: {
  remotePatterns: [{ protocol: 'https', hostname: 'cdn.example.com', pathname: '/p/**' }],
  formats: ['image/avif', 'image/webp'],
  minimumCacheTTL: 2678400,   // default is 14400 (4 hours); the larger of this and the upstream Cache-Control max-age applies
}
```
Keep patterns narrow - a wildcard hostname turns `/_next/image` into an open image proxy others can abuse.

## 4. Where optimisation runs
Self-hosted `next start` optimises on the fly with `sharp` with zero configuration (CPU/memory heavy on glibc Linux per the self-hosting guide); the cache lives in `<distDir>/cache/images` (persist it across deploys/containers) and there is no mechanism to invalidate it, so keep `minimumCacheTTL` low or change the `src`. Hosted platforms may bill for optimisation; check your host's pricing. Options: a `loader`/`loaderFile` that builds URLs for Cloudinary/imgix/Cloudflare Images, or `unoptimized: true` for already-optimised assets (SVG icons should usually be `unoptimized` or plain `<img>`; SVG optimisation is blocked unless `dangerouslyAllowSVG`).

## Verify
- [ ] Network panel: images served as AVIF/WebP at widths close to rendered size (DevTools shows intrinsic vs rendered).
- [ ] LCP image preloaded and not lazy (Lighthouse "LCP image was lazily loaded" absent).
- [ ] Requesting `/_next/image?url=https://other-site.com/x.jpg` fails (ran on 16.4.2: HTTP 400 with body `"url" parameter is not allowed`).
