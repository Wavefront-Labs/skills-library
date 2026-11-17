---
id: computing-software.it-support-helpdesk.troubleshooting-methodology.establishing-and-testing-a-theory-of-probable-cause
name: establishing-and-testing-a-theory-of-probable-cause
category: computing-software
field: it-support-helpdesk
product: troubleshooting-methodology
tags: [it-support-helpdesk, troubleshooting-methodology, troubleshooting, theory-of-probable-cause, question-the-obvious, occams-razor, hypothesis-testing, escalate-or-new-theory, comptia-a-plus, escalate-or-retheorize]
level: practitioner
status: draft
description: "CompTIA steps 2-3: list probable causes from evidence, question the obvious, test theories without changing the system, then re-theorise or escalate."
sources:
  - "https://www.comptia.org/certifications/a"
  - "https://grow.google/certificates/it-support/"
  - "https://www.thinkhdi.com/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# establishing-and-testing-a-theory-of-probable-cause

Goal: move from symptoms to the cause with the fewest, cheapest tests (A+
220-1201 5.1 steps 2 and 3).

## Step 2: establish a theory
- List candidate causes from the evidence, **simplest and most likely
  first** ("question the obvious"): cable unplugged, wrong account, caps
  lock, expired password, full disk, service outage.
- Use the scope: one user → device/profile/account; many users → service,
  network, change.
- Use the timeline: "started after X" makes X the lead theory.
- Consider multiple approaches: **top-to-bottom / bottom-to-top OSI**,
  **divide and conquer** (half-split the path).
- Research: KB, known errors, vendor docs, event IDs — "conduct external or
  internal research based on symptoms".

## Step 3: test the theory
- Prefer **tests that don't change the system**: compare with a known-good
  machine/user, try another browser/profile/network, read a log, ping,
  check a setting. Observation before intervention.
- One variable at a time; record each test and result.
- Ask: "If this theory is right, what else must be true?" — test that
  prediction (e.g. if DNS is the cause, `nslookup` will fail but pinging
  the IP works).

## Outcomes
- **Theory confirmed** → determine next steps to resolve (step 4: plan of
  action).
- **Theory not confirmed** → re-establish a new theory **or escalate**.
  Set a time-box per priority (e.g. P3: 20–30 minutes at L1) so you don't
  loop.

## Example
Symptom: one user can't reach SharePoint; others fine.
Theories: (1) browser cache/profile, (2) account/licence/CA block, (3)
device network/DNS. Tests: InPrivate window → still fails; sign-in logs
show CA block "device not compliant" → theory 2 confirmed without touching
the device.

## Gotchas
- Confirmation bias: once you like a theory you stop testing alternatives —
  write the list down.
- "It works now" after a reboot isn't a confirmed cause — note it as
  unexplained and watch for recurrence.

## Verify
Ticket shows the theories considered, the tests run with results, and the
confirmed cause before the fix is applied.
