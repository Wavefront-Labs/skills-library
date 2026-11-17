---
id: computing-software.web-development.sveltekit.sveltekit-performance-tuning
name: sveltekit-performance-tuning
category: computing-software
field: web-development
product: sveltekit
tags: [sveltekit, performance, fonts, waterfalls, preload, streaming, icons]
level: practitioner
status: docs-checked
description: "Diagnose and improve SvelteKit app speed: preload fonts, trim bundles and third-party scripts, avoid request waterfalls, stream slow data, and choose icon libraries."
sources:
  - https://github.com/sveltejs/kit/blob/main/documentation/docs/40-best-practices/05-performance.md
  - https://github.com/sveltejs/kit/blob/main/documentation/docs/40-best-practices/06-icons.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SvelteKit performance tuning

SvelteKit already does code-splitting, asset preloading, file hashing, request coalescing, parallel universal `load`, data inlining of server `fetch`, conservative invalidation, per-route prerendering and link preloading. These are the remaining levers.

## Diagnose

Use PageSpeed Insights or WebPageTest for deployed sites, plus browser devtools (Lighthouse, Network, Performance). Dev mode behaves differently from production, so test in preview mode after building. For slow API calls, instrument the backend with OpenTelemetry or `Server-Timing` headers.

## Assets

- Images: biggest win usually; see `@sveltejs/enhanced-img`.
- Video: compress (e.g. Handbrake) to `.webm`/`.mp4`, use `preload="none"` for below-the-fold videos (slows playback start), strip audio from muted videos with FFmpeg.
- Fonts are not preloaded by default. Preload selectively in `handle`:

```js
export async function handle({ event, resolve }) {
	return resolve(event, {
		preload: (asset) => {
			if (asset.type === 'font') {
				return asset.filename === 'node_modules/@fontsource/inter/files/inter-latin-400-normal.woff2';
			}
			return true;
		}
	});
}
```

`filename` is relative to the project root and exists only for fonts. Subset fonts to shrink them.

## Code size

Run the latest Svelte. Find heavy packages with `rollup-plugin-visualizer`; temporarily set `build: { minify: false }` to read output (undo before deploying). Minimize third-party scripts: prefer server-side analytics from your platform, or run scripts in a web worker via Partytown. Use dynamic `import(...)` for code needed only conditionally.

## Navigation and data

- Link preloading is set on `<body>` in new apps via link options.
- Return promises from `load` for non-essential data; server `load` streams them in.
- Avoid waterfalls: check the Network tab for resources needing preload (fonts especially). SPA mode creates a waterfall (empty page, then JS, then render). Make dependent backend calls from server `load` rather than the browser, and prefer one database join over sequential queries.

## Hosting

Colocate frontend and backend, or deploy to the edge (some adapters support per-route config). Serve images via CDN. Use HTTP/2 or newer, since Vite emits many small files.

## Icons

Prefer CSS-based icons (Iconify, with Tailwind or UnoCSS plugins), which need no per-icon import. If using a Svelte icon library, avoid ones shipping one `.svelte` file per icon: thousands of files slow Vite's dependency optimization, worst when imported both via umbrella and subpath imports.

## Checked

Checked 2026-11-07.

Method: documentation only; no commands were run.

Read 40-best-practices/05-performance.md and 06-icons.md in full; every bullet matched. No claims trimmed.
