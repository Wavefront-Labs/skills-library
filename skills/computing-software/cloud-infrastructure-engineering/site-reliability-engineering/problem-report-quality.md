---
id: computing-software.cloud-infrastructure-engineering.site-reliability-engineering.problem-report-quality
name: problem-report-quality
category: computing-software
field: cloud-infrastructure-engineering
product: site-reliability-engineering
tags: [problem-report, bug-tracking, troubleshooting, issue-template, triage, problem-report-template, bug-report-quality]
level: practitioner
status: docs-checked
description: "Get problem reports that can be acted on: expected vs actual behaviour and reproduction, a consistent searchable form, and a bug for every issue."
sources: ["https://sre.google/sre-book/effective-troubleshooting/"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Problem report quality

Per the SRE Book chapter on effective troubleshooting, every problem starts with a problem report, which may be an
automated alert or a colleague saying "the system is slow".

## What a good report holds
An effective report tells you the expected behaviour, the actual behaviour and, if possible, how to reproduce it.
Add whatever else helps you diagnose your own systems; the Book notes teams often use customised forms or small web
apps that ask for system-specific details and then generate and route a bug automatically.

## Where reports live
- Use a consistent form stored in a searchable location such as a bug tracking system.
- Open a bug for every issue, even those received by email or instant message; it leaves a log of investigation and
  remediation that can be referenced later.
- Many Google teams discourage reporting a problem directly to a person: it adds a transcription step, produces
  lower-quality reports that other team members cannot see, and concentrates the load on the few people the reporter
  happens to know rather than the person on duty.
- The report form is a good place to give reporters tools to self-diagnose or self-repair common issues.

## Alerts as reports
The Book's worked example has the alerting system file a bug automatically, with links to the black-box prober's recent
results and to the playbook entry for the alert, assigned to the on-call.

## Checked
2026-11-01. Confirmed against the SRE Book chapter "Effective Troubleshooting" (Problem Report section and its
Shakespeare example). Removed: the seven-field minimum list beyond expected, actual and reproduction, the GitHub issue
form and its source (page not read), the triage questions, the 80 percent target and the triage SLA example.
Method: documentation only; no commands were run.
