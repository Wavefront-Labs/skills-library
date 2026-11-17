---
id: computing-software.systems-network-administration.healthchecks.email-pinging
name: email-pinging
category: computing-software
field: systems-network-administration
product: healthchecks
tags: [healthchecks, email-pinging, ping-by-email, newsletter-monitoring, backup-reports]
level: practitioner
status: docs-checked
description: "Monitor jobs by sending email to a Healthchecks check's address: default success semantics, keyword classification, use cases and delivery-delay caveats."
sources:
  - https://raw.githubusercontent.com/healthchecks/healthchecks/master/templates/docs/email.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Email checks are an alternative to HTTP pings. Each check has a special address; any email received there counts as a success signal.

Optional keyword filtering looks at the subject or body and classifies each email as start, success or failure. Keywords are case-sensitive ("Error" differs from "error"). Order: failure first, then success, then start. When filtering is on and nothing matches, "If no keywords match" ignores the email or treats it as failure. Configure in the Filtering Rules dialog.

Use cases:
- Newsletter delivery: add the check's address to the recipient list of a weekly newsletter job and set the Period to 1 week. A separate check can watch the cron job itself.
- Backup reports: have the backup software email the check's address after each run, with success and failure keywords. Healthchecks stays quiet while success reports arrive on time, and alerts on a missing report or a failure report.

Caveats:
- Email is more prone to random delays than HTTP, so increase grace time.
- Start and success durations are less accurate over email and may not suit very quick jobs.

Self-hosted: the instance needs the SMTP listener (see self-hosted-email-receiving).

## Checked

2026-11-04. Confirmed against the Healthchecks Email page: any email counts as success by default, case-sensitive keywords, failure then success then start matching order, the If no keywords match options, the Filtering Rules dialog, both use cases (1 week period for newsletters), and the delivery-delay and duration-accuracy caveats. Nothing removed.

Method: documentation only; no commands were run.
