---
id: media-communication.content-creation-and-audience-growth.editorial-seo.search-intent-and-evergreen-refresh
name: search-intent-and-evergreen-refresh
category: media-communication
field: content-creation-and-audience-growth
product: editorial-seo
tags: [editorial-seo, seo, search-intent, keyword-research, headlines, seo-headline, evergreen, content-refresh, google-search-console, structured-data, schema-org, newsarticle, topic-clusters, topical-authority, internal-linking, canonical, title-tag, meta-description, google-discover, top-stories, helpful-content, e-e-a-t]
level: practitioner
status: draft
description: "Make editorial content findable: match search intent, write SEO headlines that stay honest, refresh evergreen pieces from Search Console data, add NewsArticle schema and build topic clusters."
sources: ["https://developers.google.com/search/docs", "https://developers.google.com/search/docs/appearance/structured-data/article"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Search intent and evergreen refresh for editorial SEO

**Goal:** earn steady search traffic for journalism and editorial content without
writing for robots — by matching what searchers actually want, packaging it clearly,
and keeping the pieces that already rank fresh.

## 1. Read the intent before you write
Search the query yourself (logged out / private window) and look at page one:
- **Informational** ("what is a heat dome") → explainer.
- **News** ("heat dome warning today") → Top Stories carousel; speed and freshness win.
- **Navigational/transactional** ("buy fan") → editorial rarely wins; skip.
- **Format clues:** if page one is all lists, a 3,000-word essay won't rank; if there's a
  video carousel, consider one.
Note the **People also ask** box — those questions become subheads.

## 2. Headlines: one for people, one for search
- On-page H1 can be voicey; the **SEO title** (title tag, ~55–60 characters before
  truncation) should contain the plain-language phrase people type, early.
  e.g. H1 "The summer the grid nearly broke" / SEO title "Why the power grid failed
  in the 2026 heatwave — explained".
- Never promise in the title what the piece doesn't answer. Pogo-sticking back to results
  and reader distrust cost more than the click gained.
- Meta description: a 150-ish-character summary; Google often rewrites it, but it still
  shapes the snippet.
- Google's own guidance (helpful-content, E-E-A-T) rewards demonstrated first-hand
  expertise: bylines with real author pages, sourcing, dates.

## 3. Structure for the scanner (and the crawler)
- Answer the core question in the first 2–3 paragraphs.
- Descriptive H2s that match sub-questions; short paragraphs; a table if comparing.
- **Internal links** from related stories with descriptive anchor text ("how heat pumps
  work", not "click here"). A hub/explainer page linking to all coverage of a topic is a
  **topic cluster**; it signals depth.
- **Structured data:** `NewsArticle`/`Article` JSON-LD with headline, image,
  datePublished, dateModified, author (with url). Most CMS SEO plugins generate it —
  check it's correct rather than hand-writing.

## 4. The evergreen refresh loop (where most wins are)
Monthly, in **Google Search Console › Performance › Search results**:
1. Filter last 3 months vs previous 3; sort pages by impressions.
2. Flag pages with **high impressions, falling clicks or position 5–15** — close to page
   one, worth effort.
3. Open each: what queries does it get? (Queries tab for that page.) Add a section
   answering queries it ranks for but doesn't address.
4. Update facts, figures and links; add a visible "Updated <date>: what changed" note.
5. Update `dateModified` only for substantive changes. Bumping dates without real edits
   is a known manipulation pattern and erodes trust.
6. Keep the **same URL**. A new URL throws away accumulated signals.
Consolidate: two weak pieces on the same topic → merge into one, 301 the other.

## 5. News-specific notes
- Publish fast with a stable URL, then update it as the story develops (a live
  story URL accrues links), rather than five separate thin posts.
- Google Discover favours large, high-quality images (≥1200 px wide, with
  `max-image-preview:large` allowed) and compelling but non-clickbait titles.
- *Unconfirmed / changes often:* exact ranking weights for freshness and Top Stories
  eligibility. Watch Google Search Central announcements rather than SEO folklore.

## Gotchas
- Keyword stuffing and "SEO paragraphs" at the bottom of articles read badly and don't help.
- Accidental `noindex` on templates (common after a CMS migration) silently zeroes traffic.
- Paywalled content needs the paywall structured-data markup or it can look like cloaking.

## Verify
- [ ] Page one for the target query was checked and the piece's format matches it.
- [ ] SEO title ≤ ~60 chars and contains the searcher's phrase; it is truthful.
- [ ] Google's Rich Results Test validates the Article/NewsArticle markup.
- [ ] Refreshed pieces show a dated update note and the URL is unchanged.
- [ ] Search Console shows the page indexed (URL Inspection) after publishing.
