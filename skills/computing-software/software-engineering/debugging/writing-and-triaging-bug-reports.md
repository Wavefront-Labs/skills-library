---
id: computing-software.software-engineering.debugging.writing-and-triaging-bug-reports
name: writing-and-triaging-bug-reports
category: computing-software
field: software-engineering
product: debugging
tags: [debugging, bug-reports, bug-triage, issue-tracking, severity-priority, reproduction-steps, duplicate-detection]
level: practitioner
status: draft
description: "Write bug reports developers can act on (steps, expected vs actual, environment, evidence) and triage incoming reports by severity, priority, reproducibility and duplicates."
sources: ["Why Programs Fail, 2nd ed. (Zeller), ch2 Tracking Problems", "https://bugzilla.mozilla.org/page.cgi?id=bug-writing.html", "https://developer.mozilla.org/en-US/docs/Mozilla/QA/Bug_writing_guidelines"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Writing and triaging bug reports

**Goal:** every bug report contains enough to reproduce the problem, and the backlog is
ordered by impact so the right bugs get fixed first.

## A report developers can act on
```
Title: Checkout returns 500 when coupon code has trailing space
Environment: prod web, app v4.12.1 (commit abc123), Chrome 141 / macOS 15
Steps:
  1. Add any item to cart
  2. Enter coupon "SAVE10 " (note trailing space)
  3. Click Pay
Expected: coupon applied or "invalid coupon" message
Actual: HTTP 500, "Something went wrong" page
Frequency: 5/5 attempts
Evidence: request id 7f3a...; screenshot; log excerpt attached
Workaround: remove the space
```
- One problem per report.
- Title states the symptom and trigger, not a guess at the cause.
- Exact versions and identifiers (build, commit, request/trace id, user id where allowed).
- Minimal steps: remove everything not needed to reproduce.
- Attach logs/screenshots as files, redacting secrets and personal data.

## Triage
For each new report:
1. **Reproduce** (or ask for missing info with a specific question; set a timeout for "needs info").
2. **Deduplicate**: search by error message, stack trace frames, component.
3. **Severity** (impact): data loss/security > outage > major feature broken without
   workaround > with workaround > cosmetic.
4. **Priority** (when to fix): severity x number of users affected x business context
   (release dates, contracts). A low-severity bug on the login page can be high priority.
5. **Route** to an owner/component; label regressions explicitly (they usually point to
   a recent change: bisect).
Hold a short regular triage session; never let the untriaged queue age.

## Lifecycle hygiene
- Close with a reason: fixed (link to commit/PR), duplicate (link), won't fix (why),
  cannot reproduce (what was tried).
- Fixed bugs get a regression test referenced in the ticket.
- Track reopen rate and bug age as quality signals.

## Verify
- [ ] Someone other than the reporter can reproduce from the report alone.
- [ ] Every open bug has severity, priority and owner.
