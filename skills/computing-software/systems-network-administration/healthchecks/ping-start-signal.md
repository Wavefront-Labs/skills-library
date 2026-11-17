---
id: computing-software.systems-network-administration.healthchecks.ping-start-signal
name: ping-start-signal
category: computing-software
field: systems-network-administration
product: healthchecks
tags: [healthchecks, start-signal, execution-time, job-timeout]
level: practitioner
status: docs-checked
description: "Send the optional Healthchecks /start signal so a job's duration is measured and a run that never completes within grace time is marked down."
sources:
  - https://raw.githubusercontent.com/healthchecks/healthchecks/master/templates/docs/http_api.md
  - https://raw.githubusercontent.com/healthchecks/healthchecks/master/templates/docs/measuring_script_run_time.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Append `/start` to a check's ping URL when the job begins.

- UUID form: `<ping-url>/start`
- Slug form: `<ping-key>/<slug>/start`

Effects:
- The check shows as "Started" and the start event is stored.
- Execution time is the gap between a start event and the following success or fail event.
- Grace time then also limits how long the run may take. If a start arrives and no success signal follows within the grace time, the check is marked down and alerts are sent.

Start is optional: success-only pings still work, but without durations or long-run detection.

Guard against the start ping itself blocking the job. Give the request a timeout and swallow network errors, so a failed start ping never stops the real work:

```
curl -fsS -m 10 --retry 5 <ping-url>/start
```

If you cannot change the URL on the client, keywords in the HTTP request body can classify a ping as start (see the keyword-filtering skill).

## Checked

2026-11-04: confirmed against the Pinging API page and Measuring Script Run Time page (start endpoints, durations, down after start without success within grace time, curl example).
Method: documentation only; no commands were run.
