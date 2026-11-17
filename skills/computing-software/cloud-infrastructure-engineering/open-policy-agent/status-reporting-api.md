---
id: computing-software.cloud-infrastructure-engineering.open-policy-agent.status-reporting-api
name: status-reporting-api
category: computing-software
field: cloud-infrastructure-engineering
product: open-policy-agent
tags: [status-api, status-plugin, bundle-status, status-trigger, fleet-monitoring]
level: practitioner
status: docs-checked
description: "Make OPA push status reports to a remote service: triggering events, the POST /status contract and partition names, labels, bundle fields and manual trigger mode."
sources:
  - https://www.openpolicyagent.org/docs/management-status
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: track bundle activation and plugin health across a fleet of OPA instances.

OPA periodically reports status to a remote HTTP service. It sends a report when:
- a bundle is downloaded and activated; failures carry error information, and this includes discovery bundles
- any plugin state changes (all plugin status is reported with the latest state)
- a decision log upload is attempted; failures carry error information

Set `status.trigger` to `manual` and those events no longer send reports by themselves; reports go out only when the status plugin is triggered.

The service must accept:

```
POST /status[/<partition_name>] HTTP/1.1
Content-Type: application/json
```

The optional partition name routes updates to different backends; without it, updates go to `/status`.

Every report carries `labels` that identify the instance. OPA adds `id` (globally unique per running instance) and `version` (the OPA version) automatically, alongside any labels you configure such as `app`.

Per bundle the report includes `active_revision`, `last_request`, `last_successful_request`, `last_successful_download`, `last_successful_activation`, and `metrics` timers such as `timer_rego_module_compile_ns`.

Use the timestamps to alert on bundles whose `last_successful_activation` is stale, which signals a broken distribution path rather than a broken policy.

Check: point `status` at a local listener and confirm a report arrives after loading a bundle, with your `app` label and the generated `id`.

## Checked

Trigger events, the manual trigger mode, the POST contract, partition names, labels and bundle fields were confirmed against the Status page.

Method: docs-checked 2026-11-09 against the OPA docs management-status page (docs/docs/management-status.md in the OPA repository, full file read).
