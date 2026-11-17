---
id: computing-software.cloud-infrastructure-engineering.aws.cloudformation-stacks-change-sets-and-drift
name: cloudformation-stacks-change-sets-and-drift
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, cloudformation, cfn, change-set, change-sets, stack-drift, drift-detection, stacksets, stackset, nested-stacks, stack-policy, deletion-policy, update-replace-policy, rollback, cfn-lint, cfn-guard, intrinsic-functions, parameters, outputs, exports, custom-resources, import-resources]
level: practitioner
status: docs-checked
description: "Operate CloudFormation safely: change sets before every update, DeletionPolicy and stack policies to protect data, drift detection, resource import, StackSets and rollback recovery."
sources: ["https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-changesets.html", "https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/detect-drift-stack.html", "https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/what-is-cfnstacksets.html", "https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/protect-stack-resources.html", "https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-rollback-triggers.html", "https://docs.aws.amazon.com/AWSCloudFormation/latest/APIReference/API_CreateStackRefactor.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# CloudFormation — stacks you can update on a Friday

**Goal:** every change is previewed as a change set, stateful resources cannot be replaced
or deleted by accident, drift is detected before it bites, and multi-account rollouts use
StackSets rather than a loop of `deploy` commands.

## 1. Template hygiene
- YAML; `Parameters` for environment inputs (with `AllowedValues`, SSM-backed types like
  `AWS::SSM::Parameter::Value<AWS::EC2::Image::Id>`), `Mappings` for static lookups,
  `Conditions` for per-env toggles, `Outputs` + `Export` only for truly shared values
  (an export cannot be deleted while imported — it couples stacks).
- Keep stacks by lifecycle: network (rarely changes) / data (stateful) / app (changes daily).
  A template can declare at most 500 resources; split larger stacks (nested stacks are one option).
- Name resources only when you must; a fixed physical name can collide with an existing resource or block replacement.

## 2. Protect stateful resources
```yaml
MyDB:
  Type: AWS::RDS::DBInstance
  DeletionPolicy: Snapshot        # Delete | Retain | Snapshot | RetainExceptOnCreate (Snapshot only for supported resource types)
  UpdateReplacePolicy: Snapshot   # applies when an update forces replacement
```
- Know which property updates mean **Replacement** (the resource reference page lists
  "Update requires: Replacement"); a change set shows `Replacement: True`.
- **Stack policy** can deny `Update:Replace` and `Update:Delete` on resources by logical ID pattern such as `Data*`; an explicit
  Deny always overrides an Allow.
- `aws cloudformation update-termination-protection --enable-termination-protection`.

## 3. Deploy via change sets, always
```bash
aws cloudformation deploy --stack-name app --template-file t.yaml \
  --parameter-overrides Env=prod --capabilities CAPABILITY_NAMED_IAM --no-execute-changeset
aws cloudformation describe-change-set --stack-name app --change-set-name <name> \
  --query 'Changes[].ResourceChange.[Action,LogicalResourceId,Replacement,Scope]'
aws cloudformation execute-change-set --stack-name app --change-set-name <name>
```
- Review `Replacement=True` and `Remove` actions before executing. `create-change-set --include-nested-stacks` includes nested stack changes
  (it is a `create-change-set` option, not a `deploy` option).
- `package` first for local Lambda code/nested templates (`aws cloudformation package --s3-bucket …`).
- Rollback triggers (CloudWatch alarms in `--rollback-configuration`, with `MonitoringTimeInMinutes`) roll back an update
  when an alarm fires during the monitoring window.

## 4. Drift
- `detect-stack-drift` → `describe-stack-resource-drifts --stack-resource-drift-status-filters MODIFIED DELETED`
  (resource drift statuses: IN_SYNC, MODIFIED, DELETED, NOT_CHECKED, UNKNOWN, UNSUPPORTED).
- Fix drift by changing the template to match reality then updating, or by reverting the manual change.
  Resources of types without drift support report `UNSUPPORTED`.

## 5. Import and move resources
- Bring an existing resource under management: add it to the template with the same
  properties + `DeletionPolicy: Retain`, then `create-change-set --change-set-type IMPORT
  --resources-to-import file://import.json` (identifier = physical id).
- Move resources between stacks with **stack refactoring** (`create-stack-refactor`, `execute-stack-refactor`) or retain, delete and import.
- The **IaC generator** (`create-generated-template`) creates a template from existing resources.

## 6. StackSets
- Service-managed permissions with **Organizations** support automatic deployment to accounts added to the target OUs; self-managed needs
  the `AWSCloudFormationStackSetAdministrationRole` in the administrator account and `AWSCloudFormationStackSetExecutionRole` in each target account.
- `OperationPreferences`: `MaxConcurrentPercentage` (or `MaxConcurrentCount`), `FailureTolerancePercentage` (or `FailureToleranceCount`),
  `RegionConcurrencyType` (`SEQUENTIAL` or `PARALLEL`), `RegionOrder`. Start with one account/Region, then widen.
- Quotas: 1000 stack sets per administrator account and 100,000 stack instances per stack set.

## 7. When it goes wrong
| State | Action |
|---|---|
| `UPDATE_ROLLBACK_FAILED` | `continue-update-rollback --resources-to-skip LogicalId` after fixing the resource manually |
| `CREATE_FAILED` on a new stack | With rollback disabled (`--on-failure DO_NOTHING`) the stack is kept for debugging; delete and retry |
| `DELETE_FAILED` | Usually a non-empty S3 bucket or dependency; empty it or `--retain-resources` |
| Custom resource hangs | the provider never sent SUCCESS or FAILED to the response URL; always respond, including on errors |

## Gotchas
- `CAPABILITY_AUTO_EXPAND` lets you execute a stack update directly from a template that contains macros or the `AWS::Serverless` transform.
- With rollback disabled, the successfully created resources stay (and keep billing) after a failure.

## Verify
- [ ] Every stateful resource has `DeletionPolicy` + `UpdateReplacePolicy` and the stack has termination protection.
- [ ] The pipeline shows change-set diff and requires approval when `Replacement=True`.
- [ ] Drift detection runs on a schedule and the stack drift status `DRIFTED` is acted on.
- [ ] A StackSet deployment to one test OU succeeds before widening.

## Checked
Date: 2026-10-24. Documentation release: AWS CloudFormation User Guide (awsdocs source, December 2023 snapshot), the current quotas page and the current botocore `cloudformation` model.
Confirmed: `DeletionPolicy` values including `RetainExceptOnCreate`; stack policy actions and Deny precedence; `create-change-set` `IncludeNestedStacks`, `RollbackConfiguration` with `RollbackTriggers` and `MonitoringTimeInMinutes`; resource drift status values; stack refactor and generated template operations exist; `OperationPreferences` members and `RegionConcurrencyType` values; StackSet role names; automatic deployment; 500 resources, 1000 stack sets and 100,000 stack instances; `ResourcesToSkip`; `IMPORT` change set type.
Fixed: the drift filter flag is `--stack-resource-drift-status-filters` (not `--stack-drift-status-filters`); `--include-nested-stacks` belongs to `create-change-set`, not `deploy`. Removed as unconfirmed: the AWS Config rule name, `cfn-lint` and `cfn-guard` advice, the `GetAtt` and Lambda `S3Key` gotchas, and the nested-stack rollback remark.

Method: documentation only; no commands were run.
