---
id: computing-software.general-digital-literacy.internet-navigation.searching-and-evaluating-sources
name: searching-and-evaluating-sources
category: computing-software
field: general-digital-literacy
product: internet-navigation
tags: [internet-navigation, web-search, search-engines, google, bing, duckduckgo, search-operators, site-operator, filetype, exact-phrase, verbatim, lateral-reading, sift, source-evaluation, fact-checking, misinformation, reverse-image-search, google-lens, tineye, ai-overviews, online-forms, account-creation, two-factor-authentication, passkeys, scam-sites]
level: intro
status: docs-checked
description: "Find information fast with search operators, judge it with lateral reading (SIFT), check images and AI answers, and use online forms and accounts safely."
sources:
  - https://support.google.com/websearch/answer/2466433
  - https://hapgood.us/2019/06/19/sift-the-four-moves/
  - https://blog.google/products/ads-commerce/google-search-sponsored-results-label/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Searching and evaluating sources: find it, then decide whether to believe it

**Goal:** get to the right page in one or two searches, and spend a minute deciding whether that page deserves your trust before you act on it or share it.

## 1. Search like you mean it
Start with the **distinctive words** the answer page would contain, not a question: `dishwasher E24 error <brand>` beats `why is my dishwasher showing a code`.

Google operators (no space between operator and term):
| Operator | Example | Effect |
|---|---|---|
| `"..."` | `"error 0x80070005"` | exact phrase, essential for error messages |
| `-word` | `jaguar speed -car` | leave a word out |
| `site:` | `site:youtube.com cat videos` | one site or domain |
| `filetype:` | `photoelectric effect paper filetype:pdf` | one file type |
| `before:` / `after:` | `astronomy discoveries after:2026/03/10` | documents last updated before or after a date |

- Prefer recent results for software settings: an old answer is often wrong today. Use `after:` with a year.
- Google labels text ads "Sponsored results" and Shopping ads "Sponsored products" (announced 13 October 2025). For banks, government services and downloads, use the organic result or type the official address.

## 2. Evaluate with SIFT (about a minute)
SIFT is Mike Caulfield's four moves: Stop; Investigate the source; Find better coverage; Trace claims, quotes and media to the original context.
1. **Stop.** Notice a strong emotional reaction; that is when people share without checking.
2. **Investigate the source.** Know what you are reading before you read it: open a new tab and search the outlet or author ("lateral reading").
3. **Find better coverage.** Search the claim itself: do several independent, reputable outlets report it?
4. **Trace to the original.** Follow quotes, statistics and screenshots back to the study, statement or full video. Check the date and whether context was cut.

Quick red flags: lookalike domains, no author or date, anonymous "experts", pages pushing a product, statistics with no link to a source.

## 3. Images and AI answers
- Reverse-image search suspect photos (Google Lens supports searching with an image) to find earlier uses.
- AI summaries can be wrong or out of date. Open the cited sources and check they say what the summary claims; confirm health, money and legal questions with an official or professional source.

## Verify
- [ ] Error-message searches use the exact text in quotes plus the app or OS name.
- [ ] Before sharing a claim you checked who is behind the source (in a new tab) and found an independent confirmation.
- [ ] AI-generated answers were checked against their cited sources.

## Checked
Date: 2026-10-27. Documentation: Google Search Help "Refine Google searches"; Mike Caulfield, "SIFT (The Four Moves)"; Google blog on the Sponsored results label (13 Oct 2025). Confirmed: operator syntax and examples, before/after semantics, the four SIFT moves, current ad labels. Removed unconfirmed claims (Bing and DuckDuckGo support, `site:.edu`, OR, Verbatim and Tools date filter, `+word` removal, Lens right-click path, TinEye, and the online forms and accounts section including 2FA and passkey ranking, PDF save steps) and two prose-title sources.
Method: documentation only; no commands were run.
