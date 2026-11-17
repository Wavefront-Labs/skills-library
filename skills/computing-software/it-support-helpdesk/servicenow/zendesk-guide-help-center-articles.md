---
id: computing-software.it-support-helpdesk.servicenow.zendesk-guide-help-center-articles
name: zendesk-guide-help-center-articles
category: computing-software
field: it-support-helpdesk
product: servicenow
tags: [it-support-helpdesk, servicenow, zendesk-guide, zendesk, help-center, knowledge-base, article-permissions]
level: practitioner
status: draft
description: "Run the Zendesk Guide help center: categories and sections, article permissions and user segments, agent knowledge capture, content blocks and article review."
sources:
  - "https://support.zendesk.com/hc/en-us/articles/4408846795674-Getting-started-with-the-help-center"
  - "https://support.zendesk.com/hc/en-us/articles/4408842907546-Creating-user-segments-to-restrict-access"
  - "https://support.zendesk.com/hc/en-us/articles/4408833802138-Using-the-Knowledge-Capture-app"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# zendesk-guide-help-center-articles

## Structure
- Help center hierarchy: **categories > sections > articles** (sections can nest).
  Keep it to what users look for: "Accounts and passwords", "Email", "Devices".
- Each article has a **visibility** setting via user segments and a **management
  permission** (who can edit/publish).

## User segments and permissions
- User segments (Guide admin > User permissions): signed-in users, agents and admins,
  or custom segments by tag, organization or group.
- Internal articles: visible to agents only; use for admin procedures.
- Management permissions: e.g. "Editors can edit, Publishers can publish" so articles go
  through review.

## Knowledge capture by agents
- The **Knowledge** section in the agent workspace context panel lets agents search,
  link an article to a ticket, flag an article for an issue, or create a new article from
  the ticket using a template.
- Link articles in replies; linked counts show which articles solve tickets.

## Keeping content healthy
- Set article **verification** or review dates (Guide Enterprise team publishing) and
  assign owners.
- Content blocks (Enterprise) reuse the same paragraph across articles, e.g. "how to
  open Company Portal".
- Search analytics: top searches with no results; create or retitle articles for them.

## Pitfalls
- Articles left visible to "Everyone" when they contain internal steps.
- Huge flat sections; users don't browse past the first screen.

## Verify
Anonymous, signed-in and agent views each see the right articles; flagged articles have
owners; no-result searches decline month over month.
