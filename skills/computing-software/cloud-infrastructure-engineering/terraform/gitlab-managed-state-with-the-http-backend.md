---
id: computing-software.cloud-infrastructure-engineering.terraform.gitlab-managed-state-with-the-http-backend
name: gitlab-managed-state-with-the-http-backend
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, http-backend, gitlab-http-backend, gitlab-managed-state, gitlab-terraform-template, gitlab-ci, remote-state]
level: practitioner
status: docs-checked
description: "Store state in GitLab via the http backend: address/lock URLs, CI_JOB_TOKEN auth, local access with a PAT, and the GitLab OpenTofu/Terraform CI templates."
sources: ["https://developer.hashicorp.com/terraform/language/backend/http", "https://docs.gitlab.com/user/infrastructure/iac/terraform_state/", "https://gitlab.com/components/opentofu"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# GitLab-managed state with the `http` backend

## 1. Backend block (empty on purpose)
```hcl
terraform {
  backend "http" {}
}
```
Everything else comes from env vars so the same code works locally and in CI.

## 2. The settings
```bash
PROJECT_ID=1234; STATE=prod
BASE="https://gitlab.example.com/api/v4/projects/$PROJECT_ID/terraform/state/$STATE"
export TF_HTTP_ADDRESS="$BASE"
export TF_HTTP_LOCK_ADDRESS="$BASE/lock"
export TF_HTTP_UNLOCK_ADDRESS="$BASE/lock"
export TF_HTTP_LOCK_METHOD=POST
export TF_HTTP_UNLOCK_METHOD=DELETE
export TF_HTTP_RETRY_WAIT_MIN=5
export TF_HTTP_USERNAME=gitlab-ci-token      # CI: with CI_JOB_TOKEN
export TF_HTTP_PASSWORD="$CI_JOB_TOKEN"      # local: your username + a PAT with api scope
terraform init -reconfigure
```
The generic `http` backend contract: `GET` fetches state, `POST` stores it,
optional `LOCK`/`UNLOCK` (defaults) or whatever methods you set; a 423/409 on lock
means "already locked". Any server implementing that can be a backend.

## 3. CI
The OpenTofu CI/CD component documents a migration path from GitLab's
`Terraform.gitlab-ci.yml` templates (to its `validate-plan-apply` component) and wraps
the same backend:
```yaml
include:
  - component: gitlab.com/components/opentofu/full-pipeline@<version>
    inputs:
      version: <component version>
      opentofu_version: <tofu version>
      root_dir: infra/prod
      state_name: prod
```
For Terraform proper, write the jobs yourself with the env vars above and
`terraform plan -out=tfplan` / `terraform apply tfplan`, passing the plan as an artifact.
GitLab's docs warn that applying a previous job's plan can leave you unable to lock the
state in the apply job; check its troubleshooting section.

## 4. Operating it
- UI: **Operate > Terraform states** lists states. Locking and unlocking need the
  Maintainer or Owner role; downloading needs Developer or higher.
- Individual state versions can be fetched or removed by serial number (GitLab CLI or
  API); push a downloaded version back with `terraform state push`.
- Delete a state: `curl --request DELETE --header "PRIVATE-TOKEN: $PAT" "$BASE"`.

## Gotchas
- In CI the username is `gitlab-ci-token` and the password is `CI_JOB_TOKEN`; locally use
  your username and a personal access token (legacy tokens need the API scope; fine-grained
  tokens need the Terraform State Read, Create and Lock permissions).
- Reading another project's state needs the Developer role or higher in that project.
- The http backend defaults to `LOCK` and `UNLOCK` methods; GitLab's docs set
  `lock_method=POST` and `unlock_method=DELETE`, so set both (`TF_HTTP_LOCK_METHOD`,
  `TF_HTTP_UNLOCK_METHOD`).

## Verify
- [ ] `terraform init` succeeds and the state appears under Operate > Terraform states after the first apply.
- [ ] A second concurrent plan fails to acquire the state lock.
- [ ] `terraform state pull | jq .serial` matches the latest version's serial in GitLab.

## Checked
- 2026-10-28. Confirmed against the Terraform `http` backend page (GET fetch, POST update by default, `LOCK`/`UNLOCK` defaults, 423 or 409 when locked, `TF_HTTP_*` variables including `TF_HTTP_RETRY_WAIT_MIN`), the GitLab "Terraform/OpenTofu state" doc (`.../terraform/state/<name>` and `/lock` URLs, `lock_method=POST`, `unlock_method=DELETE`, `gitlab-ci-token` with `CI_JOB_TOKEN`, Operate > Terraform states, role requirements, PRIVATE-TOKEN DELETE) and the GitLab OpenTofu component README (`full-pipeline`, inputs `version`, `opentofu_version`, `root_dir`, `state_name`, migration from `Terraform.gitlab-ci.yml`).
- Removed: the claims that the legacy templates are deprecated, that workspaces are unsupported, that LOCK requests get a 405, state-name URL-encoding, and cross-project job-token rules (not in the fetched docs).
Method: documentation only; no commands were run.
