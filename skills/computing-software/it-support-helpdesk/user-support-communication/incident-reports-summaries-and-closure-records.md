---
id: computing-software.it-support-helpdesk.user-support-communication.incident-reports-summaries-and-closure-records
name: incident-reports-summaries-and-closure-records
category: computing-software
field: it-support-helpdesk
product: user-support-communication
tags: [it-support-helpdesk, user-support-communication, incident-report, executive-summary, closure-email, accessible-communication, time-tracking, written-communication]
level: practitioner
status: draft
description: "Write incident reports and executive summaries, closure emails users understand, accessible written communication, and accurate ticket time tracking."
sources:
  - "https://www.atlassian.com/incident-management/postmortem/templates"
  - "https://www.w3.org/WAI/WCAG22/understanding/reading-level"
  - "https://www.plainlanguage.gov/guidelines/"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# incident-reports-summaries-and-closure-records

## Incident report
For any major or notable incident, within an agreed time (e.g. 5 business days):
1. Summary: what happened, impact (who, how many, how long), current status.
2. Timeline with timestamps (detection, escalation, key actions, restoration).
3. Root cause (or current hypothesis if the problem investigation continues).
4. What went well, what didn't (detection, communication, tooling).
5. Actions with owners and dates.
Blameless tone: describe systems and decisions, not people's failings.

## Executive summary
- 5-7 lines at the top, readable alone: what, impact in business terms ("payroll team
  couldn't process for 3 hours"), cause in one sentence, what's fixed, what's still at
  risk, what you need from leadership (decision, money, priority).
- No jargon or acronyms without explanation; numbers over adjectives.

## Closure emails
- State what was wrong in user terms, what you did, and anything they need to do
  ("restart Outlook once").
- How to reopen if it recurs (reply within N days) and where to find the KB article.
- Short; one screen. Thank them for their patience only if there was a wait.
```
Subject: Resolved: Shared drive access (INC0012345)
Hi Sam, you couldn't open the Finance drive because your account was missing from the
Finance group after your team move. I've added you; please sign out and back in to get
access. If it still doesn't work, reply to this email within 5 days and the ticket will
reopen.
```

## Accessible writing
- Plain language: short sentences, common words, active voice, one idea per paragraph.
- Structure with headings and numbered steps; meaningful link text ("download the VPN
  guide", not "click here").
- Don't rely on colour or images alone; add alt text to screenshots; use real text, not
  text in images.
- Check readability (aim for roughly a lower-secondary reading level for user-facing
  content) and test with a screen reader for key templates.

## Time tracking on tickets
- Log effort per ticket update (time worked field), including research and calls, not
  just remote session time.
- Consistent rounding (e.g. nearest 5 minutes); log when you stop, not at end of day from
  memory.
- Uses: cost per ticket, effort by category for automation targets, MSP billing, staffing.
- Don't use time logged as an individual performance stick; it drives under-reporting.

## Verify
Incident reports have timelines and owned actions, executive summaries fit on one screen,
closure emails pass a plain-language check, and time worked is filled on resolved tickets.
