---
id: computing-software.systems-network-administration.healthchecks.curl-options
name: curl-options
category: computing-software
field: systems-network-administration
product: healthchecks
tags: [healthchecks, curl-flags, retry-timeout, silent-ping, bash-ping]
level: intro
status: docs-checked
description: "Choose curl options for Healthchecks pings: -m timeout, --retry, -f, -s, -S and -o /dev/null, with a silent one-liner suitable for scripts and cron."
sources:
  - https://raw.githubusercontent.com/healthchecks/healthchecks/master/templates/docs/bash.md
  - https://raw.githubusercontent.com/healthchecks/healthchecks/master/templates/docs/monitoring_cron_jobs.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Typical ping lines:

```
curl -m 10 --retry 5 <ping-url>
curl -fsS -m 10 --retry 5 -o /dev/null <ping-url>
```

Options:
- `-m 10` (`--max-time`): cap each request at 10 seconds. With retries the timer resets at the start of each attempt.
- `--retry 5`: retry on transient errors (timeouts and HTTP 408, 429, 500, 502, 503, 504). The default delay grows 1s, 2s, 4s, 8s and so on. Default retries is 0.
- `-f` (`--fail`): treat non-200 responses as errors; curl returns error 22.
- `-s`: hide the progress meter and error messages.
- `-S`: show error messages again when used with `-s`.
- `-o /dev/null`: discard stdout; errors still reach stderr.

The silent form prints only on error, which suits cron, where any output may trigger mail.

Chain with `&&` so the ping runs only when the job exits 0. To report failures too, ping `<ping-url>/$?` instead (see ping-exit-status).

Wget or another HTTP client can be used instead of curl.

## Checked

2026-11-04: confirmed against the Shell Scripts page (the two curl lines, each option, retry delays and transient error codes, error 22) and the Monitoring cron jobs page (curl options, && behaviour).
Method: documentation only; no commands were run.
