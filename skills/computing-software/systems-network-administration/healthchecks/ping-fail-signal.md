---
id: computing-software.systems-network-administration.healthchecks.ping-fail-signal
name: ping-fail-signal
category: computing-software
field: systems-network-administration
product: healthchecks
tags: [healthchecks, fail-signal, failure-alerts, faster-alerts]
level: intro
status: docs-checked
description: "Report a failed job to Healthchecks with the /fail suffix or an exit status so alerts arrive immediately instead of after the grace time."
sources:
  - https://raw.githubusercontent.com/healthchecks/healthchecks/master/templates/docs/signaling_failures.md
  - https://raw.githubusercontent.com/healthchecks/healthchecks/master/templates/docs/http_api.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Without a failure signal, a broken job is noticed only when its expected success ping is missing and grace time runs out. Signalling the failure directly shortens the time to the alert.

Two ways:
- Append `/fail` to the ping URL (UUID or slug form).
- Append `/<exit-status>`, an integer 0 to 255. 0 is success, any other value is failure.

Shell: run the command, then ping with the special variable `$?` (last exit status):

```
/path/to/job.sh
curl --retry 3 <ping-url>/$?
```

Python: use `try` / `finally`; ping the normal URL when the work succeeds and the `/fail` URL otherwise.

If separate URLs are impractical, configure keyword matching so the server classifies HTTP request bodies as success or failure (see keyword-filtering).

Related: `/log` records an event without changing the check's status.

## Checked

2026-11-04: confirmed against the Signaling failures page and Pinging API page (/fail, exit status 0-255, $? example, try/finally Python, keyword alternative, /log). Changed the curl example to the page's `--retry 3`.
Method: documentation only; no commands were run.
