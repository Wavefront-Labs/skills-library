---
id: computing-software.email-administration.mailcow.mailcow-dmarc-reporting-with-rspamd
name: mailcow-dmarc-reporting-with-rspamd
category: computing-software
field: email-administration
product: mailcow
tags: [dmarc-reporting, rspamd-dmarc, ofelia, bcc-addrs, report-schedule, parsedmarc]
level: advanced
status: docs-checked
description: "Send DMARC aggregate reports from mailcow using the Rspamd DMARC module, an Ofelia schedule in a compose override and optional BCC copies."
sources: ["https://docs.mailcow.email/post_installation/firststeps-dmarc_reporting/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# DMARC reporting with Rspamd

Reporting is done by the Rspamd DMARC module. All receiving domains on the server report from one reporting domain; the docs recommend the parent domain of `MAILCOW_HOSTNAME` (for `mail.example.com` use `domain = 'example.com'`) and a sender such as `noreply-dmarc@example.com`. Creating that mailbox in mailcow to absorb bounces is optional but recommended. Watch it closely for the first few days.

Enable: create `data/conf/rspamd/local.d/dmarc.conf` with a `reporting { }` block setting `enabled = true`, `email`, `domain`, `org_name`, `helo = 'rspamd'`, `smtp = 'postfix'`, `smtp_port = 25`, `from_name`, `msgid_from`, `max_entries = 2k` and `keys_expire = 2d`.

Schedule: in `docker-compose.override.yml` give `rspamd-mailcow` the label `ofelia.enabled: "true"` and a job `ofelia.job-exec.rspamd_dmarc_reporting_yesterday.schedule: "@every 24h"` that runs `rspamadm dmarc_report` for yesterday's date (guarded by `MASTER=y`), and make `ofelia-mailcow` depend on `rspamd-mailcow`. Then bring the stack up again.

Add `bcc_addrs = ["address1","address2"]` inside `reporting` to receive hidden copies, for verification or to feed ParseDMARC. Rspamd reloads this file in real time.

For higher volume, add a second Ofelia job that runs `dmarc_report` with today's date. The Ofelia schedule uses Go cron syntax. The docs describe checks for the last run, the latest output and manual triggering.

## Checked

2026-11-09. Confirmed on the DMARC reporting page: parent domain recommendation, optional noreply-dmarc mailbox, the dmarc.conf reporting block values, the Ofelia override with the 24h schedule and MASTER guard, bcc_addrs with live reload, the second job for higher volume, Go cron syntax and the troubleshooting checks. No changes needed.

Method: docs-checked 2026-11-09 against the full DMARC reporting page (firststeps-dmarc_reporting.en.md in mailcow-dockerized-docs).
