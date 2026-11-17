---
id: computing-software.it-support-helpdesk.user-support-communication.resolution-notes-that-feed-knowledge
name: resolution-notes-that-feed-knowledge
category: computing-software
field: it-support-helpdesk
product: user-support-communication
tags: [it-support-helpdesk, user-support-communication, ticket-documentation, ticket-notes, resolution-notes, work-notes, progress-notes, knowledge-capture, comptia-a-plus]
level: intro
status: draft
description: "Write progress and resolution notes that become reusable knowledge: timestamped work notes, cause/fix/verification structure, exact commands, and what not to write."
sources:
  - "https://www.comptia.org/certifications/a"
  - "https://library.serviceinnovation.org/KCS/KCS_v6/KCS_v6_Practices_Guide"
  - "https://www.thinkhdi.com/"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# resolution-notes-that-feed-knowledge

Goal: the ticket history explains what happened and how it was fixed well
enough to turn into a KB article or reuse next time.

## Progress (work) notes
Add a note at each meaningful step, not one essay at the end:
```
10:12 Remote session. Repro confirmed: Outlook crashes opening 'Finance Leave'.
10:18 /safe mode: still crashes -> not an add-in.
10:25 New Outlook profile: shared calendar opens fine -> profile/OST issue.
10:40 Removed and re-added calendar in original profile -> works.
```
- Internal-only notes in work notes; anything the user should see in
  customer-visible comments (don't mix — see the notes gotcha in ticket
  lifecycle).
- Include negative results — "didn't work" saves the next person time.

## Resolution note structure
- **Cause**: "Corrupt cached copy of shared calendar in OST."
- **Fix**: "Removed shared calendar, cleared it from Calendar > right-click
  > Delete calendar, re-added via Open Calendar > From Address Book."
  Exact settings, commands, versions.
- **Verification**: "User opened calendar 3 times; approved leave
  request."
- **Prevention / knowledge**: "KB0012345 updated" or "KB needed".

## Write for reuse
- Same words as the symptom (searchable).
- Generalise if appropriate ("any shared calendar"), but don't guess.
- Attach useful evidence (log snippet) rather than "checked logs".

## Avoid
- "Fixed", "Done", "Sorted", "Resolved per user".
- Blame or opinion about the user/team.
- Credentials, recovery keys, personal data.

## Verify
QA sample: resolution notes contain cause, fix and verification; KB
creation from tickets rises.
