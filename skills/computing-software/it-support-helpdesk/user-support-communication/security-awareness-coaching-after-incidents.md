---
id: computing-software.it-support-helpdesk.user-support-communication.security-awareness-coaching-after-incidents
name: security-awareness-coaching-after-incidents
category: computing-software
field: it-support-helpdesk
product: user-support-communication
tags: [it-support-helpdesk, user-support-communication, security-awareness, phishing, coaching, just-culture, social-engineering, user-education]
level: practitioner
status: draft
description: "Coach a user after a security slip (phish click, scam call, data leak): timely, private and blame-free, specific red flags, praise for reporting, support for repeats."
sources:
  - "https://www.ncsc.gov.uk/collection/phishing-scams"
  - "https://www.ncsc.gov.uk/blog-post/trouble-phishing"
  - "https://www.cisa.gov/secure-our-world/recognize-and-report-phishing"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# security-awareness-coaching-after-incidents

## Principles
- **Blame-free**: people who are punished stop reporting; early reports are what save
  incidents. Thank them for reporting, even if they clicked.
- **Timely**: within a day, while they remember the details.
- **Private and short**: a 10-15 minute conversation or call, not an email to their
  manager.

## The conversation
1. Check how they are; some users are embarrassed or anxious.
2. Walk through what happened using the actual message or call: which red flags were
   there (urgent tone, unexpected request, sender address mismatch, link domain, request
   for codes or remote access, payment change).
3. What to do next time: pause, verify through a known channel, report with the Report
   button or to the service desk, never share MFA codes or approve unexpected prompts.
4. Confirm what has already been done to protect them (password reset, sessions revoked)
   and anything they still need to do.
5. Offer a short relevant training module or KB article; no generic hour-long course.

## Repeat cases
- Track by person privately (phishing simulation platform or incident records).
- Second or third event: more support, not punishment; look at role exposure (finance,
  executives' assistants) and add technical controls (stricter mail filtering, phishing-
  resistant MFA).
- Escalate to the manager only under the agreed policy and for wilful policy breaches.

## Feed it back
Share anonymised examples with the organisation ("this week's phish") and tell security
which lures are working so filters improve.

## Gotchas
- Simulations that feel like traps damage trust; pair them with immediate, kind teaching.
- Never ask users to forward suspicious mail as an attachment unless your process needs it;
  use the Report button.

## Verify
The user can name the red flags and the reporting route, the coaching is logged against
the incident, and follow-up training (if assigned) is completed.
