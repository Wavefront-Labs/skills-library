---
id: computing-software.devops-ci-cd.deployment-strategies.serverless-traffic-rollback
name: serverless-traffic-rollback
category: computing-software
field: devops-ci-cd
product: deployment-strategies
tags: [deployment-strategies, traffic-rollback, lambda-alias, cloud-run-revisions, azure-functions-slots, codedeploy-lambda, instant-rollback]
level: practitioner
status: draft
description: "Roll back serverless deployments by shifting traffic: Lambda aliases and CodeDeploy auto-rollback, Cloud Run revisions, Azure slot swaps, and data caveats."
sources:
  - https://docs.aws.amazon.com/lambda/latest/dg/configuring-alias-routing.html
  - https://docs.aws.amazon.com/codedeploy/latest/userguide/deployment-configurations.html#deployment-configuration-lambda
  - https://cloud.google.com/run/docs/rollouts-rollbacks-traffic-migration
  - https://learn.microsoft.com/en-us/azure/azure-functions/functions-deployment-slots
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Serverless traffic rollback

Serverless platforms keep previous versions around immutably, so rollback is a routing change, not a redeploy. That works only if callers hit an alias/route, not a specific version.

## AWS Lambda
Publish versions and point an alias (`live`) at them; invoke the alias everywhere (API Gateway integration, event source mappings).
```bash
aws lambda publish-version --function-name orders                 # -> version 42
aws lambda update-alias --function-name orders --name live --function-version 41 \
  --routing-config 'AdditionalVersionWeights={"42"=0.1}'           # 90% stays on 41, 10% to 42
# rollback:
aws lambda update-alias --function-name orders --name live --function-version 41 --routing-config '{}'
```
Automate with CodeDeploy (SAM `DeploymentPreference: { Type: Canary10Percent5Minutes, Alarms: [ErrorsAlarm], Hooks: { PreTraffic: ... } }`): alarms during the shift trigger automatic rollback to the previous version.

## Google Cloud Run
```bash
gcloud run deploy api --image IMAGE --no-traffic --tag candidate    # new revision gets 0% plus a test URL
gcloud run services update-traffic api --to-revisions api-00042-abc=10
gcloud run services update-traffic api --to-revisions api-00041-xyz=100   # rollback
gcloud run revisions list --service api
```
`--to-latest` makes traffic follow new deploys automatically; pin explicit revisions in production to keep rollback meaningful.

## Azure Functions / App Service
Deploy to a `staging` slot, warm it, then swap:
```bash
az functionapp deployment slot swap -g rg -n orders --slot staging --target-slot production
# rollback = swap again (previous production code now sits in staging)
```
Slot-sticky settings (`--slot-settings`) stay with the slot; check connection strings point where you expect after the swap.

## Caveats
- **Data and schema**: rolling back code doesn't roll back a migration or messages written in a new format. Keep changes backward compatible (expand/contract).
- **Async consumers**: SQS/Kinesis/Event Hubs triggers bound to the alias switch too; in-flight batches finish on the old version. Events already processed by the bad version need replay or compensation.
- **Configuration and IaC**: rollback via console/CLI creates drift with Terraform/SAM state; follow up with a commit that pins the old version.
- **Cold starts** at 100% switch: provisioned concurrency is per version/alias - configure it on the alias.

## Verify
- [ ] Rollback command executes in under a minute and the alias/route shows the previous version receiving 100%.
- [ ] Alarm-triggered automatic rollback tested once with a deliberately failing version.
