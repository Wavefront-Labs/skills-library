---
id: computing-software.cloud-infrastructure-engineering.terraform.account-and-region-directory-matrices
name: account-and-region-directory-matrices
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, account-matrix, root-module-layout, multi-account, multi-region, environment-directories, live-repo]
level: practitioner
status: docs-checked
description: "Lay out Terraform root modules as an account by region by component matrix: directory conventions, small state blast radius, shared modules, and generating the matrix in CI."
sources:
  - https://developer.hashicorp.com/terraform/language/modules/develop/structure
  - https://docs.aws.amazon.com/prescriptive-guidance/latest/terraform-aws-provider-best-practices/structure.html
  - https://terragrunt.gruntwork.io/docs/features/keep-your-terraform-code-dry/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Account and region directory matrices

For many AWS accounts / Azure subscriptions / GCP projects and regions, one root module per **account x region x component** keeps each state small, permissions narrow and plans fast.

## Layout
```
live/
  _modules -> ../modules           (or reference by git/registry source)
  prod/                            # account (or subscription/project)
    account.hcl | account.auto.tfvars
    global/                        # region-less: IAM, Route 53, org-level
      iam/
    eu-west-2/
      region.auto.tfvars
      network/        main.tf backend.tf
      eks/
      rds-orders/
    us-east-1/
      network/
  staging/
    eu-west-2/
      network/
modules/
  network/ eks/ rds/
```
- Each leaf directory is a root module with its own backend key: `prod/eu-west-2/network/terraform.tfstate`.
- Leaf `main.tf` mostly calls one module with environment-specific inputs; logic lives in `modules/`.
- Components that change together and share lifecycle go together; things owned by different teams or with different change rates split.

## Passing account/region context
- Terraform automatically loads `terraform.tfvars`, `terraform.tfvars.json` and `*.auto.tfvars` / `*.auto.tfvars.json` files it detects; a shared account-level file in a parent directory needs an explicit route: copy or symlink it into each leaf, pass `-var-file=../../account.tfvars` from a wrapper, or use Terragrunt `read_terragrunt_config(find_in_parent_folders("account.hcl"))`.
- Cross-component values: read via `terraform_remote_state` or, better, data sources/SSM parameters published by the producing component (looser coupling).

## Provider per leaf
```hcl
provider "aws" {
  region = var.region
  assume_role { role_arn = "arn:aws:iam::${var.account_id}:role/terraform-deploy" }
  default_tags { tags = { Environment = var.environment, Component = "network", ManagedBy = "terraform" } }
}
```

## CI over the matrix
```bash
# changed leaves only
git diff --name-only origin/main...HEAD | grep '^live/' | xargs -n1 dirname | sort -u | while read d; do
  while [ ! -f "$d/backend.tf" ] && [ "$d" != live ]; do d=$(dirname "$d"); done; echo "$d"
done | sort -u > changed-roots.txt
```
Feed the list into a matrix job (GitHub `strategy.matrix` from JSON). Module changes should trigger plans in every leaf that uses the module (map with a simple grep of `source = "../../modules/x"` or Terragrunt `run --all --queue-include-dir "prod/**" -- plan`).

## Trade-offs
- Many roots = many plans/applies to orchestrate and ordering between components (network before eks). A wrapper such as Terragrunt (`run --all`) can manage dependencies between components.
- Workspaces give several states for one configuration and one backend, and HashiCorp states they are not appropriate for deployments needing separate credentials and access controls; directories make prod vs staging differences explicit and reviewable.

## Verify
- [ ] Every leaf has a unique state key; a plan in one leaf never shows resources of another.
- [ ] CI plans only changed leaves (plus dependants of changed modules).

## Checked
2026-11-08. Confirmed against the Terraform variables page (automatic loading of terraform.tfvars and auto.tfvars files, -var-file), the workspaces page (one backend, multiple states; not for separate credentials), the AWS provider docs (assume_role with role_arn, default_tags), Terragrunt docs (find_in_parent_folders, read_terragrunt_config, run --all, --queue-include-dir) and the GitHub Actions matrix page (strategy.matrix, fromJSON). Removed: the claim that auto.tfvars are never read from parent directories, and Terramate, Spacelift and Terraform Stacks as dependency wrappers (not on the cited pages). The layout and blast-radius advice is design guidance, not a documented requirement.
Method: documentation only; no commands were run.
