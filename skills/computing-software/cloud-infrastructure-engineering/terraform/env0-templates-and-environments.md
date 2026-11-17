---
id: computing-software.cloud-infrastructure-engineering.terraform.env0-templates-and-environments
name: env0-templates-and-environments
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, env0, env0-templates, environments-as-a-service, custom-flows, ttl, self-service, opentofu]
level: practitioner
status: docs-checked
description: "Model Terraform on env0: templates, project assignment, environments with variables and TTLs, env0.yml custom flow hooks, approvals and the env0 provider."
sources: ["https://registry.terraform.io/providers/env0/env0/latest/docs", "https://github.com/env0/terraform-provider-env0/tree/main/docs/resources", "https://docs.env0.com/guides/admin-guide/custom-flows"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# env0 templates and environments

In env0 a **template** is a reusable definition (repository, path, IaC type and
version); an **environment** is a deployed instance of a template inside a
**project**. Design templates as products people can deploy many times (per
developer, per PR, per customer), not one-off roots.

## 1. Templates as code
```hcl
resource "env0_template" "web_stack" {
  name              = "web-stack"
  repository        = "https://github.com/example/infra"
  path              = "templates/web-stack"
  revision          = "main"
  type              = "opentofu"          # terraform, terragrunt, pulumi, k8s, workflow, cloudformation, helm, opentofu, ansible
  opentofu_version  = "<VERSION>"         # or "latest", or "RESOLVE_FROM_CODE"
  vcs_connection_id = var.vcs_connection_id
}
resource "env0_template_project_assignment" "web_dev" {
  template_id = env0_template.web_stack.id
  project_id  = env0_project.dev.id
}
```
`name`, `repository` and `type` are required. Use `terraform_version` for
Terraform templates (`latest` or `RESOLVE_FROM_TERRAFORM_CODE` are accepted).
`github_installation_id` is deprecated in favour of `vcs_connection_id`.
`retries_on_deploy` and `retries_on_destroy` configure retries.

## 2. Variables
`env0_configuration_variable` is created globally by default, or under a scope with
`project_id`, `template_id` or `environment_id`. `type` defaults to `environment`;
set `type = "terraform"` for Terraform variables. Mark secrets `is_sensitive = true`.
`is_read_only` stops lower scopes editing a value; `is_required` forces lower scopes
to set it.
```hcl
resource "env0_configuration_variable" "region" {
  name       = "region"
  value      = "<REGION>"
  type       = "terraform"
  project_id = env0_project.dev.id
}
```
Do not mix an environment's inline `configuration` block with
`env0_configuration_variable` resources for the same variables.

## 3. Environments
```hcl
resource "env0_environment" "pr_123" {
  name                       = "web-pr-123"
  project_id                 = env0_project.dev.id
  template_id                = env0_template.web_stack.id
  approve_plan_automatically = true
  ttl                        = "<ISO-8601 DATE>"   # auto-destroy; omit for no TTL
  configuration {
    name  = "instance_count"
    value = "1"
  }
}
```
- `ttl` is the ISO date the environment is destroyed; omitting it means an infinite TTL.
- With `approve_plan_automatically = false`, any deployment that changes or destroys
  resources waits for manual approval in the env0 UI after the plan.
- `drift_detection_cron` schedules drift detection.
- `force_destroy` is a destroy safeguard read from state: apply it as `true` once
  before removing the resource.
- `prevent_auto_deploy` stops the provider triggering a run on create or update.

## 4. Custom flows (env0.yml)
Create `env0.yml` under the template folder; env0 uses it when found in the git
repository. Hooks run before or after init, plan, apply, destroy and error steps.
```yaml
version: 2
deploy:
  steps:
    terraformInit:
      before:
        - tflint --init && tflint
destroy:
  steps:
    terraformDestroy:
      before:
        - ./scripts/snapshot-db.sh
```
If any command returns a non-zero exit code the deployment stops with status
Failed, which you can use for validation. Keep scripts in the repo and make sure
any extra tools exist in the runner.

## Gotchas
- A template's `revision` or path change affects every environment on its next
  deploy; pin production environments to a tag or use a separate template.
- For sub-environment configuration the API redacts sensitive values, so a secret
  changed outside Terraform is not detected.

## Verify
- [ ] A new environment can be deployed from the template in a dev project.
- [ ] TTL-expired environments destroy cleanly.
- [ ] Custom flow steps appear in the deployment log and fail the run on error.

## Checked
2026-11-09. Confirmed against the env0 provider docs (resources env0_template, env0_template_project_assignment, env0_configuration_variable, env0_environment: arguments, allowed `type` values, `ttl`, `approve_plan_automatically`, `force_destroy`, `prevent_auto_deploy`) and the env0 custom flows guide (env0.yml location, non-zero exit fails the deployment, step names).
Removed as unconfirmed: "most specific scope wins" precedence rule, credentials via OIDC objects attached to projects, the `ENV0_TF_PLAN_JSON` variable and the conftest hook, project policies enforcing a maximum TTL, "destroying a template leaves environment infrastructure", "sensitive variables are write-only in the UI", and the specific version number in the template example.
Method: documentation only; no commands were run.
