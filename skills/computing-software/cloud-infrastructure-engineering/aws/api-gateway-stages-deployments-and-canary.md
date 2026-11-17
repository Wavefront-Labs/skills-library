---
id: computing-software.cloud-infrastructure-engineering.aws.api-gateway-stages-deployments-and-canary
name: api-gateway-stages-deployments-and-canary
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, api-gateway, stage-variables, canary-release, apigw-deployment, rest-api, http-api, release-management]
level: practitioner
status: docs-checked
description: "Manage API Gateway deployments and stages: immutable deployments, stage variables for backends, canary releases with promotion/rollback, and HTTP API auto-deploy."
sources: ["https://docs.aws.amazon.com/apigateway/latest/developerguide/stages.html", "https://docs.aws.amazon.com/apigateway/latest/developerguide/canary-release.html", "https://docs.aws.amazon.com/apigateway/latest/developerguide/promote-canary-deployment.html", "https://docs.aws.amazon.com/apigateway/latest/developerguide/stage-variables.html", "https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-stages.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# API Gateway stages, deployments and canary releases

**Goal:** know what is live on each stage, ship API changes gradually, roll back in seconds.

## 1. Mental model (REST)
Editing resources/methods changes nothing live. A **deployment** is an immutable snapshot;
a **stage** points at one deployment and holds stage settings (throttling, logging, cache,
variables, canary).
```bash
aws apigateway create-deployment --rest-api-id "$API" --stage-name prod --description "v2025.10.16"
aws apigateway get-stage --rest-api-id "$API" --stage-name prod --query deploymentId
# rollback = point the stage at an earlier deployment
aws apigateway update-stage --rest-api-id "$API" --stage-name prod \
  --patch-operations op=replace,path=/deploymentId,value=<OLD_DEPLOYMENT_ID>
```
HTTP APIs: stages can use automatic deployment (changes to the API are deployed automatically) — use it on `dev` only.

## 2. Stage variables
Point one API definition at different backends per stage:
- Lambda integration URI `...:function:orders:${stageVariables.alias}` with stage variable
  `alias=prod` / `alias=beta`. When the function comes from a stage variable, grant API Gateway permission with
  `lambda add-permission` (`--principal apigateway.amazonaws.com`).
- HTTP integration `https://${stageVariables.backendHost}/orders`.
- In VTL: `$stageVariables.name`. Stage variables are not intended for sensitive data such as credentials.

## 3. Canary release (REST APIs)
```bash
aws apigateway create-deployment --rest-api-id "$API" --stage-name prod \
  --canary-settings percentTraffic=10,useStageCache=false
# watch canary metrics/logs, then promote:
aws apigateway update-stage --rest-api-id "$API" --stage-name prod --patch-operations \
  op=copy,from=/canarySettings/deploymentId,path=/deploymentId \
  op=remove,path=/canarySettings
# or roll back:
aws apigateway update-stage --rest-api-id "$API" --stage-name prod --patch-operations op=remove,path=/canarySettings
```
- With execution logging on, canary requests get their own logs and metrics, reported to the stage log group and to a
  canary-specific log group (the stage log group name with a `/Canary` suffix); compare errors and latency.
- A canary can override stage variables (`stageVariableOverrides`), for example to point at a new Lambda alias.

## Gotchas
- Canary traffic is split at random per request with the configured ratio.

## Verify
- [ ] `get-stage` deploymentId matches the deployment you just created; `get-deployments` lists history with descriptions.
- [ ] With canary at 10%, the canary log group receives about a tenth of the requests.
- [ ] Rollback command restores the previous behaviour on a test call.

## Checked
Date: 2026-10-24. Documentation release: Amazon API Gateway Developer Guide (awsdocs source, June 2023 snapshot).
Confirmed: a deployment is needed for changes to take effect; HTTP API automatic deployment; canary settings (`percentTraffic`, `useStageCache`, `stageVariableOverrides`); promotion copies `/canarySettings/deploymentId` to `/deploymentId`; removing `/canarySettings` ends the canary; separate canary logs and random per-request split; stage variables are not for credentials; `lambda add-permission` for stage-variable functions.
Removed as unconfirmed: the CloudFormation logical-ID remark, the stage-deletion and mapping remark, the `Stage: prod/Canary` metric dimension and the per-alias permission claim. The execution log group naming differs between documentation pages, so only the `/Canary` suffix is stated.

Method: documentation only; no commands were run.
