---
id: computing-software.cloud-infrastructure-engineering.aws.cloudformation-hooks
name: cloudformation-hooks
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, cloudformation, cfn-hooks, cloudformation-hooks, guard-hook, lambda-hook, cfn-guard, proactive-controls, policy-as-code, pre-provisioning-checks, change-set-validation, cloudformation-cli]
level: advanced
status: docs-checked
description: "Block non-compliant CloudFormation resources before they are provisioned with Hooks: Guard and Lambda hooks, targets and failure modes, custom hooks via cfn CLI, org rollout."
sources: ["https://docs.aws.amazon.com/cloudformation-cli/latest/hooks-userguide/what-is-cloudformation-hooks.html", "https://docs.aws.amazon.com/cloudformation-cli/latest/hooks-userguide/guard-hooks.html", "https://docs.aws.amazon.com/cloudformation-cli/latest/hooks-userguide/lambda-hooks-create-lambda-function.html", "https://docs.aws.amazon.com/cloudformation-cli/latest/hooks-userguide/hooks-target-filtering.html", "https://docs.aws.amazon.com/AWSCloudFormation/latest/TemplateReference/aws-resource-cloudformation-guardhook.html", "https://docs.aws.amazon.com/AWSCloudFormation/latest/TemplateReference/aws-resource-cloudformation-lambdahook.html", "https://github.com/aws-cloudformation/cloudformation-guard"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# CloudFormation Hooks

**Goal:** an S3 bucket without encryption, an SG open to the world or an untagged instance
is refused *by CloudFormation itself* before creation or update — for every stack, CDK app
and SAM deploy in the account — instead of being found later by AWS Config.

## 1. Kinds of hook
| Kind | You write | Good for |
|---|---|---|
| **Guard hook** (`AWS::CloudFormation::GuardHook`) | cfn-guard rules file in S3 | Declarative property checks; no code to run |
| **Lambda hook** (`AWS::CloudFormation::LambdaHook`) | A Lambda function returning pass/fail | Lookups (allowed AMIs from a table, cost checks) |
| Custom hook (registry extension) | A project created with the `cfn` CLI and a language plugin | Reusable, versioned, registered in the registry |
Targets (`TargetOperations`): `RESOURCE`, `STACK` (template-level), `CHANGE_SET` and `CLOUD_CONTROL` (Cloud Control API operations); filter actions `CREATE`/`UPDATE`/`DELETE` (for `CHANGE_SET` targets only `CREATE` applies); the only invocation point is `PRE_PROVISION`.

## 2. Guard hook
`rules/s3.guard`:
```
let buckets = Resources.*[ Type == 'AWS::S3::Bucket' ]
rule s3_encrypted_and_private when %buckets !empty {
  %buckets.Properties.BucketEncryption exists
     <<S3 buckets must declare BucketEncryption>>
  %buckets.Properties.PublicAccessBlockConfiguration.BlockPublicAcls == true
     <<S3 buckets must block public ACLs>>
}
```
Activate (as a stack so it is itself IaC):
```yaml
S3Guard:
  Type: AWS::CloudFormation::GuardHook
  Properties:
    Alias: Org::Security::S3Guard
    RuleLocation: { Uri: s3://cfn-hook-rules-<ACCOUNT_ID>/rules/s3.guard }
    LogBucket: cfn-hook-logs-<ACCOUNT_ID>        # optional: S3 bucket for the Guard output report
    ExecutionRole: !GetAtt HookRole.Arn          # trusts hooks.cloudformation.amazonaws.com; s3:GetObject on the rules, s3:PutObject on the log bucket
    TargetOperations: [RESOURCE]
    TargetFilters:
      Actions: [CREATE, UPDATE]
      TargetNames: [AWS::S3::Bucket]
    FailureMode: WARN                            # FAIL blocks the action; WARN only warns
    HookStatus: ENABLED
```
`Alias` must look like `Name1::Name2::Name3` and must not begin with `AWS`; `Alias`, `ExecutionRole` and `RuleLocation` are required, as are `TargetOperations`, `FailureMode` and `HookStatus`.
Test rules locally first with the cfn-guard CLI: `cfn-guard validate --rules rules/ --data template.json` (`-r` and `-d` are the short forms). The input a Guard hook sees differs by target type; check the Hooks User Guide.

## 3. Lambda hook
For resource targets the function receives `requestData.targetName` and `requestData.targetModel.resourceProperties` (plus `previousResourceProperties` on updates). For stack and change-set targets it receives a presigned S3 URL in `requestData.payload`, which holds the template (and, for change sets, `changedResources`). It returns `{"hookStatus": "SUCCESS"|"FAILED"|"IN_PROGRESS", "message": "...", "clientRequestToken": <the request's token>, "errorCode": "NonCompliant"|"InternalFailure"}`; `errorCode` is required on failure and `clientRequestToken` is always required. Hooks wait up to 30 seconds for the function, and a hook may return `IN_PROGRESS` up to three times. With `FailureMode: FAIL` a `FAILED` result blocks the action; with `WARN` it only warns. The Hook's execution role needs `lambda:InvokeFunction` on the function.

## 4. Rollout
1. Deploy in `WARN` mode first (for example to each account with StackSets).
2. Read the warnings in the stack events and the Hook invocation results (`list-hook-results`).
3. Fix templates, then switch to `FailureMode: FAIL` gradually.
4. Keep an exclusion path for platform stacks that must not be blocked: `StackFilters` take a `FilteringCriteria` and `StackNames` with `Include` or `Exclude` lists.

## Gotchas
- Hooks run on CloudFormation and Cloud Control API operations; changes made through other tools are not evaluated. Pair with SCPs or AWS Config for those.
- A resource-target hook receives only that resource's proposed and previous properties; rules across resources need a stack or change-set target, which receive the template.
- A buggy hook in `FAIL` mode blocks the actions it targets. `HookStatus: DISABLED` turns a hook off; keep a fast way to apply it.

## Verify
- [ ] Deploy a template with an unencrypted bucket: in `WARN` the operation continues with a warning; in `FAIL` it is blocked with your message.
- [ ] A compliant template passes.
- [ ] `aws cloudformation list-types --visibility PRIVATE --type HOOK` (or `describe-type` for the alias) shows the hook in each target account and Region.

## Checked
Date: 2026-10-24. Sources: CloudFormation Template Reference pages for AWS::CloudFormation::GuardHook and LambdaHook, CloudFormation Hooks User Guide (Lambda function request/response and target filter pages), cloudformation-guard README (main), botocore CloudFormation model (RegistryType HOOK, ListHookResults).
Confirmed: GuardHook and LambdaHook property names, required properties, alias pattern, FailureMode FAIL/WARN and HookStatus ENABLED/DISABLED, TargetOperations values, hook execution role trust principal hooks.cloudformation.amazonaws.com, RuleLocation Uri and LogBucket, StackFilters shape, TargetFilters Actions/InvocationPoints/TargetNames (CHANGE_SET supports only CREATE), Lambda hook request fields and response format (hookStatus values, errorCode values, clientRequestToken, 30 second wait, up to three IN_PROGRESS), cfn-guard validate -r/-d flags, cfn CLI language plugins.
Removed as unconfirmed: Control Tower proactive controls row and its source link, stack-rollback wording for hook failures, intrinsic-function resolution claim, HOOK_COMPLETE_SUCCEEDED event name, timeout-counts-as-failure claim, Terraform coverage claim.
Method: documentation only; no commands were run.
