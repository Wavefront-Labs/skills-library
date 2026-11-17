---
id: computing-software.cloud-infrastructure-engineering.aws.step-functions-teststate-and-local-testing
name: step-functions-teststate-and-local-testing
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, step-functions, teststate, workflow-studio, sfn-local, testing, asl, ci]
level: practitioner
status: docs-checked
description: "Test Step Functions before deploy: TestState API with inspection levels, definition validation, Workflow Studio round-trips, and Step Functions Local with mocks."
sources: ["https://docs.aws.amazon.com/step-functions/latest/dg/test-state-isolation.html", "https://docs.aws.amazon.com/step-functions/latest/dg/sfn-local.html", "https://docs.aws.amazon.com/step-functions/latest/dg/sfn-local-test-sm-exec.html", "https://docs.aws.amazon.com/step-functions/latest/apireference/API_ValidateStateMachineDefinition.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Testing Step Functions: TestState, validation, Local

**Goal:** catch data-flow and permission bugs in seconds, per state, instead of deploying
and reading execution history.

## 1. Validate the whole definition (CI gate)
```bash
aws stepfunctions validate-state-machine-definition \
  --definition file://statemachine.asl.json --type STANDARD
# {"result": "OK", "diagnostics": []}  -- FAIL lists ERROR/WARNING with location paths
```
Run it in CI before `cdk deploy`/`sam deploy`. It reports syntax and structure problems (for example invalid JSON, a missing end state, duplicate state names), not runtime data or IAM issues. Branch only on the `result` field (`OK` or `FAIL`): warnings do not fail it, and diagnostic wording and counts can change. `--type` defaults to `STANDARD`.

## 2. TestState: run one state for real
```bash
aws stepfunctions test-state \
  --definition '{"Type":"Task","Resource":"arn:aws:states:::dynamodb:getItem","Arguments":{"TableName":"customers","Key":{"pk":{"S":"{% $states.input.id %}"}}},"Output":"{% $states.result.Item %}","End":true}' \
  --role-arn arn:aws:iam::<ACCOUNT_ID>:role/sfn-orders \
  --input '{"id":"c-1"}' --inspection-level DEBUG
```
- Output includes `status` (SUCCEEDED/FAILED/RETRIABLE/CAUGHT_ERROR), `output`, `error`,
  `cause`, `nextState`, and with `DEBUG` the `inspectionData` after each processing step
  (`afterArguments`, `result`, `afterResultSelector`, `afterResultPath`, variables).
- `TRACE` adds raw HTTP request/response for HTTP Tasks (`--reveal-secrets` to include auth
  headers; needs `states:RevealSecrets`).
- Without a mock the call really executes the integration with the given role — use test resources. Flow states (Choice, Pass, Wait, ...) need a role too, but any role works because they call no AWS actions; with a `--mock` the role is optional.
- Since November 2025 (CLI and SDK only, not the console): `--mock '{"result": "..."}'` or `--mock '{"errorOutput": {...}}'` mocks an integration; Map, Parallel, Activity, `.sync` and `.waitForTaskToken` states can only be tested with a mock; `--state-configuration` and `--context` set retry count, error source and context values. The response reports `retryIndex`/`catchIndex` and `CAUGHT_ERROR` or `RETRIABLE` status.

## 3. Workflow Studio
Console designer with a **Code** mode: design visually,
then copy the ASL into your repo — the repo file is the source of truth. Its "Test state"
button uses the TestState API (without the mocking enhancements).

## 4. Step Functions Local (offline, mocked)
```bash
docker run -p 8083:8083 -e SFN_MOCK_CONFIG=/opt/mock.json \
  -v "$PWD/mock.json:/opt/mock.json" amazon/aws-stepfunctions-local
aws stepfunctions --endpoint-url http://localhost:8083 create-state-machine ...
aws stepfunctions --endpoint-url http://localhost:8083 start-execution \
  --state-machine-arn "arn:aws:states:us-east-1:123456789012:stateMachine:Orders#HappyPath"
```
`mock.json` maps test cases to mocked responses per state, so retry and
catch paths can be exercised; you run a test case by adding `#test_name` to the state machine ARN. The Step Functions guide marks Local as unsupported and without feature parity with the service, and points to the TestState API as the AWS alternative; prefer TestState and a real dev account.

## Gotchas
- TestState runs one state (or one named state inside a full definition); chain tests by feeding `output` and `nextState` into the next call. Map and Parallel tests exercise input/output processing with a mocked result, not the inner states; verify real transitions with an execution in a dev account (`start-execution` + `get-execution-history`).
- IAM failures show as `States.Permissions`-style errors only when you test with the real role.

## Verify
- [ ] CI runs `validate-state-machine-definition` and fails on `FAIL`.
- [ ] Every Task state with non-trivial data shaping has a recorded `test-state --inspection-level DEBUG` result.
- [ ] Error paths (Catch) exercised via a TestState `errorOutput` mock, a Local mocked error, or a forced test failure.

## Checked
Checked 2026-10-24 against the Step Functions developer guide (TestState API, Step Functions Local) and the ValidateStateMachineDefinition API reference.
Confirmed: inspection levels, status values and inspectionData fields, TRACE with reveal secrets and states:RevealSecrets, mocking (November 2025 enhancements, CLI/SDK only), role requirements, Map/Parallel/Activity/.sync testing only with mocks, validate result OK/FAIL semantics and default type, Local docker image and port 8083, SFN_MOCK_CONFIG and #test_name, and that AWS marks Local unsupported.
Removed as unconfirmed: unreachable-state detection claim, VS Code toolkit mention, Return/Throw mock field names, JSONata gaps in Local.

Method: documentation only; no commands were run.
