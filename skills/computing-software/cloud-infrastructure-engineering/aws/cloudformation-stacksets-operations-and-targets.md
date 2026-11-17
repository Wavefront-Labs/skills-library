---
id: computing-software.cloud-infrastructure-engineering.aws.cloudformation-stacksets-operations-and-targets
name: cloudformation-stacksets-operations-and-targets
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, cloudformation, stacksets, stackset-operations, deployment-targets, service-managed-stacksets, auto-deployment, multi-account]
level: practitioner
status: docs-checked
description: "Deploy baselines across accounts and regions with StackSets: service-managed OU targets, auto-deployment, operation preferences, failures, drift and overrides."
sources: ["https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/stacksets-concepts.html", "https://docs.aws.amazon.com/AWSCloudFormation/latest/APIReference/API_CreateStackSet.html", "https://docs.aws.amazon.com/AWSCloudFormation/latest/APIReference/API_DeploymentTargets.html", "https://docs.aws.amazon.com/AWSCloudFormation/latest/APIReference/API_StackSetOperationPreferences.html", "https://docs.aws.amazon.com/AWSCloudFormation/latest/APIReference/API_ManagedExecution.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# CloudFormation StackSets: targets and operations

## 1. Permission models
- **Service-managed** (for accounts in AWS Organizations): StackSets creates the IAM roles for you, you target OUs, and you can turn on **auto-deployment** to accounts added to the organization later. The administrator account is the management account or a delegated administrator (`--call-as DELEGATED_ADMIN`; the default is `SELF`).
- **Self-managed**: you create the IAM roles that establish trust between the administrator account and each target account (the default execution role name is `AWSCloudFormationStackSetExecutionRole`; `--administration-role-arn` and `--execution-role-name` customize them). It can deploy to any account where you can create an IAM role.
- A StackSet is a regional resource: you only see it in the Region where you created it.

## 2. Create and deploy
```bash
aws cloudformation create-stack-set --stack-set-name baseline-config-rules \
  --template-body file://config-rules.yaml --permission-model SERVICE_MANAGED \
  --auto-deployment Enabled=true,RetainStacksOnAccountRemoval=false \
  --capabilities CAPABILITY_NAMED_IAM --call-as DELEGATED_ADMIN
aws cloudformation create-stack-instances --stack-set-name baseline-config-rules \
  --deployment-targets OrganizationalUnitIds=ou-abcd-prod,ou-abcd-dev \
  --regions eu-west-1 us-east-1 \
  --operation-preferences RegionConcurrencyType=PARALLEL,MaxConcurrentPercentage=25,FailureTolerancePercentage=10 \
  --call-as DELEGATED_ADMIN
```
- `--deployment-targets` can add `AccountFilterType` (`NONE`, `INTERSECTION`, `DIFFERENCE`, `UNION`) with `Accounts=...`: `DIFFERENCE` targets all accounts in the OUs except the listed ones, `INTERSECTION` only the listed accounts that are in the OUs, and `UNION` (the default) the OUs plus the listed accounts; `UNION` is not supported for `create-stack-instances`.
- **Operation preferences**: `MaxConcurrentCount`/`MaxConcurrentPercentage`, `FailureToleranceCount`/`FailureTolerancePercentage` (applied per Region; percentages round down, and a concurrency percentage that would round to zero becomes one), `RegionOrder`, `RegionConcurrencyType` (`SEQUENTIAL` is the default, or `PARALLEL`) and `ConcurrencyMode`. If an operation exceeds the failure tolerance in a Region, CloudFormation does not continue in later Regions. Start conservative (one Region, small percentage) for risky changes.
- Parameter overrides per OU, account or Region: `update-stack-instances --parameter-overrides`.

## 3. Watch operations
```bash
aws cloudformation list-stack-set-operations --stack-set-name baseline-config-rules --call-as DELEGATED_ADMIN
aws cloudformation list-stack-set-operation-results --stack-set-name baseline-config-rules --operation-id <ID> \
  --query 'Summaries[?Status!=`SUCCEEDED`].[Account,Region,StatusReason]' --call-as DELEGATED_ADMIN
```
By default StackSets performs one operation at a time, in request order. With managed execution (`--managed-execution Active=true`) non-conflicting operations run concurrently and conflicting ones are queued; you cannot change the execution configuration while operations are running or queued.

## 4. Drift and cleanup
`detect-stack-set-drift` checks the stack instances. Deleting: `delete-stack-instances` (with
`--retain-stacks` to keep the stacks running outside the StackSet) before `delete-stack-set`, which works only when the StackSet has no stack instances.

## Gotchas
- Stack instance `OUTDATED`: the stack is not up to date with the StackSet because a create or update operation failed, or was stopped before reaching it. Fix the cause in that account and run `update-stack-instances` for it.
- `INOPERABLE` means a delete operation failed and left the stack unstable; such instances are excluded from further updates, and you may need `delete-stack-instances` with `--retain-stacks` and then delete the stack manually.

## Verify
- [ ] `list-stack-instances` shows `CURRENT` for every target account/region.
- [ ] A newly created account in a target OU receives the stack automatically.
- [ ] Drift detection reports `IN_SYNC` across instances.

## Checked
Date: 2026-10-24. Sources: botocore CloudFormation service model (develop branch, API 2010-05-15) and the CloudFormation StackSets concepts page.
Confirmed: permission models, CallAs values SELF and DELEGATED_ADMIN, AutoDeployment fields, AccountFilterType values and semantics (UNION default, unsupported for CreateStackInstances), operation preference fields and their rounding rules, region concurrency default sequential, ManagedExecution behaviour, RetainStacks, stack instance statuses OUTDATED and INOPERABLE, operation result summary fields (Account, Region, Status, StatusReason), existence of DetectStackSetDrift, ListStackSetOperations and ListStackSetOperationResults, delete order (instances before the StackSet).
Removed as unconfirmed: the management-account exclusion for service-managed StackSets, the Administration role name, the global-IAM-region collision note.
Method: documentation only; no commands were run.
