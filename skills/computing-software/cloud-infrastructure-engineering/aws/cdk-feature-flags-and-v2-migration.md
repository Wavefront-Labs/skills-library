---
id: computing-software.cloud-infrastructure-engineering.aws.cdk-feature-flags-and-v2-migration
name: cdk-feature-flags-and-v2-migration
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, cdk, feature-flags, cdk-v2-migration, aws-cdk-lib, cdk-json-context, alpha-modules]
level: practitioner
status: docs-checked
description: "Manage CDK feature flags in cdk.json without surprise resource replacement, and finish CDK v1 to v2 migrations: aws-cdk-lib imports, alpha modules and bootstrap changes."
sources: ["https://docs.aws.amazon.com/cdk/v2/guide/featureflags.html", "https://docs.aws.amazon.com/cdk/v2/guide/ref-cli-cmd-flags.html", "https://docs.aws.amazon.com/cdk/v2/guide/migrating-v2.html", "https://docs.aws.amazon.com/cdk/v2/guide/versioning.html", "https://github.com/aws/aws-cdk/blob/main/packages/aws-cdk-lib/cx-api/FEATURE_FLAGS.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# CDK feature flags and v2 migration

## Feature flags
- Flags are context keys in `cdk.json` (e.g. `"@aws-cdk/aws-iam:minimizePolicies": true`) that opt
  into behaviour changes which could alter synthesised templates for existing apps.
- Flags are disabled by default: existing projects that do not specify a flag keep working as before. Projects created with `cdk init` include flags enabling all features available in the release that created them.
- The CDK repo's `FEATURE_FLAGS.md` lists every current flag; each release's `CHANGELOG` describes new flags.
- Flags are not removed by `cdk context --reset` or `cdk context --clear`.
- The `cdk flags` command (preview: pass `--unstable=flags`) lists flags whose value differs from the recommended one or that you have not configured; it also has `--set`, `--all` and `--recommended` options. Otherwise diff `cdk.json` against a fresh `cdk init`.

### Safe procedure for enabling a flag
1. Enable one flag (or a small group) in a branch.
2. `cdk diff` every stack in every environment. Look for `[-] replace` on stateful resources
   (tables, buckets, databases, user pools) and logical id changes.
3. If replacement appears, keep the flag off, or pin the old behaviour locally (override logical id, explicit property).
4. Deploy to dev, then prod.

## v1 to v2 migration
Remove the individual `@aws-cdk/*` packages from `package.json` and depend on `aws-cdk-lib` and `constructs`:
```bash
npm i aws-cdk-lib constructs@^10.5.0
```
`awscdk-v1-stack-finder` (npm) can identify stacks deployed with CDK v1.
```ts
// v1
import * as s3 from '@aws-cdk/aws-s3';
import * as cdk from '@aws-cdk/core';
// v2
import { App, Stack, aws_s3 as s3 } from 'aws-cdk-lib';
import { Construct } from 'constructs';
```
- v2 consolidates stable modules (and L1 constructs) into `aws-cdk-lib`. Experimental modules are separate packages with an `-alpha` suffix on the package name and version.
- `Construct` comes from the `constructs` package, not core.
- Behaviour that was controlled by feature flags in v1 is the default in v2; some flag defaults differ from v1, and you can set them back to `false` to revert to v1 behaviour (check with `cdk diff`).
- v2 requires the **modern bootstrap** stack, in a newer version than v1 used; the legacy bootstrap stack is not supported, so re-bootstrap each environment.
- Deprecated APIs from v1 were removed in v2 and must be replaced (see DEPRECATED_APIs.md in the CDK repo).
- Run `cdk diff` on every stack after migration and investigate any resource replacement.

## Gotchas
- Mixing v1 and v2 packages produces type errors like "Construct is not assignable".
- Keep the CLI new enough for the library: an older CLI must support the cloud assembly schema version of the Construct Library it consumes, otherwise they are incompatible.

## Verify
- [ ] `cdk diff` shows no replacements of stateful resources after the flag change or migration.
- [ ] `package.json` contains no v1 `@aws-cdk/*` packages except `-alpha` ones.

## Checked
Date: 2026-10-24. Sources: CDK Developer Guide source for feature flags, migrating v1 to v2, versioning and cdk flags (awsdocs/aws-cdk-guide, main); aws-cdk-lib package.json peer dependency (constructs ^10.5.0).
Confirmed: flags disabled by default, cdk init behaviour, FEATURE_FLAGS.md, flags survive cdk context --reset/--clear, cdk flags needs --unstable=flags and its options, v2 consolidation into aws-cdk-lib, -alpha module naming, Construct moved to constructs, v1 flag-controlled behaviour now default, modern bootstrap requirement, removal of deprecated v1 APIs, CLI/cloud-assembly-schema compatibility rule.
Corrected: cdk init does not simply write every flag as the 'recommended true'; it enables the features available in the creating release.
Removed as unconfirmed: v1 end-of-support date, jq one-liner, claim that some flags only affect new resources.
Method: documentation only; no commands were run.
