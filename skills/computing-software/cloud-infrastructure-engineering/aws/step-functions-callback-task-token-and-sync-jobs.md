---
id: computing-software.cloud-infrastructure-engineering.aws.step-functions-callback-task-token-and-sync-jobs
name: step-functions-callback-task-token-and-sync-jobs
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, step-functions, task-token, wait-for-task-token, run-a-job, human-approval, callback-pattern, ecs, glue]
level: practitioner
status: docs-checked
description: "Pause Step Functions for external work: .waitForTaskToken callbacks, heartbeats and timeouts, and .sync Run-a-Job integrations for ECS, Glue, Batch and child workflows."
sources: ["https://docs.aws.amazon.com/step-functions/latest/dg/connect-to-resource.html", "https://docs.aws.amazon.com/step-functions/latest/dg/integrate-optimized.html", "https://docs.aws.amazon.com/step-functions/latest/dg/concepts-error-handling.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Step Functions callbacks (.waitForTaskToken) and Run-a-Job (.sync)

**Goal:** a workflow waits for something it does not control — a human, an on-prem system, a
long batch job — without polling loops and without waiting forever. Standard workflows only.

## 1. Three integration patterns
| Suffix | Behaviour |
|---|---|
| none (request/response) | call the API, move on immediately |
| `.sync` (Run a Job) | start the job, Step Functions waits (EventBridge events plus polling in the same account, polling only cross-account) until it finishes, fails the task if the job fails |
| `.waitForTaskToken` | call the API with a token, pause until someone calls `SendTask*` with that token |

## 2. Callback via SQS
```json
"WaitForApproval": {
  "Type": "Task",
  "Resource": "arn:aws:states:::sqs:sendMessage.waitForTaskToken",
  "Arguments": {"QueueUrl": "https://sqs.<REGION>.amazonaws.com/<ACCOUNT_ID>/approvals",
    "MessageBody": {"orderId": "{% $states.input.orderId %}",
                    "token": "{% $states.context.Task.Token %}"}},
  "TimeoutSeconds": 86400,
  "HeartbeatSeconds": 3600,
  "Catch": [{"ErrorEquals": ["States.Timeout", "States.HeartbeatTimeout"], "Next": "Escalate"}],
  "Next": "Fulfil"
}
```
JSONPath form: `"token.$": "$$.Task.Token"`. The worker finishes the step:
```bash
aws stepfunctions send-task-success --task-token "$TOKEN" --task-output '{"approved":true,"by":"jo"}'
aws stepfunctions send-task-failure --task-token "$TOKEN" --error Rejected --cause "budget"
aws stepfunctions send-task-heartbeat --task-token "$TOKEN"   # resets HeartbeatSeconds
```
Workers need permission for the `SendTaskSuccess`, `SendTaskFailure` and `SendTaskHeartbeat` actions. Tokens must be sent from principals in the same AWS account, and a new random token is generated if the task times out. Tokens are opaque and long; store them, don't truncate them.

## 3. Human approval by email/link
Lambda (via `lambda:invoke.waitForTaskToken`) emails approve/reject links pointing at an API
Gateway endpoint whose Lambda calls `SendTaskSuccess`/`SendTaskFailure`. Put the token in a
DynamoDB row keyed by a short ID instead of in the URL if links may be logged.

## 4. Run a Job (.sync)
```json
"RunReport": {"Type": "Task", "Resource": "arn:aws:states:::ecs:runTask.sync",
  "Arguments": {"Cluster": "reports", "TaskDefinition": "report:12", "LaunchType": "FARGATE",
    "NetworkConfiguration": {"AwsvpcConfiguration": {"Subnets": ["subnet-..."], "AssignPublicIp": "DISABLED"}}},
  "Next": "Done"}
```
Services with `.sync` support (Standard workflows only) include Athena, Batch, CodeBuild, ECS/Fargate, EKS, EMR, Glue, SageMaker AI and Step Functions itself, for example `batch:submitJob.sync` and `ecs:runTask.sync`. Express workflows support only request-response integrations.
`.sync` and `.waitForTaskToken` integrations need additional IAM permissions beyond the target action; see "How Step Functions generates IAM policies for integrated services".

## Gotchas
- No `TimeoutSeconds` or `HeartbeatSeconds` on a callback task = it can wait until the 1-year execution limit.
- Calling `SendTask*` after the task has timed out fails (the token is replaced on timeout);
  make the worker tolerate that.
- If a `.sync` task is aborted (execution stopped, or a sibling Parallel branch or Map iteration fails uncaught), Step Functions makes a best-effort attempt to cancel the job; it can fail (for example when the role lacks the stop permission), and then the integrated service may keep charging. Verify cancellation for your target.
- Express workflows support only the request-response pattern.

## Verify
- [ ] A test execution sits in `WaitForApproval`; `send-task-success` advances it with the provided output.
- [ ] With no response, the task times out into the `Escalate` path at the expected time.
- [ ] A failing ECS task (non-zero exit) fails the `.sync` state and is caught.

## Checked
Checked 2026-10-24 against the Step Functions developer guide page on service integration patterns.
Confirmed: three patterns and which services support .sync and .waitForTaskToken, Standard-only for .sync and callbacks, task token from the context object, HeartbeatSeconds and the one-year wait, token regeneration on timeout and same-account requirement, best-effort cancellation of aborted .sync tasks, polling plus EventBridge events.
Removed as unconfirmed: the :2 suffix explanation, explicit poll-permission names and managed rule name, error names returned by late SendTask calls.

Method: documentation only; no commands were run.
