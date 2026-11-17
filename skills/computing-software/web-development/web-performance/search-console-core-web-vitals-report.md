---
id: computing-software.web-development.web-performance.search-console-core-web-vitals-report
name: search-console-core-web-vitals-report
category: computing-software
field: web-development
product: web-performance
tags: [search-console-cwv, google-search-console, crux, core-web-vitals, field-data]
level: intro
status: docs-checked
description: "Using the Search Console Core Web Vitals report: URL groups, mobile vs desktop, statuses, validating fixes, the 28-day window and relating it to CrUX and RUM."
sources:
  - https://support.google.com/webmasters/answer/9205520
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Search Console Core Web Vitals report

## 1. What it shows
- Field data from the Chrome UX Report (CrUX), split by **Mobile** and **Desktop**.
- URLs are grouped by similar user experience; the group's status is the 75th-percentile LCP, INP and CLS over the last 28 days. A group without enough data is replaced by a higher-level origin group (protocol://host:port).
- Status per URL group and device: Good, Need improvement, Poor. It defaults to the slowest status of the three metrics, so one poor metric makes the group Poor.
- Thresholds: LCP 2.5 s / 4 s, INP 200 ms / 500 ms, CLS 0.1 / 0.25 (good / poor boundaries).

## 2. Working the report
1. Open the Core Web Vitals report and start with the device type that has more poor URLs.
2. Click an issue to see example URL groups (the examples table is limited to 200 rows).
3. Open an example URL in PageSpeed Insights for a lab run. PSI shows data for individual URLs and strips URL parameters, so it can differ from the group result.
4. Fix the template, deploy, then click **Validate fix**. Validation runs a 28-day monitoring session; the issue counts as fixed if no instances appear in that window.

## 3. Caveats
- 28-day rolling window: fixes take up to ~4 weeks to show; regressions too.
- Low-traffic sites may have "Not enough data" - use your own RUM.
- Groups can mix fast and slow URLs (an outlier URL may differ from its group); inspect individual URLs in PSI if the group seems wrong.
- The report is for site-wide troubleshooting, not for finding the status of one specific URL.

## 4. Pair it with
- CrUX Vis / CrUX API / BigQuery for history and origin-level trends.
- RUM (web-vitals library) for immediate feedback after deploys and for attribution.

## Checked
2026-10-31. Confirmed against the Search Console Core Web Vitals report help page: CrUX data source, mobile/desktop split, thresholds (LCP 2.5 s / 4 s, INP 200 / 500 ms, CLS 0.1 / 0.25), group status defaulting to the slowest metric, 75th percentile over 28 days, origin-group fallback, 28-day validation, PSI differences. Removed: opt-in/Chrome-only/public-pages claims, ranking-signal claim, menu path and issue-title quote (not on the page).
Method: documentation only; no commands were run.

## Verify
- [ ] Mobile and desktop reviewed monthly; each poor group mapped to a template and owner; validation started after fixes and tracked to completion.
