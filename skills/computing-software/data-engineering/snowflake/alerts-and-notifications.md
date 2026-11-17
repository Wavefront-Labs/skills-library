---
id: computing-software.data-engineering.snowflake.alerts-and-notifications
name: alerts-and-notifications
category: computing-software
field: data-engineering
product: snowflake
tags: [snowflake, snowflake-alerts, create-alert, notification-integration, system-send-email, webhook-notification, data-freshness-alert, serverless-alerts]
level: practitioner
status: docs-checked
description: "Alert from inside Snowflake: CREATE ALERT condition and action, schedules, notification integrations (email, Slack/Teams webhooks), freshness and cost alert patterns."
sources:
  - https://docs.snowflake.com/en/user-guide/alerts
  - https://docs.snowflake.com/en/user-guide/notifications/about-notifications
  - https://docs.snowflake.com/en/sql-reference/stored-procedures/system_send_snowflake_notification
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Snowflake alerts and notifications

**Goal:** detect data or cost conditions with a SQL query on a schedule and notify people or systems, without an external scheduler.

## Notification integration
```sql
create notification integration ops_email type = email enabled = true
  allowed_recipients = ('data-oncall@acme.com');

-- webhook (Slack incoming webhook / Teams / PagerDuty)
create secret ops.secrets.slack_webhook type = generic_string secret_string = '<webhook path token>';
create notification integration slack_data_alerts type = webhook enabled = true
  webhook_url = 'https://hooks.slack.com/services/SNOWFLAKE_WEBHOOK_SECRET'
  webhook_secret = ops.secrets.slack_webhook
  webhook_body_template = '{"text": "SNOWFLAKE_WEBHOOK_MESSAGE"}'
  webhook_headers = ('Content-Type'='application/json');
```

## Alert: stale table
```sql
create or replace alert ops.alerts.orders_stale
  warehouse = ops_xs                     -- omit for serverless alerts where available
  schedule = '15 minute'                 -- or 'USING CRON 0 * * * * UTC'
  if (exists (
      select 1 from raw.orders having max(_loaded_at) < dateadd(hour, -2, current_timestamp())))
  then
    call system$send_snowflake_notification(
      snowflake.notification.text_plain('raw.orders has not loaded for 2h'),
      snowflake.notification.integration('slack_data_alerts'));

alter alert ops.alerts.orders_stale resume;     -- alerts are created suspended
```
`system$send_email('ops_email', 'data-oncall@acme.com', 'subject', 'body')` for plain email.

## Patterns
- Freshness and volume checks on critical tables.
- Cost: credits used today by a warehouse above a threshold (see the warehouse metering views for their latency).
- Failed tasks: `information_schema.task_history(...)` filtered to `state = 'FAILED'` in the last interval.
- `SNOWFLAKE.ALERT.LAST_SUCCESSFUL_SCHEDULED_TIME()` / `GET_CONDITION_QUERY_UUID()` let the condition consider only new data since last run.

## Operate
- `show alerts`; run history via the ALERT_HISTORY function (see its reference for the states).
- An alert needs a warehouse or serverless compute; schedule alerts no more often than needed.

## Verify
- [ ] Force the condition (e.g. in a test table) and receive the notification.
- [ ] `alert_history` shows regular runs and no failures.

## Checked
2026-10-28. Confirmed against CREATE NOTIFICATION INTEGRATION (email: TYPE = EMAIL, ALLOWED_RECIPIENTS; webhook: TYPE = WEBHOOK, WEBHOOK_URL, WEBHOOK_SECRET, WEBHOOK_BODY_TEMPLATE, WEBHOOK_HEADERS, SNOWFLAKE_WEBHOOK_SECRET placeholder), the alerts guide (alerts are suspended by default, SNOWFLAKE.ALERT.LAST_SUCCESSFUL_SCHEDULED_TIME, GET_CONDITION_QUERY_UUID, SYSTEM$SEND_EMAIL, serverless alerts) and SYSTEM$SEND_SNOWFLAKE_NOTIFICATION. Removed: alert_history state names, the error_only argument, the metering-view freshness remark and the EXECUTE ALERT privilege note.
Method: documentation only; no commands were run.
