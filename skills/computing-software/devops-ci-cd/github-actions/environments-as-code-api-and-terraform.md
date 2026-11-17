---
id: computing-software.devops-ci-cd.github-actions.environments-as-code-api-and-terraform
name: environments-as-code-api-and-terraform
category: computing-software
field: devops-ci-cd
product: github-actions
tags: [github-actions, environments-api-create, terraform-github-environment, deployment-environments]
level: advanced
status: gated
description: "Create GitHub environments with protection rules, branch policies, secrets and variables via REST API or Terraform instead of clicking through settings."
sources: ["https://docs.github.com/en/rest/deployments/environments", "https://registry.terraform.io/providers/integrations/github/latest/docs/resources/repository_environment"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Environments as code (REST API and Terraform)

## REST API
```bash
# create/update environment with reviewers and wait timer
gh api -X PUT repos/ORG/REPO/environments/production --input - <<'EOF'
{ "wait_timer": 10, "prevent_self_review": true,
  "reviewers": [{"type":"Team","id": 1234567}],
  "deployment_branch_policy": {"protected_branches": false, "custom_branch_policies": true} }
EOF
# allow only main and release tags (deployment-branch-policies endpoint and type parameter) (gated: unconfirmed, source is paywalled or blocked)
gh api -X POST repos/ORG/REPO/environments/production/deployment-branch-policies -f name=main -f type=branch
gh api -X POST repos/ORG/REPO/environments/production/deployment-branch-policies -f name='v*' -f type=tag
# env secret/variable (gh secret/variable --env flags) (gated: unconfirmed, source is paywalled or blocked)
gh secret set DB_PASSWORD --env production --repo ORG/REPO
gh variable set REGION --env production --body eu-west-1 --repo ORG/REPO
```
Reviewer `id` is the numeric team/user id: `gh api orgs/ORG/teams/TEAM --jq .id`.

## Terraform (integrations/github provider)
The Terraform resource and argument names below were not confirmed (the registry page is JavaScript-only) (gated: unconfirmed, source is paywalled or blocked): check them against the provider documentation.
```hcl
resource "github_repository_environment" "prod" {
  repository          = "repo"
  environment         = "production"
  wait_timer          = 10
  prevent_self_review = true
  reviewers { teams = [data.github_team.sre.id] }
  deployment_branch_policy {
    protected_branches     = false
    custom_branch_policies = true
  }
}
resource "github_repository_environment_deployment_policy" "main" {
  repository     = "repo"
  environment    = github_repository_environment.prod.environment
  branch_pattern = "main"
}
resource "github_actions_environment_secret" "db" {
  repository      = "repo"
  environment     = "production"
  secret_name     = "DB_PASSWORD"
  plaintext_value = var.db_password   # lands in state: protect the state backend
}
```

## Gotchas
- `protected_branches: true` and custom policies are mutually exclusive.
- Referencing an environment in a workflow auto-creates it with no protection: create first.
- Required reviewers and wait timers on private repos need a paid plan.

## Verify
- [ ] `gh api repos/ORG/REPO/environments/production` shows the rules; a deploy from a feature branch is rejected.

## Checked

2026-11-02. Confirmed from the GitHub REST environments page: PUT repos/{owner}/{repo}/environments/{name}, wait_timer (0 to 43,200 minutes), prevent_self_review, reviewers (type User or Team, numeric id, up to six), deployment_branch_policy.protected_branches and custom_branch_policies (must differ); from the gh manual: gh api --input with - for stdin. Gated: the deployment-branch-policies endpoint, gh secret/variable set flags, and all Terraform resource names (registry page not readable).

Method: documentation only; no commands were run.
