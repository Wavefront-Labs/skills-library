---
id: computing-software.it-support-helpdesk.user-support-communication.writing-a-reproducible-problem-statement
name: writing-a-reproducible-problem-statement
category: computing-software
field: it-support-helpdesk
product: user-support-communication
tags: [it-support-helpdesk, user-support-communication, ticket-documentation, ticket-notes, problem-statement, short-description, steps-to-reproduce, expected-vs-actual, comptia-a-plus]
level: intro
status: draft
description: "Log tickets anyone can pick up: a searchable short description, expected vs actual behaviour, steps to reproduce, exact error text, scope and start time."
sources:
  - "https://www.comptia.org/certifications/a"
  - "https://www.thinkhdi.com/"
  - "https://library.serviceinnovation.org/KCS/KCS_v6/KCS_v6_Practices_Guide"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# writing-a-reproducible-problem-statement

Goal: a colleague (or you next week) can understand and reproduce the
problem from the ticket alone (A+ 220-1202 4.1: ticket notes — problem
description, progress, resolution).

## Short description
`<What> <symptom> <context>` in the user's words plus the key fact:
- Good: "Outlook crashes when opening shared calendar 'Finance Leave' —
  since update this morning"
- Bad: "Outlook issue", "Please help!!", "Sam's PC"
It's the search key for KB matching, duplicates and trends.

## Description body
```
Reported by: Sam Lee (Finance), ext 4410, prefers Teams
Device: LT-5CG1234XYZ, Windows 11 23H2, Outlook M365 Current Channel 2409
Expected: open the shared calendar 'Finance Leave'
Actual: Outlook freezes then closes; error "Microsoft Outlook has stopped working"
Steps to reproduce:
  1. Open Outlook (desktop)
  2. Calendar > Shared calendars > Finance Leave
  3. Crash within 5 seconds
Started: today ~09:00 (worked yesterday)
Scope: Sam only so far; colleague Jo can open it
Impact: can't approve leave requests due today
Already tried (by user): restart PC
```

## Habits
- Exact error text (copy/paste or screenshot) and error codes — paraphrases
  lose search value.
- Distinguish **what the user said** from **what you observed** ("User
  reports…", "Confirmed on remote session…").
- Note **what changed** recently (updates, new device, password change,
  move).
- Times with timezone; frequency for intermittent issues.

## Gotchas
- Don't record passwords or sensitive data (PII rules).
- Don't diagnose in the short description ("Exchange is broken") — describe
  symptoms; diagnoses change.

## Verify
QA sample: another agent can reproduce or understand each sampled ticket
without contacting the user.
