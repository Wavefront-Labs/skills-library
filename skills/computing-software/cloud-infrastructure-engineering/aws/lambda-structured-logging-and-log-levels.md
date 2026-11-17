---
id: computing-software.cloud-infrastructure-engineering.aws.lambda-structured-logging-and-log-levels
name: lambda-structured-logging-and-log-levels
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, lambda, lambda-logging, powertools, advanced-logging-controls, structured-logging, cloudwatch-logs]
level: practitioner
status: docs-checked
description: "Emit JSON logs from Lambda with LoggingConfig: log format, application and system log levels, custom log group, request ID fields and execution role permissions."
sources: ["https://docs.aws.amazon.com/lambda/latest/dg/monitoring-cloudwatchlogs.html", "https://docs.aws.amazon.com/lambda/latest/dg/monitoring-cloudwatchlogs-logformat.html", "https://docs.aws.amazon.com/lambda/latest/dg/monitoring-cloudwatchlogs-log-level.html", "https://docs.aws.amazon.com/lambda/latest/dg/monitoring-cloudwatchlogs-loggroups.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Lambda structured logging

**Goal:** queryable JSON logs with controllable verbosity and a request ID on every line.

## Advanced logging controls
```bash
aws lambda update-function-configuration --function-name myFunction \
  --logging-config LogFormat=JSON,ApplicationLogLevel=ERROR,SystemLogLevel=WARN,LogGroup=myLogGroup
```
- Default log format for all runtimes is plain text. AWS recommends JSON unless existing tooling needs plain text.
- Switching to JSON with no level set makes Lambda set both application and system log level to `INFO`. Only new logs use the new format.
- `ApplicationLogLevel`: `DEBUG`, `INFO`, `WARN`, `ERROR` or `FATAL` (the page's table also lists `TRACE`). `SystemLogLevel`: `DEBUG`, `INFO` or `WARN`. Lambda sends logs at the chosen level and lower in detail terms (WARN drops INFO and DEBUG). Default system level `INFO` sends the start and report messages.
- Log-level filtering requires the JSON log format. Unlevelled messages are treated as `INFO`.
- A level set in code (for example Python `setLevel()`) takes precedence over the Lambda setting.
- Python with plain text log format defaults to `WARN`; changing to JSON changes that default.
- JSON adds metadata, so messages get larger.

## What JSON logs look like
- Application logs: keys `timestamp`, `level`, `message`, plus `requestId` (Python, .NET, Node.js) or `AWSrequestId` (Java). Needs a supported logger: Java `LambdaLogger`/Log4j2, .NET `ILambdaLogger`, Node.js `console` methods, Python `logging`, Ruby `Logger`, Rust `tracing`. No code change is needed with those.
- System (platform) logs: keys `time`, `type`, `record`.
- Other runtimes or loggers: write JSON objects to stdout or stderr with a `level` key; a missing or invalid level becomes `INFO`, and `timestamp` must be RFC 3339 or Lambda adds one. Libraries such as Powertools for AWS Lambda can emit JSON; Lambda does not double-encode logs that are already JSON.
- Custom runtimes read `AWS_LAMBDA_LOG_LEVEL` and `AWS_LAMBDA_LOG_FORMAT`.
- Node.js functions emitting EMF metrics: switching to JSON may stop CloudWatch recognising them; update Powertools (TypeScript) or EMF client libraries and test.

## Log group and permissions
- Default group `/aws/lambda/<function-name>`. `LogGroup=...` sends logs to another group (created if missing); several functions can share one. Names must follow CloudWatch rules and must not begin with `aws/`.
- Custom-group stream names: `YYYY/MM/DD/<function_name>[<function_version>][<execution_environment_GUID>]`.
- Execution role needs `logs:CreateLogGroup`, `logs:CreateLogStream`, `logs:PutLogEvents`; the managed policy `AWSLambdaBasicExecutionRole` has them. Setting the group via the CLI does not add `logs:PutLogEvents`; the console may add it.
- Logs can take 5 to 10 minutes to appear after an invocation. Lambda adds no log charge; standard CloudWatch Logs charges apply.

## Query
Logs Insights example from the page: `fields @timestamp, @message | filter requestId = "<id>" | sort @timestamp asc`.

## Verify
Invoke once, open the log stream: lines are valid JSON, and lines below the chosen level are absent.

## Method
Rewritten from the four cited Lambda pages. Powertools code sample, retention default and `log_event` advice were removed as not stated there.

## Checked
Checked 2026-11-08 against the four cited Lambda Developer Guide pages (CloudWatch Logs, log formats, log-level filtering, log groups).
Method: docs-only read of cited pages, 2026-11-08
