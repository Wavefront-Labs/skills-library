---
id: computing-software.cloud-infrastructure-engineering.google-cloud.project-factory-terraform-module
name: project-factory-terraform-module
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, landing-zone, project-factory, project-factory-module, pf-module, terraform, shared-vpc, project-vending]
level: practitioner
status: docs-checked
description: "Vend projects with terraform-google-modules/project-factory: naming, billing, APIs, default SA handling, Shared VPC attachment, budgets, liens and a YAML-driven factory pattern."
sources: ["https://github.com/terraform-google-modules/terraform-google-project-factory", "https://cloud.google.com/docs/terraform/blueprints/terraform-blueprints"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Project factory module

## 1. Minimal, opinionated call
```hcl
module "payments_prod" {
  source  = "terraform-google-modules/project-factory/google"
  version = "<PINNED_VERSION>"   # pin; take the current release from the module's releases

  name              = "payments-prod"
  random_project_id = true       # adds a suffix of 4 random characters to the project ID
  org_id            = var.org_id
  folder_id         = var.folder_id
  billing_account   = var.billing_account
  labels            = { team = "payments", env = "prod" }

  activate_apis           = ["compute.googleapis.com", "run.googleapis.com"]
  default_service_account = "deprivilege"   # delete, deprivilege, disable or keep; module default is disable
  auto_create_network     = false           # module default
  lien                    = true            # module default is false

  svpc_host_project_id = var.host_project_id
  shared_vpc_subnets   = ["projects/<HOST_PROJECT_ID>/regions/<REGION>/subnetworks/<SUBNET>"]

  budget_amount               = 2000
  budget_alert_spent_percents = [0.5, 0.9, 1.0]
}
```

## 2. Shared VPC behaviour (from the module README)
- If `svpc_host_project_id` and `shared_vpc_subnets` are not set, `roles/compute.networkUser` is not assigned.
- If `svpc_host_project_id` is set but no subnets are given, `roles/compute.networkUser` is assigned on the host project, so the service project can use all shared subnets.
- If subnets are listed, the role is assigned on each listed subnet only.
- A host project itself uses `enable_shared_vpc_host_project`, and then `svpc_host_project_id` must not be set.

## 3. Factory pattern
Drive many projects from a declarative file (for example YAML read with `yamldecode`) so teams submit a pull request instead of HCL, and call the module with `for_each` over the decoded records. Validate the files in CI before `terraform plan`.

## Gotchas
- The README lists the identity running Terraform needs, among others, `roles/resourcemanager.projectCreator` and `roles/billing.user` on the organization, and for Shared VPC `roles/compute.xpnAdmin` and `roles/compute.networkAdmin` on the organization plus `roles/browser` and `roles/resourcemanager.projectIamAdmin` on the host project. Read the current README list before granting.
- `disable_services_on_destroy` defaults to true, so removing the module disables its services; set it false if that is not wanted.
- `random_project_id_length` lets you lengthen the suffix and is recommended for CI.
- `group_role` defaults to `roles/editor` for the controlling group, which is broad; set a narrower role.

## Verify
- [ ] The new project shows the intended folder, labels and billing account.
- [ ] The default compute service account has no Editor binding (default setting disables it).
- [ ] The project is attached to the intended Shared VPC host with only the intended subnets.

## Checked
2026-11-09. Confirmed in the module README on GitHub: input names and defaults (`random_project_id`, `default_service_account` values, `auto_create_network`, `lien`, `activate_apis`, `svpc_host_project_id`, `shared_vpc_subnets`, `budget_amount`, `budget_alert_spent_percents`, `disable_services_on_destroy`, `group_role`, `random_project_id_length`), the Shared VPC role logic and the required roles list. Removed: the pinned major version, submodule table (not on the README), the 30-day ID reuse claim, API/timeout advice, and gcloud verify commands. Terraform registry page returned an empty stub and was not used.
Method: documentation only; no commands were run.
