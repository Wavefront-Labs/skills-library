---
id: computing-software.cloud-infrastructure-engineering.aws.cdk-escape-hatches-and-l1-overrides
name: cdk-escape-hatches-and-l1-overrides
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, cdk, escape-hatch, cfn-override, l1-constructs, add-property-override, logical-id, infrastructure-as-code]
level: practitioner
status: docs-checked
description: "Reach below CDK L2 constructs when they lack a feature: node.defaultChild, typed L1 properties, addPropertyOverride/addOverride, raw overrides, logical ID pinning and removal."
sources: ["https://docs.aws.amazon.com/cdk/v2/guide/cfn-layer.html", "https://docs.aws.amazon.com/cdk/v2/guide/identifiers.html", "https://github.com/aws/aws-cdk/blob/main/packages/aws-cdk-lib/core/lib/cfn-element.ts"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# CDK escape hatches and L1 overrides

**When:** the L2 construct doesn't expose a CloudFormation property you need (new service
feature, edge-case setting), and waiting for a CDK release isn't an option.

## 1. Ladder (stop at the first that works)
1. L2 prop exists? Use it.
2. **Typed L1 access**: get the underlying `Cfn*` resource and set the property.
3. **Property override**: raw path into `Properties` (for properties the L1 types don't know yet).
4. **Raw override** (`addOverride`, full path from the resource root): can reach anything in the resource template fragment and delete synthesized properties.
5. Use an L1 (`CfnBucket`) directly or a custom resource.

## 2. Examples (TypeScript)
```ts
const bucket = new s3.Bucket(this, 'Data', { versioned: true });

// 2. typed L1
const cfnBucket = bucket.node.defaultChild as s3.CfnBucket;
cfnBucket.analyticsConfigurations = [{ id: 'all', storageClassAnalysis: {} }];

// 3. property override (path is CloudFormation property casing)
cfnBucket.addPropertyOverride('NotificationConfiguration.EventBridgeConfiguration.EventBridgeEnabled', true);
cfnBucket.addPropertyDeletionOverride('VersioningConfiguration.Status');

// 4. raw override: full path from the resource root, including 'Properties.'
cfnBucket.addOverride('UpdateReplacePolicy', 'Retain');
cfnBucket.cfnOptions.condition = isProdCondition;

// nested construct: find children by id
const role = myConstruct.node.findChild('ServiceRole') as iam.Role;
(role.node.defaultChild as iam.CfnRole).addPropertyOverride('MaxSessionDuration', 7200);
```
Array index paths work: `addOverride('Properties.Tags.0.Value', 'NewValue')`; `addPropertyOverride` is a shortcut for paths starting with `Properties.`, and `addDeletionOverride`/`addPropertyDeletionOverride` remove synthesized values.

## 3. Logical IDs
Refactoring construct trees changes logical IDs → CloudFormation **replaces** resources
(dangerous for buckets/tables). Pin them:
```ts
cfnBucket.overrideLogicalId('DataBucketE3889A50');
```
Check with `cdk diff` before deploying any refactor.

## 4. Aspects for org-wide overrides
An Aspect visiting every `CfnBucket` can apply the same escape hatch across stacks consistently.

## Gotchas
- Overrides bypass type checking — a typo in the path silently produces an invalid template; run `cdk synth` and inspect the template (or validate it with CloudFormation tooling).
- When CDK later adds the L2 prop, remove your override (conflicts produce merged/duplicated values).
- `node.defaultChild` is undefined for constructs that wrap several resources — use `findChild`.

## Verify
- [ ] `cdk synth` output (`cdk.out/*.template.json`) contains the overridden property at the right path.
- [ ] `cdk diff` shows only the intended modification, no replacement.
- [ ] Each override has a comment linking the missing L2 feature/issue for later removal.

## Checked
Date: 2026-10-24. Sources: CDK Developer Guide source for the CloudFormation layer and identifiers pages (awsdocs/aws-cdk-guide, main); aws-cdk-lib cfn-element.ts (main).
Confirmed: node.defaultChild escape hatch, addOverride with dot paths from the resource root, addPropertyOverride as a shortcut for Properties paths, list index paths, addDeletionOverride and addPropertyDeletionOverride, overrideLogicalId, logical ID derived from the construct path plus an 8-character hash.
Corrected: the list-index example now uses the documented path form; raw override description now matches the guide.
Removed as unconfirmed: DependsOn/UpdatePolicy list, bucket-key example, cfn-lint recommendation.
Method: documentation only; no commands were run.
