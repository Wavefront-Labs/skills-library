---
id: computing-software.cloud-infrastructure-engineering.aws.step-functions-versions-aliases-and-gradual-deployment
name: step-functions-versions-aliases-and-gradual-deployment
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, step-functions, sfn-versions, sfn-aliases, gradual-deployment, canary, state-machine-alias]
level: practitioner
status: docs-checked
description: "Publish immutable Step Functions state machine versions, route traffic with aliases, and roll out new definitions gradually with CloudFormation deployment preferences."
sources: ["https://docs.aws.amazon.com/step-functions/latest/dg/concepts-state-machine-version.html", "https://docs.aws.amazon.com/step-functions/latest/dg/concepts-state-machine-alias.html", "https://docs.aws.amazon.com/AWSCloudFormation/latest/TemplateReference/aws-resource-stepfunctions-statemachinealias.html", "https://docs.aws.amazon.com/step-functions/latest/dg/procedure-cw-metrics.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Step Functions versions, aliases and gradual deployment

**Goal:** callers start executions against a stable alias, new definitions are published as
immutable versions, and traffic shifts to them in steps with automatic rollback.

## Versions
```bash
aws stepfunctions update-state-machine --state-machine-arn "$SM" \
  --definition file://def.json --publish --version-description "add fraud check"
aws stepfunctions list-state-machine-versions --state-machine-arn "$SM"
```
- A version (`...:stateMachine:orders:3`) freezes the definition, role ARN, logging and tracing config.
- Up to 1,000 versions per state machine (soft limit); delete unused ones (`delete-state-machine-version`). Version numbers are never reused.
- Starting the unqualified ARN runs the most recent revision, not a version.

## Aliases
```bash
aws stepfunctions create-state-machine-alias --name prod \
  --routing-configuration stateMachineVersionArn=$SM:3,weight=90 stateMachineVersionArn=$SM:4,weight=10
aws stepfunctions start-execution --state-machine-arn "$SM:prod" --input '{}'
```
- An alias routes to one or two versions of the same state machine by weight (weights total 100); up to 100 aliases per state machine. An alias cannot point to another alias.
- When you start an execution from an alias, Step Functions randomly picks the version according to the weights.
- A redriven execution keeps the version and alias of the original attempt.

## Gradual deployment with CloudFormation
```yaml
Version:
  Type: AWS::StepFunctions::StateMachineVersion
  Properties: {StateMachineArn: !Ref Orders, StateMachineRevisionId: !GetAtt Orders.StateMachineRevisionId}
ProdAlias:
  Type: AWS::StepFunctions::StateMachineAlias
  Properties:
    Name: prod
    DeploymentPreference:
      StateMachineVersionArn: !Ref Version
      Type: LINEAR            # or CANARY / ALL_AT_ONCE
      Percentage: 20
      Interval: 5             # minutes between steps
      Alarms: [!Ref OrdersFailedAlarm]
```
- If any listed alarm goes to ALARM during the shift, CloudFormation rolls the alias back to the previous version.
- Alarm on `ExecutionsFailed` / `ExecutionsTimedOut`; execution metrics have `Version` and `Alias` dimensions (with `StateMachineArn`) for executions started through them. `RoutingConfiguration` and `DeploymentPreference` are mutually exclusive on the alias resource.

## Gotchas
- With `StateMachineRevisionId`, CloudFormation publishes a new version when that value differs from the previous stack, so the version always points at the most recent revision.
- All versions of a state machine share the same type (Standard or Express), name and creation date; the definition, role, tracing and logging configuration can differ per version.

## Verify
- [ ] Callers reference `:prod`, not the unqualified ARN.
- [ ] A canary deploy with a forced failing version triggers the alarm and rolls back.
- [ ] Old versions pruned by a lifecycle script.

## Checked
Checked 2026-10-24 against the Step Functions developer guide (versions, aliases, CloudWatch metrics, redrive) and the CloudFormation AWS::StepFunctions::StateMachineAlias reference.
Confirmed: versions are immutable snapshots with what can differ, up to 1,000 versions and 100 aliases, alias routing to at most two versions, unqualified start uses the latest revision, publish via update-state-machine with publish, CloudFormation DeploymentPreference (LINEAR, CANARY, ALL_AT_ONCE, Percentage, Interval, Alarms) with alarm-triggered rollback, StateMachineRevisionId usage, Version and Alias metric dimensions, redrive keeps version and alias.
Removed as unconfirmed: SAM AutoPublishAlias statement, StartExecution-on-alias IAM pinning, Express alias remark.

Method: documentation only; no commands were run.
