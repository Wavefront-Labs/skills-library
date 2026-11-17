---
id: computing-software.cloud-infrastructure-engineering.aws.cdk-stages-and-environments-for-multi-account
name: cdk-stages-and-environments-for-multi-account
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, cdk, cdk-stage, cdk-environments, multi-account, cdk-bootstrap-trust, cross-region-references]
level: practitioner
status: docs-checked
description: "Structure CDK apps for several accounts and regions: explicit env per stack, Stage classes, bootstrapping with trust, environment-agnostic pitfalls and cross-region references."
sources: ["https://docs.aws.amazon.com/cdk/v2/guide/environments.html", "https://docs.aws.amazon.com/cdk/v2/guide/stages.html", "https://docs.aws.amazon.com/cdk/v2/guide/stacks.html", "https://docs.aws.amazon.com/cdk/v2/guide/ref-cli-cmd-bootstrap.html", "https://docs.aws.amazon.com/cdk/v2/guide/context.html", "https://github.com/aws/aws-cdk/blob/main/packages/aws-cdk-lib/pipelines/README.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# CDK stages and environments for multi-account apps

## Environments
```ts
const app = new App();
const envs = {
  dev:  { account: '111111111111', region: 'eu-west-1' },
  prod: { account: '222222222222', region: 'eu-west-1' },
};
```
- Stacks without `env` are **environment-agnostic**: `Stack.of(this).region` is a token,
  `Vpc.fromLookup` and other lookups fail, and AZ selection defaults to 2 AZs.
- `env: { account: process.env.CDK_DEFAULT_ACCOUNT, region: process.env.CDK_DEFAULT_REGION }`
  binds to whatever credentials run the CLI; convenient for dev, risky for prod.
- Lookups are cached in `cdk.context.json`; the guide says it must be committed with the app so other environments (such as CI) synthesize consistently.

## Stage = one copy of the application
```ts
class OrdersStage extends Stage {
  constructor(scope: Construct, id: string, props: StageProps) {
    super(scope, id, props);
    const data = new DataStack(this, 'Data');
    new ApiStack(this, 'Api', { table: data.table });
  }
}
new OrdersStage(app, 'Dev', { env: envs.dev });
new OrdersStage(app, 'Prod', { env: envs.prod });
```
- Stack names become `Dev-Data`, `Prod-Api`; deploy with `cdk deploy 'Prod/*'`.
- Pass configuration through stage props, not context lookups scattered in constructs.
- With CDK Pipelines: `pipeline.addStage(new OrdersStage(this, 'Prod', {env: envs.prod}), {pre: [new ManualApprovalStep('Approve')]})`.

## Bootstrap every target environment
```bash
cdk bootstrap aws://222222222222/eu-west-1 --trust 333333333333 \
  --cloudformation-execution-policies arn:aws:iam::222222222222:policy/CdkDeployPolicy
```
- `--trust` lets the pipeline/tooling account assume the deploy roles.
- By default stacks deploy with the `AdministratorAccess` policy; supply a scoped policy through `--cloudformation-execution-policies` where that is too broad. `--trust` requires `--cloudformation-execution-policies`.
- `--trust-for-lookup` trusts an account to perform lookups only.
- A pipeline relies on the bootstrap stack; do not delete it or change its qualifier, and upgrade it by re-running `cdk bootstrap`.

## Cross-stack and cross-region
- Passing constructs between stacks in the same env creates exports automatically (and the ImportValue coupling).
- Across regions: the experimental `crossRegionReferences: true` stack property creates CloudFormation custom resources in both the producing and consuming stack to perform the export and import. Across accounts there are no automatic references; pass values through configuration.

## Gotchas
- Hard-coded account ids leak into code; centralise them in one config module.
- A stack's name includes its stage (for example `Prod-Api`), so moving a stack to another stage changes its name and creates a new stack.
- Stale cached lookups can be cleared with `cdk context --reset <key or index>`.

## Verify
- [ ] `cdk ls` lists one stack set per stage (for example `Dev/Data (Dev-Data)`).
- [ ] Each target account has a current `CDKToolkit` stack trusting the pipeline account.

## Checked
Date: 2026-10-24. Sources: CDK Developer Guide source (awsdocs/aws-cdk-guide, main): environments, stages, stacks, context, resources, bootstrap reference; aws-cdk-lib stack.ts (crossRegionReferences) and pipelines README.
Confirmed: environment-agnostic stacks (two AZs, lookups need a known environment), CDK_DEFAULT_ACCOUNT/REGION usage, Stage stack naming (Dev-AppStack) and cdk deploy 'Dev/*', bootstrap --trust, --trust-for-lookup, --cloudformation-execution-policies and AdministratorAccess default, cdk.context.json committed, cdk context --reset, crossRegionReferences is experimental and uses custom resources.
Removed as unconfirmed: SSM parameters as the cross-region mechanism, RAM suggestion, 'bootstrap version too old' message text.
Method: documentation only; no commands were run.
