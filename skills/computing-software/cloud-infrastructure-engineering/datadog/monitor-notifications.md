---
id: computing-software.cloud-infrastructure-engineering.datadog.monitor-notifications
name: monitor-notifications
category: computing-software
field: cloud-infrastructure-engineering
product: datadog
tags: [datadog, monitor-message, template-variables, conditionals, handles]
level: practitioner
status: docs-checked
description: "Write Datadog monitor messages with template and tag variables, state conditionals, @-notification handles, renotify blocks and test notifications."
sources: ["https://docs.datadoghq.com/monitors/notify/", "https://docs.datadoghq.com/monitors/notify/variables/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Monitor notification messages
Goal: actionable, routed alerts.

```
{{#is_alert}}
CRITICAL: {{host.name}} metric is {{value}} (alert threshold {{threshold}}).
@slack-incident-response
{{/is_alert}}
{{#is_warning}}
Warning on {{host.name}} @ops-team@company.com
{{/is_warning}}
{{#is_recovery}}
Recovered: {{host.name}} @ops-team@company.com
{{/is_recovery}}
```

- Template variables: `{{value}}` (the value that breached, for metric-based monitors), `{{threshold}}`, `{{warn_threshold}}`, `{{comparator}}`, `{{last_triggered_at}}`.
- Tag variables for multi alert monitors: `{{key.name}}` inserts the value of the grouped tag, for example `{{env.name}}` or `{{host.name}}`; if the key contains a period use brackets, `{{[dot.key.test].name}}`. Multiple values show as a comma-separated string.
- State conditionals open with `{{#name}}` and close with `{{/name}}`; the `{{^name}}` form is the negation. Documented names include `is_alert`, `is_warning`, `is_no_data`, `is_recovery`, `is_alert_recovery`, `is_warning_recovery`, `is_alert_to_warning`, `is_no_data_recovery`, `is_match` and `is_exact_match`.
- State blocks cannot be combined, because a monitor is in one state at a time; each needs its own block. Text and handles outside any conditional fire on every state transition.
- `is_match` takes a tag variable and one or more strings, for example `{{#is_match "host.role.name" "db" "database"}}`.
- If you add a handle inside an alert or warning block, the docs recommend a matching recovery block so the handle gets the recovery.
- Handles: type `@` and pick from the drop-down (team member, integration, workflow, case). Examples from the docs: `@slack-incident-response`, `@pagerduty-sre`, `@ops-team@company.com`, `@webhook-<name>`. Leave a space between the last text character and the handle (`low @ops-team@company.com`, not `low@ops-team@company.com`).
- Datadog recommends monitor notification rules to route recipients by tags instead of setting handles on every monitor.
- Renotify: set an interval, the states to renotify from (alert, no data, warn) and an optional limit; put extra detail in a `{{#is_renotify}}` block, since the original message is repeated too.
- Test Notifications (bottom right of the monitor page) sends the chosen transition and group; tests are tagged `[TEST]` in the title and appear in the Event Explorer. It is supported for host, metric, anomaly, outlier, forecast, logs, rum, apm, composite and several other monitor types.

Gotcha: if a monitor recovers because no data matches, the recovery message has no data; group by extra tags to keep them accessible.

## Verify
- Test Notifications for each state reaches the intended destination with variables rendered.

## Checked
2026-11-03. Confirmed against the Monitor Notifications and Monitor Variables pages. Removed: the `{{service.name}}` and `https://wiki.example.net` runbook example, the claim that a wrong handle gives no error, the Terraform versioning and "group related alerts" advice, and secret/PII wording not on the pages.
Method: documentation only; no commands were run.
