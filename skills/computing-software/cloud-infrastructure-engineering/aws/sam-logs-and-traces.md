---
id: computing-software.cloud-infrastructure-engineering.aws.sam-logs-and-traces
name: sam-logs-and-traces
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, sam, sam-logs, sam-traces, sam-cli, cloudwatch-logs, x-ray]
level: practitioner
status: docs-checked
description: "Debug deployed serverless apps from the terminal with sam logs (tail, filter, multiple resources, Logs Insights) and sam traces (X-Ray), plus enabling tracing in templates."
sources: ["https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-cli-command-reference-sam-logs.html", "https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-cli-command-reference-sam-traces.html", "https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-logging.html", "https://github.com/aws/aws-sam-cli/blob/develop/samcli/commands/logs/command.py"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# sam logs and sam traces

## 1. sam logs
Fetch logs for resources in a deployed stack by **logical ID**, no need to know log group
names:
```bash
sam logs --stack-name orders-api --tail
sam logs --stack-name orders-api -n OrdersFunction --tail
sam logs --stack-name orders-api -n OrdersFunction -n OrdersApi --start-time '10min ago'
sam logs --stack-name orders-api -n OrdersFunction --filter 'ERROR' --start-time '1h ago'
sam logs --stack-name orders-api --cw-log-group /aws/apigateway/orders-access --tail
sam logs --stack-name orders-api --include-traces --tail
```
- Without `-n` (and without `--cw-log-group`), SAM scans the stack and pulls logs from all supported resources.
- Nested stacks: `-n ChildStackLogicalId/ResourceLogicalId`.
- `--filter` takes a keyword or a CloudWatch Logs filter pattern (`'{ $.level = "ERROR" }'` for JSON logs).
- `--cw-log-group` adds log groups that are not auto-discovered; when given, only those groups are tailed unless you also pass `-n`.
- `--output` selects the output format (`text` or `json`).

## 2. Make logs useful
- Structured JSON logging (Powertools Logger or Lambda's `LoggingConfig: {LogFormat: JSON,
  ApplicationLogLevel: INFO}` in the template) so filters can target fields.
- API Gateway access logging configured in the template (`AccessLogSetting` on the stage)
  so `sam logs` can include API logs.

## 3. sam traces
```bash
sam traces --tail
sam traces --start-time '15min ago' --output json
sam traces --trace-id 1-6712ab34-5f6e7d8c9b0a1f2e3d4c5b6a
```
Shows X-Ray traces; `--trace-id` fetches one trace and `--tail` follows new ones. Use `sam logs --include-traces` (`-i`) to include traces in log output.
Enable tracing in the template:
```yaml
Globals:
  Function:
    Tracing: Active
  Api:
    TracingEnabled: true
Resources:
  OrdersStateMachine:
    Type: AWS::Serverless::StateMachine
    Properties:
      Tracing: {Enabled: true}
```
Instrument SDK calls (for example with the Powertools Tracer or ADOT) to get subsegments.

## 4. Local equivalents
`sam local invoke -e event.json --debug` prints logs locally; `sam remote invoke
OrdersFunction --stack-name orders-api --event-file event.json` invokes the deployed
function and prints its logs.

## Gotchas
- `sam logs` takes a stack name (`--stack-name`) or a resource name via `--name`; a wrong region or profile shows nothing.
- Define `AWS::Logs::LogGroup` resources with `RetentionInDays` in the template to control retention.

## Verify
- [ ] `sam logs --stack-name ... --tail` shows function and API logs during a test request.
- [ ] `sam traces` shows the request trace with API Gateway, Lambda and downstream subsegments.
- [ ] Log groups defined with retention in the template.

## Checked
Date: 2026-10-24. Documentation release: AWS SAM Developer Guide (awsdocs source, June 2023 snapshot) plus the aws/aws-sam-cli `develop` source for `sam logs` and `sam traces` (help text of every option).
Confirmed: `--stack-name`, `-n/--name` (repeatable, `NestedStackLogicalId/ResourceLogicalId`), `--filter`, `--tail`, `--include-traces`, `--cw-log-group`, `--trace-id`; scan-all behaviour without `-n`; SAM function properties `Tracing` and `LoggingConfig`, API properties `TracingEnabled` and `AccessLogSetting`, state machine `Tracing` (aws/serverless-application-model schema).
Removed as unconfirmed: the Logs Insights recipe, X-Ray permission statements, default log group retention and API cost remarks.

Method: documentation only; no commands were run.
