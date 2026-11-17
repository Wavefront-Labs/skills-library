---
id: computing-software.cloud-infrastructure-engineering.terraform.github-actions-setup-terraform-with-environment-protection
name: github-actions-setup-terraform-with-environment-protection
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, setup-terraform, hashicorp-setup-terraform, github-actions, environment-protection, concurrency-group, oidc]
level: practitioner
status: docs-checked
description: "Build a GitHub Actions Terraform pipeline with hashicorp/setup-terraform, AWS OIDC credentials, environment protection rules for approval, and per-state concurrency groups."
sources:
  - "https://github.com/hashicorp/setup-terraform"
  - "https://docs.github.com/en/actions/how-tos/deploy/configure-and-manage-deployments/manage-environments"
  - "https://docs.github.com/en/actions/how-tos/write-workflows/choose-when-workflows-run/control-workflow-concurrency"
  - "https://github.com/aws-actions/configure-aws-credentials"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# GitHub Actions: setup-terraform, environments, concurrency

```yaml
name: terraform-prod
on:
  pull_request: { paths: ["live/prod/network/**"] }
  push: { branches: [main], paths: ["live/prod/network/**"] }

permissions:
  id-token: write        # needed for OIDC
  contents: read
  pull-requests: write   # only if a step comments the plan on the PR

concurrency:
  group: tf-live-prod-network          # one run per state at a time
  cancel-in-progress: false

defaults:
  run: { working-directory: live/prod/network }

jobs:
  plan:
    if: github.event_name == 'pull_request'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: hashicorp/setup-terraform@v4
        with: { terraform_version: "<TERRAFORM_VERSION>" }
      - uses: aws-actions/configure-aws-credentials@v6
        with: { role-to-assume: "arn:aws:iam::<ACCOUNT_ID>:role/<PLAN_ROLE>", aws-region: "<REGION>" }
      - run: terraform init -input=false
      - run: terraform plan -input=false -no-color

  apply:
    if: github.event_name == 'push'
    runs-on: ubuntu-latest
    environment: production             # protection rules apply before this job runs
    steps:
      - uses: actions/checkout@v4
      - uses: hashicorp/setup-terraform@v4
        with: { terraform_version: "<TERRAFORM_VERSION>", terraform_wrapper: false }
      - uses: aws-actions/configure-aws-credentials@v6
        with: { role-to-assume: "arn:aws:iam::<ACCOUNT_ID>:role/<APPLY_ROLE>", aws-region: "<REGION>" }
      - run: terraform init -input=false
      - run: terraform plan -input=false -out=tfplan
      - run: terraform apply -input=false tfplan
```
Action major versions above follow the examples in each action's README (setup-terraform `@v4`;
the AWS action's README example uses a full `v6.x` tag); check the current release before copying.

## Key points
- **setup-terraform** downloads a Terraform CLI version onto the PATH, can write HCP Terraform or
  Terraform Enterprise credentials into the CLI config (`cli_config_credentials_token`, and
  `cli_config_credentials_hostname`, default `app.terraform.io`), and by default installs a wrapper
  that exposes `stdout`, `stderr` and `exitcode` step outputs. Set `terraform_wrapper: false` if
  later steps do not need those outputs. `terraform_version` accepts a version or a constraint; with
  none given it defaults to latest, so pin it. It runs on ubuntu, windows and macos hosted runners
  (use Bash on Windows).
- **PR plan comments:** a GitHub comment is limited to 65535 characters, so a long plan can fail
  the run even when the plan succeeds; the README suggests appending the plan to
  `$GITHUB_STEP_SUMMARY` instead.
- **Environments:** a job that references an environment must follow its protection rules before
  it runs or can read the environment's secrets. Rules include required reviewers (up to 6 people or
  teams; one approval is enough; optional prevent self-review), a wait timer, optionally disallowing
  admin bypass, and a deployment-branches restriction. Environment secrets and variables are only
  available to jobs that use the environment. Required reviewers and other rules on private repositories
  need a paid plan (see the page). A workflow that references a non-existent environment creates it
  with no protection rules, so create and configure it first.
- **OIDC:** the AWS action recommends OIDC because it gives temporary credentials. Needs
  `permissions: id-token: write`, an IAM identity provider for GitHub, and a role whose trust policy
  allows `sts:AssumeRoleWithWebIdentity` with conditions on `aud` and `sub`. For workflows running in a
  GitHub environment the `sub` claim includes an `environment:<ENVIRONMENT_NAME>` stanza, so the
  apply role's trust policy can be tied to the environment. Also check the README's note on the
  organisation and repository ID suffixes in newer `sub` values.
- **Concurrency:** at most one running job or workflow per concurrency group. By default a newly
  queued run replaces any existing pending run in that group (`queue: single`); `cancel-in-progress: true`
  also cancels the running one. `queue: max` allows up to 100 pending runs, processed first-in-first-out,
  and cannot be combined with `cancel-in-progress: true`. Group names are case insensitive and must be
  unique across workflows or they will cancel each other's runs. Use one group per state, and leave
  `cancel-in-progress` false so an apply is never cancelled midway. Combine with Terraform state locking.

## Gotchas
- With the default `queue: single`, a third quick push replaces the second pending run rather than
  queuing behind it; use `queue: max` if every merge must apply in order.
- Set a protection rule on the environment that the OIDC apply role trusts, otherwise the trust policy
  alone does not make anyone approve.
- Never put credentials in the repository; the AWS README recommends least privilege and monitoring
  the credentials' activity.

## Verify
- [ ] The apply job waits for approval in the Actions UI.
- [ ] Two pushes in quick succession do not apply concurrently.

## Checked
Checked 2026-11-08 against the hashicorp/setup-terraform README, the GitHub Docs pages on managing
environments and on controlling concurrency, and the aws-actions/configure-aws-credentials README.
Removed: the saved-plan artifact upload and download steps and the claims about plan artifacts holding
secrets, fork pull requests lacking OIDC tokens and runner-image matching (not on those pages), and the
claim that the wrapper breaks `terraform output -raw`.
Method: docs-only read of cited pages, 2026-11-08
