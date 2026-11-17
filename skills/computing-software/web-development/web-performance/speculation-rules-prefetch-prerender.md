---
id: computing-software.web-development.web-performance.speculation-rules-prefetch-prerender
name: speculation-rules-prefetch-prerender
category: computing-software
field: web-development
product: web-performance
tags: [critical-rendering-path, resource-hints, speculation-rules, prerender, prefetch, instant-navigation, document-rules, eagerness]
level: practitioner
status: verified
description: "Making navigations near-instant with the Speculation Rules API: prefetch vs prerender, list and document rules, eagerness levels, and side-effect safety."
sources:
  - https://developer.chrome.com/docs/web-platform/prerender-pages
  - https://developer.mozilla.org/en-US/docs/Web/API/Speculation_Rules_API
  - https://web.dev/learn/performance/prefetching-prerendering-precaching
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Speculation Rules: prefetch and prerender

**Goal:** the next page loads before the user clicks, for multi-page sites (MPAs) without a client router.

## 1. Rules
```html
<script type="speculationrules">
{
  "prerender": [{
    "where": { "and": [ { "href_matches": "/*" },
                        { "not": { "href_matches": ["/logout", "/cart/*", "/*\\?*"] } },
                        { "not": { "selector_matches": "[data-no-prerender]" } } ] },
    "eagerness": "moderate"
  }],
  "prefetch": [{ "urls": ["/pricing"], "eagerness": "eager" }]
}
</script>
```
- **prefetch**: fetches the document only (no subresources, no JS execution). Cheap.
- **prerender**: loads and renders the page in a hidden tab, running JS. Activation is instant but costs memory/CPU and bandwidth.
- **Eagerness** (Chrome docs): `immediate` (as soon as the rules are seen; the default for list rules), `eager` (since Chrome 143 on desktop: pointer held over the link for 10 ms; before that it behaved like `immediate`), `moderate` (hover 200 ms or pointerdown, whichever is first), `conservative` (pointer or touch down; the default for document rules). Run in Chromium: a `urls` list with `eager` did not fetch on load while `immediate` did, `moderate` fired on hover. `moderate` is a good default for document rules.
- Can be delivered via `Speculation-Rules` HTTP header pointing to a JSON file.

## 2. Safety
Prerendered pages run their JS before the user sees them:
- Exclude URLs with side effects (logout, add-to-cart GETs, one-time tokens).
- Defer analytics pageviews until activation:
```js
if (document.prerendering) document.addEventListener('prerenderingchange', sendPageview, { once: true });
else sendPageview();
```
- Server sees `Sec-Purpose: prefetch` for a speculation prefetch and `Sec-Purpose: prefetch;prerender` for a prerender (both seen in a Chromium run) - can skip expensive work or refuse: a non-2xx final response cancels the prerender or discards the prefetch (204/205 are also invalid for prerender).

## 3. Limits
Chromium-led: per MDN compat data Chrome 109+ (the `Speculation-Rules` header 121+), Safari 26.2 behind a preference with prefetch only, Firefox only a preview of URL-list prefetch; unsupported browsers ignore the script, so it is progressive enhancement. Chrome's limits: 50 prefetches and 10 prerenders for `immediate`, and 2 (FIFO) of each for `eager`/`moderate`/`conservative`; speculation is also blocked under Save-Data, Energy Saver on low battery, memory constraints and when the "Preload pages" setting is off. Prerender is same-origin by default; cross-origin prefetch only works when no cookies exist for that origin.

## 4. Measure
`performance.getEntriesByType('navigation')[0].activationStart > 0` means the page was prerendered; segment field metrics (LCP) by it. The DevTools Application panel has a view of speculation rules and their statuses (see Chrome's "Debugging speculation rules" guide). Note: Playwright and other CDP-attached sessions report `PrerenderingDisabledByDevTools`, so prerender activation cannot be reproduced in automation; prefetch can (run).

## Verify
- [ ] Hovering a link triggers prerender (Speculative loads panel), clicking is instant.
- [ ] Analytics counts only activated views.
- [ ] Excluded URLs never speculated (server logs with Sec-Purpose).
