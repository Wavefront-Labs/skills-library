---
id: computing-software.cloud-infrastructure-engineering.aws.cdk-refactoring-without-resource-replacement
name: cdk-refactoring-without-resource-replacement
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, cdk, cdk-refactor, logical-id-stability, overridelogicalid, stack-refactoring, construct-ids]
level: advanced
status: docs-checked
description: "Refactor CDK code (rename constructs, move between stacks) without replacing stateful resources: how logical IDs are derived, overrideLogicalId, cdk refactor and imports."
sources: ["https://docs.aws.amazon.com/cdk/v2/guide/identifiers.html", "https://docs.aws.amazon.com/cdk/v2/guide/refactor.html", "https://docs.aws.amazon.com/cdk/v2/guide/ref-cli-cmd-refactor.html", "https://docs.aws.amazon.com/AWSCloudFormation/latest/APIReference/API_CreateStackRefactor.html", "https://docs.aws.amazon.com/cdk/v2/guide/ref-cli-cmd-import.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Refactoring CDK without replacing resources

## 1. Why refactors replace resources
CloudFormation identifies resources by **logical ID**. CDK derives the logical ID from the
construct path (path components from the construct tree, excluding the stack) plus an 8-character hash, e.g.
`ApiOrdersTable1A2B3C4D`. Renaming a construct ID, wrapping it in a new parent construct, or
moving it to another stack changes the logical ID, so CloudFormation sees "delete old,
create new". For a DynamoDB table or bucket that means data loss (or failure if
`RETAIN`, leaving an orphan and a name clash).

## 2. Detect before deploying
`npx cdk diff` shows `[-]` for the old ID and `[+]` for the new. Any stateful resource
appearing as both is a refactor that needs handling. Add a CI check that fails when a
`AWS::DynamoDB::Table`, `AWS::S3::Bucket`, `AWS::RDS::*`, `AWS::Cognito::UserPool` or
`AWS::KMS::Key` is removed.

## 3. Option A: pin the old logical ID
```ts
const table = new dynamodb.Table(this, 'OrdersTableV2', { /* ... */ });
(table.node.defaultChild as dynamodb.CfnTable).overrideLogicalId('ApiOrdersTable1A2B3C4D');
```
Simple and safe within the same stack. Leave a comment; the override must stay forever
(or until a deliberate migration).
Alternative: when wrapping an existing construct inside a new parent, name the inner construct `Default`; the CDK drops a `Default` path component from the logical ID, so the logical ID is unchanged.

## 4. Option B: cdk refactor / CloudFormation stack refactoring
CloudFormation stack refactoring (the `CreateStackRefactor` and `ExecuteStackRefactor` API operations) can rename logical IDs and move resources between
stacks without replacement. The CDK CLI wraps it; the command is in preview and needs `--unstable=refactor`:
```bash
npx cdk refactor --unstable=refactor --dry-run     # prints the mapping without applying it
npx cdk refactor --unstable=refactor
```
It compares your code with the deployed state, requires that the app contains exactly the same resources and differs only in construct-tree location, and then shows the plan for confirmation. If it sees any resource addition, deletion or modification the refactor is rejected, so do the refactor in its own change and deploy other changes separately. Prerequisites: a recent CLI and an environment bootstrapped with the latest template (the feature needs new bootstrap permissions).
When the CLI cannot resolve an ambiguity, pass `--override-file overrides.json`, a JSON file of `"<stack>.<logicalId>": "<stack>.<logicalId>"` mappings grouped by `environments` (account, region, `resources`). `cdk diff` also annotates candidate moves ("OR move to ...").

## 5. Option C: retain, remove, import
For moves between stacks when refactoring is not available:
1. Set `removalPolicy: RETAIN` on the resource in the old stack; deploy.
2. Remove it from the old stack's code; deploy (resource kept, stack forgets it).
3. Add it to the new stack and import: `npx cdk import NewStack` (prompts for the physical
   name/ARN) or a CloudFormation import change set.
4. Fix any cross-stack references (exports) that pointed at it, in the right order (a
   stack cannot delete an export another stack imports).

## 6. Construct ID hygiene
- Choose stable, meaningful IDs early; avoid IDs derived from changing values.
- When extracting code into a custom construct, keep IDs stable using `overrideLogicalId`
  or pass the parent scope so paths do not change.
- Enabling new feature flags after a CDK upgrade can change synthesized output; read the release notes and run `cdk diff` before deploying.

## Verify
- [ ] `cdk diff` after refactor shows no replacement of stateful resources.
- [ ] Data present in the resource after deploy (same physical ID/ARN as before).
- [ ] CI guard against stateful resource removal is in place.

## Checked
Date: 2026-10-24. Sources: CDK Developer Guide source for identifiers, refactor and cdk refactor/import (awsdocs/aws-cdk-guide, main); botocore CloudFormation service model (CreateStackRefactor, ExecuteStackRefactor operations present).
Confirmed: logical ID algorithm (path components minus stack, 8-character hash, Default component dropped), overrideLogicalId, cdk refactor needs --unstable=refactor and is in preview, --dry-run, --override-file format, rejection when resources are added/deleted/modified, bootstrap and CLI prerequisites, cdk import usage.
Corrected: refactor is documented as preview (not just 'released as unstable'); added the rejection rule.
Removed as unconfirmed: the '2025' date for stack refactoring.
Method: documentation only; no commands were run.
