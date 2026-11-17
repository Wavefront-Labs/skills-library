---
id: computing-software.web-development.web-performance.build-time-image-processing-with-sharp
name: build-time-image-processing-with-sharp
category: computing-software
field: web-development
product: web-performance
tags: [sharp-image, libvips, image-pipeline, avif-encoding, srcset-generation, image-optimization]
level: practitioner
status: verified
description: "Generating optimised responsive images at build or upload time with sharp: resizing, auto-orientation, AVIF/WebP encoding settings, srcset sets, metadata and caching."
sources:
  - https://sharp.pixelplumbing.com/api-resize
  - https://sharp.pixelplumbing.com/api-output
  - https://github.com/JonasKruckenberg/imagetools
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Build-time image processing with sharp

sharp (libvips) is fast and memory-light; Next.js Image, Astro and many CMSs use it underneath.

## 1. Script
```js
import sharp from "sharp";
import { glob } from "node:fs/promises";           // Node 22+; use fast-glob on older Node
const WIDTHS = [400, 800, 1200, 1600];
for await (const file of glob("src/images/**/*.{jpg,jpeg,png}")) {
  const base = sharp(file).rotate();                         // apply EXIF orientation, then metadata is stripped
  const meta = await base.metadata();                        // metadata() reports the UNROTATED size
  const srcW = meta.orientation >= 5 ? meta.height : meta.width;   // EXIF orientation 5-8 swaps width and height
  for (const w of WIDTHS.filter(w => w <= srcW)) {
    const img = base.clone().resize({ width: w, withoutEnlargement: true });
    await img.clone().avif({ quality: 50, effort: 4 }).toFile(out(file, w, "avif"));
    await img.clone().webp({ quality: 75 }).toFile(out(file, w, "webp"));
    await img.clone().jpeg({ quality: 78, mozjpeg: true }).toFile(out(file, w, "jpg"));
  }
}
```
- Output strips metadata by default (privacy, size); `.keepIccProfile()` / `.withMetadata()` when colour profiles matter.
- AVIF quality scales differently from JPEG: a starting point is AVIF 45-55 against JPEG 75-80 (a rule of thumb, not a guarantee; compare visually on your images); `effort` (0-9, default 4) trades encode time for size.
- `.rotate()` with no argument applies the EXIF orientation. Run on sharp 0.35.5: a 2000x1000 JPEG tagged orientation 6 reports `width: 2000` from `metadata()` but resizes to 800x1600, and `withoutEnlargement` capped a 3000 request at 1000 wide, so filtering widths by the unrotated width gives wrong or duplicate sizes for portrait photos.
- Never upscale; cap the largest width at what layouts need at 2x DPR.

## 2. Emit markup
```html
<picture>
  <source type="image/avif" srcset="/img/hero-400.avif 400w, /img/hero-800.avif 800w, /img/hero-1600.avif 1600w" sizes="(min-width: 60rem) 50vw, 100vw">
  <source type="image/webp" srcset="...">
  <img src="/img/hero-800.jpg" srcset="..." sizes="(min-width: 60rem) 50vw, 100vw" width="1600" height="900" alt="...">
</picture>
```
Vite: `vite-imagetools` (`import srcset from "./hero.jpg?w=400;800;1600&format=avif&as=srcset"`) does this at import time.

## 3. Operations
- Cache outputs keyed by source hash + settings; AVIF encoding of many large images is slow in CI.
- Limit concurrency on small CI machines (`sharp.concurrency(2)`); sharp prebuilt binaries cover common platforms, Alpine/musl and ARM need matching installs (`npm install --os=linux --libc=musl --cpu=x64 sharp` in cross builds).
- Upload pipelines: process asynchronously, also defend against decompression bombs (`limitInputPixels`, default 268402689 pixels; run: a smaller limit throws "Input image exceeds pixel limit").

## Verify
- [ ] Generated sizes match `sizes` usage (DevTools shows the chosen candidate); total image bytes per page drop versus originals.
