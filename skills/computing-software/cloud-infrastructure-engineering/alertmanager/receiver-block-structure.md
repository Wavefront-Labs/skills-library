---
id: computing-software.cloud-infrastructure-engineering.alertmanager.receiver-block-structure
name: receiver-block-structure
category: computing-software
field: cloud-infrastructure-engineering
product: alertmanager
tags: [alertmanager, receivers, receiver-block, integrations]
level: intro
status: docs-checked
description: "The receiver block: unique name, optional labels, and the list of supported integration config sections such as slack_configs and webhook_configs."
sources: ["https://prometheus.io/docs/alerting/latest/configuration/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# The receiver block

A receiver is a named configuration of one or more notification integrations. Fields:

- `name`: the unique name, referenced by routes.
- `labels`: labels attached to the receiver for querying and filtering.
- One list per integration type.

Supported integration lists in the reference: `discord_configs`, `email_configs`, `mattermost_configs`, `msteams_configs`, `msteamsv2_configs`, `jira_configs`, `opsgenie_configs`, `pagerduty_configs`, `incidentio_configs`, `pushover_configs`, `rocketchat_configs`, `slack_configs`, `sns_configs`, `telegram_configs`, `victorops_configs`, `webex_configs`, `webhook_configs`, `wechat_configs`.

```yaml
receivers:
- name: 'team-X-pager'
  email_configs:
  - to: 'team-X+alerts-critical@example.org'
  pagerduty_configs:
  - routing_key: <key>
```

A receiver can mix several integrations, as above, so one route can notify by email and PagerDuty together.

Note from the reference: when the moratorium on new receivers was lifted, it was agreed that new notification integrations require a committed maintainer with push access, in addition to existing requirements.

Most integrations share `send_resolved` and an `http_config` that defaults to `global.http_config`. Default values of `send_resolved` differ per integration.

## Checked

2026-11-03. Confirmed against the Alertmanager Configuration page (prometheus.io/docs/alerting/latest/configuration): receiver block, labels, integration lists.

Method: documentation only; no commands were run.
