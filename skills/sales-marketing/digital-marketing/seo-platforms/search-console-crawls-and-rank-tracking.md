---
id: sales-marketing.digital-marketing.seo-platforms.search-console-crawls-and-rank-tracking
name: search-console-crawls-and-rank-tracking
category: sales-marketing
field: digital-marketing
product: seo-platforms
tags: [seo-platforms, seo-tools, google-search-console, gsc, performance-report, page-indexing-report, url-inspection, sitemaps, screaming-frog, seo-spider, site-crawl, ahrefs, semrush, keyword-explorer, site-explorer, backlink-audit, rank-tracking, position-tracking, content-gap, competitor-analysis, site-audit, core-web-vitals-report, bing-webmaster-tools]
level: practitioner
status: draft
description: "Use the SEO tool stack: Google Search Console performance and indexing diagnostics, Screaming Frog crawls, and Ahrefs/Semrush for keyword research, competitor gaps, backlinks and rank tracking."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# SEO platforms — Search Console, Screaming Frog, Ahrefs/Semrush

**Goal:** use each tool for what it's best at: Search Console for Google's own data,
a crawler for your site's technical state, and a third-party suite for keywords,
competitors and links. Strategy lives in
`sales-marketing.digital-marketing.seo.keyword-intent-on-page-and-technical-seo`.

Menus and report names change; the routines below match these tools as commonly
used in 2025–26 — confirm in each product's documentation.

## 1. Google Search Console (GSC) — ground truth from Google
Setup: add a **Domain property** (DNS TXT verification covers all subdomains and
protocols); submit your XML sitemap under *Sitemaps*. Add Bing Webmaster Tools too —
it can import GSC settings.

Weekly routine:
- **Performance report:** clicks, impressions, CTR, average position by query and page.
  Filter to a page to see its queries; compare date ranges (28 days vs previous).
  Pages with high impressions and low CTR → rewrite titles/descriptions. Queries ranking
  at positions ~5–15 → candidates for content improvement.
- **Pages (indexing) report:** read the "why pages aren't indexed" reasons. Prioritise
  important URLs showing "Crawled – currently not indexed", "Duplicate without
  user-selected canonical", or accidental "Excluded by noindex tag".
- **URL Inspection:** check a single URL's indexed status, Google-selected canonical,
  and live test rendering; request indexing after fixing a key page.
- **Core Web Vitals** and **Manual actions / Security issues** checked monthly.
GSC data is sampled/thresholded for privacy and arrives with a couple of days' delay.

## 2. Screaming Frog SEO Spider — crawl your site
- Free version crawls up to 500 URLs; paid licence removes the limit and adds features.
- Crawl: enter the domain → Start. For JS-heavy sites set *Configuration › Spider ›
  Rendering* to JavaScript.
- Connect GSC/GA4 APIs (*Configuration › API Access*) to overlay clicks and sessions.
- Check tabs: **Response Codes** (4xx, 5xx, redirect chains), **Page Titles/Meta
  Description/H1** (missing, duplicate, too long), **Canonicals**, **Directives**
  (noindex), **Images** (missing alt, oversized), **Internal** (orphan pages need a
  sitemap/GA crawl source).
- Export issues via *Reports* or bulk export to a spreadsheet and assign fixes.
- Save crawls and compare before/after a release or migration (crawl comparison in paid version).

## 3. Ahrefs / Semrush — market data
These estimate third-party data (volumes, traffic, links) from their own crawlers and
clickstream panels — directionally useful, not exact.
- **Keyword research:** Keywords Explorer (Ahrefs) / Keyword Magic Tool (Semrush): volume,
  difficulty, SERP features, parent topic, questions. Export to the keyword map.
- **Competitor gap:** Content Gap (Ahrefs) / Keyword Gap (Semrush): keywords competitors
  rank for and you don't.
- **Backlinks:** Site Explorer / Backlink Analytics: referring domains growth, new/lost
  links, top-linked pages; Link Intersect / Backlink Gap for prospects linking to
  competitors.
- **Site audit:** cloud crawl alternative to Screaming Frog, schedulable.
- **Rank tracking:** Rank Tracker / Position Tracking — set target keywords, location,
  device; tag by page or topic; weekly report on movement and share of voice.

## 4. Monthly SEO report
Organic clicks and conversions (GSC + analytics), top gaining/losing pages, indexing
issues fixed/open, technical crawl issue counts, new referring domains, rank-tracking
share of voice. List actions for next month.

## Gotchas
- Average position in GSC is impression-weighted; a page ranking for many low terms looks worse.
- Third-party volumes can differ greatly from GSC impressions; trust GSC for your site.
- Crawling a large site at high speed can strain the server; throttle threads/speed.
- "Site health" scores are tool-specific; fix what affects important pages, not the score.

## Verify
- [ ] GSC domain property verified; sitemap submitted and read successfully.
- [ ] Indexing report reviewed; important URLs indexed with the right canonical.
- [ ] Full crawl done; 4xx/5xx, redirect chains, duplicate titles assigned for fixing.
- [ ] Competitor gap and backlink gap exported into the keyword map and outreach list.
- [ ] Rank tracking configured with correct location and device.
