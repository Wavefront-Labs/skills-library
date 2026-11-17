---
id: computing-software.systems-network-administration.healthchecks.cron-job-monitoring
name: cron-job-monitoring
category: computing-software
field: systems-network-administration
product: healthchecks
tags: [healthchecks, crontab, cron-monitoring, curl-and-chain, heartbeat]
level: intro
status: docs-checked
description: "Add Healthchecks heartbeat monitoring to a crontab entry by chaining a curl ping after the job, and what failures this detects compared with MAILTO."
sources:
  - https://raw.githubusercontent.com/healthchecks/healthchecks/master/templates/docs/monitoring_cron_jobs.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Steps: create a check, copy its ping URL, append a curl call to the crontab entry.

Before:

```
8 6 * * * /path/to/backup.sh
```

After:

```
8 6 * * * /path/to/backup.sh && curl -fsS -m 10 --retry 5 -o /dev/null <ping-url>
```

`&&` runs curl only if the script exits 0, avoiding false success signals. Alternatively put the curl line last inside the script to keep the crontab short.

This heartbeat detects: the machine being down, cron not running or misconfigured, a non-zero exit, and a job running abnormally long. No new software is needed when curl or wget exists.

Set grace time above the job's typical runtime, and configure several notification channels for redundancy.

Why not MAILTO? It needs a working MTA, will not alert if the machine is off or offline, and any stdout output mails on every run, causing alert fatigue.

Extras: signal failures actively, send a start signal to time the run, and POST stdout/stderr to attach logs.

## Checked

2026-11-04: confirmed against the Monitoring cron jobs page (curl line with && and -fsS -m 10 --retry 5 -o /dev/null, failure modes, grace time, redundancy, MAILTO drawbacks, advanced techniques).
Method: documentation only; no commands were run.
