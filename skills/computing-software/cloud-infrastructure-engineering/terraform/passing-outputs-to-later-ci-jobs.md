---
id: computing-software.cloud-infrastructure-engineering.terraform.passing-outputs-to-later-ci-jobs
name: passing-outputs-to-later-ci-jobs
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, github-output, output-to-ci, output-json, ci-cd, github-actions]
level: practitioner
status: docs-checked
description: "Pass Terraform outputs to later CI steps and jobs with terraform output -raw/-json, GITHUB_OUTPUT job outputs and GitLab dotenv reports, and keep sensitive values out of them."
sources: ["https://developer.hashicorp.com/terraform/cli/commands/output", "https://docs.github.com/en/actions/using-jobs/defining-outputs-for-jobs", "https://docs.gitlab.com/ee/ci/yaml/artifacts_reports.html#artifactsreportsdotenv", "https://github.com/hashicorp/setup-terraform", "https://docs.github.com/en/actions/security-guides/using-secrets-in-github-actions", "https://docs.gitlab.com/ee/ci/variables/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Passing outputs to later CI jobs

## What `terraform output` gives you
- Only root-module outputs are shown; to expose a child module's value, add a root
  `output` that references `module.<name>.<output>`.
- Plain `terraform output` is human-readable and "can change over time": for
  scripts use `-json` (stable JSON; one object with a key per output, or just the value
  when you name an output) or `-raw` (prints a string, number or bool with no quotes or
  newline decoration; not for lists or objects).
- `-json` and `-raw` print sensitive values in plain text, and so does
  `terraform output NAME`. Ephemeral outputs are omitted entirely.

## GitHub Actions
```yaml
jobs:
  infra:
    runs-on: ubuntu-latest
    outputs:
      api_url: ${{ steps.out.outputs.api_url }}
    steps:
      - uses: hashicorp/setup-terraform@v4
        with: { terraform_wrapper: false }
      - run: terraform init -input=false && terraform apply -auto-approve -input=false
      - id: out
        run: |
          echo "api_url=$(terraform output -raw api_url)" >> "$GITHUB_OUTPUT"
  deploy:
    needs: infra
    runs-on: ubuntu-latest
    steps:
      - env:
          API_URL: ${{ needs.infra.outputs.api_url }}
        run: curl -fsS "$API_URL/health"
```
- Step outputs are written to `$GITHUB_OUTPUT`; a job maps them under `outputs:`;
  a dependent job lists it in `needs:` and reads `needs.<job_id>.outputs.<name>`.
- `hashicorp/setup-terraform` installs a wrapper by default that exposes each call's
  `stdout`, `stderr` and `exitcode` as step outputs. Set `terraform_wrapper: false`
  when you only capture output in the shell, as above. The README lists v4 in its
  examples.
- Mask any sensitive value that is not a GitHub secret with `::add-mask::VALUE`;
  better, do not pass secrets between jobs, and re-read them where needed.
- Avoid putting secrets on command lines, where other users may see them with `ps`.

## GitLab CI
```yaml
infra:
  script:
    - terraform apply -auto-approve
    - echo "API_URL=$(terraform output -raw api_url)" >> build.env
  artifacts:
    reports:
      dotenv: build.env
deploy:
  needs: [infra]
  script: curl -fsS "$API_URL/health"
```
The `dotenv` report collects variables from the file and makes them available as
CI/CD variables to later jobs; jobs listed in `needs` or `dependencies` receive them.
## Rules
- Use `-raw` for single strings, `-json` for structures; never parse the human format.
- Do not pass secrets through CI outputs or artifacts; fetch them where needed.

## Verify
- [ ] Downstream job receives the exact value (echo length, not the secret).
- [ ] No secret appears in job logs.

## Checked
2026-11-08. Confirmed on the cited pages: `terraform output` flags and warnings,
root-module-only behaviour, GitHub job outputs / `needs` / `$GITHUB_OUTPUT`, the
setup-terraform wrapper and `terraform_wrapper` input, `::add-mask::`, the `ps`
warning, the GitLab dotenv report (needs/dependencies pickup per the GitLab variables
page). Removed unconfirmed claims: that the wrapper breaks `$(terraform output -raw)`,
the `terraform-bin` alternative, heredoc syntax for multi-line outputs, GitHub
redacting masked job outputs, the jq `map_values` example, the Azure Pipelines section,
and the version `@v3` (README shows `@v4`).
Method: documentation only; no commands were run.
