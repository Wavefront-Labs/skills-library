---
id: computing-software.email-administration.mail-server-administration.feedback-loops
name: feedback-loops
category: computing-software
field: email-administration
product: mail-server-administration
tags: [feedback-loops, feedback-loop, arf, complaint-handling]
level: advanced
status: draft
description: "Join provider feedback loops (complaint reports in ARF format), parse them and remove complaining recipients."
sources:
  - https://www.m3aawg.org/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Feedback loops

**Goal:** stop mailing people who report you.
## Steps
1. Register your IP/domain with each provider that offers a feedback loop (enrolment rules differ per provider).
2. Receive ARF reports (multipart/report, RFC 5965 format; unconfirmed beyond the name) at a dedicated mailbox.
3. Extract the original recipient and suppress that address in your sending list.
## Failure modes
- Ignoring complaints: rising complaint rate leads to blocking.
## Verify
- Suppression list grows and complaint rate trends down in postmaster tools.

## Notes
- Written from the cited documentation; not run end to end here, so confirm option names against your Postfix/Dovecot version.
- Change one thing at a time in staging and keep a copy of the previous config.
