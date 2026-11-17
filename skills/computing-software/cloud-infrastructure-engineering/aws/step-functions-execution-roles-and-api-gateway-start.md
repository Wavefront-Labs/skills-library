---
id: computing-software.cloud-infrastructure-engineering.aws.step-functions-execution-roles-and-api-gateway-start
name: step-functions-execution-roles-and-api-gateway-start
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, step-functions, sfn-execution-role, api-gateway, startexecution, iam-passrole, startsyncexecution]
level: practitioner
status: docs-checked
description: "Write least-privilege Step Functions execution roles per integration pattern, and start executions from API Gateway REST and HTTP APIs with the right role and mapping."
sources: ["https://docs.aws.amazon.com/step-functions/latest/dg/manage-state-machine-permissions.html", "https://docs.aws.amazon.com/step-functions/latest/dg/tutorial-api-gateway.html", "https://docs.aws.amazon.com/step-functions/latest/dg/state-map-distributed.html", "https://docs.aws.amazon.com/step-functions/latest/dg/input-output-resultwriter.html", "https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-develop-integrations-aws-services-reference.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Step Functions execution roles and starting from API Gateway

## Execution role
Trust policy (the execution role must trust the Step Functions service principal):
```json
{"Effect":"Allow","Principal":{"Service":"states.amazonaws.com"},"Action":"sts:AssumeRole"}
```
Permissions depend on the integration pattern:
| Pattern | Extra permissions |
|---|---|
| Request-response (`lambda:invoke`) | the target action only (`lambda:InvokeFunction` on the function ARN) |
| `.sync` (ECS, Batch, Glue, nested SFN) | target action plus the extra actions Step Functions uses to monitor and cancel the job (EventBridge events and polling); see "How Step Functions generates IAM policies for integrated services" |
| `.waitForTaskToken` | the send action (e.g. `sqs:SendMessage`) |
| Distributed Map | `states:StartExecution` on the state machine itself, `states:DescribeExecution` on its executions, S3 read on the items, `s3:PutObject`, `s3:GetObject`, `s3:ListMultipartUploadParts` and `s3:AbortMultipartUpload` on the ResultWriter prefix |
| Logging to CloudWatch | the `logs:*Delivery` actions, `logs:CreateLogStream`, `logs:PutLogEvents`, `logs:PutResourcePolicy`, `logs:DescribeResourcePolicies`, `logs:DescribeLogGroups` on `*` (see the logging skill for the full list) |
| X-Ray | an X-Ray tracing policy (Workflow Studio adds one to every role it generates) |
Workflow Studio can generate a least-privilege role per state machine for HTTP tasks, optimized integrations, nested workflows, Distributed Map, X-Ray and logging, but not for AWS SDK integrations, which you must write yourself; copy the generated role rather than using `*`.

## Start from API Gateway REST API
AWS service integration: service Step Functions, HTTP method POST (all Step Functions actions use POST), action name `StartExecution`, and an integration role that allows `states:StartExecution`. Mapping template (the doc's version reads the state machine ARN from a stage variable):
```
{"input": "$util.escapeJavaScript($input.json('$'))",
 "stateMachineArn": "$util.escapeJavaScript($stageVariables.arn)"}
```
- Returns `executionArn` and `startDate` immediately (async); call `DescribeExecution` to get the result.
- For a synchronous answer use an **Express** workflow and action `StartSyncExecution` (from the Step Functions console the request expires after 60 seconds; via SDK or CLI it can run up to five minutes).
- Set `name` (for example the request id): starting a Standard execution with the same name as a running one returns an idempotent response, while Express starts are not idempotent.

## Start from an HTTP API
First-class integration: `IntegrationSubtype: StepFunctions-StartExecution` (or `-StartSyncExecution`)
with `RequestParameters` for `StateMachineArn` (required) and optional `Name`, `Input` and `Region`, and a credentials role. The sync subtype works only with Express state machines.

## Gotchas
- `AccessDeniedException` in history names the missing action; add exactly that.
- Escaping: without `escapeJavaScript` the input string breaks on quotes.

## Verify
- [ ] Role has no `*` actions except logging delivery; trust has SourceArn condition.
- [ ] `curl -X POST` to the API starts an execution visible in the console with the request id as name.

## Checked
Checked 2026-10-24 against the Step Functions developer guide (execution roles with Workflow Studio, Distributed Map and ResultWriter IAM, API Gateway tutorial, workflow type guarantees) and the API Gateway HTTP API integration subtype reference.
Confirmed: every state machine needs an execution role, Workflow Studio generation scope and the SDK-integration gap, Distributed Map and ResultWriter permissions, REST integration settings (POST, StartExecution action name, mapping template with escapeJavaScript and stage variable), DescribeExecution needed for async results, StartSyncExecution limits, HTTP API subtypes and parameters, idempotent same-name starts for Standard.
Removed as unconfirmed: confused-deputy trust conditions, iam:PassRole statement, 29 s integration timeout, output-unwrapping template, X-Ray action names, specific .sync monitor permissions.

Method: documentation only; no commands were run.
