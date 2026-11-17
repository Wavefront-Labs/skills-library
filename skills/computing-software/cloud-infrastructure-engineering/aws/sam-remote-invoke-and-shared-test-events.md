---
id: computing-software.cloud-infrastructure-engineering.aws.sam-remote-invoke-and-shared-test-events
name: sam-remote-invoke-and-shared-test-events
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, sam, remote-invoke, shared-test-events, sam-cli, lambda-testing, cloud-testing]
level: practitioner
status: docs-checked
description: "Test deployed serverless resources from the SAM CLI: sam remote invoke for Lambda, SQS, Kinesis and Step Functions, and shareable test events stored for the whole team."
sources: ["https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/using-sam-cli-remote-invoke.html", "https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/using-sam-cli-remote-test-event.html", "https://docs.aws.amazon.com/lambda/latest/dg/testing-functions.html", "https://github.com/aws/aws-sam-cli/blob/develop/samcli/commands/remote/invoke/cli.py"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# sam remote invoke and shared test events

**Goal:** exercise the real deployed function or workflow from your terminal with the same
events your team uses in the console, instead of mocking AWS locally.

## Remote invoke
```bash
sam remote invoke WorkerFunction --stack-name orders-dev --event '{"orderId":"42"}'
sam remote invoke WorkerFunction --stack-name orders-dev --event-file events/order.json \
  --output json                                  # full SDK response (text prints a readable response)
sam remote invoke OrderStateMachine --stack-name orders-dev --event-file events/sfn.json
sam remote invoke OrdersQueue --stack-name orders-dev --event '{"orderId":"42"}'   # SendMessage
sam remote invoke arn:aws:lambda:eu-west-1:111122223333:function:fn --event '{}'    # by ARN, no stack
```
- Supported targets: Lambda functions, SQS queues (send a message), Kinesis streams (put a record), Step
  Functions state machines (start an execution and wait for the result).
- The resource id can be a logical id (with `--stack-name`), a physical id or an ARN; for nested stacks use `Child/Function`.
  With a single Lambda function in the stack, `--stack-name` alone is enough.
- `--parameter` customises the Boto3 call, e.g. `--parameter InvocationType="Event"` or `"DryRun"` and `--parameter LogType="None"`;
  repeat the option for several parameters.
- Functions configured for response streaming (`FunctionUrlConfig` with `InvokeMode: RESPONSE_STREAM`) are detected and streamed.

## Shared test events
```bash
sam remote test-event put WorkerFunction --stack-name orders-dev --name big-order --file events/big.json
sam remote test-event list WorkerFunction --stack-name orders-dev
sam remote invoke WorkerFunction --stack-name orders-dev --test-event-name big-order
sam remote test-event get WorkerFunction --stack-name orders-dev --name big-order --output-file x.json
```
- Stored as schemas in the EventBridge schema registry `lambda-testevent-schemas`, so they are the
  same shareable test events visible in the Lambda console Test tab; do not edit that registry by hand.
- Users need permissions for the EventBridge schema registry operations the Lambda guide lists (`CreateRegistry`, `CreateSchema`,
  `DeleteSchema`, `DeleteSchemaVersion`, `DescribeRegistry`, `DescribeSchema`, `GetDiscoveredSchema`, `ListSchemaVersions`, `UpdateSchema`).
- Generate realistic payloads: `sam local generate-event sqs receive-message --body '{"orderId":"42"}'`.

## Gotchas
- Options such as `stack_name` and `event` can be set in `samconfig.toml` under `[default.remote_invoke.parameters]`; a wrong profile or region invokes the wrong environment.
- Remote invoke runs real code with real side effects: point it at dev stacks.

## Verify
- [ ] `sam remote invoke` returns the expected payload and logs from the deployed function.
- [ ] A test event saved via CLI appears in the console Test tab and vice versa.

## Checked
Date: 2026-10-24. Documentation release: current AWS SAM Developer Guide page for `sam remote invoke`, the current Lambda Developer Guide page on testing (shareable test events) and the aws/aws-sam-cli `develop` source for `sam remote invoke` and `sam remote test-event put/get/list/delete` options.
Confirmed: supported targets; resource id forms and `Child/Function`; `--event`, `--event-file`, `--test-event-name`, `--output` (text or json), `--parameter` (repeatable); response streaming detection; `samconfig.toml` `remote_invoke` table; registry name `lambda-testevent-schemas` and its permission list; `test-event put` needs `--name`, with `--file` and `--force`; `get` has `--name` and `--output-file`.
Removed as unconfirmed: the `Qualifier` and `MessageGroupId` parameter examples, the `schemas:*` wording and the 6 MB payload note.

Method: documentation only; no commands were run.
