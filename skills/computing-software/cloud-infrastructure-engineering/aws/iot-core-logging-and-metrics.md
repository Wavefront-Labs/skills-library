---
id: computing-software.cloud-infrastructure-engineering.aws.iot-core-logging-and-metrics
name: iot-core-logging-and-metrics
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, iot, iot-core, iot-logging, awsiotlogsv2, iot-metrics, rule-errors, lifecycle-events]
level: practitioner
status: docs-checked
description: "Debug AWS IoT Core fleets with v2 logging (default and per-thing-group levels), the AWSIotLogsV2 log group, key CloudWatch metrics, rule error actions and lifecycle events."
sources: ["https://docs.aws.amazon.com/iot/latest/developerguide/configure-logging.html", "https://docs.aws.amazon.com/iot/latest/developerguide/cwl-format.html", "https://docs.aws.amazon.com/iot/latest/developerguide/metrics_dimensions.html", "https://docs.aws.amazon.com/iot/latest/developerguide/life-cycle-events.html", "https://docs.aws.amazon.com/iot/latest/developerguide/rule-error-handling.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# IoT Core logging and metrics

## Logging (v2)
```bash
aws iot set-v2-logging-options --role-arn arn:aws:iam::111122223333:role/IoTLogging --default-log-level ERROR
aws iot set-v2-logging-level --log-target targetType=THING_GROUP,targetName=canary-devices --log-level DEBUG
aws iot list-v2-logging-levels
```
- Levels: `DISABLED`, `ERROR`, `WARN`, `INFO`, `DEBUG` (each level includes the more severe ones). Keep the default at ERROR (DEBUG on a whole fleet is verbose); raise per thing group, client id, source IP or principal ID (`targetType` `THING_GROUP`, `CLIENT_ID`, `SOURCE_IP`, `PRINCIPAL_ID`) while debugging.
- Logs go to log group **`AWSIotLogsV2`** by default (event-level configuration can set other log groups); events include `Connect`, `Disconnect`, `Publish-In`,
  `Publish-Out`, `Subscribe`, `Queued`, `RuleExecution`, `RuleMatch`, with `status`, `reason`, `clientId`, `principalId`, `topicName`.
```
fields @timestamp, eventType, clientId, status, reason
| filter logLevel = "ERROR"
| stats count() by eventType, reason | sort count() desc
```
Documented reasons include `DUPLICATE_CLIENT_ID` on Disconnect entries (a new connection used the same client ID, so two devices sharing one id kick each other off), `throttled` and `client_id_throttled` on Connect failures, and `throttled`, `connection_throttled` and `CLIENT_ERROR` on Publish-In failures. See the CloudWatch log entry format page for each event type's reason codes.

## Metrics (AWS/IoT)
| Metric | Watch for |
|---|---|
| `Connect.Success` / `Connect.AuthError` / `Connect.ClientError` / `Connect.ServerError` / `Connect.Throttle` / `Connect.ClientIDThrottle` | fleet connectivity, cert problems |
| `PublishIn.Success` / `PublishIn.AuthError` / `PublishIn.ClientError` / `PublishIn.ServerError` / `PublishIn.Throttle` | ingestion health |
| `RulesExecuted`, `TopicMatch`, `ParseError` | rules firing and JSON parse problems |
| `RuleNotFound`, `RuleExecutionThrottled` | rule configuration and throttling |
| `Failure` / `Success` (dimensions RuleName, ActionType) | failed and successful rule actions |
| `ErrorActionFailure` / `ErrorActionSuccess` | outcome of error actions |
Alarm on rule action failures and on drops in `PublishIn.Success` against a baseline.

## Rule error actions
Every rule should have an `errorAction` (for example CloudWatch Logs or SQS) so failed deliveries are kept. The rules engine runs it when an action fails (for example no permission on an S3 bucket, or DynamoDB throughput exceeded) and sends one message per rule and message that lists all failures:
```json
"errorAction":{"cloudwatchLogs":{"logGroupName":"/iot/rule-errors","roleArn":"arn:aws:iam::111122223333:role/IoTRuleErrors"}}
```

## Lifecycle events
Subscribe a rule to `$aws/events/presence/connected/+` and `.../disconnected/+` for connection
tracking (the event carries `clientInitiatedDisconnect` and `disconnectReason`); `$aws/events/presence/connect_failed/<clientId>` reports failed connects.
Fleet indexing connectivity status is often easier for "who is offline".

## Verify
- [ ] Default log level ERROR; a test thing group at DEBUG produces detailed logs.
- [ ] All rules have error actions; alarms on rule failures and auth errors exist.

## Checked

2026-10-27, AWS documentation (current release as read on that date). AWS IoT Core Developer Guide logging configuration, CloudWatch log entry format, metrics and dimensions, lifecycle events and rule error handling pages; botocore iot 2015-05-28 model. Fixed metric names: Connect.AuthError and PublishIn.AuthError (the skill had AuthNError and AuthZError); RuleMessageThrottled does not exist (rule metrics include RuleExecutionThrottled, ParseError, ErrorActionFailure, ErrorActionSuccess); AUTHORIZATION_FAILURE is not a documented reason code and was replaced with the documented ones. Confirmed: log levels, target types, AWSIotLogsV2 default group, event types, lifecycle topics, errorAction with cloudwatchLogs roleArn and logGroupName.
Method: documentation only; no commands were run.
