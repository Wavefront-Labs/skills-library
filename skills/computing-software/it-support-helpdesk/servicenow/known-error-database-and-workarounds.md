---
id: computing-software.it-support-helpdesk.servicenow.known-error-database-and-workarounds
name: known-error-database-and-workarounds
category: computing-software
field: it-support-helpdesk
product: servicenow
tags: [it-support-helpdesk, servicenow, problem-management, known-error, kedb, workaround, known-error-article, communicate-workaround, itil-4, workaround-management]
level: practitioner
status: draft
description: "Run a known error database the desk uses: when a problem becomes a known error, writing agent-ready workarounds, publishing as KB, linking incidents, retiring entries."
sources:
  - "https://www.axelos.com/certifications/itil-service-management"
  - "https://www.servicenow.com/docs/"
  - "https://www.thinkhdi.com/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# known-error-database-and-workarounds

Goal: when a fault has a known cause but no permanent fix yet, every agent
can find and apply the workaround in under a minute.

## Known error
ITIL 4: a problem that has been analysed but not resolved — cause and/or
workaround known. In ServiceNow: Problem record state **Fix in Progress /
Known Error** (Problem Management with "Known error" flag), and
**Create Known Error Article** publishes a KB article in the Known Error
knowledge base.

## Writing the workaround
- Symptoms exactly as users report them (and error text) — that's what
  agents search.
- Scope: affected versions/devices/sites.
- Workaround steps an L1 agent can perform (or that users can self-apply),
  with time required and side effects.
- When to escalate instead (e.g. workaround fails → attach to problem
  PRB0012).
- Status line: "Permanent fix expected with change CHG00456, target date".

## Agent workflow
1. Search KB/known errors at triage (portal and agent workspace contextual
   search on short description).
2. Apply workaround, **link the incident to the problem** (Problem field)
   — this counts impact and lets you notify affected users when fixed.
3. Resolve incident with code "Solved (workaround)".
4. Report if the workaround didn't work → update the article.

## Maintain
- Problem owner updates the article when cause/fix status changes.
- When the permanent fix is deployed: retire the article (or mark
  resolved with version info), resolve the problem; optional notification to
  linked incidents' callers.
- Review KEDB entries older than 90 days: still valid? fix stalled?

## Gotchas
- Workarounds hidden in problem work notes aren't findable — publish them.
- Vendor bugs: include the vendor case/bug ID and link to vendor advisory.
- Security-sensitive known errors may need restricted KB visibility.

## Verify
Incidents linked to open known errors are rising while time-to-resolve for
those incidents falls; no known error without a published workaround or a
"no workaround" statement.
