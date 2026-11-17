---
id: sales-marketing.digital-marketing.seo.keyword-intent-on-page-and-technical-seo
name: keyword-intent-on-page-and-technical-seo
category: sales-marketing
field: digital-marketing
product: seo
tags: [seo, search-engine-optimisation, search-engine-optimization, organic-search, keyword-research, search-intent, keyword-mapping, on-page-seo, title-tag, meta-description, h1, internal-linking, technical-seo, crawlability, indexability, robots-txt, xml-sitemap, canonical, core-web-vitals, structured-data, schema-org, link-building, digital-pr, content-strategy, topic-clusters, eeat]
level: practitioner
status: draft
description: "Earn organic search traffic that converts: keyword and intent research, keyword-to-page mapping, on-page optimisation, technical crawl/index checks, link earning and a topic-cluster content plan."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# SEO — intent, on-page, technical, links

**Goal:** rank for the searches your buyers actually make, with pages that answer them
better than the current results — and make sure search engines can crawl and index
those pages. Tooling is covered in
`sales-marketing.digital-marketing.seo-platforms.search-console-crawls-and-rank-tracking`.

## 1. Keyword and intent research
1. Seed list: your products, problems they solve, customer words from sales calls,
   support tickets and reviews, competitor page titles.
2. Expand with a keyword tool (Google Keyword Planner, Ahrefs, Semrush) for volume,
   difficulty, related terms and questions.
3. **Classify intent** by searching each keyword and looking at what ranks:
   informational (guides), commercial (comparisons, "best X"), transactional (product/
   category pages), navigational (brand). Match the page *type* that already ranks —
   Google is telling you what it thinks the intent is.
4. Prioritise by business value × achievable ranking × volume. Long-tail, high-intent
   terms usually pay first for newer sites.

## 2. Map keywords to pages
One primary keyword cluster per URL. A spreadsheet: URL | primary keyword | secondary
keywords | intent | status. Two pages targeting the same cluster compete
(cannibalisation) — merge or differentiate them.

## 3. On-page
- **Title tag:** primary keyword near the front, specific benefit, ~50–60 characters
  (display truncates by pixel width). Unique per page.
- **Meta description:** ~150–160 characters, a reason to click; not a ranking factor
  directly, but affects click-through. Google often rewrites it.
- **One H1** matching the page topic; logical H2/H3s covering sub-questions.
- Content that fully answers the query: cover what top results cover, then add what
  they lack (original data, examples, clearer steps). Show first-hand experience and
  author credentials (Google's E-E-A-T guidance).
- Descriptive URLs (`/blue-widgets/`), image alt text, **internal links** from related
  pages with descriptive anchor text.
- **Structured data** (schema.org Product, FAQ, Article, LocalBusiness) where it
  matches visible content; validate with Google's Rich Results Test.

## 4. Technical checks
- **Crawlable:** robots.txt doesn't block important paths; key content in HTML (or
  rendered reliably if JavaScript-driven).
- **Indexable:** no stray `noindex`; correct `rel="canonical"` on duplicates/variants
  (filters, tracking parameters).
- XML sitemap of canonical, indexable URLs submitted in Search Console.
- HTTPS, mobile-friendly, **Core Web Vitals** (LCP, INP, CLS) in good ranges.
- Fix broken internal links and redirect chains; use 301s for moved pages.

## 5. Earning links
Links from relevant, reputable sites still matter. Ways that work: original research
or data others cite, useful tools/calculators, digital PR (newsworthy stories pitched to
journalists), supplier/partner pages, unlinked brand mentions. Avoid buying links or
link schemes — they violate Google's spam policies and risk penalties.

## 6. Content strategy
Build **topic clusters**: a pillar page for a broad topic linking to detailed pages for
subtopics (and back). Publish to fill keyword gaps in priority order; update existing
pages before writing new ones on the same topic.

## Gotchas
- SEO results lag weeks to months; judge changes over a quarter, not days.
- Chasing volume over intent brings traffic that never buys.
- Site migrations without a redirect map can wipe out rankings.
- AI-generated pages at scale without real value fall under Google's scaled-content
  abuse policy; specifics of search ranking change frequently — check current guidance.

## Verify
- [ ] Each target keyword has intent classified by checking the live results page.
- [ ] Keyword-to-URL map with no two pages on the same cluster.
- [ ] Titles, H1s and meta descriptions unique and keyword-aligned.
- [ ] No important page blocked by robots.txt, noindex or a wrong canonical; sitemap submitted.
- [ ] Rankings, clicks and conversions from organic tracked per mapped page.
