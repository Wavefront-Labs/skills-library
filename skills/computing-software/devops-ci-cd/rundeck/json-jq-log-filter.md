---
id: computing-software.devops-ci-cd.rundeck.json-jq-log-filter
name: json-jq-log-filter
category: computing-software
field: devops-ci-cd
product: rundeck
tags: [rundeck, jq-filter, log-filter, data-context, step-output]
level: practitioner
status: docs-checked
description: "Capture values from JSON step output into Rundeck data variables with the JSON jq key/value mapper log filter and reuse them in later steps."
sources:
  - https://raw.githubusercontent.com/rundeck/docs/4.0.x/docs/manual/log-filters/json-jq.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The JSON jq key/value mapper log filter parses JSON in a step's output and creates key-value variables in the Rundeck data context, using jq queries.

Fields:
- jq Filter (required): jq-style query run against the log output of the step the filter is attached to.
- Prefix (optional): prefix used for the variable key in the data context.
- Log Data: if checked, logs the captured data to the job's log stream.

Walkthrough from the page: run an HTTP Request node step against the Rundeck API using a working API token, attach the filter to that step, and run the job. The filter produces a data variable which later steps can read.

Steps:
1. Add a step that prints JSON (for example an HTTP Request step).
2. Add the JSON jq key/value mapper filter to that step with your jq query.
3. Reference the resulting variable in a later step.

Verify by ticking Log Data and checking the variable appears in the log.

## Checked

2026-11-04. Confirmed against the Rundeck docs page JSON jq key/value mapper: the three fields (jq Filter required, Prefix optional, Log Data), creation of data context variables, and the HTTP Request node step walkthrough. Nothing removed.

Method: documentation only; no commands were run.
