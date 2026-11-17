---
id: computing-software.data-engineering.databricks.terraform-provider-for-workspace-infrastructure
name: terraform-provider-for-workspace-infrastructure
category: computing-software
field: data-engineering
product: databricks
tags: [databricks, databricks-terraform, terraform, infrastructure-as-code, unity-catalog]
level: advanced
status: docs-checked
description: "Manage Databricks account and workspace infrastructure with the Terraform provider: auth, account vs workspace providers, UC objects, policies, and where bundles fit."
sources:
  - https://docs.databricks.com/aws/en/dev-tools/terraform/
  - https://github.com/databricks/terraform-provider-databricks/tree/main/docs
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Terraform provider for Databricks infrastructure

**Goal:** workspaces, Unity Catalog objects, permissions and compute policies defined as code and reviewed in PRs.

## Providers
```hcl
terraform {
  required_providers { databricks = { source = "databricks/databricks" } }  # pin a version in real use
}
provider "databricks" {                 # account level
  alias      = "account"
  host       = "https://accounts.cloud.databricks.com"
  account_id = var.account_id
}
provider "databricks" {                 # workspace level
  alias = "ws"
  host  = var.workspace_url
}
```
Auth via service principal OAuth: `client_id` / `client_secret` provider arguments or env `DATABRICKS_CLIENT_ID` / `DATABRICKS_CLIENT_SECRET`. The provider docs strongly recommend OAuth over personal access tokens. `account_id` is required for account-level operations only: do not set it on a workspace-level provider (it causes invalid-account-configuration errors). The account host on AWS is `https://accounts.cloud.databricks.com`.

## Typical resources
```hcl
resource "databricks_catalog" "sales" {
  provider = databricks.ws
  name     = "sales"
  storage_root = "s3://acme-uc/sales"
}
resource "databricks_grants" "sales" {
  provider = databricks.ws
  catalog  = databricks_catalog.sales.name
  grant {
    principal = "data-engineers"
    privileges = ["USE_CATALOG", "CREATE_SCHEMA"]
  }
  grant {
    principal = "analysts"
    privileges = ["USE_CATALOG", "SELECT"]
  }
}
resource "databricks_cluster_policy" "jobs" {
  provider   = databricks.ws
  name       = "jobs-standard"
  definition = jsonencode({ "autotermination_minutes" = { type = "fixed", value = 30 } })
}
```
Account level: `databricks_mws_workspaces`, `databricks_metastore`, `databricks_metastore_assignment`, account groups/service principals.

## Split of responsibilities
- Terraform: Databricks recommends it for cloud-level and external resources and admin actions such as workspace provisioning and cloud networking. The provider also has resources for metastores, catalogs, grants and cluster policies, as above.
- Declarative Automation Bundles (formerly Asset Bundles): Databricks recommends them for jobs, pipelines, notebooks and other Databricks resources; keep per-project resources out of the platform repo.

## Gotchas
- `databricks_grants` is authoritative for all grants on that securable: it overwrites existing grants and resets changes made outside Terraform. `databricks_grant` (singular) is authoritative only for one principal on the securable, and also overwrites that principal's existing grants. Neither is purely additive.
- Importing existing objects: use `terraform import` before managing them, to avoid recreation.
- A metastore without `storage_root` requires each catalog to define one; the provider docs recommend defining `storage_root` at catalog level.

## Verify
`terraform plan` is empty after apply; a UI-made grant is reset to the Terraform-declared state on the next apply.

## Checked
Date: 2026-11-09. Confirmed against the Databricks Terraform provider docs (docs/index.md, grants, grant, catalog, cluster_policy, metastore, mws_workspaces on the provider's GitHub repo) and the Databricks page Databricks Terraform provider. Fixed: the additive claim about databricks_grant (it is authoritative per principal). Removed: the version pin, the claim that bundles use Terraform internally, the "Never personal tokens in CI" line (replaced by the docs' OAuth recommendation), the claim that data sources are needed before import. The registry page itself returned empty text; the repo docs were read instead. Not verified: the `autotermination_minutes` policy example beyond the attribute appearing in the cluster_policy doc, and the databricks_metastore_assignment details.
Method: documentation only; no commands were run.
