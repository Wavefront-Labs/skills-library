---
id: computing-software.it-support-helpdesk.servicenow.knowledge-feedback-and-flagged-articles
name: knowledge-feedback-and-flagged-articles
category: computing-software
field: it-support-helpdesk
product: servicenow
tags: [it-support-helpdesk, servicenow, knowledge-base, knowledge-feedback, flagged-articles, kb-feedback-task, article-helpfulness, content-gaps, knowledge-manager]
level: practitioner
status: draft
description: "Close the loop on knowledge feedback: article ratings and comments, flagged articles and feedback tasks, search-with-no-results gaps, and response targets for article owners."
sources:
  - "https://www.servicenow.com/docs/"
  - "https://library.serviceinnovation.org/KCS/KCS_v6/KCS_v6_Practices_Guide"
  - "https://www.thinkhdi.com/"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# knowledge-feedback-and-flagged-articles

Goal: when someone says an article is wrong or unhelpful, it's fixed within
days, and the gaps people search for get filled.

## Feedback sources (ServiceNow Knowledge Management)
- **Helpful? Yes/No** and star ratings on articles (portal and agent views).
- **Flag article** with a reason/comment (agents and users).
- Comments on the article.
- **Knowledge feedback tasks** (kb_feedback_task) generated from flags or
  "No" votes with comments, assigned to the article's owner/ownership group.
- Search analytics: **searches with no results** and "searched then raised a
  ticket".

## Process
1. Feedback task assigned to article owner group; target: respond within
   e.g. 5 business days.
2. Owner fixes the article (new version), or rejects feedback with a
   reason, or retires the article.
3. Reply to the person who flagged (portal notification) — people keep
   flagging when they see results.
4. Knowledge manager reviews the feedback task backlog weekly.

## Using "not helpful" data
Sort articles by views × low helpfulness: high traffic, poor rating = top
rewrite candidates. Read the comments; often the article is right but the
title matches a different problem.

## Content gaps
Monthly: top no-result searches and top incident categories without linked
articles → create articles (assign to SMEs). Add synonyms to search
configuration for jargon mismatches (e.g. "MFA" ↔ "authenticator").

## Gotchas
- Articles without an owner group accumulate unanswered feedback — require
  ownership on publish.
- Thumbs-down without comment is low signal; prompt for a reason.
- Don't let users' complaints about the *service* in KB comments sit
  unanswered — route to the desk.

## Verify
Feedback task median age under target, top-20 viewed articles have ≥ 80 %
helpful, no-result search count falling.
