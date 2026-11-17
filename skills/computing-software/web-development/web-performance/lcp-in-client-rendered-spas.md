---
id: computing-software.web-development.web-performance.lcp-in-client-rendered-spas
name: lcp-in-client-rendered-spas
category: computing-software
field: web-development
product: web-performance
tags: [client-side-rendering-lcp, spa-performance, lcp, ssr, prerendering]
level: advanced
status: docs-checked
description: "Improving LCP in client-rendered SPAs: why CSR delays LCP, SSR and prerendering options, shrinking the boot chain, and preloading data and LCP images."
sources:
  - https://web.dev/articles/optimize-lcp
  - https://web.dev/articles/rendering-on-the-web
  - https://developer.chrome.com/docs/web-platform/soft-navigations-experiment
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# LCP in client-rendered single-page apps

In a CSR app the HTML is an empty `<div id="root">`. LCP waits for: HTML -> JS bundle download -> parse/execute -> API fetch -> render -> image discovery and download. Each step is serial, which delays LCP.

## 1. Biggest wins, in order
1. **Render HTML on the server or at build time** for landing pages: SSR (Next.js, Remix/React Router, Nuxt, SvelteKit) or static prerendering puts the LCP element in the initial HTML.
2. If staying CSR, **ship an app shell with the above-the-fold markup** in `index.html` (hero text and image) that the app hydrates or replaces.
3. **Cut the boot chain**: route-level code splitting, remove heavy dependencies from the entry chunk, `modulepreload` the route chunk.

## 2. Parallelise data and images
```html
<link rel="preload" as="fetch" href="/api/home" crossorigin>          <!-- start API call with the HTML -->
<link rel="preload" as="image" href="/hero-800.avif" fetchpriority="high"
      imagesrcset="/hero-400.avif 400w, /hero-800.avif 800w" imagesizes="100vw">
```
- Fetch data in the route loader, not in a `useEffect` after the component mounts (render-then-fetch waterfall).
- If the LCP image URL comes from the API, it can't be discovered by the preload scanner: return it in the HTML (server-inject a preload) or use a predictable URL.
- `fetchpriority="high"` on the rendered LCP `<img>`; never `loading="lazy"` on it.

## 3. Avoid self-inflicted delays
- Loading spinners/skeletons that wait for all data before showing anything: render the hero first.
- Auth checks that block the whole tree: render public parts immediately.
- Large CSS-in-JS runtimes injecting styles at runtime: extract static CSS.

## 4. Measuring SPAs
- Chrome has launched APIs for measuring soft navigations (client-side route changes) and experimental soft-navigation metrics in CrUX; see the Chrome Soft Navigations page for current status.
- Test on throttled mobile devices or emulation, not only on a fast desktop.

## Verify
- [ ] LCP element present in the initial HTML (view-source) for key landing routes, or its image preloaded from HTML; LCP p75 under 2.5 s in field data.

## Checked

2026-10-28. Confirmed from web.dev Optimize LCP (good LCP is 2.5 seconds or less at the 75th percentile; lazy-loaders hide image URLs from the preload scanner) and the Chrome Soft Navigations page (soft-navigation APIs and experimental CrUX metrics). Removed (not found): the 3-6 s range, named prerender tools, the claim that CrUX ignores route changes, and the 4x CPU / Fast 4G throttle values.

Method: documentation only; no commands were run.
