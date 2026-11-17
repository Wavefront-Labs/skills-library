---
id: computing-software.devops-ci-cd.deployment-strategies.serverless-and-lambda-deployments
name: serverless-and-lambda-deployments
category: computing-software
field: devops-ci-cd
product: deployment-strategies
tags: [deployment-strategies, serverless-deploy, lambda-deployment, lambda-aliases, lambda-versions, weighted-alias, routing-config, codedeploy-lambda, linear10percentevery1minute, canary10percent5minutes, sam-deploy, deploymentpreference, pre-traffic-hook, post-traffic-hook, cloudwatch-alarms-rollback, provisioned-concurrency, cold-starts, cloud-run-revisions, traffic-splitting, azure-functions-slots, deployment-slots, cloudfront-functions, api-gateway-stages, stage-variables, immutable-versions, serverless-framework, cdk-lambda-alias]
level: practitioner
status: draft
description: "Ship functions safely: Lambda versions and aliases with weighted traffic, CodeDeploy canary/linear shifts with alarm rollback and SAM DeploymentPreference, Cloud Run revisions, Azure slots."
sources: ["https://docs.aws.amazon.com/lambda/latest/dg/configuration-aliases.html", "https://docs.aws.amazon.com/lambda/latest/dg/lambda-rolling-deployments.html", "https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/automating-updates-to-serverless-apps.html", "https://cloud.google.com/run/docs/rollouts-rollbacks-traffic-migration", "https://learn.microsoft.com/en-us/azure/azure-functions/functions-deployment-slots"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Serverless and Lambda deployments

**Goal:** a new function version takes traffic gradually, rolls back automatically on
alarms, and invokers (API Gateway, EventBridge, SQS) never point at `$LATEST`.

## 1. Lambda model: versions are immutable, aliases route
- `aws lambda publish-version` freezes code + config as `:N`. `$LATEST` is mutable —
  **never** invoke it from production triggers.
- An **alias** (`prod`, `staging`) points at a version and can split traffic between
  **two** versions by weight: `routing-config AdditionalVersionWeights={"42"=0.1}`.
  Routing is random per invocation (not sticky); both versions must be compatible with
  the same event shapes.
- Triggers reference the alias ARN (`…:function:orders:prod`). Event source mappings
  (SQS/Kinesis/DynamoDB streams) attached to an alias follow it; with weighted aliases,
  stream/queue sources **ignore the weights** and use the primary version — gradual
  shifting only applies to synchronous/async invokes (API Gateway, EventBridge, direct).
- Env vars, memory, layers are part of the version: config changes need a new version.

```bash
V=$(aws lambda publish-version --function-name orders --description "$GIT_SHA" --query Version --output text)
aws lambda update-alias --function-name orders --name prod --function-version "$PREV" \
  --routing-config "AdditionalVersionWeights={\"$V\"=0.1}"        # 10 % canary
# … watch alarms …
aws lambda update-alias --function-name orders --name prod --function-version "$V" --routing-config '{}'   # promote
# rollback = point alias back at $PREV
```

## 2. CodeDeploy does the shifting and the rollback
AWS SAM/CDK/Serverless Framework wire this for you:
```yaml
# template.yaml (SAM)
Resources:
  Orders:
    Type: AWS::Serverless::Function
    Properties:
      AutoPublishAlias: prod
      DeploymentPreference:
        Type: Canary10Percent5Minutes          # or Linear10PercentEvery1Minute, AllAtOnce, Canary10Percent30Minutes…
        Alarms: [!Ref OrdersErrorsAlarm, !Ref OrdersLatencyAlarm]
        Hooks: { PreTraffic: !Ref PreTrafficHook, PostTraffic: !Ref PostTrafficHook }
      ProvisionedConcurrencyConfig: { ProvisionedConcurrentExecutions: 5 }
  OrdersErrorsAlarm:
    Type: AWS::CloudWatch::Alarm
    Properties:
      Namespace: AWS/Lambda
      MetricName: Errors
      Dimensions: [{ Name: FunctionName, Value: !Ref Orders }, { Name: Resource, Value: !Sub "${Orders}:prod" }]
      Statistic: Sum
      Period: 60
      EvaluationPeriods: 2
      Threshold: 1
      ComparisonOperator: GreaterThanOrEqualToThreshold
      TreatMissingData: notBreaching
```
`sam deploy` publishes a version, creates a CodeDeploy deployment that shifts the alias
by the chosen schedule, and **rolls back** (alias → previous version) if any alarm goes
to ALARM or a hook fails. Hooks are Lambdas that call
`codedeploy put-lifecycle-event-hook-execution-status` (`Succeeded`/`Failed`) — the
PreTraffic hook invokes the *new version* directly (`:$NEW_VERSION` ARN passed in the
event) with synthetic requests before any traffic; PostTraffic runs smoke checks.
Alarm dimensions must target the **alias** (`Resource: name:prod`) or the new version,
otherwise a quiet function never alarms (`TreatMissingData: notBreaching` keeps a
no-traffic canary from false-alarming — but then also add an **invocation-count** sanity
check in the PostTraffic hook).
CDK: `new codedeploy.LambdaDeploymentGroup(... { alias, deploymentConfig: LambdaDeploymentConfig.CANARY_10PERCENT_5MINUTES, alarms })`.
Serverless Framework: `serverless-plugin-canary-deployments`.

## 3. Things that bite
- **Cold starts during shift**: the new version has no warm sandboxes; p99 spikes can
  trip latency alarms → use provisioned concurrency on the alias (it applies per
  version; CodeDeploy warms the new version when PC is configured on the alias) or alarm
  on p95 over longer periods.
- **Layers and runtime deprecations**: a version pins a runtime; AWS blocks *updates*
  (not invokes) to deprecated runtimes — plan upgrades as versions.
- **Concurrency limits**: reserved concurrency is per function (all versions); a canary
  plus provisioned concurrency can exhaust the account's regional limit.
- **Async retries**: failed async invokes retry twice by default — during a bad canary
  that's amplified; set `MaximumRetryAttempts` and a DLQ/on-failure destination.
- **API Gateway stages**: stage variables (`${stageVariables.alias}`) in the integration
  URI let one API stage target the alias; deploying an API stage is separate from
  deploying the function — don't forget `aws apigateway create-deployment` (SAM does it).
- **Alias weights on versions with different IAM/env**: the execution role is per
  function, env per version — a canary with a new env var works; a new permission needs
  the role updated first (roles aren't versioned).

## 4. Google Cloud Run (revisions)
```bash
gcloud run deploy orders --image gcr.io/p/orders@sha256:… --no-traffic --tag canary   # new revision, 0 %
curl https://canary---orders-xyz.a.run.app/health                                        # tagged URL for smoke tests
gcloud run services update-traffic orders --to-revisions orders-00042-abc=10,orders-00041-def=90
gcloud run services update-traffic orders --to-latest                                   # promote
```
Revisions are immutable; `--no-traffic` + tag gives a private URL; rollback =
`update-traffic --to-revisions <old>=100`. Min instances per revision avoid cold starts
on the canary. Cloud Functions 2nd gen are Cloud Run services underneath — same model.

## 5. Azure Functions (deployment slots)
Premium/Dedicated plans: a `staging` slot gets the new package; warm it; **swap** with
production (near-instant, swaps hostnames; config marked "deployment slot setting"
stays with the slot). Traffic percentage routing between slots is available on App
Service plans (`az webapp traffic-routing set --distribution staging=10`). Consumption
plan: one slot only on Windows (preview/limited) — prefer Flex Consumption or Premium
for safe rollouts. Rollback = swap back.

## 6. Pipeline shape (any provider)
build + unit tests → package (zip/image, immutable, digest) → deploy to **staging
function/alias/revision** → integration tests via the tagged/alias URL → production
canary via platform traffic shifting with alarms → promote → record version in the
deployment log. Infrastructure for the function (roles, queues, API) via IaC in the same
pipeline, applied *before* the code shift.

## Verify
- [ ] No production trigger references `$LATEST`; `aws lambda list-event-source-mappings` and API integrations point at the `prod` alias.
- [ ] A deploy with a forced error in the new version rolls back automatically within the canary window and the alias still points at the old version.
- [ ] PreTraffic hook invokes the new version and blocks a broken build before any user traffic.
- [ ] p99 during a shift is within the SLO (provisioned concurrency sized) and alarms use alias dimensions.
