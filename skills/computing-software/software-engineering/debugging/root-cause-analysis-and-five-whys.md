---
id: computing-software.software-engineering.debugging.root-cause-analysis-and-five-whys
name: root-cause-analysis-and-five-whys
category: computing-software
field: software-engineering
product: debugging
tags: [debugging, root-cause-analysis, five-whys, postmortems, contributing-factors, fishbone]
level: practitioner
status: draft
description: "Do root cause analysis after a bug or incident: five whys done well, contributing-factor trees, separating trigger from cause, and actions that prevent the class of bug."
sources: ["https://sre.google/sre-book/postmortem-culture/", "https://www.atlassian.com/incident-management/postmortem/5-whys", "https://how.complexsystems.fail/", "https://www.learningfromincidents.io/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Root cause analysis and five whys

## Five whys, done well
Start from the precise failure and ask "why?" repeatedly, each answer backed by evidence:
1. Why did customers get double-charged? The payment job ran twice for the same orders.
2. Why twice? Two workers picked the same batch.
3. Why? The batch lock expired while the first worker was still running.
4. Why? Lock TTL 60 s; the job took 4 min after the payment API slowed.
5. Why was that possible? The job wasn't idempotent and lock TTL wasn't tied to job duration
   (no lease renewal, no fencing).
Fixes then target several levels: idempotency key per charge (prevents the class), lease renewal
with fencing tokens, alert on job duration, and API timeout.

## Rules
- Branch: most failures have **several contributing factors**; a single chain hides the others.
  Draw a tree or fishbone (people/process/tooling/code/environment/dependencies).
- Stop at causes you can act on; don't stop at "human error". Ask why the system made the error
  easy and its consequences severe (Cook, How Complex Systems Fail).
- Separate **trigger** (deploy, traffic spike, bad input) from underlying causes (missing
  validation, no rate limit).
- Each "why" needs evidence (logs, code, metrics), not a guess.

## For a code bug specifically
- Find the defect (the line), then ask why it was written, why review didn't catch it, why tests
  didn't, why monitoring didn't detect it sooner. Each answer is a possible action.
- Search for the **same pattern elsewhere** (`rg`, Semgrep/CodeQL query) and fix all instances.
- Add a regression test and, where possible, a static check that bans the pattern.

## Write it up (blameless)
Summary, impact, timeline, root cause and contributing factors, what went well, action items with
owners and dates (prevent, detect, mitigate). Track action items to completion; unfinished actions
are the most common postmortem failure.
