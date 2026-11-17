---
id: computing-software.cloud-infrastructure-engineering.google-cloud.managing-vpc-sc-perimeters-with-terraform
name: managing-vpc-sc-perimeters-with-terraform
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, vpc-service-controls, perimeter-terraform, vpc-sc-terraform, google-access-context-manager-service-perimeter, dry-run, infrastructure-as-code]
level: practitioner
status: gated
description: "Manage VPC Service Controls with Terraform: perimeter and access level resources, dry-run spec with use_explicit_dry_run_spec, resource membership patterns and safe apply order."
sources: ["https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/access_context_manager_service_perimeter", "https://github.com/terraform-google-modules/terraform-google-vpc-service-controls", "https://cloud.google.com/vpc-service-controls/docs/dry-run-mode"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Managing VPC-SC perimeters with Terraform

## Resources
```hcl
resource "google_access_context_manager_access_level" "corp" {
  parent = "accessPolicies/${var.policy_id}"
  name   = "accessPolicies/${var.policy_id}/accessLevels/corp_network"
  title  = "corp_network"
  basic { conditions { ip_subnetworks = ["<CORP_CIDR>"] } }
}

resource "google_access_context_manager_service_perimeter" "data" {
  parent = "accessPolicies/${var.policy_id}"
  name   = "accessPolicies/${var.policy_id}/servicePerimeters/data"
  title  = "data"
  use_explicit_dry_run_spec = true
  status {                          # enforced
    resources           = [for n in var.enforced_project_numbers : "projects/${n}"]
    restricted_services = ["storage.googleapis.com", "bigquery.googleapis.com"]
    access_levels       = [google_access_context_manager_access_level.corp.name]
  }
  spec {                            # dry run (candidate config)
    resources           = [for n in var.all_project_numbers : "projects/${n}"]
    restricted_services = ["storage.googleapis.com", "bigquery.googleapis.com", "secretmanager.googleapis.com"]
    access_levels       = [google_access_context_manager_access_level.corp.name]
    egress_policies { /* ... */ }
  }
}
```
Project **numbers**, not IDs. Promote by copying `spec` into `status` once dry-run logs are clean.

## Membership patterns
- Single perimeter resource owning `resources` (authoritative) vs
  `google_access_context_manager_service_perimeter_resource` (adds one project; used by project
  factories) (gated: unconfirmed, source is paywalled or blocked). Do not mix both for the same perimeter or they fight; if using the per-resource
  resource, add `lifecycle { ignore_changes = [status[0].resources] }` on the perimeter.
- A dry-run counterpart for `spec` membership may exist: check the provider docs (gated: unconfirmed, source is paywalled or blocked).

## Apply safely
- Perimeter changes are not instant; apply enforced changes in a maintenance window.
- The Terraform runner itself must be allowed (ingress rule or access level for its identity/network),
  or the next plan fails reading restricted APIs.
- A plural `google_access_context_manager_service_perimeters` resource replaces all perimeters at once; use it only if one team owns everything (gated: unconfirmed, source is paywalled or blocked).

## Verify
- [ ] `terraform plan` clean after apply; dry-run violations query empty before promotion.

## Checked
2026-10-28. Confirmed: VPC Service Controls dry-run mode page (dry-run configuration vs enforced configuration) and the terraform-google-vpc-service-controls module page was readable.
Gated: Terraform registry pages for the provider resources returned empty text, so the resource names `..._service_perimeter_resource`, the dry-run resource and the plural perimeters resource are unconfirmed.
Removed: the 30-minute propagation figure and a documentation IP range.
Method: documentation only; no commands were run.
