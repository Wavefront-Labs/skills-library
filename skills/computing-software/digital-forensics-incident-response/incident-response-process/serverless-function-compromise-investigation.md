---
id: computing-software.digital-forensics-incident-response.incident-response-process.serverless-function-compromise-investigation
name: serverless-function-compromise-investigation
category: computing-software
field: digital-forensics-incident-response
product: incident-response-process
tags: [serverless-forensics, cloud-incident-response, cloud-forensics, aws-lambda, dfir]
level: advanced
status: docs-checked
description: "Investigate a compromised AWS Lambda function: preserve code versions and config, read Lambda management and data events in CloudTrail, and check event sources and permissions."
sources: ["https://docs.aws.amazon.com/lambda/latest/dg/logging-using-cloudtrail.html", "https://docs.aws.amazon.com/lambda/latest/dg/configuration-versions.html", "https://learn.microsoft.com/en-us/azure/azure-functions/functions-monitoring"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Serverless function compromise investigation

**Goal:** there is no host to image. Evidence lives in the function's code versions,
configuration, execution role activity and logs. This skill is AWS Lambda-specific; for Azure Functions, telemetry
goes to Application Insights (connection string in an application setting), so check what was configured before the
incident.

## Preserve
- Download the deployed code for every version and alias:
  `aws lambda get-function --function-name f --qualifier <ver>` (the response has `Configuration`, `Code`, `Tags` and
  `Concurrency`; fetch the code from the location in `Code` promptly).
- Configuration: `get-function-configuration` (environment variables may hold secrets; also layers, execution role,
  VPC config).
- Layers: `get-layer-version` for each attached layer.
- Understand versions first: the unpublished version is `$LATEST` and every code deploy overwrites it. A published
  version's code, runtime, architecture, memory, layers and most settings are immutable, so published versions are your
  evidence of earlier state, while `$LATEST` may already be overwritten. Triggers, destinations, provisioned
  concurrency, asynchronous invocation and database connections can still change on a published version. Version
  numbers are never reused.
- Logs: whatever logging and tracing the function was configured with. Record the gap if none.

## Questions and where to answer them
| Question | Evidence |
|---|---|
| Was code or config changed? | CloudTrail management events `UpdateFunctionCode20150331v2`, `UpdateFunctionConfiguration20150331v2`, `PublishLayerVersion20181031`, `AddPermission20150331v2`, `PublishVersion20150331` |
| Was the function exploited at runtime (injection via event input)? | Function logs, upstream access logs, input payloads |
| What did the attacker do with the role? | CloudTrail where `userIdentity` is a temporary role session for the execution role |
| Persistence? | `CreateEventSourceMapping20150331`, `UpdateEventSourceMapping20150331`, `CreateFunctionUrlConfig`, `AddPermission20150331v2`, `AddLayerVersionPermission`, `CreateFunction20150331` |

CloudTrail notes from the Lambda page:
- The `eventName` may carry date and version information (for example `GetFunction20150331v2` for the `GetFunction`
  API), so search with a wildcard or the exact versioned names.
- The `Environment` and `ZipFile` parameters are omitted from the logs for `CreateFunction`,
  `UpdateFunctionConfiguration` (Environment) and `UpdateFunctionCode` (ZipFile), and `ZipFile` for
  `PublishLayerVersion`. CloudTrail will not show you the payload or the environment values an attacker set.
- Management events are logged by default and in the 90-day Event history; `Invoke` is a data event
  (`AWS::Lambda::Function`) and is not logged unless you enabled data events. Without them, invocation abuse may be
  invisible. For history beyond 90 days you need a trail or CloudTrail Lake event data store.
- Single-Region trails see only their Region; multi-Region is recommended.

## Contain and remediate
Revoke or restrict the execution role's permissions, remove attacker triggers and permissions, redeploy from source
control, and least-privilege the role. Capture evidence (versions, configuration, logs) before changing anything.

## Verify
Deployed code hash matches the repo build, and no attacker triggers, URL configs or resource-policy statements remain.

## Checked
2026-11-08. Confirmed on the cited Lambda pages: the $LATEST and published-version immutability behaviour, version
numbers never reused, the management event names with version suffixes, omitted parameters, `Invoke` as a data event
that is off by default, 90-day Event history, and multi-Region trail guidance; the Azure Functions monitoring page for
Application Insights integration. `aws lambda get-function` and the `Qualifier` option, and the Lambda operation
names, confirmed in the botocore model. Removed (unconfirmed): the 10-minute validity of the presigned code URL,
`/proc/self/environ` credential theft details, /tmp persistence, reserved concurrency of 0 as a stop mechanism,
`aws:TokenIssueTime` revocation, and X-Ray / log-group specifics.
Method: documentation only; no commands were run.
