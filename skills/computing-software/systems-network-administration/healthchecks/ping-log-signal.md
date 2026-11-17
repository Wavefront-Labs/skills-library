---
id: computing-software.systems-network-administration.healthchecks.ping-log-signal
name: ping-log-signal
category: computing-software
field: systems-network-administration
product: healthchecks
tags: [healthchecks, log-signal, events-log, diagnostic-events]
level: practitioner
status: docs-checked
description: "Use the Healthchecks /log endpoint to record diagnostic events with a Log label in a check's Events section without changing the check's status."
sources:
  - https://raw.githubusercontent.com/healthchecks/healthchecks/master/templates/docs/http_api.md
  - https://raw.githubusercontent.com/healthchecks/healthchecks/master/templates/docs/attaching_logs.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The log signal records an event in the check's "Events" section, labelled "Log". The check's status does not change, so it is safe for progress notes or warnings from a job that is still running.

- UUID form: `<ping-url>/log`
- Slug form: `<ping-key>/<slug>/log`

Send text with a POST body:

```
curl -fsS -m 10 --retry 5 --data-raw "step 3 of 5 done" <ping-url>/log
```

Details:
- Like other pings, the body is stored only up to the server's ping body limit.
- The optional `rid` query parameter is accepted.
- Use it for non-state information; use `/fail`, `/start` or the bare URL when you want the status to change.

To read the stored text: open the check, go to Events, click the event, and choose "Download Original" for the exact submitted body.

## Checked

2026-11-04: confirmed against the Pinging API page (/log, Log label, status unchanged, rid parameter) and the Attaching Logs page (POST body, Events, Download Original). Removed the claim that rid is not used for duration matching, which the page does not state.
Method: documentation only; no commands were run.
