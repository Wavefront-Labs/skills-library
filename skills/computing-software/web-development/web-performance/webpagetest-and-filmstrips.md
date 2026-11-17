---
id: computing-software.web-development.web-performance.webpagetest-and-filmstrips
name: webpagetest-and-filmstrips
category: computing-software
field: web-development
product: web-performance
tags: [performance-measurement, webpagetest, filmstrip, waterfall, synthetic-testing]
level: practitioner
status: draft
description: "Using WebPageTest for synthetic performance testing: test locations and connection profiles, reading waterfalls and filmstrips, repeat views, scripting, and experiments."
sources:
  - https://docs.webpagetest.org/
  - https://docs.webpagetest.org/scripting/
  - https://www.webpagetest.org/
  - https://web.dev/articles/lab-and-field-data-differences
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# WebPageTest and filmstrips

WebPageTest runs real browsers on real devices/locations with traffic shaping - more realistic than Lighthouse in your laptop's DevTools, with richer visuals.

## 1. Configure a test
- **Location** near your users; **browser/device**: Chrome on a Moto G (mid-range Android) is the representative mobile default.
- **Connection**: 4G (9 Mbps, 170 ms RTT) or "3G Fast" for stress; packet-level shaping is more accurate than DevTools throttling.
- **Runs**: 3 or more; WPT picks the median run.
- **Repeat view**: tests caching (second visit).
- Options: block domains (measure third-party impact), custom headers/cookies, disable JS (no-JS baseline), capture video.

## 2. Read the waterfall
- Row per request: DNS (teal), connect (orange), TLS (purple), TTFB (light), download (dark). Vertical lines: start render (green), LCP, DOMContentLoaded, onload.
- Look for: long chains (request discovered late - CSS -> font -> image), render-blocking resources before start render (orange "blocking" icon), many connections to different origins, large images, redirects, third-party scripts on the critical path.
- Request details show priority, HTTP version, protocol (h2/h3) and compression.

## 3. Filmstrip and video
Filmstrip at 100 ms intervals shows what users actually see: blank time, layout shifts (red highlight), hero image arrival, cookie banner timing. Compare two tests side by side ("Compare" view) to communicate before/after to stakeholders.

## 4. Scripting
```
logData 0
navigate https://shop.example.com/login
setValue name=email test@example.com
setValue name=password secret
submitForm id=login
logData 1
navigate https://shop.example.com/account
```
Measure logged-in or multi-step flows; `blockDomains`, `setCookie`, `exec` for JS.

## 5. Experiments (paid tier) and alternatives
"Opportunities & Experiments" let you test fixes (e.g., remove a render-blocking script, preload an image) without deploying. Self-host WPT private instances for CI, or use alternatives (DebugBear, SpeedCurve, Calibre) for monitoring over time.

## Verify
Filmstrip shows hero content visible earlier after changes; median-run LCP and start render improve across 3+ runs; compare view saved for the PR/report.
