---
id: computing-software.cloud-infrastructure-engineering.pulumi.aws-classic-vs-native
name: aws-classic-vs-native
category: computing-software
field: cloud-infrastructure-engineering
product: pulumi
tags: [cloud-infrastructure-engineering, pulumi, aws-native, aws-classic, cloudcontrol]
level: practitioner
status: docs-checked
description: "Choose between the Pulumi AWS provider and the AWS Cloud Control (aws-native) provider and add native resources as needed."
sources:
  - https://www.pulumi.com/registry/packages/aws/
  - https://www.pulumi.com/registry/packages/aws-native/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# AWS provider vs AWS Cloud Control

- `@pulumi/aws` (package `aws`): Pulumi's primary AWS provider. Pulumi recommends new projects start here.
- `@pulumi/aws-native` (package `aws-native`, titled AWS Cloud Control): manages resources through the AWS Cloud Control API, which typically supports new AWS features on the day of launch. Its resources are based on the resources defined in the AWS CloudFormation Registry. It covers hundreds of resources, but some AWS resources are not yet available in Cloud Control.

Recommended approach: start with the AWS provider and add Cloud Control resources on an as-needed basis, for example for a brand-new AWS resource the primary provider does not yet cover.

```typescript
import * as aws from "@pulumi/aws";
import * as awsnative from "@pulumi/aws-native";

const bucket = new aws.s3.Bucket("classic");          // primary provider
// add awsnative.* resources only where aws lacks coverage
```

## Gotchas
- Both are separate packages; each needs credentials configured per its Installation and Configuration page.
- Install steps differ between native providers, bridged providers and component packages, so follow each package's own installation page.

## Verify
`pulumi about` lists the plugins in use.

## Checked

Method: docs-checked 2026-11-09 against the Pulumi Registry aws and aws-native package pages. Removed unconfirmed claims: Terraform bridging, awsx details, per-provider region config keys, property casing differences and throttling.
