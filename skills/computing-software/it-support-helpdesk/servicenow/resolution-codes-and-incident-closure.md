---
id: computing-software.it-support-helpdesk.servicenow.resolution-codes-and-incident-closure
name: resolution-codes-and-incident-closure
category: computing-software
field: it-support-helpdesk
product: servicenow
tags: [it-support-helpdesk, servicenow, incident-management, resolution-codes, close-code, resolution-notes, auto-close, user-confirmation, reopen-rate, itil-4, user-closure-confirmation]
level: practitioner
status: draft
description: "Resolve and close incidents properly: confirming with the user, meaningful resolution codes, notes another agent can reuse, resolved-to-closed auto-close, and reopen handling."
sources:
  - "https://www.axelos.com/certifications/itil-service-management"
  - "https://www.servicenow.com/docs/"
  - "https://www.thinkhdi.com/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# resolution-codes-and-incident-closure

Goal: incidents close only when fixed, with data good enough to find
patterns and knowledge gaps later.

## Resolve vs close
- **Resolved**: you believe it's fixed; user is notified and can reject
  within the window.
- **Closed**: final — automatically after N days resolved (ServiceNow
  property `glide.ui.autoclose.time`, commonly 3–5 days) or on user
  confirmation. Reopened-after-closed should be a new incident linked to
  the old one.

## Before resolving
1. Confirm with the user (or test the exact failing action yourself) —
   "should be fixed" isn't resolved.
2. Fill **resolution code** (close code) and **resolution notes**.
3. Link knowledge used/created, problem record, change that caused it.
4. Correct the category/CI to the actual cause service.

## Resolution codes that mean something
Keep the list short and cause-oriented:
| Code | Use when |
|---|---|
| Solved (workaround) | service restored but underlying fault remains (link problem) |
| Solved (permanent fix) | fault removed |
| Solved by user / self-resolved | user fixed it or it went away — note what happened |
| User error / training | coach + KB link (no blame language in notes) |
| Duplicate | linked to the original |
| Not reproducible | after defined attempts and user agreement |
| Resolved by change / caused by change | link change record |
| Hardware replaced | with asset updates |
"Closed/Resolved by caller" without notes kills trend analysis.

## Resolution notes template
- Cause: what was wrong (one line).
- Fix: what was done, with exact settings/commands.
- Verification: how it was confirmed.
- Prevention/knowledge: KB number or "KB needed".

## Reopens
Track reopen rate per agent/team: high reopens = premature resolution.
Users replying "still broken" after resolution → reopen (within window),
never open a new ticket and lose history.

## Gotchas
- Pending-user auto-resolution (e.g. 3 reminders over 7 days) must be
  communicated in the reminders; otherwise users feel dismissed.
- Satisfaction surveys trigger on resolve/close — closing prematurely
  depresses CSAT.

## Verify
Sampled resolved incidents have cause, fix and verification in notes; reopen
rate under target (often < 5 %).
