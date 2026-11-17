---
id: computing-software.data-engineering.snowflake.managing-snowflake-with-terraform
name: managing-snowflake-with-terraform
category: computing-software
field: data-engineering
product: snowflake
tags: [snowflake, snowflake-terraform, terraform, snowflakedb-provider, infrastructure-as-code, grants, warehouses, rbac]
level: advanced
status: draft
description: "Manage Snowflake account objects with the snowflakedb/snowflake Terraform provider: auth, warehouses, databases, roles and grants, importing existing objects, and safe plans."
sources:
  - https://registry.terraform.io/providers/snowflakedb/snowflake/latest/docs
  - https://docs.snowflake.com/en/user-guide/terraform
  - https://github.com/snowflakedb/terraform-provider-snowflake/blob/main/MIGRATION_GUIDE.md
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Managing Snowflake with Terraform

**Goal:** warehouses, databases, roles, users and grants are code-reviewed and reproducible; ad hoc console changes become visible drift.

Scope split that works: Terraform for account-level and access objects; dbt/schemachange for tables and views.

## Provider and auth
```hcl
terraform {
  required_providers {
    snowflake = { source = "snowflakedb/snowflake", version = "~> 2.0" }
  }
}
provider "snowflake" {
  organization_name = "MYORG"
  account_name      = "PROD"
  user              = "SVC_TERRAFORM"
  role              = "SYSADMIN"
  authenticator     = "SNOWFLAKE_JWT"
  private_key       = file(var.private_key_path)
}
# second aliased provider for SECURITYADMIN-owned objects (roles, grants, users)
provider "snowflake" {
  alias             = "security"
  organization_name = "MYORG"
  account_name      = "PROD"
  user              = "SVC_TERRAFORM"
  role              = "SECURITYADMIN"
  authenticator     = "SNOWFLAKE_JWT"
  private_key       = file(var.private_key_path)
}
```
The provider moved from `Snowflake-Labs/snowflake` to `snowflakedb/snowflake`; 1.0+/2.0 renamed many resources. Follow the migration guide when upgrading.

## Core resources
```hcl
resource "snowflake_warehouse" "transform" {
  name                = "TRANSFORM_WH"
  warehouse_size      = "MEDIUM"
  auto_suspend        = 60
  auto_resume         = true
  initially_suspended = true
}
resource "snowflake_database" "sales" {
  name                        = "SALES"
  data_retention_time_in_days = 7
}
resource "snowflake_account_role" "analyst" {
  provider = snowflake.security
  name     = "ANALYST"
}

resource "snowflake_grant_privileges_to_account_role" "analyst_wh" {
  provider          = snowflake.security
  account_role_name = snowflake_account_role.analyst.name
  privileges        = ["USAGE"]
  on_account_object {
    object_type = "WAREHOUSE"
    object_name = snowflake_warehouse.transform.name
  }
}
resource "snowflake_grant_privileges_to_account_role" "analyst_future_tables" {
  provider          = snowflake.security
  account_role_name = snowflake_account_role.analyst.name
  privileges        = ["SELECT"]
  on_schema_object {
    future {
      object_type_plural = "TABLES"
      in_database        = snowflake_database.sales.name
    }
  }
}
resource "snowflake_grant_account_role" "analyst_to_sysadmin" {
  provider         = snowflake.security
  role_name        = snowflake_account_role.analyst.name
  parent_role_name = "SYSADMIN"
}
```

## Importing existing objects
```bash
terraform import snowflake_warehouse.transform '"TRANSFORM_WH"'
```
Or Terraform 1.5+ `import {}` blocks plus `terraform plan -generate-config-out=gen.tf`. Plan must show **no changes** after import before you trust it.

## Safe practices
- Separate states per environment/account; least-privilege service user per state.
- `prevent_destroy` lifecycle on databases holding data.
- Review plans for `-/+` (replace) on databases/schemas: replacement = drop + create = data loss (Time Travel may save you).
- Grants: avoid managing the same grant both in Terraform and manually/dbt (`grants` config), or they fight.

## Gotchas
- Identifiers are case-sensitive in quotes; keep names uppercase unquoted-style.
- Some parameters show perpetual diffs when Snowflake normalises values; pin provider versions and check known issues.
- `ACCOUNTADMIN` for Terraform is tempting and dangerous; use SYSADMIN/SECURITYADMIN split.

## Verify
- [ ] `terraform plan` on main is clean (no drift) daily in CI.
- [ ] Destroy-protected resources cannot be removed by a plan.
