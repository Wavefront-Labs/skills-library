---
id: computing-software.cloud-infrastructure-engineering.alertmanager.opsgenie-receiver-fields
name: opsgenie-receiver-fields
category: computing-software
field: cloud-infrastructure-engineering
product: alertmanager
tags: [alertmanager, opsgenie-config, responders, priority]
level: practitioner
status: docs-checked
description: "opsgenie_configs fields: api_key, message limit of 130 characters, responders, tags, priority P1 to P5, update_alerts default false."
sources: ["https://prometheus.io/docs/alerting/latest/configuration/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# opsgenie_configs

```yaml
receivers:
- name: ops
  opsgenie_configs:
  - api_key_file: /path/to/opsgenie-key
    priority: P2
    tags: 'prod,database'
    responders:
    - name: db-team
      type: team
```

Fields and defaults:
- `send_resolved`: default `true`.
- `api_key` (default `global.opsgenie_api_key`) or `api_key_file` (default `global.opsgenie_api_key_file`); the file form conflicts with `api_key`.
- `api_url`: default `global.opsgenie_api_url`.
- `message`: alert text limited to 130 characters; default `opsgenie.default.message` template.
- `description`, `source`: default `opsgenie.default.description` and `opsgenie.default.source`.
- `details`: key/value pairs; all common labels are included by default.
- `tags`: comma-separated list. `note`: additional alert note. `entity`: domain the alert relates to. `actions`: comma-separated actions.
- `priority`: P1, P2, P3, P4 or P5.
- `update_alerts`: default `false`. By default the alert is never updated in OpsGenie and a new message only appears in the activity log.

Responders: exactly one of `id`, `name` or `username` per entry, plus required `type`, one of `team`, `teams`, `user`, `escalation` or `schedule`. The `teams` type uses `name` and may hold a comma-separated list of team names; an empty list configures no responders.

## Checked

2026-11-03. Confirmed against the Alertmanager Configuration page (prometheus.io/docs/alerting/latest/configuration): opsgenie_config and responder fields.

Method: documentation only; no commands were run.
