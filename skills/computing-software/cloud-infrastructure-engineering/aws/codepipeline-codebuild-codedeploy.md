---
id: computing-software.cloud-infrastructure-engineering.aws.codepipeline-codebuild-codedeploy
name: codepipeline-codebuild-codedeploy
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, codepipeline, codebuild, codedeploy, blue-green-deployment, canary-deployment, ci-cd, buildspec, appspec, codeconnections, pipeline-v2, deployment-group, lambda-alias-shift, ecs-blue-green, in-place-deployment, manual-approval, cross-account-deploy, build-cache]
level: practitioner
status: draft
description: "Build AWS-native CI/CD: CodePipeline V2 stages and triggers, CodeBuild buildspecs with caching and secrets, CodeDeploy in-place/blue-green for EC2, ECS and Lambda canary shifts with alarm rollback."
sources: ["AWS CodePipeline User Guide - Pipeline types and stage actions", "AWS CodeBuild User Guide - Build specification reference", "AWS CodeDeploy User Guide - Deployment configurations and AppSpec file reference", "AWS CodeDeploy User Guide - Blue/green deployments on Amazon ECS"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# CodePipeline, CodeBuild, CodeDeploy — the AWS-native delivery chain

**Goal:** commit → build → test → deploy with approvals, cross-account targets, and
deployments that shift traffic gradually and roll back on alarms.

## 1. CodePipeline
- Use **V2 pipelines**: Git triggers with branch/path/tag filters, pipeline-level
  variables, per-execution billing. Source via **CodeConnections** (GitHub/GitLab/Bitbucket
  app-based connection), not OAuth tokens or webhooks you manage.
- Stages run sequentially; actions inside a stage with the same `runOrder` run in parallel.
  Artifacts pass between stages through the pipeline's S3 bucket (KMS-encrypted for
  cross-account).
- Actions: `CodeBuild` (build/test/anything), `CloudFormation` (`CREATE_UPDATE`,
  `CHANGE_SET_REPLACE` + `CHANGE_SET_EXECUTE`), `CodeDeploy`, `ECS`, `S3`, `Lambda` invoke,
  `Manual approval` (SNS notify), `Commands` (shell without a project), `ECRBuildAndPublish`.
- Cross-account deploy: artifact bucket policy + KMS key policy grant the target account;
  the action assumes a `RoleArn` in the target; CloudFormation action gets its own
  execution role there.
- Execution modes: `QUEUED` (default V2), `SUPERSEDED` (newer commit cancels waiting
  executions), `PARALLEL`. Stage-level **rollback** on failure and **conditions**
  (`on failure`/`on success` rules, e.g. alarm checks) exist in V2.

## 2. CodeBuild
```yaml
version: 0.2
env:
  secrets-manager: { DOCKER_TOKEN: "ci/dockerhub:token" }   # never plain env for secrets
  variables: { CI: "true" }
phases:
  install: { runtime-versions: { nodejs: 20 } }
  pre_build: { commands: ["npm ci"] }
  build: { commands: ["npm test", "npm run build"] }
  post_build: { commands: ["aws s3 sync dist s3://$BUCKET"] }
artifacts: { files: ["**/*"], base-directory: dist }
cache: { paths: ["node_modules/**/*"] }
reports: { jest: { files: ["junit.xml"], file-format: JUNITXML } }
```
- Compute: `BUILD_GENERAL1_SMALL…2XLARGE`, Graviton (`ARM_CONTAINER`), **Lambda compute**
  for short builds (fast start, no Docker), reserved capacity fleets for queue-free starts.
- Docker builds need `privilegedMode: true`; log in with `aws ecr get-login-password`.
  Pull-through cache or ECR copies of base images avoid Docker Hub rate limits.
- Cache: S3 cache (paths above) or **local cache** (`LOCAL_DOCKER_LAYER_CACHE`,
  `LOCAL_SOURCE_CACHE`) — local cache only helps when the same host is reused.
- Builds inside a VPC need a NAT/endpoints for S3/ECR/Logs; attach a security group.
- Batch builds (`build-graph`/`build-matrix`) fan out tests. Webhook-triggered builds for
  GitHub Actions runners (`codebuild-hosted` runners) are also supported.

## 3. CodeDeploy
| Platform | Deployment types | Traffic control |
|---|---|---|
| **EC2/on-prem** | In-place or blue/green (new ASG or copy) | ALB/NLB deregistration; `CodeDeployDefault.OneAtATime/HalfAtATime/AllAtOnce` |
| **ECS** | Blue/green only (two target groups, one listener) | `CodeDeployDefault.ECSCanary10Percent5Minutes`, `ECSLinear10PercentEvery1Minutes`, `ECSAllAtOnce` |
| **Lambda** | Alias traffic shift | `LambdaCanary10Percent5Minutes`, `LambdaLinear10PercentEvery1Minute` |

- **EC2 appspec.yml**: `files` to copy, `hooks` (`BeforeInstall`, `AfterInstall`,
  `ApplicationStart`, `ValidateService`) running scripts with timeouts; the CodeDeploy agent
  must be installed (SSM `AWS-ConfigureAWSPackage` `AWSCodeDeployAgent`).
- **ECS appspec**: `TaskDefinition`, `LoadBalancerInfo.ContainerName/Port`; hooks
  `BeforeAllowTestTraffic`/`AfterAllowTestTraffic` are Lambda functions that hit the **test
  listener** (port 8080/9443) before production traffic shifts; `terminationWaitTimeInMinutes`
  keeps blue tasks for instant rollback.
- **Lambda appspec**: `Name`, `Alias`, `CurrentVersion`, `TargetVersion`, hooks `BeforeAllowTraffic`/`AfterAllowTraffic`.
- Deployment group: **auto rollback** on `DEPLOYMENT_FAILURE` and `DEPLOYMENT_STOP_ON_ALARM`
  with CloudWatch alarms (5xx rate, p99) attached. ECS native blue/green (without CodeDeploy)
  is newer; CodeDeploy still gives the hook + alarm model.

## 4. Reference pipeline shape
`Source` → `Build` (unit tests, image push, `cdk synth`/`sam package`) → `Deploy-Staging`
(CloudFormation change set + execute) → `IntegrationTests` (CodeBuild) → `Approve` →
`Deploy-Prod` (CodeDeploy canary with alarms). Notifications via **CodeStar Notifications**
→ SNS/Slack (Chatbot).

## Gotchas
- Pipeline service role needs `codestar-connections:UseConnection` or sources fail with
  a vague permissions error.
- CodeBuild `secrets-manager` env lookups bill per build; `parameter-store` is free for
  non-secret config.
- ECS blue/green requires the service to be *created* with `deploymentController: CODE_DEPLOY`;
  you cannot flip an existing rolling-update service.
- Hooks that time out fail the deployment but **do not** stop traffic already shifted;
  alarms are the real safety net.
- Artifacts over 5 GB or ZIP paths with symlinks break between actions — keep artifacts small.
- Unconfirmed: exact V2 condition/rollback feature availability per region — check the console.

## Verify
- [ ] Push to a non-matching branch does not trigger the pipeline; matching branch does.
- [ ] `buildspec` secrets never appear in logs (check `CODEBUILD_*` output masking).
- [ ] Staging deploy executes a change set that was visible in the previous action's output.
- [ ] Canary with a forced 500 in the new version rolls back on the alarm; old version serves 100 %.
- [ ] Cross-account prod deploy uses the target-account role, not the tooling account's.
