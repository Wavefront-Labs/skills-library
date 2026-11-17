---
id: computing-software.cloud-infrastructure-engineering.aws.codepipeline-notifications-and-execution-monitoring
name: codepipeline-notifications-and-execution-monitoring
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, codepipeline, pipeline-notifications, codestar-notifications, eventbridge, chatbot, pipeline-monitoring]
level: practitioner
status: docs-checked
description: "Know when pipelines fail or wait for approval: notification rules to SNS or chat, EventBridge pipeline/stage/action events, and CLI checks of execution state and history."
sources: ["https://docs.aws.amazon.com/codepipeline/latest/userguide/notification-rule-create.html", "https://docs.aws.amazon.com/codepipeline/latest/userguide/detect-state-changes-cloudwatch-events.html", "https://docs.aws.amazon.com/codepipeline/latest/userguide/execution-modes.html", "https://docs.aws.amazon.com/codepipeline/latest/userguide/limits.html", "https://docs.aws.amazon.com/codepipeline/latest/userguide/monitoring.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# CodePipeline notifications and execution monitoring

## Notification rules (simplest)
```bash
aws codestar-notifications list-event-types --query 'EventTypes[?ServiceName==`CodePipeline`].EventTypeId'
aws codestar-notifications create-notification-rule --name app-pipeline-alerts \
  --resource arn:aws:codepipeline:<REGION>:<ACCOUNT_ID>:app \
  --detail-type FULL \
  --event-type-ids <EVENT_TYPE_ID> <EVENT_TYPE_ID> \
  --targets TargetType=SNS,TargetAddress=$TOPIC_ARN
```
- Pick event type IDs from `list-event-types` (failed executions, manual approval needed, and so on).
- Targets: an SNS topic, or a Slack client configured in Amazon Q Developer in chat applications (you cannot create that client while creating the rule). Subscribe users to the SNS topic or they receive nothing; the topic needs the policy that allows notifications (a topic created from the console is named `codestar-notifications-<name>` and already has it).
- Notification rules also exist for CodeBuild, CodeDeploy and other developer-tool resources.

## EventBridge (for automation)
```json
{"source":["aws.codepipeline"],
 "detail-type":["CodePipeline Pipeline Execution State Change"],
 "detail":{"pipeline":["app"],"state":["FAILED","SUPERSEDED"]}}
```
- Three detail types: `CodePipeline Pipeline Execution State Change`, `CodePipeline Stage Execution State Change`, `CodePipeline Action Execution State Change`. The `execution-id` in the detail identifies the execution.
- Feed into Lambda to post rich messages, open tickets or compute delivery metrics. The monitoring page also lists CodePipeline CloudWatch metrics; check it for what is published.

## Inspect from the CLI
```bash
aws codepipeline get-pipeline-state --name app \
  --query 'stageStates[].[stageName,latestExecution.status]' --output table
aws codepipeline list-pipeline-executions --pipeline-name app --max-items 10 \
  --query 'pipelineExecutionSummaries[].[pipelineExecutionId,status,trigger.triggerType,startTime]'
aws codepipeline list-action-executions --pipeline-name app \
  --filter pipelineExecutionId=$EID --query 'actionExecutionDetails[?status==`Failed`]'
```
- Retry from the failed stage: `aws codepipeline retry-stage-execution --retry-mode FAILED_ACTIONS` (see the API reference for the other mode).
- Stage rollback is not available for pipelines in PARALLEL mode.
- Audit who approved: approval results and CloudTrail.

## Gotchas
- `SUPERSEDED` (a newer execution advanced past this one while it waited for the next stage) is not a failure; filter it out of failure alerts.
- Execution modes: SUPERSEDED, QUEUED and PARALLEL (the last two need a V2 pipeline). The quota is 50 concurrent executions per pipeline in QUEUED or PARALLEL mode and 5 concurrent action executions per PARALLEL execution.
- Switching modes cancels active and pending executions (after in-progress actions finish) when moving between SUPERSEDED and QUEUED, or into PARALLEL; do it between releases.
- Alert on "approval needed" so approvals do not wait unnoticed; action time-outs per type are on the quotas page (for example CodeBuild build action 36 hours).

## Verify
- [ ] Forced failing build sends a chat/SNS message with a link to logs.
- [ ] Approval-needed notifications reach approvers.

## Checked
2026-10-28. Confirmed on the notification-rule-create, detect-state-changes-cloudwatch-events, execution-modes, limits and monitoring pages: target types and SNS rules, the three detail types, SUPERSEDED meaning, mode names and V2 requirement, concurrency quotas, mode-switch cancellation, PARALLEL stage-rollback limit, action time-outs. Removed as unconfirmed: the literal event type IDs (replaced by `list-event-types`), the claim that CodePipeline publishes no execution metrics (the monitoring page lists CodePipeline CloudWatch metrics), the 7-day approval expiry, `ALL_ACTIONS` as a V2-only mode, queue-length monitoring, a made-up account ID.
Method: documentation only; no commands were run.
