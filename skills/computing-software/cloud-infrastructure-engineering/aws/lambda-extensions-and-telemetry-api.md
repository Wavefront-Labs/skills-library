---
id: computing-software.cloud-infrastructure-engineering.aws.lambda-extensions-and-telemetry-api
name: lambda-extensions-and-telemetry-api
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, lambda, extensions-api, telemetry-api, observability, lambda-layers]
level: advanced
status: docs-checked
description: "Build or evaluate Lambda extensions with the Extensions API lifecycle and subscribe to platform, function and extension logs with the Telemetry API."
sources: ["https://docs.aws.amazon.com/lambda/latest/dg/runtimes-extensions-api.html", "https://docs.aws.amazon.com/lambda/latest/dg/telemetry-api.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Lambda Extensions API and Telemetry API

## 1. External extension lifecycle
An extension is a separate process in the execution environment, deployed as a layer for zip functions or inside
a container image. Up to 10 extensions can register per function. Lifecycle phases: Init (extension init,
runtime init, function init), Invoke and Shutdown.
```bash
# register (extension init phase); Lambda-Extension-Name must be the extension's full file name
curl -si -X POST "http://${AWS_LAMBDA_RUNTIME_API}/2020-01-01/extension/register" \
  -H "Lambda-Extension-Name: my-ext" -d '{"events":["INVOKE","SHUTDOWN"]}'
# response header Lambda-Extension-Identifier: <ID>
# loop (blocking; set no timeout on this GET)
curl -s "http://${AWS_LAMBDA_RUNTIME_API}/2020-01-01/extension/event/next" -H "Lambda-Extension-Identifier: <ID>"
```
The invoke phase ends only after the runtime and every extension call `Next`; there is no separate post-invoke
phase, so slow extensions add duration. The function timeout bounds the whole phase. Lambda returns the
function response to the client without waiting for extensions to finish. Lambda Managed Instances extensions can
register only for `SHUTDOWN`.

## 2. Telemetry API subscription
The Telemetry API supersedes the Logs API; subscribing through one makes subscribing through the other fail.
```bash
curl -s -X PUT "http://${AWS_LAMBDA_RUNTIME_API}/2022-07-01/telemetry" \
  -H "Lambda-Extension-Identifier: <ID>" -d '{
  "schemaVersion":"2025-01-29",
  "types":["platform","function","extension"],
  "buffering":{"maxItems":1000,"maxBytes":262144,"timeoutMs":100},
  "destination":{"protocol":"HTTP","URI":"http://sandbox.localdomain:8080"}}'
```
- Use HTTP (recommended; plain HTTP only, delivered with POST) or TCP (NDJSON; telemetry can be lost if the
  extension crashes). Lambda reserves port 9001. Lambda only delivers to destinations inside the execution environment.
- Buffering limits: `maxBytes` 262,144 (default and minimum) to 1,048,576; `maxItems` 1,000 to 10,000
  (default 10,000); `timeoutMs` 25 to 30,000 (default 1,000). Read buffers should allow `2 * maxBytes` plus metadata.
- Event types include `platform.initStart`, `platform.initRuntimeDone`, `platform.initReport`, `platform.start`,
  `platform.runtimeDone`, `platform.report`, `platform.logsDropped`, plus `function` and `extension` log records.
  If a subscriber cannot keep up Lambda may drop records and sends `platform.logsDropped`.
- Lambda still sends logs and metrics to CloudWatch and traces to X-Ray when an extension subscribes. Batch
  telemetry and flush during Invoke and Shutdown events.

## 3. Internal extensions
An internal extension runs as a thread inside the runtime process (started and stopped by the runtime) and
cannot register for `SHUTDOWN`. Another route is language-specific environment variables and wrapper scripts
(see the Lambda "modify the runtime environment" page).

## 4. Costs and gotchas
- Extension init time counts toward Init; post-invoke work extends the invoke duration; the
  `PostRuntimeExtensionsDuration` metric shows the overhead.
- The Shutdown phase allows 0 ms with no extensions, 500 ms with an internal extension and 2,000 ms with one
  or more external extensions; after that Lambda sends `SIGKILL`.
- Extensions share CPU, memory and `/tmp` with the function, and its IAM role.

## Verify
- [ ] `platform.report` records reach the backend for each invoke.
- [ ] p99 duration with the extension within budget compared with the baseline.

## Checked
Date 2026-10-23. Lambda Developer Guide Extensions API and Telemetry API pages (current release). Confirmed: register path
and headers, `events` values, `Next` behaviour, 10 extension limit, no separate post-invoke phase, shutdown limits
0/500/2,000 ms, telemetry endpoint and path version, schema `2025-01-29`, types, buffering defaults and limits, HTTP vs
TCP and port 9001, Logs API exclusivity, event type names. Wrong in the old text: shutdown stated as "about 2 s"
without the 0/500/2000 split, the schema version `2022-12-13` was replaced by the documented `2025-01-29`, and the
buffering example's `maxItems` default was not stated. Removed the unconfirmed `/opt/extensions` path,
`AWS_LAMBDA_EXEC_WRAPPER`/`JAVA_TOOL_OPTIONS` specifics and `platform.report` field list.
Method: documentation only; no commands were run.
