---
id: computing-software.devops-ci-cd.deployment-strategies.ecs-blue-green-with-codedeploy
name: ecs-blue-green-with-codedeploy
category: computing-software
field: devops-ci-cd
product: deployment-strategies
tags: [deployment-strategies, codedeploy-ecs, blue-green, target-groups]
level: advanced
status: docs-checked
description: "Run Amazon ECS blue/green deployments: CodeDeploy appspec, two target groups and listeners, test traffic, lifecycle hooks, alarms rollback; plus native ECS blue/green."
sources: ["https://docs.aws.amazon.com/AmazonECS/latest/developerguide/deployment-type-bluegreen.html", "https://docs.aws.amazon.com/codedeploy/latest/userguide/reference-appspec-file-structure-hooks.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ECS blue/green with CodeDeploy

## Prerequisites
- ALB/NLB with **two target groups** (blue, green) and a production listener (443); optional test
  listener (e.g. 8443) for pre-traffic testing.
- ECS service with `deploymentController: { type: CODE_DEPLOY }`.
- CodeDeploy application (compute platform ECS) + deployment group referencing cluster, service,
  target groups, listeners, rollback alarms.

## appspec.yaml
```yaml
Resources:
  - TargetService:
      Type: AWS::ECS::Service
      Properties:
        TaskDefinition: "arn:aws:ecs:eu-west-1:123456789012:task-definition/api:42"
        LoadBalancerInfo: { ContainerName: api, ContainerPort: 8080 }
Hooks:
  - AfterAllowTestTraffic: "arn:aws:lambda:eu-west-1:123456789012:function:api-smoke"
```
Hook Lambdas must report their result back to CodeDeploy (see the AppSpec hooks page).

## Traffic shifting configs
`CodeDeployDefault.ECSAllAtOnce`, `ECSLinear10PercentEvery1Minutes`, `ECSCanary10Percent5Minutes`,
or custom. The deployment group's original revision termination setting keeps blue tasks for fast rollback.

## Native ECS blue/green
Amazon ECS also offers a built-in blue/green deployment type with bake time and lifecycle hooks (see the ECS developer guide page on blue/green deployments); compare it with CodeDeploy before choosing for a new service.

## Gotchas
- Pipeline must register a new task definition revision and pass it via appspec.
- Blue and green run side by side during the deployment: check capacity and service quotas.

## Verify
- [ ] Failing hook or alarm reverts traffic to blue automatically.

## Checked

2026-10-28. Confirmed against the ECS developer guide and CodeDeploy docs: CODE_DEPLOY deployment controller, the three ECS traffic-shifting configs (`CodeDeployDefault.ECSAllAtOnce`, `ECSLinear10PercentEvery1Minutes`, `ECSCanary10Percent5Minutes`), the `AfterAllowTestTraffic` hook, the appspec `Resources` / `TargetService` / `LoadBalancerInfo` structure, original revision termination settings, and ECS native blue/green with bake time and lifecycle hooks. Removed: the immutable-controller claim, `version: 0.0`, the hook API call name, `terminationWaitTimeInMinutes`, the 2025 date and BLUE_GREEN API field, the alarm-placement and direct-update claims, Fargate limits and the console status text.

Method: documentation only; no commands were run.
