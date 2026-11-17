---
id: computing-software.cloud-infrastructure-engineering.aws.cdk-migrate-watch-and-hotswap
name: cdk-migrate-watch-and-hotswap
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, cdk, aws-cdk, cdk-migrate, cdk-watch, hotswap, hotswap-fallback, cdk-import, cloudformation-to-cdk, inner-loop, iac-scanner, drift]
level: practitioner
status: docs-checked
description: "Bring existing stacks or unmanaged resources into CDK with cdk migrate and cdk import, and speed up dev loops with cdk watch and hotswap without drifting production."
sources: ["https://docs.aws.amazon.com/cdk/v2/guide/migrate.html", "https://docs.aws.amazon.com/cdk/v2/guide/ref-cli-cmd-migrate.html", "https://docs.aws.amazon.com/cdk/v2/guide/ref-cli-cmd-watch.html", "https://docs.aws.amazon.com/cdk/v2/guide/ref-cli-cmd-deploy.html", "https://docs.aws.amazon.com/cdk/v2/guide/ref-cli-cmd-import.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# cdk migrate, cdk import, cdk watch and hotswap

**Goal:** a CloudFormation stack (or a pile of console-made resources) becomes a CDK app
without recreating anything, and developers iterate on Lambda/ECS code in seconds in their
own dev stacks while production only ever changes through full CloudFormation deploys.

## 1. cdk migrate
Three sources:
```bash
# from a deployed stack (keeps the stack; generates an app that manages it)
cdk migrate --stack-name orders-prod --from-stack --language typescript --output-path ./orders-cdk
# from a template file
cdk migrate --stack-name orders --from-path ./orders.yaml --language python
# from resources not in any stack (uses the IaC generator scan)
cdk migrate --stack-name legacy --from-scan new --filter resource-type-prefix="AWS::S3::" --filter tag-key="app" --language typescript
```
- Output is a new CDK project with **L1 constructs only** (`CfnBucket`, ...) in a single stack, named after `--stack-name`; an existing folder of that name is overwritten. It works, but it is not idiomatic CDK. `--language` defaults to `typescript`. Refactor to L2 gradually, checking `cdk diff`
  shows *no replacement* after each step (logical IDs must stay identical — use
  `overrideLogicalId` or keep the L1 where IDs would change).
- `--from-stack`: the stack name in the new app must match the deployed CloudFormation stack, and you deploy with the same account and Region.
- `--from-scan new|most-recent` uses the CloudFormation IaC generator; `cdk migrate` itself runs `cdk import` to bring the resources into the new app. The IaC generator has data and quota limitations, see the CloudFormation guide.
- `--filter` takes the keys `resource-identifier`, `resource-type-prefix`, `tag-key` and `tag-value`; keys in one `--filter` are ANDed and repeating `--filter` ORs them.
- Run `cdk diff` before the first deploy.

## 2. cdk import (adopting existing resources into a CDK stack)
1. Add the construct to code with the real resource's properties; set
   `removalPolicy: RETAIN` while adopting.
2. `cdk import MyStack` — CDK prompts for each new resource's physical identifier, or reads a
   mapping file (`--resource-mapping <file>`); `--record-resource-mapping <file>` writes a mapping without importing. By default the CLI exits if the diff includes updates or deletions (`--force` overrides).
3. `cdk diff` should then be empty or show only tags/metadata.

## 3. cdk watch and hotswap (dev only)
```bash
cdk deploy --hotswap MyStack-dev          # update supported resources (Lambda code, Step Functions definitions, ECS images, ...) directly via service APIs
cdk deploy --hotswap-fallback MyStack-dev # hotswap if possible, otherwise full CFN deploy
cdk watch MyStack-dev                     # shortcut for cdk deploy --watch: watches files and deploys (hotswap by default)
```
`cdk.json` controls what is watched through the `"watch"` key (`include` and `exclude`; a project from `cdk init` includes all files and excludes dot-files, the output directory and `node_modules` by default):
```json
{"watch": {"include": ["src/**", "lib/**"], "exclude": ["**/*.test.ts", "cdk.out", "node_modules"]}}
```
- Hotswap bypasses CloudFormation, so the deployed resources can differ from what CloudFormation knows. The CLI docs say `cdk watch` and `--hotswap` are meant for development and not recommended for production. Hotswap uses your current credentials, not the bootstrap roles.
- Changes that cannot be hotswapped are ignored with a message under `--hotswap`, and trigger a full CloudFormation deployment under `--hotswap-fallback`. Supported changes include Lambda code, tags, description and environment variables.

## Gotchas
- A SAM template must first be converted to a CloudFormation template (or deployed as a stack) before `cdk migrate`.
- Generated code mirrors the template; review it and parameterise environment-specific values before reuse.
- A migrated stack with `Retain` policies omitted can delete data on a later refactor that
  changes logical IDs. Add a test that snapshots logical IDs.

## Verify
- [ ] `cdk diff` against the migrated stack shows no resource replacements.
- [ ] CloudFormation drift detection on prod stacks reports `IN_SYNC` (nobody hotswapped prod).
- [ ] `cdk watch` updates a Lambda in a personal dev stack.

## Checked
Date: 2026-10-24. Sources: CDK Developer Guide source (awsdocs/aws-cdk-guide, main): migrate, cdk migrate, cdk watch, cdk deploy and cdk import reference pages.
Confirmed: cdk migrate source options (--from-stack, --from-path, --from-scan new|most-recent), languages and default, single-stack L1-only output, folder overwrite, stack-name match rule, SAM conversion first, import options, hotswap and hotswap-fallback behaviour and supported changes, watch defaults and cdk.json watch keys.
Corrected: the --filter syntax (the skill used type=...; the documented keys are resource-identifier, resource-type-prefix, tag-key, tag-value); environment variables are hotswappable for Lambda.
Removed as unconfirmed: per-day scan quota, nested-stack and custom-resource failure claim, 10-second timing.
Method: documentation only; no commands were run.
