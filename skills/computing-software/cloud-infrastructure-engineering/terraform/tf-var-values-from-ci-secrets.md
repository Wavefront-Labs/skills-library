---
id: computing-software.cloud-infrastructure-engineering.terraform.tf-var-values-from-ci-secrets
name: tf-var-values-from-ci-secrets
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, ci-secret-variables, tf-var-env, secrets, github-actions, gitlab-ci]
level: practitioner
status: docs-checked
description: "Feed secrets into Terraform as TF_VAR_ environment variables from GitHub Actions secrets or GitLab CI/CD variables, with masking, protection and the limits of what this guards."
sources: ["https://developer.hashicorp.com/terraform/cli/config/environment-variables#tf_var_name", "https://docs.github.com/en/actions/security-guides/using-secrets-in-github-actions", "https://docs.gitlab.com/ee/ci/variables/", "https://developer.hashicorp.com/terraform/cli/commands/plan", "https://developer.hashicorp.com/terraform/language/values/outputs"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# TF_VAR_ from CI secrets

Terraform reads input variables from environment variables named `TF_VAR_<name>`;
this source is checked last, so `-var` and `-var-file` override it. Non-string
values are written as HCL expressions, for example
`TF_VAR_alist='[1,2,3]'` or `TF_VAR_amap='{ foo = "bar", baz = "qux" }'`.

```hcl
variable "datadog_api_key" {
  type      = string
  sensitive = true
}
```

## GitHub Actions
Create the secret at repository, environment or organization level (Settings >
Secrets and variables > Actions, or `gh secret set NAME`; `--env` for an environment).
```yaml
jobs:
  plan:
    env:
      TF_VAR_datadog_api_key: ${{ secrets.DATADOG_API_KEY }}
    steps:
      - run: terraform plan -input=false -out=tfplan
```
- Secrets are not passed to the runner for workflows triggered from forks (except
  `GITHUB_TOKEN`), not automatically to reusable workflows, and not to workflows
  triggered by Dependabot events.
- A secret that was never set evaluates to an empty string.
- Mask any sensitive value that is not a GitHub secret with `::add-mask::VALUE`.
- Prefer environment variables over command-line arguments for secrets, since
  command lines can be visible to other users via `ps`.

## GitLab CI/CD
Add the variable `TF_VAR_datadog_api_key` under Settings > CI/CD > Variables (project
needs Maintainer, group needs Owner). Variables are exposed to jobs as environment
variables. Options:
- Visibility **Masked** replaces the value with `[MASKED]` in job logs. The value must
  be a single line, 8 or more characters, and must not match an existing variable
  name. Output that is modified (for example shell-escaped) is not masked.
- **Protect variable** limits it to pipelines on protected branches or tags.
- Do not keep secrets in `.gitlab-ci.yml`: those values are visible to everyone with
  repository access.
- Masking is not a guarantee against a malicious job script; review changes to
  `.gitlab-ci.yml` before running pipelines (GitLab warns that malicious code can read
  masked and protected variables). By default fork pipelines cannot read the
  parent project's variables, but a merge request pipeline run in the parent project
  gets them all.

## What this protects and what it does not
- Keeps the secret out of version control and `.tfvars` files.
- A saved plan (`-out`) holds sensitive data in cleartext even if the terminal output
  hides it; treat plan files as sensitive artifacts.
- Sensitive output values are stored in state. An output marked `ephemeral` is
  omitted from state and plan files but has restrictions on what can be assigned.
- `terraform output -json` or `-raw` prints sensitive outputs in plain text.

## Better where possible
GitHub documents OpenID Connect so workflows authenticate to cloud providers directly
instead of storing long-lived credentials as secrets; GitLab documents connecting
an external secrets manager.

## Verify
- [ ] Secret not present in job logs or plan text.
- [ ] Prod secrets scoped to the prod environment (GitHub) or protected (GitLab).

## Checked
2026-11-08. Confirmed on the cited pages: `TF_VAR_name` precedence and HCL examples,
GitHub secret scopes, `gh secret set` and `--env`, fork/reusable-workflow/Dependabot
behaviour, empty-string result, `::add-mask::`, GitLab masking rules, protection,
fork behaviour, role requirements, plan-file cleartext warning, sensitive outputs in
state and the `ephemeral` output argument. Removed: the Azure Pipelines section,
`pull_request_target` advice, the write-only argument advice, the claim that sensitive
variables are redacted in plan output, and the "approvals" claim for GitHub
environments, none of which are on the cited pages.
Method: documentation only; no commands were run.
