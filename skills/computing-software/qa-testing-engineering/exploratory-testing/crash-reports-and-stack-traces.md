---
id: computing-software.qa-testing-engineering.exploratory-testing.crash-reports-and-stack-traces
name: crash-reports-and-stack-traces
category: computing-software
field: qa-testing-engineering
product: exploratory-testing
tags: [crash-reports, sentry, crashlytics, bug-investigation, symbolication]
level: practitioner
status: docs-checked
description: "Use Sentry Issues and Firebase Crashlytics crash grouping for triage: fingerprints, variants, event and user counts, regressions and symbol mapping."
sources:
  - https://docs.sentry.io/product/issues/
  - https://firebase.google.com/docs/crashlytics
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Crash reports and stack traces in Sentry and Crashlytics

**Goal:** extract from a crash tool what failed, where, for whom and how often, to file an actionable bug and prioritise it.

## Sentry Issues
- An issue is a single bug or problem; Sentry groups similar events into issues by a fingerprint, so you can see how often a problem happens and how many users it affects. Quota is consumed by events, not issues.
- The list shows issue type and description, project, and first and last seen. For error issues, hovering the title shows the latest event's stack trace, and the colour square shows its level (error, info, fatal, warning, debug or sample).
- Filter by properties such as browser, device, impacted users or whether an error is unhandled.
- Triage tabs and their queries: All Unresolved (`is:unresolved`), For Review (`is:unresolved is:for_review`, new issues or regressions not yet reviewed), Regressed (`is:regressed`, resolved issues that came back), Archived (`is:archived`), Escalating (`is:escalating`, archived issues over forecast volume).
- Sort by Recommended, Last Seen, First Seen, Trends, Events (total volume) or Users (users affected).

## Firebase Crashlytics
- A realtime crash reporter for Apple, Android, Flutter and Unity apps. It collects crashes, non-fatal exceptions and other events and uses the build's mapping information to make readable reports (for Apple platform apps, dSYM files).
- Its analysis engine groups events into issues using stack trace frames, exception message, error code and other characteristics; all events in an issue share a common point of failure. More matching events move an issue up the Issues table.
- Within an issue, **variants** are sub-groups with the same failure point and a similar stack trace; a different stack trace may mean a different root cause, so inspect the most common variants.
- Alerts exist for new, regressed and growing issues; Crashlytics can record app errors as `app_exception` events in Google Analytics, showing events leading up to a crash. Data can be exported to BigQuery or Cloud Logging.
- Custom logs, keys and non-fatal error tracking are opt-in setup steps described on separate pages not read here.

## Triage information to capture
Release or build, affected users and event counts, first and last seen, whether it is new or a regression, link to the issue in the tool.

## Verify
Crash bugs link the tool issue, quote the exception, include frequency and users affected, and the report resolves to readable frames rather than raw addresses.

## Checked
2026-11-09: checked against the Sentry Issues overview and the Firebase Crashlytics overview, both read in full; the detail pages (Issue Details, symbol upload, stack trace formats) were not read. Removed because those pages do not state them: the stack-trace reading rules (first app frame, `Caused by:` chains, bottom-up Python order), example exception strings, Sentry breadcrumbs, suspect commits and release linking, crash-free users percentage, ProGuard/R8 `mapping.txt` and source map upload requirements, iOS `.ips` file reading, and the Apple source (not fetched). Tags `stack-trace-reading` trimmed.

Method: documentation only; no commands were run.
