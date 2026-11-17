---
id: computing-software.systems-network-administration.healthchecks.ping-exit-status
name: ping-exit-status
category: computing-software
field: systems-network-administration
product: healthchecks
tags: [healthchecks, exit-status, exit-code, dollar-question-mark]
level: intro
status: docs-checked
description: "Pass a process exit code to Healthchecks by appending it to the ping URL: 0 means success, 1 to 255 mean failure, with UUID and slug forms."
sources:
  - https://raw.githubusercontent.com/healthchecks/healthchecks/master/templates/docs/http_api.md
  - https://raw.githubusercontent.com/healthchecks/healthchecks/master/templates/docs/signaling_failures.md
  - https://raw.githubusercontent.com/healthchecks/healthchecks/master/templates/docs/monitoring_systemd_tasks.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The exit status signal is the ping URL plus `/<exit-status>`, where the value is an integer 0 to 255.

- UUID form: `<ping-url>/<exit-status>`
- Slug form: `<ping-key>/<slug>/<exit-status>`
- 0 counts as success; any other value counts as failure.

Shell usage, right after the command whose result you are reporting:

```
#!/bin/sh
/usr/bin/certbot renew
curl --retry 3 <ping-url>/$?
```

`$?` must be read before any other command runs, since it holds only the last status.

Slug endpoints respond 400 for an invalid URL format and 404 when the ping key does not match a project.

systemd can do the same with `ExecStopPost` and `${EXIT_STATUS}` (see systemd-curl). For pipelines, set `pipefail` first so the status reflects any failing stage (see shell-pipefail).

## Checked

2026-11-04: confirmed against the Pinging API page (exit status 0-255, 0 success, 400 and 404 codes for slug form), Signaling failures page ($? example) and Monitoring systemd tasks page (ExecStopPost and EXIT_STATUS). Changed the curl example to the page's `--retry 3`. The pipefail pointer is not covered by these pages.
Method: documentation only; no commands were run.
