---
id: computing-software.cloud-infrastructure-engineering.aws.step-functions-sdk-and-optimized-integrations
name: step-functions-sdk-and-optimized-integrations
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, step-functions, sdk-integrations, optimized-integrations, arn-states, http-task, lambda, dynamodb]
level: practitioner
status: docs-checked
description: "Call AWS services directly from Step Functions with optimized and AWS SDK integrations: resource ARN shapes, parameter casing, error names, IAM and when to drop the Lambda."
sources: ["https://docs.aws.amazon.com/step-functions/latest/dg/supported-services-awssdk.html", "https://docs.aws.amazon.com/step-functions/latest/dg/connect-to-resource.html", "https://docs.aws.amazon.com/step-functions/latest/dg/call-https-apis.html", "https://docs.aws.amazon.com/step-functions/latest/dg/manage-state-machine-permissions.html", "https://docs.aws.amazon.com/step-functions/latest/dg/concepts-error-handling.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Step Functions service integrations

**Goal:** remove "glue" Lambdas that only call one AWS API — fewer cold starts, less code,
lower cost — and know which integration flavour you are using.

## 1. Two flavours, one ARN prefix
| | Optimized | AWS SDK |
|---|---|---|
| ARN | `arn:aws:states:::dynamodb:putItem` | `arn:aws:states:::aws-sdk:dynamodb:putItem` |
| Coverage | curated list of optimized integrations | over 200 services (some operations unsupported, e.g. S3 `SelectObjectContent`, Lambda `InvokeAsync`) |
| Extras | `.sync`/`.waitForTaskToken` for many (Standard workflows) | `.waitForTaskToken` only (Standard); no `.sync` |
| Params | per integration page | **PascalCase** parameters even when the native API is camelCase; action name in camelCase |

Examples:
```json
"Put": {"Type": "Task", "Resource": "arn:aws:states:::dynamodb:putItem",
  "Arguments": {"TableName": "orders",
    "Item": {"pk": {"S": "{% $states.input.id %}"}, "status": {"S": "NEW"}},
    "ConditionExpression": "attribute_not_exists(pk)"}, "Next": "Notify"},
"Notify": {"Type": "Task", "Resource": "arn:aws:states:::sns:publish",
  "Arguments": {"TopicArn": "arn:aws:sns:<REGION>:<ACCOUNT_ID>:orders", "Message": "{% $string($states.input) %}"}, "Next": "Tag"},
"Tag": {"Type": "Task", "Resource": "arn:aws:states:::aws-sdk:s3:putObjectTagging",
  "Arguments": {"Bucket": "docs", "Key": "{% $states.input.key %}",
    "Tagging": {"TagSet": [{"Key": "processed", "Value": "true"}]}}, "End": true}
```

## 2. Lambda: use the optimized invoke
`arn:aws:states:::lambda:invoke` returns the function result under `Payload` —
unwrap with `"Output": "{% $states.result.Payload %}"` (JSONata) or
`"ResultSelector": {"body.$": "$.Payload"}` (JSONPath). Add the standard Lambda retrier
(`Lambda.ServiceException`, `Lambda.SdkClientException`, `Lambda.TooManyRequestsException`).

## 3. HTTP Task for third-party APIs
`arn:aws:states:::http:invoke` with an EventBridge **connection** for auth (Basic, OAuth or API key). Required: `ApiEndpoint`, `Method` and the connection (`InvocationConfig.ConnectionArn`, which the guide recommends over the older `Authentication.ConnectionArn`); optional `Headers`, `QueryParameters`, `RequestBody`, `Transform`. Requests time out after 60 seconds; mutual TLS is not supported; binary and image responses fail with `States.Runtime`. The role needs `states:InvokeHTTPEndpoint`,
`events:RetrieveConnectionCredentials`, and `secretsmanager:GetSecretValue` and `secretsmanager:DescribeSecret` on the
connection's secret.

## 4. Errors
SDK integration errors are the service's exception prefix plus the error name, always with the `Exception` suffix, e.g.
`DynamoDb.ConditionalCheckFailedException` (prefix `DynamoDb`), `S3.NoSuchKeyException`, `Lambda.TooManyRequestsException`; the guide lists each service's prefix. Copy the exact string
from a failed execution's `TaskFailed` event into `ErrorEquals` if in doubt.

## 5. IAM
The state machine role needs the underlying permission (`dynamodb:PutItem`, `s3:PutObjectTagging`).
Workflow Studio cannot auto-generate policies for AWS SDK integrations; write them yourself and scope each action to the specific resource ARN.

## Gotchas
- 256 KiB payload limit applies to service responses too: `aws-sdk:s3:getObject` on a large
  object fails with `States.DataLimitExceeded`. Pass references (bucket/key), not bodies.
- Paginated APIs return one page; loop with a Choice on `NextToken` or keep a Lambda.

## Verify
- [ ] Each Task's `TaskSucceeded` event shows the expected API response shape.
- [ ] A forced failure (e.g. conditional put on an existing key) is caught by the exact `ErrorEquals` string.
- [ ] The role policy contains only the actions/resources the integrations use (Access Analyzer policy validation clean).

## Checked
Checked 2026-10-24 against the Step Functions developer guide (AWS SDK integrations, service integration patterns, HTTP Task, execution roles).
Confirmed: aws-sdk ARN form with camelCase action, PascalCase parameters, over 200 services, unsupported operations, .waitForTaskToken only, optimized-vs-SDK pattern support table, HTTP Task fields, permissions, 60 s timeout and limits, SDK error naming with service prefix and Exception suffix (DynamoDb, S3, Lambda prefixes), DataLimitExceeded for large connector output, no policy generation for SDK integrations.
Corrected: the DynamoDB error prefix is DynamoDb, not DynamoDB. Removed as unconfirmed: StatusCode in the Lambda wrapper, binary field handling.

Method: documentation only; no commands were run.
