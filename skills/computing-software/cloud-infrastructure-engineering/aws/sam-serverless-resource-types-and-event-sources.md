---
id: computing-software.cloud-infrastructure-engineering.aws.sam-serverless-resource-types-and-event-sources
name: sam-serverless-resource-types-and-event-sources
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, sam, serverless-function, sam-events, aws-serverless, sam-globals, sam-policy-templates, sam-connectors]
level: practitioner
status: docs-checked
description: "Write SAM templates with the right AWS::Serverless resource types and event sources: Function events, Globals, policy templates, connectors and what SAM generates underneath."
sources: ["https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-property-function-eventsource.html", "https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-resource-layerversion.html", "https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-resource-connector.html", "https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-property-function-s3.html", "https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/automating-updates-to-serverless-apps.html", "https://github.com/aws/serverless-application-model/blob/develop/samtranslator/model/eventsources/push.py"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SAM resource types and event sources

## Resource types
| Type | Generates |
|---|---|
| `AWS::Serverless::Function` | Lambda function, role, permissions, event source resources, optional alias/version |
| `AWS::Serverless::Api` / `HttpApi` | REST / HTTP API, stage, deployment |
| `AWS::Serverless::StateMachine` | Step Functions state machine with role and event triggers |
| `AWS::Serverless::SimpleTable` | single-key DynamoDB table |
| `AWS::Serverless::LayerVersion` | Lambda layer (`RetentionPolicy`: `Retain` or `Delete` for old versions) |
| `AWS::Serverless::Application` | nested stack (SAR or local) |
| `AWS::Serverless::Connector` | IAM permissions between two resources |
| `AWS::Serverless::GraphQLApi` | AppSync API |
Template needs `Transform: AWS::Serverless-2016-10-31`.

## Function with events
```yaml
Globals:
  Function: {Runtime: python3.12, Architectures: [arm64], Timeout: 10, Tracing: Active}
Resources:
  Worker:
    Type: AWS::Serverless::Function
    Properties:
      Handler: app.handler
      CodeUri: src/
      Policies: [DynamoDBCrudPolicy: {TableName: !Ref Table}, SQSPollerPolicy: {QueueName: !GetAtt Q.QueueName}]
      Events:
        Queue: {Type: SQS, Properties: {Queue: !GetAtt Q.Arn, BatchSize: 10, FunctionResponseTypes: [ReportBatchItemFailures]}}
        Nightly: {Type: ScheduleV2, Properties: {ScheduleExpression: "cron(0 2 * * ? *)"}}
        Api: {Type: HttpApi, Properties: {Path: /orders, Method: post}}
        Upload: {Type: S3, Properties: {Bucket: !Ref Bucket, Events: s3:ObjectCreated:*}}
```
Event types: `AlexaSkill`, `Api`, `CloudWatchEvent`, `CloudWatchLogs`, `Cognito`, `DocumentDB`, `DynamoDB`, `EventBridgeRule`, `HttpApi`,
`IoTRule`, `Kinesis`, `MQ`, `MSK`, `S3`, `Schedule`, `ScheduleV2`, `SelfManagedKafka`, `SNS`, `SQS`.

## Connectors instead of hand-written policies
```yaml
WorkerToTable:
  Type: AWS::Serverless::Connector
  Properties: {Source: {Id: Worker}, Destination: {Id: Table}, Permissions: [Read, Write]}
```

## Gotchas
- The `S3` event's `Bucket` must be a bucket declared in the same template.
- `Policies` are appended to the function's default execution role.
- `DeploymentPreference` (CodeDeploy traffic shifting) works with `AutoPublishAlias`, which creates an alias pointing at the new version.
- Validate with `sam validate --lint`.
- Deploys show `CAPABILITY_IAM`; `CAPABILITY_AUTO_EXPAND` appears in the SAM CLI docs for nested applications and macros.

## Verify
- [ ] `sam validate --lint` passes; `sam build && sam deploy --guided` deploys.
- [ ] Each event source shows on the function's triggers in the Lambda console.

## Checked
Date: 2026-10-24. Documentation release: AWS SAM Developer Guide (awsdocs source, June 2023 snapshot) plus the aws/serverless-application-model translator source (version 1.115.0, event source classes) and its JSON schema.
Confirmed: Function event type list (the documentation `Valid values` list, matching the translator's event classes plus `ScheduleV2`); `Connector` structure with `Source`, `Destination` and `Permissions`; `S3` bucket must be in the same template; `Policies` are appended to the default role; `AutoPublishAlias` plus `DeploymentPreference`; SQS `BatchSize` and `FunctionResponseTypes` properties; LayerVersion `RetentionPolicy` values.
Removed as unconfirmed: the default layer retention, the EventBridge advice for existing buckets, the `Policies` and `Role` exclusivity claim and the claim that every code change creates a version.

Method: documentation only; no commands were run.
