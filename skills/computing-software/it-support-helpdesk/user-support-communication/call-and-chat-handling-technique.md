---
id: computing-software.it-support-helpdesk.user-support-communication.call-and-chat-handling-technique
name: call-and-chat-handling-technique
category: computing-software
field: it-support-helpdesk
product: user-support-communication
tags: [it-support-helpdesk, user-support-communication, phone-support, chat-support, call-opening, call-closing, hold-procedure, chat-macros, canned-responses, multi-chat, qa-scoring, call-quality, live-chat-etiquette, phone-etiquette]
level: practitioner
status: draft
description: "Phone and chat handling mechanics for service desk: call opening/closing structure, hold procedure, chat macros/canned responses, multi-chat concurrency, QA scoring criteria."
sources: []
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# call-and-chat-handling-technique

Goal: the actual mechanics of running a call or chat session well —
distinct from `ticket-communication-and-escalation`'s focus on written
notes, tone, and escalation content; this is the live-interaction
technique.

## Call structure
- **Opening**: identify yourself and the team, confirm who you're
  speaking with and get a brief problem statement in their words before
  touching any tool — jumping straight to "let me pull up your account"
  before the user has finished describing the issue causes you to solve
  the wrong problem half the time; let them finish once, then
  summarize back ("so the issue is X, happening since Y, is that
  right?") to confirm you heard it correctly before acting.
- **During**: narrate what you're doing in plain terms while working
  ("I'm checking your account's group membership now, one moment") —
  silence longer than 20–30 seconds on a call reads as the agent being
  stuck or having given up, even when productive work is happening;
  a short status line costs nothing and prevents the user re-explaining
  or escalating out of frustration.
- **Hold procedure**: always ask permission before placing someone on
  hold, give an estimate ("this will take about two minutes"), and when
  you come back, come back even if the estimate wasn't met yet — a
  user left on hold past the stated estimate with no check-in is the
  single most common driver of "the agent went silent/hung up on me"
  complaints, more than actual resolution speed.
- **Closing**: restate what was done, confirm the user considers it
  resolved (don't assume silence means yes — ask directly), and give a
  next step if it isn't fully resolved yet (ticket number, expected
  follow-up time) before ending the call — an unconfirmed close is how
  a ticket gets reopened days later with the user confused about what
  was actually agreed.

## Chat-specific technique
- **Canned responses/macros** speed up repetitive phrasing (greetings,
  common instructions) but always personalize at least the specifics
  (the user's actual error, device name) — a chat reply that's
  obviously 100% template, with no reference to what the user actually
  said, reads as impersonal and erodes trust faster than a slower,
  real response would.
- **Response time expectations in chat are stricter than email** — users
  expect near-real-time pacing; going silent for several minutes mid-chat
  without a "still working on this" message causes abandonment or a
  parallel ticket/call for the same issue, doubling the workload for no
  gain.
- **Multi-chat concurrency**: when handling more than one chat at once,
  be explicit about pacing to each user ("I'm also assisting another
  customer, I'll have an update for you in a few minutes") rather than
  silently switching attention — users who don't know you're juggling
  multiple chats interpret a pause as being ignored.
- Confirm resolution in writing in chat the same way as on calls — chat's
  advantage is a written record, use it: end with a clear "resolved" or
  "next step" line the user can refer back to.

## QA scoring (what gets measured and why it matters beyond compliance)
- Typical call/chat QA rubrics score: greeting/identification, active
  listening (did the agent correctly restate the issue), technical
  accuracy of the resolution, adherence to hold/escalation procedure, and
  closing confirmation — knowing the rubric isn't about gaming a score,
  it maps directly to the behaviors in this skill that measurably reduce
  reopened tickets and repeat contacts.
- A common scoring blind spot: an agent can nail every scripted element
  and still fail the interaction if the actual technical fix was wrong —
  QA that only checks soft-skill boxes without verifying resolution
  accuracy misses the thing that matters most to the user; cross-check
  a sample of "perfect script" calls against whether the ticket reopened
  within the SLA window.

## Gotchas
- Reading from a script too literally on a call sounds robotic and
  erodes trust faster than minor grammar slips in natural speech — the
  goal of a call structure is consistency of *content* covered, not
  verbatim wording.
- A user who's clearly frustrated or in a hurry at the start of a call
  needs the opening shortened, not skipped — still confirm identity and
  get the problem statement, just move faster and skip pleasantries;
  skipping confirmation entirely to save 30 seconds is how you solve the
  wrong problem under time pressure.

## Verify
- A recorded/reviewed call or chat sample shows: correct opening
  confirmation of the issue, no unexplained silences over ~30 seconds,
  an explicit resolution confirmation before closing, and (for chat) a
  written summary the user can refer back to. Reopen rate for sessions
  following this structure should trend lower than for sessions that
  skip the confirmation steps — check this against actual ticket data,
  not just QA script adherence.
