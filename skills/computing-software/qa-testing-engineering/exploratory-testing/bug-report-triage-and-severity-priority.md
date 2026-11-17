---
id: computing-software.qa-testing-engineering.exploratory-testing.bug-report-triage-and-severity-priority
name: bug-report-triage-and-severity-priority
category: computing-software
field: qa-testing-engineering
product: exploratory-testing
tags: [bug-triage, defect-triage, severity, priority, bug-reports, defect-management, jira, triage-meeting, duplicate-bugs, bug-lifecycle, reproduction-steps, regression-vs-new, defect-taxonomy, root-cause-tagging, qa, defect-density, wont-fix]
level: practitioner
status: draft
description: "Triage found defects: separate severity from priority, write reports a developer can act on without reproducing them live, spot duplicates, and run a triage meeting that doesn't stall."
sources: ["https://www.developsense.com/resources/", "https://www.atlassian.com/software/jira/guides/issues/triage"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Bug report triage: severity, priority, and reports that get fixed

**Goal:** turn a found defect into a report that a developer can act on without
re-finding it, and sort the backlog so the team fixes what actually matters first.

## 1. Severity is not priority — keep them as two fields
**Severity** = technical impact if nothing is done (data loss, crash, security hole,
cosmetic). It's a property of the bug and rarely changes. **Priority** = how soon it
gets fixed, which depends on severity *and* business context (release date, how
many users hit it, a demo tomorrow). A cosmetic typo on the CEO's demo slide can be
P0/Sev-5; a crash in a feature flag at 0% rollout can be P3/Sev-1. Conflating the
two fields produces a backlog where "urgent" just means "loud," and quietly-severe
bugs rot.

## 2. A report a developer can act on, written in minutes
Minimum fields, in this order:
1. **Title**: symptom + where, not a diagnosis ("Checkout total is wrong for 2+
   discount codes" not "discount code bug").
2. **Environment**: build/commit, browser/OS/device, account/role, feature flags on.
3. **Preconditions**: state needed before the steps (logged in as X, cart has Y).
4. **Steps**: the *minimal* reproduction — cut every step that doesn't change the
   outcome (see below). Numbered, one action per line.
5. **Actual vs expected**, each one sentence, with the actual result as *observed
   fact* ("total shows $38.00") not interpretation ("total is broken").
6. **Evidence**: screenshot/video/HAR/console log/trace attached, not described.
7. **Reproduction rate**: always / ~50% / once — intermittent bugs need this flagged
   so they aren't closed as "could not reproduce" after one failed attempt.

## 3. Minimizing the repro (the step that saves everyone time)
Before filing, strip steps one at a time and re-test: does the bug still happen
with fewer discount codes, a different browser, logged out? Each removed variable
that still reproduces narrows the search space for the developer by roughly half.
A report with 11 steps where 3 matter costs the team an hour of back-and-forth; the
minimizing pass costs you ten minutes.

## 4. Spotting duplicates and regressions before filing
Search existing tickets by the *symptom*, not your hypothesis of the cause — two
different symptoms of the same root cause get filed as separate tickets more often
than true duplicates do. Check whether the behavior is new (regression — tag the
last known-good build/commit if you can bisect it with a quick smoke check) or has
always existed (then it's a backlog item, not a release blocker).

## 5. Running triage without stalling
Timebox each bug to the decision needed (severity confirmed, priority set, owner
assigned) — not a design discussion, which gets its own ticket. Decline "can't
reproduce" as a closing reason until reproduction rate and environment are checked
against the reporter's; ask for the missing field instead of closing. A running
tally of "won't fix" reasons (by design, out of scope, cost > impact) surfaces
patterns — e.g., the same component generating repeat won't-fixes signals a spec
gap, not a QA gap.

## Unconfirmed / notes
Process-dependent by team/tool (Jira workflow fields, triage cadence); the
severity/priority split and minimal-repro discipline are the portable parts.

## Verify
- [ ] Severity and priority are separate fields with separate justifications.
- [ ] Repro steps are minimized — no step left that doesn't change the outcome.
- [ ] Evidence is attached, not described in prose.
- [ ] Searched existing tickets by symptom before filing.
- [ ] Intermittent bugs carry a reproduction rate, not silently treated as always-on.
