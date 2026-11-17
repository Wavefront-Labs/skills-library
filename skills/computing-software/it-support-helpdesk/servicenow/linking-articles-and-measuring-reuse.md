---
id: computing-software.it-support-helpdesk.servicenow.linking-articles-and-measuring-reuse
name: linking-articles-and-measuring-reuse
category: computing-software
field: it-support-helpdesk
product: servicenow
tags: [it-support-helpdesk, servicenow, knowledge-base, article-linking, link-rate, reuse-rate, m2m-kb-task, knowledge-use, citation, knowledge-metrics]
level: practitioner
status: draft
description: "Link knowledge articles to tickets and measure it: link and reuse rates, ServiceNow attach and kb_use records, linked vs unlinked resolution time, gap detection."
sources:
  - "https://library.serviceinnovation.org/KCS/KCS_v6/KCS_v6_Practices_Guide"
  - "https://www.servicenow.com/docs/"
  - "https://www.thinkhdi.com/"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# linking-articles-and-measuring-reuse

Goal: every resolved ticket points to the knowledge used (or created), so
you know which articles carry the load and where knowledge is missing.

## Linking in ServiceNow
- From the incident's contextual search results: **Attach** — inserts the
  article link into comments/notes and creates the relationship
  (`m2m_kb_task`, Knowledge related list on the task).
- **Create Knowledge** from the ticket links the new article automatically.
- Article views and uses are logged (`kb_use`, view counts) — portal views
  that led to no ticket count as self-service success.

## Metrics (KCS)
| Metric | Meaning |
|---|---|
| **Link rate** | % of resolved tickets with an article linked (used or created) |
| **Reuse rate** | % linked to an existing article (vs new) — rising means coverage is good |
| **Create rate** | new articles per agent/team — expected early in adoption |
| **Linked vs unlinked time to resolve** | value of knowledge |
| **Article usage concentration** | top 20 % of articles cover ~80 % of links; review those most |
| **Participation** | % of agents linking/contributing |

## Reading the signals
- Low link rate + high reuse on a few articles → agents solve from memory;
  fine for seniors, but junior onboarding suffers — encourage linking.
- High-volume categories with low link rate → missing articles.
- Articles linked often to reopened tickets → article may be wrong.

## Making linking easy
Show suggestions automatically on the form; one-click attach; include
linking in resolution checklist and QA. Don't require a link on tickets
where none applies (e.g. hardware swap) — allow "no article applicable".

## Gotchas
- Pasting a KB URL in notes without using Attach creates no relationship —
  invisible to reports.
- Link-rate targets enforced harshly produce random links; QA sample for
  relevance.

## Verify
Monthly report shows link and reuse rates by team with QA-sampled
relevance ≥ 90 %, and the gap list is fed into article creation.
