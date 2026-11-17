---
id: computing-software.cloud-infrastructure-engineering.aws.cloudformation-create-failed-and-delete-failed-troubleshooting
name: cloudformation-create-failed-and-delete-failed-troubleshooting
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, cloudformation, create-failed, delete-failed, stack-events, update-rollback-failed, retain-resources]
level: practitioner
status: docs-checked
description: "Unstick CloudFormation stacks: read stack events for the root cause, common CREATE_FAILED reasons, DELETE_FAILED with retain/force, ROLLBACK_COMPLETE, and preserve-on-failure."
sources: ["https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/troubleshooting.html", "https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/stack-failure-options.html", "https://docs.aws.amazon.com/AWSCloudFormation/latest/APIReference/API_DeleteStack.html", "https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-continueupdaterollback.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# CloudFormation CREATE_FAILED and DELETE_FAILED

## 1. Find the first failure
The last events show cascading "Resource creation cancelled"; the **earliest** `*_FAILED`
event is the root cause.
```bash
aws cloudformation describe-stack-events --stack-name app \
  --query 'reverse(StackEvents)[?contains(ResourceStatus, `FAILED`)] | [0].{r:LogicalResourceId,t:ResourceType,why:ResourceStatusReason}'
```
For nested stacks, follow the failed nested stack's physical ID and repeat. The console
"Detect root cause" view does the same.

## 2. Common CREATE_FAILED reasons
| Symptom | Fix |
|---|---|
| a resource "already exists" | name collision with a resource outside the stack: drop the explicit name (let CFN generate) or import the existing resource |
| `AccessDenied`, or not authorized to `iam:PassRole` | the deploying role (or CloudFormation service role) lacks permissions |
| resource handler error message | property values invalid for the service; read the service error inside the message |
| template error about unresolved dependencies | `Ref`/`GetAtt` to a missing logical ID |
| requires capabilities | acknowledge them with `--capabilities` (`CAPABILITY_IAM`, `CAPABILITY_NAMED_IAM`, `CAPABILITY_AUTO_EXPAND`) |
| service limit exceeded (VPCs, EIPs, buckets) | Service Quotas increase or cleanup |
| `Failed to receive N resource signal(s)` within the timeout | `cfn-signal` never sent: user data failed, the instance cannot reach CloudFormation, or the wrong logical ID or Region was used |
| Custom resource stuck | the provider never sent SUCCESS or FAILED to the pre-signed S3 URL; fix the handler to always respond |
| nested stack failed | look inside the nested stack |

## 3. Fast iteration: disable rollback
```bash
aws cloudformation create-stack ... --on-failure DO_NOTHING
aws cloudformation update-stack ... --disable-rollback
# fix, then retry the update, or roll back explicitly:
aws cloudformation rollback-stack --stack-name app
```
"Preserve successfully provisioned resources" keeps what succeeded so you can fix the
failed resource and retry the update without recreating everything. A stack that failed
creation with rollback ends in `ROLLBACK_COMPLETE`: it cannot be updated, only deleted.

## 4. DELETE_FAILED
Typical causes: non-empty S3 bucket, network interfaces still attached, security group referenced by another SG or resource outside the
stack, resource modified or deleted out of band, or an export still imported by another stack.
```bash
aws cloudformation delete-stack --stack-name app --retain-resources LogsBucket SharedSg
# DeletionMode FORCE_DELETE_STACK is also available (values: STANDARD, FORCE_DELETE_STACK):
aws cloudformation delete-stack --stack-name app --deletion-mode FORCE_DELETE_STACK
```
`--retain-resources` applies to stacks in the `DELETE_FAILED` state (useful for a non-empty S3 bucket). Clean up retained
resources manually afterwards.

## 5. Stuck in UPDATE_ROLLBACK_FAILED
```bash
aws cloudformation continue-update-rollback --stack-name app --resources-to-skip BrokenResource
```
Skip resources that cannot roll back (the stack then marks them as rolled back; reconcile
them manually).

## Verify
- [ ] Root cause identified from the first FAILED event, not the cascade.
- [ ] Stack reaches `CREATE_COMPLETE`/`UPDATE_COMPLETE` or is cleanly deleted with retained resources documented.
- [ ] A change set review is part of the pipeline to catch the class of error.

## Checked
Date: 2026-10-24. Documentation release: AWS CloudFormation User Guide (awsdocs source, December 2023 snapshot) plus the current botocore `cloudformation` model.
Confirmed: `--on-failure DO_NOTHING` (values DO_NOTHING, ROLLBACK, DELETE); `rollback-stack` operation; `RetainResources` applies to `DELETE_FAILED` stacks; `DeletionMode` values STANDARD and FORCE_DELETE_STACK; `ResourcesToSkip` on `continue-update-rollback`; capability names; the "Preserve successfully provisioned resources" option; the `Failed to receive N resource signal(s)` event.
Removed as unconfirmed: verbatim error message strings (the table now lists symptoms), the Lambda ENI release time and the bucket-emptying advice.

Method: documentation only; no commands were run.
