---
id: computing-software.cloud-infrastructure-engineering.aws.cdk-constructs-and-pipelines
name: cdk-constructs-and-pipelines
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, cdk, aws-cdk, cdk-constructs, cdk-pipelines, l1-l2-l3-constructs, cdk-synth, cdk-diff, cdk-bootstrap, cdk-nag, assertions, aspects, context, cdk-stacks, cross-stack-references, typescript, infrastructure-as-code]
level: practitioner
status: docs-checked
description: "Build AWS infrastructure with CDK v2: construct levels, stack/app layout, bootstrap, diff-before-deploy, assertions and cdk-nag tests, and self-mutating CDK Pipelines for multi-account delivery."
sources: ["https://docs.aws.amazon.com/cdk/v2/guide/constructs.html", "https://docs.aws.amazon.com/cdk/v2/guide/bootstrapping.html", "https://docs.aws.amazon.com/cdk/v2/guide/ref-cli-cmd-bootstrap.html", "https://docs.aws.amazon.com/cdk/v2/guide/feature-flags.html", "https://github.com/aws/aws-cdk/blob/main/packages/aws-cdk-lib/pipelines/README.md", "https://github.com/aws/aws-cdk/blob/main/packages/aws-cdk-lib/assertions/README.md", "https://github.com/cdklabs/cdk-nag"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# AWS CDK — infrastructure in a real language, delivered by a pipeline that updates itself

**Goal:** a CDK app whose stacks synthesise deterministically, are tested like code, diffed
before every deploy, and roll through accounts via a self-mutating pipeline.
(Testing IaC in general: `computing-software.cloud-infrastructure-engineering.infrastructure-as-code.iac-testing-strategies`.)

## 1. Constructs
| Level | What | When |
|---|---|---|
| **L1** `CfnBucket` | 1:1 CloudFormation resource | Property L2 lacks; escape hatch |
| **L2** `s3.Bucket` | Sensible defaults, grant methods, metrics | Default choice |
| **L3** patterns `ecs_patterns.ApplicationLoadBalancedFargateService` | Opinionated multi-resource | Prototypes; outgrown quickly |
- Escape hatch: `(bucket.node.defaultChild as s3.CfnBucket).addPropertyOverride('X', 'y')`.
- `grant*` methods (`table.grantReadWriteData(fn)`) generate least-privilege IAM; avoid
  hand-written `PolicyStatement` with `*`.
- Write your own L3 for anything repeated (`class ServiceStack extends Construct`), published
  as an internal package; keep business config in props, not in `context`.

## 2. App and stack layout
- One `App`; stacks per lifecycle (`NetworkStack`, `DataStack`, `AppStack`); environments
  explicit: `env: { account, region }` (env-agnostic stacks cannot look up AZs/VPCs).
- Cross-stack references create CloudFormation exports; removing the consumer first is
  mandatory or the update fails ("export in use"). Prefer passing values via SSM parameters
  for loosely coupled stacks.
- Stable **logical ids**: renaming a construct id replaces the resource. For stateful
  resources set `removalPolicy: RemovalPolicy.RETAIN` / `SNAPSHOT`, and override the logical
  id (`cfnRes.overrideLogicalId`) when refactoring.
- Feature flags live in `cdk.json`: projects created with `cdk init` include flags enabling all features available in that release; existing projects keep old behaviour until you add flags. After upgrading `aws-cdk-lib`, review flags against FEATURE_FLAGS.md rather than blindly flipping them.

## 3. Workflow
```bash
npx cdk bootstrap aws://111111111111/eu-west-1 --cloudformation-execution-policies arn:aws:iam::aws:policy/AdministratorAccess   # once per account/region
npx cdk synth               # writes cdk.out/*.template.json
npx cdk diff AppStack       # review before deploy
npx cdk deploy AppStack --require-approval broadening   # prompts on IAM/SG widening
npx cdk deploy --hotswap    # dev only: direct Lambda/ECS updates, bypasses CFN
```
- Bootstrap creates the assets bucket, ECR repository and deploy/execution roles. By default stacks deploy with the `AdministratorAccess` policy; pass a scoped policy via `--cloudformation-execution-policies` in prod. `--trust` (which requires `--cloudformation-execution-policies`) names the accounts allowed to deploy into the environment, for cross-account pipelines.
- `cdk watch` (a shortcut for `cdk deploy --watch`) is for the dev inner loop; the CLI docs say not to use it or `--hotswap` for production deployments.
- Lambda code: `lambda.Code.fromAsset` or `NodejsFunction` (esbuild bundling);
  `DockerImageFunction` builds and pushes to the bootstrap ECR.

## 4. Tests
```ts
import { Template, Match } from 'aws-cdk-lib/assertions';
const t = Template.fromStack(stack);
t.hasResourceProperties('AWS::S3::Bucket', { BucketEncryption: Match.anyValue() });
t.resourceCountIs('AWS::IAM::Role', 2);
```
- Snapshot tests catch unintended diffs; assertion tests express intent.
- **cdk-nag** packs such as `AwsSolutionsChecks` check constructs at synth. The current cdk-nag README registers them with `Validations.of(app).addPlugins(new AwsSolutionsChecks(app))` and acknowledges a finding with `Validations.of(resource).acknowledge({ id, reason })`; follow the README for the cdk-nag version you install.
- **Aspects** also enforce org rules (tag every resource, deny public buckets) at synth time.

## 5. CDK Pipelines (self-mutating)
```ts
const pipeline = new pipelines.CodePipeline(this, 'Pipeline', {
  synth: new pipelines.ShellStep('Synth', {
    input: pipelines.CodePipelineSource.connection('org/repo', 'main', { connectionArn }),
    commands: ['npm ci', 'npm run build', 'npx cdk synth'],
  }),
  crossAccountKeys: true,   // needed for cross-account stages
});
const prod = pipeline.addStage(new AppStage(this, 'Prod', { env: { account: '2222', region: 'eu-west-1' } }));
prod.addPre(new pipelines.ManualApprovalStep('Promote'));
```
- The pipeline is self-mutating: after you deploy `PipelineStack` once by hand, adding stages or stacks in source makes the pipeline reconfigure itself.
- All environments must be bootstrapped first, with `--trust <tooling-account>` for the ones the pipeline deploys into. Do not delete the bootstrap stack or change its qualifier after a pipeline uses it.
- Add `pipelines.ShellStep` post-steps for integration tests; use `ConfirmPermissionsBroadening`
  to gate IAM changes.

## Gotchas
- `cdk diff` compares templates; a Lambda code change appears only as a changed asset hash.
- Asset hashes depend on file contents *and* bundling; non-deterministic builds (timestamps)
  mean "changes" on every synth.
- `Token` values (`bucket.bucketName`) are unresolved at synth — string ops on them break;
  use `Fn.select`/`Fn.split` or `Lazy`.
- Upgrading `aws-cdk-lib` can change L2 defaults → surprise replacements; always diff.

## Verify
- [ ] `cdk synth` is reproducible (two runs, identical `cdk.out` hashes).
- [ ] cdk-nag passes or every suppression has a reason.
- [ ] `cdk diff` in CI posts to the PR; prod deploy requires approval on broadening.
- [ ] Stateful resources have RETAIN/SNAPSHOT removal policies (check `DeletionPolicy` in the synthesised template).
- [ ] Pipeline self-mutates: change a stage name, push, and watch the pipeline update before deploying.

## Checked
Date: 2026-10-24. Sources: CDK Developer Guide source (awsdocs/aws-cdk-guide, main), aws-cdk-lib pipelines and assertions READMEs (main), cdk-nag README (main).
Confirmed: feature-flag behaviour of cdk init, bootstrap resources and default AdministratorAccess execution policy, --trust requiring --cloudformation-execution-policies, deploy --hotswap and --require-approval default of broadening, cdk watch as a shortcut and its production caveat, CDK Pipelines self-mutation, crossAccountKeys, ConfirmPermissionsBroadening, ManualApprovalStep and CodePipelineSource.connection usage, Template assertions (hasResourceProperties, resourceCountIs, Match.anyValue), cdk-nag current registration API, logical-ID behaviour.
Corrected: cdk-nag registration shown with the Validations plugin API from the current README rather than Aspects.
Removed as unconfirmed: removed-stack-not-deleted note, claims about default flags and bootstrap template versions.
Method: documentation only; no commands were run.
