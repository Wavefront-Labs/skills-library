---
id: computing-software.web-development.sveltekit.sveltekit-enhanced-img
name: sveltekit-enhanced-img
category: computing-software
field: web-development
product: sveltekit
tags: [sveltekit, images, enhanced-img, avif, srcset, cdn, lcp]
level: practitioner
status: docs-checked
description: "Optimize SvelteKit images with Vite asset imports, the @sveltejs/enhanced-img plugin (setup, sizes, widths, transforms), or a CDN for runtime images."
sources:
  - https://github.com/sveltejs/kit/blob/main/documentation/docs/40-best-practices/07-images.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SvelteKit images

Goals: modern formats (`avif`, `webp`), multiple sizes, effective caching.

## Option 1: Vite asset imports

Imported assets get hashed filenames; those under `assetsInlineLimit` are inlined. CSS `url()` is processed too.

```svelte
<script>
	import logo from '#lib/assets/logo.png';
</script>

<img alt="The project logo" src={logo} />
```

## Option 2: @sveltejs/enhanced-img

Build-time only: it processes files on your machine, not remote images. It adds `width`/`height`, generates multiple sizes and formats, and strips EXIF data.

```sh
npm i -D @sveltejs/enhanced-img
```

```js
import { enhancedImages } from '@sveltejs/enhanced-img';
import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vite';

export default defineConfig({
	plugins: [
		enhancedImages(), // must come before the SvelteKit plugin
		sveltekit({/* ... */})
	]
});
```

First build is slow; output is cached in `./node_modules/.cache/imagetools`.

Use `<enhanced:img src="./path/to/your/image.jpg" alt="An alt text" />`. It becomes an `<img>` inside a `<picture>`. Provide the highest resolution you need (about 2x display size); it only downscales. In a `<style>` block write the tag selector as `enhanced\:img`.

Dynamic choice: `import MyImage from './image.jpg?enhanced'` then `<enhanced:img src={MyImage} .../>`, or `import.meta.glob(..., { eager: true, query: { enhanced: true } })` and use `module.default`. SVG is supported only statically.

Dimensions: `width` and `height` are inferred. To size with CSS, set the other to `auto` (e.g. `width: var(--size); height: auto;`).

Sizes: for large images add `sizes`, e.g. `sizes="min(1280px, 100vw)"`. Smallest auto-generated width is 540px. Custom widths: `src="./image.png?w=1280;640;400"` with a matching `sizes`. Without `sizes`, a standard and a HiDPI version are generated.

Transforms via query string, e.g. `image.jpg?blur=15`; the full directive list is in the imagetools repo.

## Option 3: CDN for runtime images

For images not available at build time (CMS, database). A CDN can serve the right format from a plain `<img>` based on `User-Agent`, but may add setup and cost, require a 304 revalidation, and lazily generate images (slow for low-traffic sites). Libraries: `@unpic/svelte` (CDN-agnostic), Cloudinary's Svelte support, or CMS built-ins.

## Best practices

- Mix all three approaches as fits.
- LCP image: `fetchpriority="high"`, no `loading="lazy"`.
- Constrain images to avoid layout shift (CLS).
- Always write meaningful `alt`; Svelte warns if missing.
- Do not use `em`/`rem` in `sizes`, and do not change root font size (e.g. `html { font-size: 62.5%; }`), because the browser preloader's slot will differ from the real layout.

## Checked

2026-11-07. Read in full from the sveltejs/kit docs source (including inline snippets; the pages have no external include files): `40-best-practices/07-images.md`. Every remaining claim, name, default and option was compared line by line with that text. Removed or reworded: nothing; every claim matched the pages.

Method: documentation only; no commands were run.
