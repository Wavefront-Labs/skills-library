---
id: computing-software.cloud-infrastructure-engineering.google-cloud.migrating-from-deployment-manager
name: migrating-from-deployment-manager
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, infrastructure-as-code, deployment-manager-migration, dm-convert, terraform-import, infrastructure-manager]
level: advanced
status: docs-checked
description: "Move Deployment Manager deployments to Terraform or Infrastructure Manager after support ended (1 April 2026): DM Convert, imports, abandoning DM ownership, no-op plans."
sources: ["https://docs.cloud.google.com/deployment-manager/docs/dm-convert", "https://docs.cloud.google.com/deployment-manager/docs/deprecations", "https://developer.hashicorp.com/terraform/language/import", "https://deploymentmanager.googleapis.com/$discovery/rest?version=v2"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Migrating from Deployment Manager

Google Cloud discontinued support for Deployment Manager on 1 April 2026 (per Google's deprecation page). The service keeps running until 30 June 2027 and is then turned down; existing resources keep working but cannot be managed with `gcloud deployment-manager`. Migrate to Infrastructure Manager (Terraform), self-run Terraform, or KRM/Config Connector.

## 1. Inventory
```bash
gcloud deployment-manager deployments list
gcloud deployment-manager manifests describe --deployment=<DEP> --format='value(expandedConfig)' > expanded.yaml
gcloud deployment-manager resources list --deployment=<DEP>
```
Use the **expanded** config (templates rendered) as conversion input.

## 2. Convert with DM Convert
DM Convert (Preview) is a tool you run locally; it converts Deployment Manager YAML and Jinja or Python templates to Terraform or KRM. Check the DM Convert docs for the install steps and current flags. `--list-supported-types` shows which type providers and resource types are supported, and `--opt_out_data_collection=true` turns off its default anonymous usage reporting.
Before converting, reconcile active deployments so resources are up to date. Review the output: hard-coded values and naming. Not converted: composite types, custom type providers, outputs, and Actions without a declarative Terraform equivalent (patch, delete and list APIs, custom APIs).

## 3. Import live resources
Verify the generated Terraform reflects the live resources, then add `import` blocks (see the Terraform import docs for the version that introduced them), e.g.
```hcl
import {
  to = google_compute_network.vpc
  id = "projects/<P>/global/networks/prod-vpc"
}
```
`terraform plan` must show **0 to add/change/destroy** apart from imports. Fix drift in code, not in the cloud.

## 4. Detach from DM
Delete the DM deployment **with abandon** so resources survive:
```bash
gcloud deployment-manager deployments delete <DEP> --delete-policy=ABANDON
```
Then `terraform apply` the imports. Google also recommends keeping Terraform state in a Cloud Storage bucket.

## Gotchas
- Deleting without `--delete-policy=ABANDON` destroys the resources.
- DM Convert maps authoritative `accessControl` bindings to `<resource_type>_iam_policy` and non-authoritative `iamMemberBinding` to `<resource_type>_iam_member`; setIamPolicy actions become `_iam_policy` or `_iam_member` depending on whether getIamPolicy is used. Prefer `_iam_member` unless you mean to own the whole policy.
- Resources created by DM templates via Python logic or custom type providers may need hand-written Terraform.

## Verify
- [ ] DM deployment list no longer shows it; `terraform plan` is a no-op; resource IDs and creation timestamps unchanged.

## Checked
2026-10-31. Confirmed in the Deployment Manager deprecation page and DM Convert page: 1 April 2026 end of support, 30 June 2027 turn-down, Infra Manager as the target, Terraform and KRM outputs, `--list-supported-types`, `--opt_out_data_collection`, unsupported items, IAM mapping, abandon on delete, state-in-Cloud-Storage advice; in the Deployment Manager v2 discovery document (`Manifest.expandedConfig`); and the four gcloud commands via check_commands. Removed: the container image invocation and its flags, `--output_format TF/KRM` values, and the Terraform 1.5 version claim (the migrate-to-terraform page returned 404).
Method: documentation only; no commands were run.
