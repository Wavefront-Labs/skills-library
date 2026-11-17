---
id: computing-software.qa-testing-engineering.exploratory-testing.thread-based-exploratory-testing
name: thread-based-exploratory-testing
category: computing-software
field: qa-testing-engineering
product: exploratory-testing
tags: [thread-based-testing, exploratory-testing, test-management, rst, sbtm]
level: practitioner
status: draft
description: "Run thread-based exploratory test management: organise testing as threads instead of time-boxed sessions, track them on a board, and report coverage in busy, interrupted contexts."
sources:
  - https://www.satisfice.com/rapid-testing-methodology
  - https://www.satisfice.com/download/session-based-test-management
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Thread-based exploratory testing

**Goal:** manage exploratory testing where uninterrupted 90-minute sessions are unrealistic (constant interruptions, many small changes), as described by James and Jon Bach as thread-based test management.

## What a thread is
A test activity or test idea that a tester follows over time, possibly in many short bursts: "explore new discount rules", "investigate slow search on large accounts", "keep checking the payment provider sandbox after each deploy". Unlike a session, a thread has no fixed length or single sitting.

## Managing threads
- Keep a **thread list or board** (mind map, Kanban, spreadsheet): thread name, priority, status (not started, active, parked, done enough), notes link, owner.
- Threads can split ("search performance" spawns "index rebuild timing") and be tied off ("done enough for this release").
- Notes per thread, appended each time someone works on it: what was tried, findings, bugs, questions.
- Daily stand-up or debrief reviews active and parked threads, not individual sessions.

## Reporting
- Report coverage as the thread map with status and depth (e.g. 0 to 3) per area, plus bugs and issues per thread.
- Combine with sessions when focus time is available: a session can work on one thread.

## When to use
Early project phases, support-heavy teams, embedded testers in fast agile teams, investigations that span days.

## Verify
Every active thread has notes and an owner, the board shows status and depth per area, and stakeholders can see which threads are done enough before release.
