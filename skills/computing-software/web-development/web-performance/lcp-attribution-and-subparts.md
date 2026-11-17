---
id: computing-software.web-development.web-performance.lcp-attribution-and-subparts
name: lcp-attribution-and-subparts
category: computing-software
field: web-development
product: web-performance
tags: [lcp-attribution, lcp-subparts, lcp-element, web-vitals-attribution, rum, performance]
level: practitioner
status: docs-checked
description: "Identifying the LCP element and which subpart is slow (TTFB, load delay, load duration, render delay) using web-vitals attribution and lab tools."
sources:
  - https://web.dev/articles/optimize-lcp
  - https://github.com/GoogleChrome/web-vitals
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# LCP attribution and subparts

## 1. The four subparts
web.dev: every page load's LCP breaks into four subparts with no overlap or gap; together they add up to the full LCP time.

| Subpart | Meaning | Share on a well-optimized page |
|---|---|---|
| Time to First Byte | user starts loading the page until the first byte of the HTML response | ~40% |
| Resource load delay | TTFB until the browser starts loading the LCP resource (0 if none is needed, for example a system-font text node) | <10% |
| Resource load duration | time to load the LCP resource (0 if none) | ~40% |
| Element render delay | LCP resource finished loading until the element is fully rendered | <10% |

The shares are guidelines, not strict rules, and the page warns against converting them to absolute numbers; the subparts are only meaningful relative to each other. Optimize all four: speeding up one can merely shift the time to another (the page's example: a smaller image only moved time into render delay because the element stayed hidden until JavaScript loaded).

## 2. Field data
The web-vitals attribution build (`web-vitals/attribution`) exposes the subparts on `LCPAttribution`: `target` (selector of the LCP element), `url` (LCP image URL, unset for text), `timeToFirstByte`, `resourceLoadDelay`, `resourceLoadDuration`, `elementRenderDelay`, plus `navigationEntry`, `lcpResourceEntry` and `lcpEntry`. Metric objects carry `value` and `rating` (`good`, `needs-improvement`, `poor`).
```js
import { onLCP } from "web-vitals/attribution";
onLCP(({ value, rating, attribution: a }) => send({
  value, rating, target: a.target, url: a.url,
  ttfb: a.timeToFirstByte, loadDelay: a.resourceLoadDelay,
  loadDuration: a.resourceLoadDuration, renderDelay: a.elementRenderDelay,
}));
```
(`send` is your own reporting function.)

## 3. Lab
- PageSpeed Insights shows CrUX field data (URL and origin level, by device type) and Lighthouse's "Largest Contentful Paint element" diagnostic with the breakdown. If Lighthouse and CrUX disagree, web.dev says CrUX likely reflects user experience better.
- Chrome DevTools and Lighthouse measure the subparts; WebPageTest or DevTools can identify the LCP element, which you then match to its request in the network waterfall.

## 4. Fix by subpart (web.dev order: biggest impact first)
- **Load delay**: the LCP resource should start loading at the same time as the first resource the page loads. Make it discoverable in the initial HTML (not JS-inserted, not `data-src`, not an un-preloaded CSS background), never `loading="lazy"` on it, `fetchpriority="high"` on likely LCP images (no more than one or two), preload with a high fetch priority when it is only referenced from CSS or JS, and prefer the same origin as the HTML.
- **Render delay**: remove what blocks rendering after the resource arrives: large stylesheets (inline small ones; otherwise shrink, remove unused CSS, defer non-critical CSS), synchronous scripts in the head, an LCP element not yet in the DOM, an A/B-testing library hiding it, long main-thread tasks. Server-side rendering or prerendering makes images discoverable from the HTML at the cost of extra server time.
- **Load duration**: smaller resource, closer to the user (CDN), less bandwidth contention, or no network (cache). web.dev notes that load duration is usually not a significant bottleneck for most sites.
- **TTFB**: minimise redirects and make sure a CDN edge can serve cached HTML (unique URL parameters used for analytics can defeat this).

## Verify
- [ ] RUM data shows which subpart dominates for the page; the fix targets that subpart rather than the usual one.

## Checked
2026-11-09. Read "Optimize Largest Contentful Paint" in full and the web-vitals README's `LCPAttribution` and attribution-build sections (searched, not read end to end). Removed (not on those pages): the `LCP by phase` insight name, WebPageTest filmstrip, p75 aggregation by template, mobile versus desktop LCP element claim, Early Hints, image CDN format advice beyond what is stated, and font-display advice. The cited DevTools overview page was dropped as a source because it does not describe the subpart breakdown.
Method: documentation only; no commands were run.
