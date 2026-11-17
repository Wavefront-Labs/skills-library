---
id: computing-software.devops-ci-cd.rundeck.webhook-run-job-plugin
name: webhook-run-job-plugin
category: computing-software
field: devops-ci-cd
product: rundeck
tags: [rundeck, run-job-webhook, post-url, webhook-payload, json-payload]
level: practitioner
status: docs-checked
description: "Trigger a Rundeck job from a JSON webhook, map payload fields to job options, node filter and run-as user, and read the returned execution id."
sources:
  - https://raw.githubusercontent.com/rundeck/docs/4.0.x/docs/manual/webhooks/run-job.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The Run Job webhook event plugin receives a webhook and executes a configured job. It handles JSON payloads only.

Setup: add a new webhook in the UI, pick the *Run Job* event plugin, fill the Plugin Configuration and save. Rundeck then shows a `Post Url`; test it with curl or another API client.

A successful call returns:

```json
{"executionId": "7", "jobId": "<job-uuid>"}
```

Use the execution id to check progress.

Mapping payload data into the configuration fields (options, node filter, run-as user):
- Parsed fields: for `{"field1":"value1","sub1":{"subfield":"subval"}}` use `${data.field1}` or `${data.sub1.subfield}`.
- Whole payload: pass `-whkpayload ${raw}` to an option named `whkpayload`.
- Context: `${webhook.id}`, `${webhook.project}`, `${webhook.sender}` (sender IP), `${webhook.timestamp}` (epoch ms).

Gotcha: options are sent to the job even if the job does not declare them. Reference them in steps as `${option.<name>}`, for example `${option.field1}` or `${option.raw}`.

The Log Data step type (`log-data-step`) shows all variables during an execution, which helps debug mappings.

## Checked

2026-11-04: JSON-only note, setup, response, data mapping, raw payload, context variables and option behaviour confirmed against the Run Job Webhook Plugin page; log-data-step appears in its example job.
Method: documentation only; no commands were run.
