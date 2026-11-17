---
id: computing-software.cloud-infrastructure-engineering.aws.sam-templates-and-local-testing
name: sam-templates-and-local-testing
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, sam, serverless-application-model, sam-cli, sam-build, sam-deploy, sam-local, sam-sync, sam-accelerate, aws-serverless-function, aws-serverless-api, globals, gradual-deployment, codedeploy-alias, lambda, api-gateway, local-testing, samconfig]
level: practitioner
status: docs-checked
description: "Build serverless apps with AWS SAM: template shorthand, sam build and deploy with samconfig, local invoke and start-api, sam sync for fast iteration, and canary deployments via alias."
sources: ["https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-specification-template-anatomy-globals.html", "https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/automating-updates-to-serverless-apps.html", "https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/using-sam-cli-sync.html", "https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-cli-command-reference-sam-build.html", "https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-cli-command-reference-sam-pipeline-bootstrap.html", "https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-policy-templates.html", "https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/validate-cfn-lint.html", "https://github.com/aws/serverless-application-model/blob/develop/samtranslator/model/preferences/deployment_preference_collection.py"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# AWS SAM — CloudFormation shorthand plus a CLI that builds, runs and ships Lambda

**Goal:** a serverless stack defined in a short SAM template, built reproducibly, tested
locally, and deployed with a canary that rolls back on alarms.

## 1. Template
```yaml
AWSTemplateFormatVersion: '2010-09-09'
Transform: AWS::Serverless-2016-10-31
Globals:
  Function: { Runtime: python3.12, Timeout: 10, MemorySize: 512, Architectures: [arm64], Tracing: Active }
Resources:
  Api:
    Type: AWS::Serverless::HttpApi
  Orders:
    Type: AWS::Serverless::Function
    Properties:
      CodeUri: src/orders/
      Handler: app.handler
      Policies: [DynamoDBCrudPolicy: { TableName: !Ref Table }]
      Events:
        Http: { Type: HttpApi, Properties: { ApiId: !Ref Api, Path: /orders, Method: POST } }
      AutoPublishAlias: live
      DeploymentPreference: { Type: Canary10Percent5Minutes, Alarms: [!Ref ErrorsAlarm] }
  Table:
    Type: AWS::Serverless::SimpleTable
```
- Resource types include `Function`, `Api` (REST), `HttpApi`, `SimpleTable`, `LayerVersion`,
  `StateMachine`, `Application` (nested from SAR) and `Connector` (configures permissions between two resources
  with `Permissions: [Read, Write]`; an alternative to hand-written policies).
- `Policies` accepts **SAM policy templates** (`SQSPollerPolicy`, `S3ReadPolicy`, `DynamoDBCrudPolicy`…), appended to the function's default execution role.
- Any plain CloudFormation resource can sit in the same template; SAM is a transform.
- Validate: `sam validate --lint` (validates with AWS CloudFormation Linter, cfn-lint).

## 2. Build and deploy
```bash
sam build --use-container          # builds deps in a Lambda-like image (native deps!)
sam deploy --guided                # first time: writes samconfig.toml
sam deploy --config-env prod       # later: non-interactive
```
- `sam deploy --guided` writes your answers to `samconfig.toml`; later `sam deploy` reuses them, and `--config-env` selects an
  environment section. Keep secrets out of it.
- Custom builds use a `Makefile` (`BuildMethod: makefile`); Rust uses `cargo-lambda`; `--cached` reuses unchanged artifacts
  (cache in `.aws-sam/cache`) and `--parallel` builds functions and layers in parallel.
- Container images: `PackageType: Image` + `Metadata.DockerContext`; `sam build` runs Docker,
  `sam deploy` pushes to the ECR repo in samconfig.
- `sam deploy` creates a change set and shows it; `--no-confirm-changeset` for CI,
  `--no-fail-on-empty-changeset` so a no-op does not fail the pipeline.

## 3. Local testing
```bash
sam local invoke Orders -e events/post-order.json --env-vars env.json
sam local start-api --warm-containers EAGER     # HTTP on :3000 routing to functions
sam local start-lambda                           # SDK-compatible endpoint for integration tests
sam local generate-event s3 put --bucket b --key k > events/s3.json
```
- Needs Docker; `sam local start-api` listens on port 3000 by default (`-p` changes it).
- Local runs are for handler logic and event shapes; do not point them at production resources.
- `--env-vars` supplies environment variable overrides from a JSON file.

## 4. Fast iteration: sam sync
`sam sync --stack-name dev --watch` uses AWS service APIs for resources that support them and falls back to a
CloudFormation deployment otherwise. The docs recommend it for development environments only; use `sam deploy` or a CI/CD pipeline for production.

## 5. Gradual deployments
`AutoPublishAlias` + `DeploymentPreference` makes SAM create the alias and use CodeDeploy to shift alias traffic.
Types include `Canary10Percent5Minutes`, `Canary10Percent10Minutes`, `Linear10PercentEvery1Minute`, `Linear10PercentEvery10Minutes`
and `AllAtOnce`. `Alarms` (CloudWatch alarms) trigger automatic rollback; `Hooks` run pre-traffic and post-traffic test functions.
Invocations should use the alias qualifier to take advantage of the shift.

## 6. Pipelines
`sam pipeline bootstrap` creates the pipeline resources and `sam pipeline init` generates the pipeline configuration;
`--permissions-provider [oidc | iam]` chooses how the pipeline execution role is assumed (default `iam`).

## Gotchas
- `Globals` are supported by `AWS::Serverless::Function`, `Api`, `HttpApi` and `SimpleTable` (check the Globals page for newer types); resources can override but not remove a global property.
- `--use-container` builds in a container image of the runtime, which helps with native dependencies.

## Verify
- [ ] `sam validate --lint` clean; `sam build --use-container` succeeds in CI.
- [ ] `sam local invoke` with a generated event returns the expected status for every handler.
- [ ] A repeat `sam deploy --config-env dev --no-fail-on-empty-changeset` with no changes succeeds.
- [ ] A canary deploy with a deliberately failing version rolls back on the alarm.
- [ ] Policies in the transformed template are scoped to the resources the function needs.

## Checked
Date: 2026-10-24. Documentation release: AWS SAM Developer Guide (awsdocs source, June 2023 snapshot) plus the aws/serverless-application-model translator source (version 1.115.0) and the botocore Lambda runtime list.
Confirmed: `Transform: AWS::Serverless-2016-10-31`; policy template names; Connector `Permissions` values Read and Write; `sam validate --lint` uses cfn-lint; `samconfig.toml` written by `sam deploy --guided`; `--config-env`, `--cached`, `--parallel`, `--use-container`; `sam local start-api` default port 3000; `sam sync` behaviour and the development-only recommendation; deployment preference type names (from the translator source) and `Alarms` and `Hooks`; `--permissions-provider [oidc | iam]`; Globals support list and override rule; `python3.12` is a Lambda runtime identifier.
Removed as unconfirmed: statements about what `sam local` does not emulate, native-wheel examples, the two-stage pipeline description, implicit API behaviour, non-deterministic build redeploys and the cost note on Globals.

Method: documentation only; no commands were run.
