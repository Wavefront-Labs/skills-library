---
id: computing-software.cloud-infrastructure-engineering.terraform.cicd-pipeline-integration
name: cicd-pipeline-integration
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, cicd, github-actions, gitlab-ci, atlantis, plan-on-pr, apply-on-merge, concurrency-control, oidc, github-oidc, plan-artifact, pr-comment, drift-check-pipeline, pipeline-permissions]
level: advanced
status: docs-checked
description: "Build a plan-on-PR, apply-on-merge Terraform pipeline (GitHub Actions or Atlantis) with locking, OIDC cloud auth, and a plan artifact applied unchanged."
sources: ["https://developer.hashicorp.com/terraform/cli/commands/apply", "https://developer.hashicorp.com/terraform/cli/commands/plan", "https://developer.hashicorp.com/terraform/language/backend/s3", "https://github.com/aws-actions/configure-aws-credentials", "https://docs.github.com/en/actions/how-tos/write-workflows/choose-when-workflows-run/control-workflow-concurrency", "https://www.runatlantis.io/docs/repo-level-atlantis-yaml"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# CI/CD pipeline integration for Terraform

**Goal:** every change goes plan-on-PR, human-reviewed plan, apply-on-merge, with the
exact plan that was reviewed being the one applied, not a fresh plan that could differ
because of a race, a provider update or drift. This complements
`computing-software.cloud-infrastructure-engineering.terraform.terraform-cloud-remote-runs-and-vcs-workflows`
for orgs on HCP Terraform; this skill is for rolling your own in GitHub Actions or
using Atlantis.

## 1. Apply the reviewed plan, not a new one
```yaml
# on PR
- run: terraform plan -out=tfplan -lock-timeout=5m
- uses: actions/upload-artifact@v4
  with: { name: tfplan-${{ github.event.pull_request.number }}, path: tfplan }
# on merge to main
- uses: actions/download-artifact@v4   # same artifact, not a re-plan
- run: terraform apply -lock-timeout=5m tfplan
```
Passing a saved plan to `terraform apply` performs exactly those operations without
prompting, and you cannot add planning options. Use `terraform show` to inspect the
saved plan first. The two-step `-out` workflow is intended for automation. If the
apply of a stored plan fails because the world moved, re-plan and re-review rather
than working around it. A plan made without `-out` is only speculative.
`-lock-timeout=DURATION` makes Terraform wait for the state lock up to that long.

## 2. OIDC over static credentials
```yaml
permissions: { id-token: write, contents: read }
- uses: aws-actions/configure-aws-credentials@v4
  with: { role-to-assume: <ROLE_ARN>, aws-region: <REGION> }
```
GitHub OIDC federation to a cloud role means no long-lived access key in repo
secrets. GitHub's AWS OIDC guide recommends evaluating the
`token.actions.githubusercontent.com:sub` condition key in the role trust policy to
limit which workflows can assume the role. Trust-policy syntax differs per provider;
follow the provider-specific guide.

## 3. Concurrency control
Two merges must not apply concurrently to the same state. The backend lock
(for the S3 backend, `use_lockfile = true`; the DynamoDB option is deprecated) blocks
the second; add a CI concurrency group keyed by environment:
```yaml
concurrency:
  group: tf-apply-${{ inputs.environment }}
  cancel-in-progress: false   # do not cancel a running apply
```
With `cancel-in-progress: false`, a running apply is not cancelled by a newer one;
cancelling an apply mid-flight can leave infrastructure half-changed.

## 4. PR feedback loop
Post the plan output (and the cost diff and policy results; see
`computing-software.cloud-infrastructure-engineering.terraform.cost-estimation-with-infracost`
and `computing-software.cloud-infrastructure-engineering.terraform.policy-as-code-with-sentinel-and-opa`)
as one updating PR comment rather than a new comment per push, so stale plans do not
mislead reviewers.

## 5. Atlantis as the self-hosted alternative
Atlantis receives PR events and runs plans and applies from PR comments
(`atlantis plan [options] -- [terraform plan flags]`, `atlantis apply`). A repo-level
`atlantis.yaml` defines `projects` and `workflows`; `apply_requirements` accepts
`mergeable`, `approved` and `undiverged` (since v0.17.0). It pays off when many repos
need the same workflow.

## 6. Per-environment promotion
Use platform-native environment protection (for GitHub, required reviewers on the
environment; see
`computing-software.cloud-infrastructure-engineering.terraform.terraform-change-approval-and-change-windows`)
rather than custom approval logic in pipeline scripts.

## Gotchas
- Treat the `tfplan` artifact as sensitive: restrict download to the same pipeline
  and keep retention short.
- A retried CI job re-plans unless the pipeline reuses the stored artifact, which
  defeats the "apply the reviewed plan" rule.
- Pick a `-lock-timeout` shorter than the job timeout so you get a clear lock message.

## Verify
- [ ] The artifact applied on merge is the one reviewed on the PR.
- [ ] No static cloud credential in pipeline secrets where OIDC is available.
- [ ] Concurrent merges against one state serialise without cancelling a running apply.
- [ ] Each environment's promotion gate is a platform-native protection rule.

## Checked
2026-11-09. Confirmed against the `terraform plan` and `terraform apply` command pages (`-out`, saved plan mode, speculative plan, `-lock-timeout`), the S3 backend page (`use_lockfile`, deprecated `dynamodb_table`), the aws-actions/configure-aws-credentials README (`id-token: write`, `role-to-assume`), GitHub's AWS OIDC guide (`sub` condition key), GitHub's concurrency page (`cancel-in-progress`) and the Atlantis `atlantis.yaml` and command pages.
Removed as unconfirmed: the claim that apply refuses a plan tied to an older state serial, the specific `gh pr comment --edit-last` approach and "terraform-plan-comment" action, GitLab CI content, hard-coded role ARN and region, and the "highest-value hardening step" ranking.
Method: documentation only; no commands were run.
