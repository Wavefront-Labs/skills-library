---
id: computing-software.cloud-infrastructure-engineering.aws.ecs-blue-green-with-codedeploy
name: ecs-blue-green-with-codedeploy
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, ecs, codedeploy, ecs-blue-green-codedeploy, ecs-codedeploy, blue-green-deployment, alb, appspec]
level: practitioner
status: docs-checked
description: "Run ECS blue/green deployments with CodeDeploy: two target groups and listeners, appspec hooks, canary and linear configs, alarm-based rollback, native alternative."
sources: ["https://docs.aws.amazon.com/AmazonECS/latest/developerguide/deployment-type-bluegreen.html", "https://docs.aws.amazon.com/codedeploy/latest/userguide/deployment-steps-ecs.html", "https://docs.aws.amazon.com/codedeploy/latest/userguide/reference-appspec-file-structure-hooks.html", "https://docs.aws.amazon.com/AmazonECS/latest/developerguide/alb.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ECS blue/green with CodeDeploy

## 1. Infrastructure
- ALB (or NLB) with a **production listener** (443) and an optional **test listener** (e.g. 8443, restricted SG); both listeners must belong to the same load balancer. With an NLB only `CodeDeployDefault.ECSAllAtOnce` is supported.
- Two target groups (`tg-blue`, `tg-green`); awsvpc tasks (including Fargate) register as `ip` targets.
- ECS service with `deploymentController: {type: CODE_DEPLOY}`.
- CodeDeploy application (compute platform ECS) + deployment group referencing cluster,
  service, both target groups, both listeners, an IAM role that lets CodeDeploy call ECS, Elastic Load Balancing, Lambda and CloudWatch
  (the ECS guide names it `ecsCodeDeployRole`), alarms and auto-rollback settings.

## 2. appspec.yaml
```yaml
version: 0.0
Resources:
  - TargetService:
      Type: AWS::ECS::Service
      Properties:
        TaskDefinition: "arn:aws:ecs:<REGION>:<ACCOUNT_ID>:task-definition/web:42"
        LoadBalancerInfo:
          ContainerName: web
          ContainerPort: 8080
Hooks:
  - AfterAllowTestTraffic: "arn:aws:lambda:<REGION>:<ACCOUNT_ID>:function:smoke-test-green"
  - BeforeAllowTraffic: "arn:aws:lambda:<REGION>:<ACCOUNT_ID>:function:pre-traffic-check"
```
Hook Lambdas must report `Succeeded` or `Failed` through the CodeDeploy `PutLifecycleEventHookExecutionStatus`
API within one hour, otherwise the deployment fails. Scriptable ECS hooks run in this order: BeforeInstall → AfterInstall → AfterAllowTestTraffic →
BeforeAllowTraffic → AfterAllowTraffic.

## 3. Deploy
```bash
aws deploy create-deployment --application-name web --deployment-group-name web-prod \
  --deployment-config-name CodeDeployDefault.ECSCanary10Percent5Minutes \
  --revision '{"revisionType":"AppSpecContent","appSpecContent":{"content":"<appspec yaml/json>"}}'
```
Configs: `ECSAllAtOnce`, `ECSLinear10PercentEvery1Minutes`/`...3Minutes`,
`ECSCanary10Percent5Minutes`/`...15Minutes`, or custom. The deployment group's termination wait time keeps blue tasks
for fast rollback.

## 4. Rollback
Deployment group CloudWatch alarms (5XX on green TG, latency) that stop the deployment, plus the deployment group's
auto-rollback settings. Manual: `aws deploy stop-deployment`.

## Alternative
The ECS guide recommends the **native ECS blue/green deployment** (see "Creating an Amazon ECS blue/green deployment")
over this CodeDeploy-controlled type; evaluate it before building the CodeDeploy setup.

## Gotchas
- If the service's network configuration or platform version changes, the AppSpec file must state those details too.
- CodeDeploy waits up to an hour for the green task set to reach steady state when the service is scaling; a scaling event during traffic shifting that does not reach steady state within 5 minutes fails the deployment.
- Keep the test listener off the public internet.

## Verify
- [ ] A deployment shifts 10% → 100% with green TG healthy; blue tasks terminated after the wait time.
- [ ] Failing hook or alarm triggers rollback; prod listener back on blue.

## Checked
Checked 2026-10-24 against the current ECS developer guide and CodeDeploy user guide.
Confirmed: predefined ECS deployment configurations and canary/linear/all-at-once semantics, NLB limited to ECSAllAtOnce, production and optional test listener on one load balancer, CodeDeploy-controlled blue/green is not the recommended type (native ECS blue/green is), ecsCodeDeployRole, ECS hook list and run order, one-hour hook result window, appspec network/platform note, scaling and steady-state behaviour, ip targets for awsvpc.
Removed as unconfirmed: CodePipeline appspec generation, auto-rollback event names, the immutability of the deployment controller, rollback timing.

Method: documentation only; no commands were run.
