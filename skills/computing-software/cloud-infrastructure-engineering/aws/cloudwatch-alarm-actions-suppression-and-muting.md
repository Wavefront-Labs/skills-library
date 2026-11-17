---
id: computing-software.cloud-infrastructure-engineering.aws.cloudwatch-alarm-actions-suppression-and-muting
name: cloudwatch-alarm-actions-suppression-and-muting
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, cloudwatch, alarm-mute, actions-suppressor, composite-alarms, maintenance-windows, alarm-noise]
level: practitioner
status: docs-checked
description: "Silence CloudWatch alarm notifications, keep state: composite alarm actions suppressors, disabling actions for maintenance, scheduled muting, and avoiding forgotten mutes."
sources: ["https://docs.aws.amazon.com/AmazonCloudWatch/latest/APIReference/API_PutCompositeAlarm.html", "https://docs.aws.amazon.com/AmazonCloudWatch/latest/APIReference/API_PutAlarmMuteRule.html", "https://docs.aws.amazon.com/AmazonCloudWatch/latest/APIReference/API_DisableAlarmActions.html", "https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/cloudwatch_limits.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# CloudWatch alarm actions suppression and muting

**Goal:** alarms keep evaluating (state history stays accurate) while notifications are held back
during deployments, maintenance, or when a parent problem already paged someone.

## Composite alarm actions suppressor
```bash
aws cloudwatch put-composite-alarm --alarm-name api-unhealthy \
  --alarm-rule 'ALARM("api-5xx") OR ALARM("api-latency-p99")' \
  --actions-suppressor deploy-in-progress \
  --actions-suppressor-wait-period 120 \
  --actions-suppressor-extension-period 300 \
  --alarm-actions "$PAGER_TOPIC"
```
- While the suppressor alarm (`deploy-in-progress`) is in ALARM, the composite alarm changes state but does not run actions.
- **Wait period:** the maximum time in seconds the composite alarm waits for the suppressor to enter ALARM; after it, the composite runs its actions (covers races).
- **Extension period:** the maximum time in seconds the composite waits after the suppressor leaves ALARM before running its actions (covers warm-up after deploy).
- Both periods are required whenever a suppressor is set; the suppressor can be an alarm name or ARN.
- The suppressor can be any alarm: a metric alarm on a custom `DeploymentInProgress` metric the pipeline sets to 1, or a "dependency down" alarm so downstream alarms stay quiet.

## Disable actions for maintenance
```bash
aws cloudwatch disable-alarm-actions --alarm-names api-5xx api-latency-p99
# ... maintenance ...
aws cloudwatch enable-alarm-actions --alarm-names api-5xx api-latency-p99
```
- Disabling is indefinite: wrap it in the runbook/automation with a guaranteed re-enable, or use a
  mute rule with an `ExpireDate` or one-time `at(...)` window instead.
- Alarms with actions disabled are easy to forget: report on `ActionsEnabled=false`:
```bash
aws cloudwatch describe-alarms --query 'MetricAlarms[?ActionsEnabled==`false`].AlarmName'
```

## Scheduled muting
Alarm mute rules (`put-alarm-mute-rule`) mute the actions of targeted alarms during a window while the alarms keep evaluating and changing state. A rule has a `Schedule` with an `Expression` (`cron(...)` for recurring or `at(...)` for one-time), a `Duration` (ISO 8601, for example `PT2H`) and a `Timezone`, optional `StartDate` and `ExpireDate`, and `MuteTargets.AlarmNames` (up to 100 alarms by name). Callers need `cloudwatch:PutAlarmMuteRule` on the rule and on each targeted alarm. An account can have 2,000 mute rules per Region (not adjustable, read 2026-10-27).

## Routing instead of muting
- Separate topics for page vs ticket; send noisy alarms to the ticket topic rather than muting them.

## Verify
- [ ] During a test deploy, child alarms go to ALARM but the composite sends no page.
- [ ] Weekly check lists zero alarms with actions disabled outside a maintenance window.

## Checked
Checked 2026-10-27 against the live CloudWatch docs (current release) and the botocore cloudwatch 2010-08-01 model.
- PutCompositeAlarm API reference: ActionsSuppressor, wait and extension period semantics; botocore: put-composite-alarm parameters match the example.
- PutAlarmMuteRule API reference: cron and at expressions, Duration, Timezone, ExpireDate, 100 alarms per rule, permissions; CloudWatch quotas page: 2,000 mute rules.
- DisableAlarmActions and EnableAlarmActions in the botocore model: AlarmNames list of up to 100.
- Removed the unsourced remark about third-party maintenance windows.

Method: documentation only; no commands were run.
