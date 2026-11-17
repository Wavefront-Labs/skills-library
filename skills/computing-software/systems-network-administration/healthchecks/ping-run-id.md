---
id: computing-software.systems-network-administration.healthchecks.ping-run-id
name: ping-run-id
category: computing-software
field: systems-network-administration
product: healthchecks
tags: [healthchecks, run-id, rid-parameter, concurrent-runs]
level: advanced
status: docs-checked
description: "Use the rid query parameter on Healthchecks pings to pair start and finish signals for concurrent job runs, and know how it changes alerting."
sources:
  - https://raw.githubusercontent.com/healthchecks/healthchecks/master/templates/docs/measuring_script_run_time.md
  - https://raw.githubusercontent.com/healthchecks/healthchecks/master/templates/docs/http_api.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
When several instances of a job run at once, durations may be computed wrongly. Pass a run ID in the `rid` query parameter on each ping of one execution.

Format:
- A UUID in canonical form, without curly braces; upper or lower case letters.
- Random or deterministic, as long as the start and completion pings of one execution share it.

Shell example:

```
RID=`uuidgen`
curl -fsS -m 10 --retry 5 "<ping-url>/start?rid=$RID"
# ... run the job ...
curl -fsS -m 10 --retry 5 "<ping-url>?rid=$RID"
```

Accepted on all signals (success, start, fail, log, exit status).

Effects:
- The Events section shows a shortened run ID.
- Alerting changes: only the most recently started run is monitored, not every concurrent run. A slow earlier run may not alert if the latest run finishes within the grace time.
- Without run IDs, a success not preceded by a start shows no execution time.

## Checked

2026-11-04: confirmed against the Measuring Script Run Time page (rid format, uuidgen example, shortened IDs in Events, most-recent-run alerting caveat) and the Pinging API page (rid on all endpoints). Removed the claim that rid is not used on the log signal, which the page does not state.
Method: documentation only; no commands were run.
