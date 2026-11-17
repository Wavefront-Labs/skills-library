---
id: media-communication.media-relations-and-press-liaison.media-monitoring.monitoring-setup-coverage-reports-and-early-warning
name: monitoring-setup-coverage-reports-and-early-warning
category: media-communication
field: media-relations-and-press-liaison
product: media-monitoring
tags: [media-relations-and-press-liaison, media-monitoring, coverage-analysis, coverage-report, press-clippings, social-listening, boolean-search, keyword-alerts, google-alerts, share-of-voice, sov, sentiment-analysis, tone, message-pull-through, reach, ave, barcelona-principles, amec, early-warning, issues-management, crisis-detection, meltwater, cision, talkwalker, brandwatch]
level: practitioner
status: draft
description: "Track what's said about you: build Boolean monitoring queries, produce coverage reports with share of voice, tone and message pull-through, avoid AVE, and spot a story about to break."
sources:
  - "AMEC Barcelona Principles 3.0 and Integrated Evaluation Framework, paraphrased"
  - "Common PR measurement and media-monitoring practice, paraphrased"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Monitoring setup, coverage reports and early warning

**Goal:** you know about relevant coverage the same day (and about a brewing issue
before it peaks), and your reports show whether communications are achieving anything.

## 1. Build the monitoring query
Most platforms (Meltwater, Cision, Talkwalker, Brandwatch, or free Google Alerts for
basics) accept **Boolean** search. Pattern:
```
("Acme Health" OR "AcmeHealth" OR "@acmehealth" OR "Acme clinic")
AND (NHS OR hospital OR patient*)
NOT ("Acme Anvil" OR "Wile E")
```
- Include brand variants, misspellings, handles, product names, executives' names,
  campaign hashtags.
- **Exclude noise** (namesakes, stock-price spam) — review a week of results and add
  NOT terms. Expect several rounds.
- Separate queries for: your organisation, each competitor (for share of voice), and
  issues (topics that could hurt you).
- Set source scope: print, online news, broadcast, podcasts, social, forums; languages
  and countries. Note what the tool **can't** see (paywalled content, private groups,
  some broadcast) — *coverage varies by vendor and licence.*

## 2. Daily operation
- Alerts in real time for high-priority terms (crisis words + your name); daily digest
  for the rest.
- Human review: tag each item for tone, key-message presence, spokesperson quoted,
  outlet tier. Automated sentiment is often wrong on sarcasm, mixed coverage and
  specialist language — spot-check it.

## 3. Coverage report
What leadership actually needs:
1. **Headline summary** — 3–5 bullets: what happened, so what.
2. **Volume** over time vs the previous period, annotated with what caused the peaks.
3. **Share of voice** — your mentions ÷ (yours + named competitors') for the same
   query scope and period. Only comparable if the queries are built the same way.
4. **Tone/sentiment** — positive/neutral/negative, human-checked.
5. **Message pull-through** — % of coverage carrying each key message.
6. **Top pieces** — best and worst, with outlet and reach.
7. **Outcomes where possible** — website visits from coverage, enquiries, sign-ups,
   survey shifts in awareness or trust.

## 4. What not to report
**Advertising value equivalence (AVE)** — the cost of buying equivalent ad space — is
rejected by the industry's measurement body (AMEC's Barcelona Principles) as a measure
of PR value. If someone asks for it, explain why and offer outcome-based measures.
Raw "reach" or "impressions" numbers summed across outlets overstate audience; label
them as potential reach.

## 5. Early-warning signals
- A sudden rise in mentions above the normal baseline (set volume-spike alerts).
- An unusual journalist or outlet asking questions, or several reporters asking about
  the same topic.
- A critical post gaining traction among accounts journalists follow; a niche forum
  thread getting picked up by trade press.
- Freedom-of-information requests, court listings, regulator publications, employee
  review sites.
When triggered: verify facts internally, alert the press office and the issue owner,
prepare a holding statement, and decide whether to respond, monitor or engage directly.

## Gotchas
- Query drift: products and people change; review queries quarterly.
- Copyright: sharing full articles internally may need a licence (e.g. from a
  copyright licensing agency in some countries); share links and summaries.
- *Uncertain:* tool capabilities and source coverage change often; verify per vendor.

## Verify
- [ ] Queries tested on a week of data; noise excluded; brand variants covered.
- [ ] Competitor queries built identically for share of voice.
- [ ] Sentiment human-checked on a sample.
- [ ] Report leads with "so what", includes pull-through and outcomes, no AVE.
- [ ] Spike alerts set and an escalation route agreed.
