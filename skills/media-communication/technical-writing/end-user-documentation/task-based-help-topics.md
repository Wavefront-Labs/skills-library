---
id: media-communication.technical-writing.end-user-documentation.task-based-help-topics
name: task-based-help-topics
category: media-communication
field: technical-writing
product: end-user-documentation
tags: [end-user-documentation, user-documentation, user-manual, help-centre, help-center, knowledge-base, task-topics, dita, topic-based-authoring, concept-task-reference, procedures, screenshots, callouts, plain-language, readability, minimalism, zendesk-guide, intercom, information-architecture, findability, search-logs, support-tickets, writing-for-non-experts]
level: practitioner
status: draft
description: "Write end-user help that people can follow: task-based topics with numbered steps, screenshot and callout standards, help-centre structure driven by search and ticket data, and plain language."
sources: ["https://www.plainlanguage.gov/guidelines/", "https://docs.oasis-open.org/dita/dita/v1.3/dita-v1.3-part0-overview.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Task-based help topics

**Goal:** help content where a non-expert finds the right article from the words they'd
use, follows numbered steps without getting lost, and finishes the task — cutting
support tickets rather than generating them.

## 1. Topic types (keep them separate)
From topic-based authoring (DITA's concept/task/reference model):
- **Task** — how to do one thing: "Export your invoices as CSV". Most of a help centre.
- **Concept** — what something is and why it matters: "How billing cycles work".
- **Reference** — lookup tables: keyboard shortcuts, plan limits, field definitions.
- **Troubleshooting** — symptom › cause › fix: "Export button greyed out".
One topic = one purpose. Link between them rather than merging.

## 2. Anatomy of a task topic
```
Title: Export invoices as a CSV file          ← verb-first, user's words
Short intro (1–2 sentences): what you'll get, when you'd do this.
Before you start: permissions needed, plan required, prerequisites.
Steps:
1. Go to **Billing** › **Invoices**.
2. Select the date range.
3. Select **Export** › **CSV**.
   The file downloads to your browser's downloads folder.   ← result, indented
Result / next steps: what happens now, link to related tasks.
```
Rules:
- **One action per step**; put the location before the action ("In **Settings**, select …").
- UI labels **bold**, matching the screen exactly (case, wording).
- Say what the user should see after important steps — it's how they know they're on track.
- Put conditions *before* the action ("If you use SSO, skip to step 5").
- Over ~10 steps → split into sub-tasks.
- Use "select" rather than "click" if users may be on touch devices; follow your style guide.

## 3. Screenshots and callouts
- Screenshots support steps; they don't replace text (screen readers, search, translation).
- Crop tightly to the relevant area; include enough context to find it.
- Callouts (box/arrow/number) in one consistent colour and style; no freehand circles.
- Blur personal data; use a demo account with realistic fake data.
- Every screenshot needs alt text describing what it shows, and a **refresh plan** — UI
  changes make screenshots lie. Fewer, well-chosen screenshots age better.
- GIFs/short videos for multi-step gestures; always with a text alternative.

## 4. Help-centre structure driven by data
- Group by **user goals** (Getting started, Managing your team, Billing), not product
  menus or internal team names.
- Mine **site search logs** (zero-result and top queries) and **support ticket tags**
  monthly: top ticket drivers without an article are your backlog; queries in user
  vocabulary become titles and synonyms ("cancel", "delete account", "close account").
- Keep a "Getting started" path of ≤5 topics for new users.
- Track per-article: views, "was this helpful", and tickets created after viewing.

## 5. Writing for non-experts (plain language)
Short sentences (aim ~15–20 words), active voice, second person ("you"), common words,
define unavoidable terms on first use, no internal jargon or codenames. Test with a
readability check (aim around reading age 12–14 for general audiences — *a rough
guide, not a target to game*) and, better, with a real user.

## Gotchas
- Documenting what the UI does instead of what the user is trying to achieve.
- Notes/warnings overused — if everything is a warning, nothing is. Reserve "Warning"
  for data loss or security.
- Articles for features that differ by plan or platform without saying which.

## Verify
- [ ] Every task topic title starts with a verb in the user's vocabulary.
- [ ] Steps have one action each, exact bold UI labels and stated results.
- [ ] A new user completed three core tasks from the docs alone.
- [ ] Top 10 ticket drivers each have an article; zero-result searches reviewed monthly.
- [ ] Screenshots have alt text and were checked against the current UI this quarter.
