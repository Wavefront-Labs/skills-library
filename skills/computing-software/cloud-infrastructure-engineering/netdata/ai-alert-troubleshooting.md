---
id: computing-software.cloud-infrastructure-engineering.netdata.ai-alert-troubleshooting
name: ai-alert-troubleshooting
category: computing-software
field: cloud-infrastructure-engineering
product: netdata
tags: [netdata, ai-troubleshooting, ask-ai, ai-credits]
level: intro
status: docs-checked
description: "Start a Netdata Cloud AI alert investigation from the Alerts tab, Insights tab or an alert email, and know the wait time, plan access and usage limits."
sources:
  - https://raw.githubusercontent.com/netdata/netdata/master/docs/troubleshooting/troubleshoot.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Three ways to start an investigation:
- Alerts tab: click Ask AI next to any active or recent alert.
- Insights tab: choose Alert Troubleshooting in the investigations section, then pick a recent alert from the dropdown.
- Alert email: click the Troubleshoot with AI link.

Results:
- Reports typically take 1-2 minutes.
- The report shows in the Alerts tab, a copy is saved under Investigations in the Insights tab, and you get an email summary.

Access and limits:
- Generally available in Netdata Cloud on Business and Free Trial plans.
- Eligible Spaces get 10 free AI runs per month; extra runs use AI Credits.
- Check credit usage at Settings, Usage and Billing, AI Credits.

## Checked

2026-11-04: the three start points, the 1-2 minute report time, where the report and email appear, plan availability, the 10 free runs per month and the AI Credits path confirmed against the Netdata AI-Powered Alert Troubleshooting page. Removed the Cloud-only gotcha and the verify line (not stated on the page).

Method: documentation only; no commands were run.
