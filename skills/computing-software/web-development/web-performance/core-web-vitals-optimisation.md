---
id: computing-software.web-development.web-performance.core-web-vitals-optimisation
name: core-web-vitals-optimisation
category: computing-software
field: web-development
product: web-performance
tags: [web-performance, performance, core-web-vitals, cwv, lcp, largest-contentful-paint, inp, interaction-to-next-paint, cls, cumulative-layout-shift, ttfb, crux, pagespeed-insights, lighthouse, web-vitals, rum, field-data, lab-data, fetchpriority, preload, preconnect, avif, webp, responsive-images, font-display, code-splitting, long-tasks, cache-control, cdn, bfcache, seo, web-development, lcp-subparts]
level: practitioner
description: "Improving Core Web Vitals (LCP, INP, CLS at p75): field vs lab data, CrUX, web-vitals lib, fetchpriority, preload, images, fonts, long tasks, code splitting, caching."
sources:
  - https://web.dev/articles/vitals
  - https://web.dev/articles/optimize-lcp
  - https://web.dev/articles/optimize-inp
  - https://web.dev/articles/optimize-cls
  - https://github.com/GoogleChrome/web-vitals
licence: Apache-2.0
status: docs-checked
version: 4
updated: 2026-11-17
---

# Core Web Vitals optimisation — measure in the field, fix the biggest sub-part

**Goal:** get each page template to "good" on all three Core Web Vitals at the 75th
percentile of real users, mobile and desktop separately.

## 1. Targets
| Metric | Good | Measures |
|---|---|---|
| LCP Largest Contentful Paint | within 2.5 s | loading of the main content |
| INP Interaction to Next Paint | 200 ms or less | responsiveness |
| CLS Cumulative Layout Shift | 0.1 or less | visual stability |

INP became a stable Core Web Vital in 2024, replacing FID. A page "passes" when it meets the targets at the 75th percentile for all three, segmented by mobile and desktop.

## 2. Field data first, lab data to debug
- **Field (real users):** CrUX via PageSpeed Insights (top panel), Search Console's Core Web Vitals report, or your own RUM. Fixes take time to show in CrUX; PageSpeed Insights can show page-level and origin-level CrUX data.
- **Lab:** Lighthouse and the DevTools Performance panel — reproducible, but a single device and network.
- **Your own RUM** with the `web-vitals` library, using the attribution build to learn *why*:
```js
import { onLCP, onINP, onCLS } from 'web-vitals/attribution';
const send = (m) => navigator.sendBeacon('/rum', JSON.stringify({
  name: m.name, value: m.value, rating: m.rating, page: location.pathname, attr: m.attribution }));
onLCP(send); onINP(send); onCLS(send);
```
Group by template and device; optimise the worst p75 with the most traffic first.

## 3. LCP: split it into four sub-parts
LCP = TTFB + resource load delay + resource load duration + element render delay.
- **TTFB:** CDN, cache HTML where possible, avoid redirect chains.
- **Load delay:** the LCP image must be discoverable in the HTML — not a CSS background, not injected by JS, never `loading="lazy"`.
```html
<img src="hero-1200.avif" srcset="hero-800.avif 800w, hero-1200.avif 1200w, hero-1800.avif 1800w"
     sizes="100vw" width="1200" height="600" fetchpriority="high" alt="…">
<link rel="preload" as="image" href="hero.avif" fetchpriority="high">  <!-- only if not in the HTML -->
<link rel="preconnect" href="https://cdn.example.com" crossorigin>
```
- **Load duration:** AVIF or WebP, correctly sized via `srcset`/`sizes`, compressed.
- **Render delay:** render-blocking CSS/JS in `<head>`, client-side rendering of the main content, A/B testing scripts that hide the page. `defer` scripts; inline critical CSS for large stylesheets.

## 4. INP: keep the main thread free
INP = input delay + processing time + presentation delay. Long tasks on the main thread extend input delay.
- Find them: DevTools Performance with CPU 4× slowdown, or `web-vitals` attribution (`longAnimationFrameEntries`, target selector).
- Do the visible update first, defer the rest: break up long tasks with `setTimeout`, which runs its callback in a new task.
- Ship less JS: route-level code splitting, remove unused dependencies, audit third-party tags (chat, analytics, tag managers often dominate).
- Avoid very large DOMs, which make rendering work grow, and layout thrashing in handlers.
- Debounce input handlers that do heavy filtering, or move the work to a Web Worker.

## 5. CLS: reserve space
- Always set `width`/`height` (or `aspect-ratio`) on images, video and iframes; never lazy-load the LCP image.
- Reserve slots for ads, embeds and cookie banners with `min-height`; banners should overlay, not push content.
- Insert late content below the viewport, or in response to user input (shifts within 500 ms of input don't count).
- Fonts: minimise differences between fallback and web font with `size-adjust`, `ascent-override`, `descent-override` and `line-gap-override`; preload the one or two critical WOFF2 files.
- Animate with `transform`, not `top`/`height`.

## Verify
- [ ] Field p75 (CrUX or RUM) is good for LCP, INP and CLS on mobile for each key template.
- [ ] LCP element is in the initial HTML, not lazy-loaded, has `fetchpriority="high"`, and is correctly sized.
- [ ] No long tasks in the main interactions under CPU throttling.
- [ ] Every image/iframe/ad slot has reserved dimensions; Layout Shift regions show nothing unexpected.
- [ ] RUM dashboard alerts on regression per template.

## Checked
2026-10-31. Confirmed against web.dev vitals, optimize-lcp, optimize-inp and optimize-cls: 2.5 s, 200 ms and 0.1 targets, p75 by device, the four LCP subparts, fetchpriority and never lazy-loading the LCP image, 500 ms input grace for CLS, size-adjust/ascent-override/descent-override/line-gap-override, INP stable in 2024 replacing FID. Removed: poor thresholds, 28-day CrUX window, TTFB and image-size figures, 50 ms long-task and DOM node counts, scheduler.yield, bfcache and caching-header section.
Method: documentation only; no commands were run.
