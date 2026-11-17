---
id: computing-software.systems-network-administration.healthchecks.cron-troubleshooting
name: cron-troubleshooting
category: computing-software
field: systems-network-administration
product: healthchecks
tags: [healthchecks, timedatectl, journalctl-cron, timezone-mismatch, late-pings]
level: practitioner
status: docs-checked
description: "Troubleshoot a cron job monitored by Healthchecks: check the server time zone with timedatectl, read cron logs with journalctl, and confirm the ping and grace settings."
sources:
  - https://raw.githubusercontent.com/healthchecks/healthchecks/master/templates/docs/monitoring_cron_jobs.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Pings consistently an hour early or late: the server time zone probably differs from the check's. Inspect it:

```
timedatectl status
```

Read the `Time zone:` line (it may look like `Europe/Riga (EET, +0200)`), then match the check's time zone setting.

Cron logs on systemd-based systems:

```
# follow live
journalctl -f

# cron daemon logs from the last hour
journalctl --since "1 hour ago" -t CRON
```

Checklist:
- Did you replace the placeholder with the real ping URL?
- Does the curl line use `&&` so it runs only after success?
- `-f` makes non-200 replies errors; `--retry` covers only transient errors (timeouts and 5xx).
- Is grace time longer than the job's normal runtime?
- Does the check use a cron schedule needing the right time zone, or a simple schedule that ignores time of day?
- Are several notification channels configured, so one outage does not hide the alert?

## Checked

2026-11-04: confirmed against the Monitoring cron jobs page (time zone mismatch, timedatectl status, journalctl -f and journalctl --since "1 hour ago" -t CRON, curl options, grace time, notification redundancy).
Method: documentation only; no commands were run.
