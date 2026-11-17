---
id: computing-software.cloud-infrastructure-engineering.aws.sam-cli-with-terraform-projects
name: sam-cli-with-terraform-projects
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, sam, sam-terraform, terraform, hook-name-terraform, sam-local-invoke, lambda-local-testing]
level: practitioner
status: docs-checked
description: "Use SAM CLI local build, invoke and start-api against Lambda functions defined in Terraform via the terraform hook, including module addresses and sam_metadata resources."
sources: ["https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/using-samcli-terraform.html", "https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/terraform-sam-metadata.html", "https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/terraform-support.html", "https://github.com/aws/aws-sam-cli/blob/develop/samcli/commands/_utils/options.py"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SAM CLI with Terraform projects

**Goal:** keep Terraform as the IaC but get `sam local invoke` / `start-api` / `build` for
Lambda functions it defines.

## Prerequisites
- A recent SAM CLI, Terraform, and Docker running.
- Terraform support is an opt-in (beta/experimental) feature: the CLI asks you to accept it when you use `--hook-name`, or
  you pass `--beta-features` or set `beta_features = true` in `samconfig.toml`.

## Commands
```bash
cd infra/
sam build --hook-name terraform                        # builds functions found in the plan
sam local invoke --hook-name terraform aws_lambda_function.orders -e event.json
sam local invoke --hook-name terraform 'module.api.aws_lambda_function.handler[0]' -e event.json
sam local start-api --hook-name terraform              # API Gateway resources in the plan
sam local start-lambda --hook-name terraform
```
- Add `hook_name = "terraform"` and `beta_features = true` to `samconfig.toml` to avoid repeating the flags.
- A function can be named by its Lambda function name or its full Terraform resource address (including the module path).
- `--skip-prepare-infra` (valid only together with `--hook-name`) skips preparing the infrastructure metadata again.

## Build metadata for code not packaged by Terraform
When Terraform points at a zip produced elsewhere, add a `sam_metadata` resource so SAM knows how to build:
```hcl
resource "null_resource" "sam_metadata_aws_lambda_function_orders" {
  triggers = {
    resource_name        = "aws_lambda_function.orders"
    resource_type        = "ZIP_LAMBDA_FUNCTION"
    original_source_code = "${path.module}/../src/orders"
    built_output_path    = "${path.module}/build/orders.zip"
  }
}
```
Similar metadata covers layers (`LAMBDA_LAYER`) and container images (`IMAGE_LAMBDA_FUNCTION`).

## Gotchas
- `--env-vars env.json` overrides environment variables for local runs.
- If you define Lambda artifacts with Terraform variables, a `sam_metadata` resource is not needed.
- Deploying is still done with Terraform.

## Verify
- [ ] `sam local invoke --hook-name terraform <address>` returns the expected output in Docker.
- [ ] `sam build --hook-name terraform` produces artifacts at the paths Terraform expects.

## Checked
Date: 2026-10-24. Documentation release: AWS SAM Developer Guide (awsdocs source, June 2023 snapshot) plus the aws/aws-sam-cli source (`develop` branch: `--hook-name`, `--skip-prepare-infra`, Terraform listed as an experimental IaC support flag).
Confirmed: `--hook-name terraform` on `sam build`, `sam local invoke`, `sam local start-lambda` and `sam local start-api`; beta opt-in prompt, `--beta-features` and the `samconfig.toml` keys `hook_name` and `beta_features`; function id as Lambda name or full Terraform address; `sam_metadata` null_resource triggers (`resource_name`, `resource_type`, `original_source_code`, `built_output_path`) and resource types `ZIP_LAMBDA_FUNCTION`, `IMAGE_LAMBDA_FUNCTION`, `LAMBDA_LAYER`; `--skip-prepare-infra` requires `--hook-name`.
Removed as unconfirmed: Terraform version requirement, variable-value and remote-state remarks and cross-account layer download.

Method: documentation only; no commands were run.
