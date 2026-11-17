---
id: computing-software.cloud-infrastructure-engineering.aws.fis-experiment-reports-and-logs
name: fis-experiment-reports-and-logs
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, fault-injection-service, fis, experiment-report, experiment-logging, chaos-engineering, evidence]
level: practitioner
status: docs-checked
description: "Evidence from AWS FIS experiments: experiment logging to CloudWatch Logs or S3, automatic PDF experiment reports with dashboard widgets, EventBridge state events and history."
sources: ["https://docs.aws.amazon.com/fis/latest/userguide/stop-conditions.html", "https://docs.aws.amazon.com/fis/latest/userguide/fis-actions-reference.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# FIS experiment reports and logs

## Experiment logging
In the template:
```json
"logConfiguration": {
  "logSchemaVersion": 2,
  "cloudWatchLogsConfiguration": {"logGroupArn": "arn:aws:logs:<REGION>:<ACCOUNT_ID>:log-group:/fis/experiments:*"},
  "s3Configuration": {"bucketName": "<LOG_BUCKET>", "prefix": "experiments/"}}
```
- `logSchemaVersion` is required; CloudWatch Logs takes a `logGroupArn`, S3 takes a `bucketName` and optional `prefix`.
- The experiment role needs permissions to deliver to the log destination (see the FIS logging page).

## Experiment reports
```json
"experimentReportConfiguration": {
  "outputs": {"s3Configuration": {"bucketName": "<REPORT_BUCKET>", "prefix": "reports/"}},
  "dataSources": {"cloudWatchDashboards": [{"dashboardIdentifier": "arn:aws:cloudwatch::<ACCOUNT_ID>:dashboard/orders-slo"}]},
  "preExperimentDuration": "PT20M", "postExperimentDuration": "PT20M"}
```
- `outputs` sets the S3 destination; `dataSources.cloudWatchDashboards` lists dashboards to include;
  `preExperimentDuration` and `postExperimentDuration` are ISO 8601 durations (`PT20M`).
- Good evidence for resilience reviews, audits and post-game-day write-ups.

## History and events
```bash
aws fis list-experiments --query 'experiments[].[id,state.status,creationTime]' --output table
aws fis get-experiment --id EXP123 --query 'experiment.[state,actions]'
```
- A stop condition stops the experiment when its CloudWatch alarm fires; treat that as a finding, not a failure of the tool.

## Write-up template
Hypothesis, scope (targets), expected behaviour, observed behaviour (report graphs), findings with
owners, follow-up experiment date.

## Verify
- [ ] Last experiment has logs with resolved targets and a generated report in S3.

## Checked
2026-10-28: Confirmed by the botocore fis model (CreateExperimentTemplate: logConfiguration with logSchemaVersion, cloudWatchLogsConfiguration.logGroupArn, s3Configuration.bucketName/prefix; experimentReportConfiguration with outputs, dataSources.cloudWatchDashboards, preExperimentDuration, postExperimentDuration) and the FIS stop-conditions page. The list-experiments and get-experiment commands passed check_commands.py. Read end to end. Removed as unconfirmed: the list of what logs record, log and report IAM permission names, the PDF/summary description, EventBridge source and states. Replaced real-looking account IDs with placeholders; sources now point to the FIS User Guide.

Method: documentation only; no commands were run.
