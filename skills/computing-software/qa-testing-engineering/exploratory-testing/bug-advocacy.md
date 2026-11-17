---
id: computing-software.qa-testing-engineering.exploratory-testing.bug-advocacy
name: bug-advocacy
category: computing-software
field: qa-testing-engineering
product: exploratory-testing
tags: [bug-advocacy, defect-reporting, influencing, triage, rst]
level: practitioner
status: draft
description: "Advocate for bugs so the right ones get fixed: maximise impact evidence, follow-up testing to find worse variants, clear summaries and respectful negotiation in triage."
sources:
  - https://associationforsoftwaretesting.org/
  - https://www.satisfice.com/rapid-testing-methodology
  - https://kaner.com/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Bug advocacy

**Goal:** a bug report is a persuasive document: its job is to get the right decision on the bug (Cem Kaner, BBST Bug Advocacy). Advocacy means giving decision-makers the best information, not winning.

## Make the bug look as important as it really is
- **Follow-up testing:** before filing, vary the steps to find the worst consequence: does it lose data, affect other users, happen with common data, happen on other platforms, escalate with repetition? Report the most severe variant you found.
- **Show user impact:** who hits it, how often (analytics or log counts), what it costs (support tickets, abandoned checkouts, compliance exposure).
- **Reduce to the simplest reproduction:** fewer steps, general data, so nobody dismisses it as a corner case.
- **Summary line that sells:** symptom + trigger + impact. "Saving an invoice with a 0% tax line deletes all line items" beats "Invoice issue".

## Remove reasons to dismiss
- Exact build, environment, data and evidence attached (video, logs, HAR).
- Neutral, factual tone; no blame, no sarcasm.
- Separate facts from speculation about cause.

## In triage
- Know the bug well enough to answer questions; bring the impact evidence.
- If deferred, ask what would change the decision and record it.
- Accept business decisions gracefully; re-raise only with new information (more frequency, new impact, customer report).
- Track your own bugs that were deferred and later escaped; use them as evidence for future calls.

## Verify
Reports include the worst-case variant and impact data, triage decisions are recorded with reasons, and deferred bugs are re-raised only with new evidence.
