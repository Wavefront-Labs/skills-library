---
id: computing-software.data-science-and-analytics.apache-superset.alerts-reports-slack-webhook-limits
name: alerts-reports-slack-webhook-limits
category: computing-software
field: data-science-and-analytics
product: apache-superset
tags: [alerts-reports, slack, webhook, execution-budget, timeouts]
level: advanced
status: docs-checked
description: "Superset Alerts and Reports Slack, webhook and execution budget settings: scopes, retry and timeout defaults, HTTPS-only webhooks."
sources:
  - https://github.com/apache/superset/blob/master/docs/admin_docs/configuration/alerts-reports.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: tune delivery channels and time budgets for reports.

Slack: `SLACK_API_TOKEN` is the Bot User OAuth token (`xoxb-...`); enable `ALERT_REPORT_SLACK_V2`. Required scopes: `incoming-webhook`, `files:write`, `chat:write`, `channels:read`, `groups:read`. Settings:
- `SLACK_TEAM_ID` (default `None`; only for org-scoped tokens).
- `SLACK_API_TIMEOUT = 30`, `SLACK_SEND_RETRY_MAX_TIME = 150`.
- `SLACK_API_RATE_LIMIT_RETRY_COUNT` default `2`.
- `SLACK_CACHE_TIMEOUT` default 86400 seconds.
- `SLACK_CHANNEL_REFRESH_COOLDOWN_SECONDS = 300`.
The Celery task `slack.cache_channels` warms the channel cache.

Webhooks (flag `ALERT_REPORT_WEBHOOK`): `ALERT_REPORTS_WEBHOOK_HTTPS_ONLY` enforces HTTPS URLs; `ALERT_REPORTS_WEBHOOK_TIMEOUT = 60` seconds (`None` disables).

Execution budget:
- `ALERT_REPORTS_EXECUTION_BUDGET_SECONDS = 3600`.
- Reserves: `..._CAPTURE_RESERVE_SECONDS = 60`, `..._DELIVERY_RESERVE_SECONDS = 120`, `..._CLEANUP_RESERVE_SECONDS = 30`, `..._HARD_TIMEOUT_GRACE_SECONDS = 30`.
- `ALERT_REPORTS_RETRY_MAX_DELAY_SECONDS`.
- `ALERT_REPORTS_CSV_REQUEST_TIMEOUT = 60`; `ALERT_REPORTS_CSV_REQUEST_RETRY` defaults `False`.

Other: `ALERT_REPORTS_ENABLE_LINK_REDIRECT` defaults `True`; `ALERT_REPORTS_EXECUTORS` is deprecated (example `[FixedExecutor("admin")]`); `ALERT_MINIMUM_INTERVAL` and `REPORT_MINIMUM_INTERVAL` are fallbacks, deprecated in favour of UI configuration.

## Checked

2026-11-08. Confirmed against the Alerts and Reports page (read in full): Slack scopes and settings with defaults, slack.cache_channels, webhook flag, HTTPS-only and timeout settings, execution budget and reserve values, retry and CSV request settings, link redirect default, executors and minimum interval deprecations. Nothing removed.
Method: documentation only; no commands were run.
