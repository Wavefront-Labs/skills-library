---
id: computing-software.it-support-helpdesk.servicenow.kcs-solve-loop-in-practice
name: kcs-solve-loop-in-practice
category: computing-software
field: it-support-helpdesk
product: servicenow
tags: [it-support-helpdesk, servicenow, knowledge-base, kcs, kcs-solve-loop, capture-structure-reuse-improve, search-early-search-often, work-in-progress-articles, knowledge-centered-service]
level: practitioner
status: draft
description: "Apply the KCS v6 Solve Loop on every ticket: capture in the user's words, structure with the article template, search early and often, reuse and link, and improve as you go."
sources:
  - "https://library.serviceinnovation.org/KCS/KCS_v6/KCS_v6_Practices_Guide"
  - "https://www.servicenow.com/docs/"
  - "https://www.thinkhdi.com/"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# kcs-solve-loop-in-practice

Goal: knowledge becomes a by-product of solving tickets, not a separate
writing project nobody has time for (KCS v6 Practices Guide, Solve Loop).

## The four Solve Loop practices
1. **Capture** — while working the ticket, record the requester's context
   in *their* words (symptoms, error text, environment). That text is what
   the next person will search with.
2. **Structure** — use the article template: Issue, Environment, Resolution,
   Cause. Short, complete thoughts; not full prose.
3. **Reuse** — **search early, search often**: search the KB with the
   captured words before troubleshooting; if found, use and **link** the
   article to the ticket. "Search is creating" — if not found, your captured
   text becomes the start of a new article.
4. **Improve** — "Reuse is review": if the article is incomplete or wrong,
   fix it (if licensed) or flag it, right then.

## In ServiceNow
- Contextual search in Agent Workspace / incident form suggests articles
  from the short description; **Attach** links it.
- **Create Knowledge** from the incident pre-fills an article draft
  (configure field mapping to the KCS template).
- Draft/Work-in-progress articles visible internally immediately ("just in
  time" publishing) with a confidence state (Work in progress → Not
  validated → Validated) rather than long approval queues.
- KCS roles/licensing (Candidate, Contributor, Publisher) map to who can
  publish internally vs externally.

## Habits for agents
- Copy the exact error message into the ticket and the article.
- One article per issue; resolution steps numbered.
- Don't write the article "later" — later never happens.

## Gotchas
- Heavy approval workflows kill KCS; keep validation light for internal
  audience.
- Articles written in IT jargon fail to match user-language searches.
- Linking rate is the leading indicator — no linking, no measurement.

## Verify
Article link rate on resolved incidents (target ≥ 60–70 % for L1), share of
new articles created from tickets, time-to-resolve on linked vs unlinked
incidents.
