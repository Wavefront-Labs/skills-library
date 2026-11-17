---
id: computing-software.it-support-helpdesk.servicenow.article-quality-index-and-coaching
name: article-quality-index-and-coaching
category: computing-software
field: it-support-helpdesk
product: servicenow
tags: [it-support-helpdesk, servicenow, knowledge-base, kcs, article-quality-index, aqi, kcs-coach, content-standard, knowledge-quality, knowledge-centered-service]
level: practitioner
status: draft
description: "Measure and raise knowledge quality with a KCS Article Quality Index: a content standard checklist, sampling articles per author, coaching conversations, and tracking AQI trends."
sources:
  - "https://library.serviceinnovation.org/KCS/KCS_v6/KCS_v6_Practices_Guide"
  - "https://www.servicenow.com/docs/"
  - "https://www.thinkhdi.com/"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# article-quality-index-and-coaching

Goal: articles are consistently findable, correct and usable — improved by
coaching authors, not by a central editor rewriting everything (KCS v6
Evolve Loop: content health, performance assessment, coaching).

## Content standard (write it down, one page)
Template fields, title rules (symptom in user words), formatting, required
environment info, how to write steps, what not to include (passwords,
personal data), audience/visibility rules. The AQI checks against this.

## Article Quality Index
Sample ~5 articles per author per month (new and modified). Score each on
a checklist; weight serious defects higher:
| Criterion | Example check |
|---|---|
| Unique (not a duplicate) | searched before creating? |
| Complete thought, correct resolution | does it work as written? |
| Title/issue in requester's words | would a user search this? |
| Environment captured | OS/app/version present |
| Content standard format | template used, steps numbered |
| Links/attachments valid | no broken links |
| Appropriate visibility | internal vs external correct |
AQI = (1 − weighted defects / possible) × 100. Track per author and team.

## Coaching
- **KCS coaches** (experienced agents, not managers) review AQI results with
  authors 1:1, monthly, 15 minutes: one or two specific improvements,
  examples from their own articles.
- Authors move up licence levels (Candidate → Contributor → Publisher) when
  AQI is consistently high.
- Coaching is developmental, not punitive.

## In ServiceNow
Knowledge feedback, article quality fields (or a custom AQI table/survey),
reports on article views/use/helpfulness; some orgs run AQI in a
spreadsheet — fine to start.

## Gotchas
- Scoring everything — sampling is enough.
- Using AQI alone for performance reviews encourages fewer, safer articles;
  balance with contribution and reuse.

## Verify
Team AQI above target (e.g. 90 %), defects trending down by criterion, and
coaching sessions logged monthly.
