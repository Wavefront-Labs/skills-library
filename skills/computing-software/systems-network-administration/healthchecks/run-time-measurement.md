---
id: computing-software.systems-network-administration.healthchecks.run-time-measurement
name: run-time-measurement
category: computing-software
field: systems-network-administration
product: healthchecks
tags: [healthchecks, run-time, duration-display, start-success-pair, python-start-ping]
level: practitioner
status: docs-checked
description: "Measure script run times in Healthchecks with start and success pings, the 72 hour pairing window, where durations show, and a Python start-ping pattern."
sources:
  - https://raw.githubusercontent.com/healthchecks/healthchecks/master/templates/docs/measuring_script_run_time.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Send `/start` when the job begins and a normal success (or fail) ping when it ends. Execution time is the gap between adjacent start and success events.

Display rules:
- A duration appears in the checks list when a start is followed by a regular ping or fail signal less than 72 hours later.
- Events more than 72 hours apart are treated as unrelated and show no duration.
- Previous run durations also appear on the check's detail page.

Alerting: a start with no success inside the grace time marks the check down and sends alerts.

Python pattern; the try/except keeps a network error from stopping the job:

```python
import requests
URL = "<ping-url>"

try:
    requests.get(URL + "/start", timeout=5)
except requests.exceptions.RequestException:
    pass

# run the job here
requests.get(URL)
```

For concurrent runs, add a `rid` run ID (see ping-run-id). If you cannot append `/start`, use keyword filtering on HTTP bodies to classify pings as start.

## Checked

2026-11-04. Confirmed against the Healthchecks Measuring Script Run Time page: the /start suffix, duration as the gap between adjacent start and success events, the 72 hour display rule, the detail page history, the down-after-grace rule, the Python example with its try and except, the rid run ID pointer and keyword filtering as the alternative to /start. Nothing removed.

Method: documentation only; no commands were run.
