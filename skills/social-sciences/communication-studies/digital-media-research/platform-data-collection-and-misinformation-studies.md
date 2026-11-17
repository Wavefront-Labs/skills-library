---
id: social-sciences.communication-studies.digital-media-research.platform-data-collection-and-misinformation-studies
name: platform-data-collection-and-misinformation-studies
category: social-sciences
field: communication-studies
product: digital-media-research
tags: [digital-media-research, social-media-research, computational-social-science, platform-data, research-api, tiktok-research-api, meta-content-library, crowdtangle, youtube-data-api, reddit-api, x-api, bluesky, mastodon, dsa-article-40, digital-services-act, web-scraping, terms-of-service, data-donation, gdpr, sampling-bias, virality, information-cascades, cascade-size, structural-virality, misinformation, fact-checking, source-credibility-ratings, newsguard, coordinated-inauthentic-behaviour, bots, aoir-ethics]
level: advanced
status: draft
description: "Collecting and analysing platform data ethically: research APIs, DSA access, scraping and data donation, sampling bias, cascade/virality metrics and misinformation labelling."
sources: ["franzke et al., Internet Research: Ethical Guidelines 3.0 (AoIR, 2020)", "Goel, Anderson, Hofman & Watts, 'The Structural Virality of Online Diffusion' (2016)", "Vosoughi, Roy & Aral, 'The Spread of True and False News Online' Science (2018)", "Lazer et al., 'The Science of Fake News' Science (2018)", "EU Digital Services Act (Regulation 2022/2065), Article 40", "Boeschoten et al., 'Digital Trace Data Collection through Data Donation' (2022)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Platform data collection and misinformation studies

**Goal:** gather digital-platform data you're allowed to use, know what it does and
doesn't represent, and measure spread and misinformation without the common errors.

## 1. Routes to data (check current terms — this landscape changes yearly)
- **Platform research APIs:** e.g. the TikTok Research API, YouTube Data API, the
  Meta Content Library (successor to CrowdTangle, which Meta shut down in 2024),
  Reddit's API (heavily restricted since 2023; Pushshift no longer openly available).
  X/Twitter's API became paid in 2023, ending most free academic access. Open
  protocols (**Bluesky** firehose, **Mastodon** instance APIs) are comparatively open.
  *Access tiers, quotas and eligibility change often — verify before planning.*
- **EU Digital Services Act, Article 40:** vetted researchers can request data from
  very large platforms on systemic risks; a delegated act sets the procedure via
  national Digital Services Coordinators. *Implementation status is evolving — check.*
- **Scraping:** may breach terms of service and, in some jurisdictions, laws on
  computer access or databases; personal data falls under GDPR in the EU. Get legal/
  ethics advice; respect robots.txt and rate limits; collect the minimum.
- **Data donation:** participants download their own platform data (GDPR access
  rights) and donate selected parts through a tool (e.g. Port/OSD2F-style software)
  that filters locally — strong consent, linkable to surveys.
- **Browser/app tracking panels** for exposure (see media-effects skill
  social-sciences.communication-studies.media-effects-research.framing-agenda-setting-and-exposure-measurement).

## 2. Sampling and representativeness
- Platform users ≠ population; posters ≠ users (a small share produces most content).
- Keyword/hashtag queries miss relevant posts and capture irrelevant ones — report
  query, time window and precision on a hand-checked sample.
- APIs return what platforms choose; deleted/suspended content disappears (decay),
  biasing retrospective collection. Collect in near-real-time for live events.
- Record collection timestamps and API versions for reproducibility.

## 3. Virality and diffusion
- Reconstruct **cascades** (reshare trees) where platforms expose parent links.
- Measures: **cascade size**, depth, breadth, and **structural virality** (average path
  distance in the tree: distinguishes one broadcast from many person-to-person hops).
- Gotcha: popular ≠ viral; most large cascades are broadcasts from big accounts.
  Control for follower counts and algorithmic amplification (unobserved).

## 4. Misinformation research
- Define the unit: claim-level (fact-checked false claims) vs **source-level**
  (domains rated low-credibility by fact-checker lists or services like NewsGuard).
  Source-level is scalable but misclassifies individual items.
- Fact-check corpora are selective (what fact-checkers chose to check).
- Detect **coordinated inauthentic behaviour** via synchronised posting, shared links
  and account creation patterns; bot classifiers have high error rates — validate
  manually and avoid labelling individual accounts publicly as bots without strong evidence.
- Exposure vs sharing vs belief are different outcomes; most people see little
  misinformation while a small, older, more partisan group shares most of it (in US
  studies — generalisation uncertain).

## 5. Ethics (AoIR guidelines)
Public ≠ fair game: users rarely expect research use. Paraphrase or alter quotes from
small/vulnerable communities (verbatim text is searchable), don't publish handles of
private individuals, secure storage, and consider harms to researchers studying toxic
content.

## Verify
- [ ] Data access route complies with current platform terms and law; documented.
- [ ] Query, timeframe, collection time and API version recorded; precision checked.
- [ ] Representativeness limits stated (users, posters, deletions).
- [ ] Virality measures distinguish broadcast from structural spread.
- [ ] Misinformation unit (claim vs source) defined; quotes de-identified where needed.
