---
id: computing-software.data-engineering.databricks.databricks-sql-alerts
name: databricks-sql-alerts
category: computing-software
field: data-engineering
product: databricks
tags: [databricks, databricks-sql-alerts, sql-alerts, data-alerting, notification-destinations, alert-task, sql-warehouse]
level: practitioner
status: docs-checked
description: "Databricks SQL alerts: scheduled query conditions, OK/TRIGGERED/ERROR states, notification destinations and running alerts as job tasks."
sources:
  - https://docs.databricks.com/aws/en/sql/user/alerts/
  - https://docs.databricks.com/aws/en/jobs/sql
  - https://docs.databricks.com/aws/en/admin/workspace-settings/notification-destinations
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Databricks SQL alerts

**Goal:** a data condition (data quality issue, cost spike, slow query, unusual activity) notifies its owner automatically, without a custom script.

## 1. What alerts do
Alerts run a query on a schedule and notify you when a condition you define is met against the result. You can view alert history to review past evaluations. Documented uses: business KPIs (including Unity Catalog metric views referenced by fully qualified name), data quality and anomaly detection, usage and cost from system tables, SQL warehouse and query health, audit log events, and agent quality metrics.

## 2. Latest alerts versus legacy alerts
- Each alert owns its query definition, written in the alert editor; an existing saved query cannot be reused when creating an alert.
- Evaluations resolve to OK, TRIGGERED or ERROR; the UNKNOWN status of legacy alerts is gone. Treat ERROR as something to notice, since a broken query stops the monitoring.
- Latest and legacy alerts can run side by side during a transition.
- Related pages (not read for this skill): Create an alert, SQL alert webhook payload, Manage alerts, Alert query patterns.

## 3. Alerts as job tasks
In a job, add a task of type SQL and choose **Alert** to evaluate a SQL alert on the specified warehouse, optionally adding subscribers to notify with the results. This lets condition checks run on a pipeline trigger so downstream tasks can branch on the result. The SQL task needs Databricks SQL and a serverless or pro SQL warehouse. Job parameters are not passed to an alert through the generic SQL task; use the SQL alert task for that.

## 4. Notification destinations
- Workspace admins manage destinations (Settings > Notifications > Manage > Add destination); once configured they are available to all users.
- Types: Email, Slack, Webhook (optional OAuth, Beta), Microsoft Teams, PagerDuty. Slack and Teams can also use the Databricks Genie app (Beta), which supports SQL alerts.
- Webhook destinations must use HTTPS with a certificate signed by a trusted CA, and the receiver must allowlist the workspace control plane and data plane outbound IP addresses. The SQL alert webhook payload is sent after a state change.
- Use different credentials (webhook URL, integration key, username/password or client credentials) for each destination, so one can be revoked without affecting others.
- Slack and Teams destinations do not support HTML in custom notification bodies; some support markdown. Email recipient addresses are limited to 1,300 characters.

## Verify
- [ ] The alert reaches its destination when its condition is met, and ERROR evaluations are noticed.
- [ ] Each destination uses its own credentials and the receiving endpoint allows the Databricks IP ranges.

## Checked

2026-11-09. Read in full the Databricks SQL alerts overview, SQL task for jobs and Manage notification destinations pages. Confirmed the states, legacy differences, alert job task, destination types and networking and credential guidance. Removed, as not stated on those pages: the example freshness, DQ and volume queries, one-row result rules, comparison operators, empty-result handling, schedule and warehouse-size advice, template variables, notify-on-change defaults, the alerts REST API path, Terraform support and permission levels. The Create an alert page was not among the sources, so these details are left out rather than guessed.

Method: documentation only; no commands were run.
