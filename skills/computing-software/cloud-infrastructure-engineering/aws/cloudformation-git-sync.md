---
id: computing-software.cloud-infrastructure-engineering.aws.cloudformation-git-sync
name: cloudformation-git-sync
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, cloudformation, git-sync, gitops, codeconnections, deployment-file, stack-sync]
level: practitioner
status: docs-checked
description: "Deploy CloudFormation stacks GitOps-style with Git sync: CodeConnections link, stack deployment file, sync role, pull request comments and troubleshooting failed syncs."
sources: ["https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/git-sync-concepts-terms.html", "https://docs.aws.amazon.com/codeconnections/latest/APIReference/API_CreateSyncConfiguration.html", "https://docs.aws.amazon.com/codeconnections/latest/APIReference/API_UpdateSyncBlocker.html", "https://docs.aws.amazon.com/codeconnections/latest/APIReference/API_GetResourceSyncStatus.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# CloudFormation Git sync

**Goal:** a push to a branch updates a stack, with no pipeline to maintain, for stacks that are
just a template plus parameters.

## Pieces
1. **Connection** (CodeConnections) to a Git provider: GitHub, GitHub Enterprise, GitLab, Bitbucket or GitLab self-managed; complete the provider handshake in the CodeConnections console (or create the connection with the AWS CLI).
2. **Repository link** for the repo.
3. **Stack deployment file** in the repo (JSON or YAML; `template-file-path`, a `parameters` dictionary of up to 50 entries and an optional `tags` dictionary of up to 50 entries; Git sync can also generate one for you):
```yaml
# deployments/orders-prod.yaml
template-file-path: templates/orders.yaml
parameters:
  Env: prod
  InstanceType: t3.small
tags:
  owner: orders-team
```
4. **Sync configuration** binding stack + branch + file + IAM role:
```bash
aws codeconnections create-repository-link --connection-arn "$CONN" \
  --owner-id my-org --repository-name infra
aws codeconnections create-sync-configuration --branch main \
  --config-file deployments/orders-prod.yaml --repository-link-id "$LINK" \
  --resource-name orders-prod --role-arn "$SYNC_ROLE" --sync-type CFN_STACK_SYNC
```
`--trigger-resource-update-on` (`ANY_CHANGE` or `FILE_CHANGE`), `--publish-deployment-status` and `--pull-request-comment` (each `ENABLED` or `DISABLED`) are further options of `create-sync-configuration`.
Or enable it when creating the stack in the console ("Sync from Git"): you pick the repository, branch and template, and Git sync opens a pull request that adds (or generates) the stack deployment file; merging it provisions the stack.

## Role
The `--role-arn` role grants permission for Git sync to update the stack on your behalf. Use the trust policy and permissions given in the Git sync section of the CloudFormation User Guide, and scope the permissions for the stack's resources like any deployment role.

## Behaviour
- Commits to the monitored template file or stack deployment file on the configured repository and branch update the stack automatically; if your team uses pull requests, changes are deployed once the pull request is accepted.
- Optional **pull request comments**: CloudFormation posts a summary of the changes on pull requests (console option "Enable comment on pull request").
- Sync status: `aws codeconnections get-resource-sync-status --resource-name orders-prod --sync-type CFN_STACK_SYNC`.
- Blockers: `get-sync-blocker-summary` lists them; after fixing the cause, `update-sync-blocker` takes `--id`, `--sync-type`, `--resource-name` and `--resolved-reason`.

## Fit
Good for simple stacks per environment. Use CodePipeline/CDK Pipelines when you need build steps,
tests, approvals, multi-account promotion or StackSets.

## Gotchas
- Git sync monitors only the configured repository and branch, for changes to the template file and the stack deployment file.
- A sync configuration is created per resource (`--resource-name`, for `CFN_STACK_SYNC` a CloudFormation stack).
- Treat git as the source of truth for the stack.

## Verify
- [ ] Push a tag change; the stack updates and the console shows the commit in the sync history.
- [ ] With pull request comments enabled, a PR touching the files gets a summary comment; `get-resource-sync-status` shows a healthy status.

## Checked
Date: 2026-10-24. Sources: CloudFormation User Guide page 'How Git sync works with CloudFormation' (fetched 2026-10-24) and the botocore CodeConnections service model (API 2023-12-01).
Confirmed: supported Git providers, stack deployment file keys and limits (template-file-path, parameters up to 50, tags up to 50), pull-request flow, pull request comments option, monitored repository, branch and files, CreateRepositoryLink and CreateSyncConfiguration parameters, SyncType CFN_STACK_SYNC, TriggerResourceUpdateOn and PublishDeploymentStatus values, GetResourceSyncStatus, GetSyncBlockerSummary and UpdateSyncBlocker parameters.
Removed as unconfirmed: the trust principal and exact role permissions (read from the current Git sync pages before use), EventBridge rule detail, automatic change-set execution wording, template size remark, manual-console-update overwrite claim.
Method: documentation only; no commands were run.
