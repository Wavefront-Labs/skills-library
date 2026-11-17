---
id: computing-software.cloud-infrastructure-engineering.aws.cdk-diff-synth-and-deploy-workflow
name: cdk-diff-synth-and-deploy-workflow
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, cdk, require-approval, cdk-deploy, cdk-synth, change-sets, concurrency]
level: practitioner
status: docs-checked
description: "Use the CDK CLI safely: synth and diff before deploy, security-change approvals, change sets, selecting stacks, parameters/outputs, rollback options and CI flags."
sources: ["https://docs.aws.amazon.com/cdk/v2/guide/cli.html", "https://docs.aws.amazon.com/cdk/v2/guide/ref-cli-cmd-deploy.html", "https://docs.aws.amazon.com/cdk/v2/guide/ref-cli-cmd-diff.html", "https://docs.aws.amazon.com/cdk/v2/guide/ref-cli-cmd-destroy.html", "https://docs.aws.amazon.com/cdk/v2/guide/ref-cli-cmd-list.html", "https://docs.aws.amazon.com/cdk/v2/guide/context.html", "https://docs.aws.amazon.com/cdk/v2/guide/best-practices.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# CDK synth, diff and deploy workflow

## 1. Synth
```bash
npx cdk synth                       # all stacks to cdk.out/
npx cdk synth ProdStack --quiet     # one stack, no template printed
npx cdk ls --long                   # stack names, environments
```
Synth runs your app code: context lookups (`fromLookup`) are cached in
`cdk.context.json`, which must be committed with the app. Aspects and cdk-nag run here; failures stop synthesis.

## 2. Diff before every deploy
```bash
npx cdk diff ProdStack
npx cdk diff --security-only        # IAM statements and SG changes only
npx cdk diff --fail ProdStack       # exit 1 if differences (CI gate)
```
Read for: **replacements** (`[-] ... (requires replacement)` destroys and recreates
resources: databases, buckets with data), IAM broadening, SG openings, removed resources.
`cdk diff --method` selects how the diff is computed: `auto` (default) creates a CloudFormation change set to show accurate replacement information and falls back to a template-only diff if it cannot (for example, missing permissions); `change-set` always creates one; `template` compares templates only.

## 3. Deploy
```bash
npx cdk deploy ProdStack --require-approval broadening
npx cdk deploy --all --concurrency 4 --require-approval never   # CI after a reviewed diff
npx cdk deploy ProdStack --parameters ProdStack:Env=prod --outputs-file outputs.json
npx cdk deploy ProdStack --method=prepare-change-set --change-set-name review-123
npx cdk deploy ProdStack --method=execute-change-set --change-set-name review-123
```
- `--require-approval`: `never`, `any-change`, `broadening` (default: approval needed when permissions or security group rules broaden). Use `never` in CI only after a gated diff.
- `--method`: `change-set` (default), `direct` (no change set; faster but less progress detail), `prepare-change-set` (create the change set without deploying), or `execute-change-set` (run a previously prepared one; name defaults to `cdk-deploy-change-set`, or use `--change-set-name`).
- `--exclusively` deploys only the named stack without its dependencies.
- `--hotswap` for dev only: it updates supported resources directly through service APIs using your current credentials (not the bootstrap roles), so the stack drifts from CloudFormation.
- `--no-rollback` (`-R`) leaves changes in place after a failure; if you then want to roll back, use `cdk rollback`.
- `--asset-parallelism` and `--concurrency <n>` speed up large apps (CloudFormation rate limits still apply).

## 4. Destroy and safety
`npx cdk destroy DevStack` asks for confirmation (`--force` skips it). The CDK's default removal policy for resources that hold data, such as S3 buckets and database tables, is to retain them (orphan them from the stack); set `RemovalPolicy.DESTROY` (and `autoDeleteObjects` for buckets) only for ephemeral environments.
Termination protection on prod stacks: `new Stack(app, 'Prod', { terminationProtection: true })`.

## 5. CI pattern
1. `npm ci && npx cdk synth` (fail on cdk-nag errors).
2. `npx cdk diff --security-only` posted to the PR; human approval if IAM changes.
3. `npx cdk deploy --require-approval never --all` using a deploy role (bootstrap roles).
Or use CDK Pipelines, which runs synth, self-mutation and deploy stages with change sets.

## Gotchas
- `cdk diff` against a stack deployed by someone else with uncommitted context can show
  noise; keep `cdk.context.json` committed.
- Environment-agnostic stacks (no `env`) cannot use lookups and produce region-agnostic
  templates; set `env` explicitly for real deployments.
- Different CDK CLI versions on laptops and in CI can behave differently; pin the `aws-cdk` CLI in `package.json` and run it with `npx`.

## Verify
- [ ] CI posts `cdk diff` output and blocks on replacements of stateful resources without approval.
- [ ] Prod stacks have termination protection; stateful resources have a retain or snapshot removal policy.
- [ ] CLI version pinned; `cdk.context.json` committed.

## Checked
Date: 2026-10-24. Sources: CDK Developer Guide source (awsdocs/aws-cdk-guide, main), CLI command reference pages, aws-cdk-lib README for terminationProtection.
Confirmed: deploy --require-approval values and default, --method values including execute-change-set, --change-set-name, --exclusively, --concurrency, --asset-parallelism, --parameters STACK:KEY=VALUE, --outputs-file, --hotswap credentials behaviour, --no-rollback and cdk rollback; diff --security-only, --fail and --method auto/change-set/template; destroy --force; list --long; synth --quiet; cdk.context.json must be committed; stack terminationProtection prop; default retain policy for data resources.
Removed as unconfirmed: statement that asset hashes change between CLI versions, user pools as retain-by-default.
Method: documentation only; no commands were run.
