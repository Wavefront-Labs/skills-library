---
id: computing-software.data-engineering.data-warehouse-architecture.data-policy-as-code
name: data-policy-as-code
category: computing-software
field: data-engineering
product: data-warehouse-architecture
tags: [data-warehouse-architecture, policy-as-code, opa, rego, access-policy-automation, terraform-grants, data-contracts-enforcement]
level: practitioner
status: verified
description: "Enforce data governance policies as code: OPA/Rego and conftest checks on dbt and IaC, warehouse grants and masking in Terraform, CI gates for tags and contracts."
sources:
  - https://www.conftest.dev/
  - https://github.com/open-policy-agent/conftest/releases
  - https://docs.getdbt.com/reference/artifacts/manifest-json
  - https://github.com/snowflakedb/terraform-provider-snowflake/blob/main/docs/resources/masking_policy.md
  - https://github.com/dbt-checkpoint/dbt-checkpoint
licence: Apache-2.0
version: 4
updated: 2026-11-17
---
# Policy as code

Policies written in documents drift from reality. Encode them as checks and declarative configuration that run in CI and on the platform.

## What to encode
| Policy | Implementation |
|---|---|
| Every model has an owner and classification | dbt `meta` required, CI check |
| PII columns must be masked | tags + tag-based masking policies managed in Terraform |
| No public buckets / sharing of restricted data | OPA on Terraform plans, cloud org policies |
| Access only via roles, not users | grants in Terraform; drift detection |
| Data contracts (schema, freshness) | contract tests in CI and on ingestion |
| Retention | lifecycle rules and scheduled purge jobs as code |

## CI checks on dbt metadata (conftest)
```bash
dbt parse && jq -c '.nodes | map(select(.resource_type=="model"))' target/manifest.json > models.json
conftest test models.json -p policy/
```
Conftest evaluates each element of a top-level JSON array as its own document, so the rules read `input` as ONE model, not as a list (a rule that loops `input[_]` silently passes). Conftest 0.71.1 defaults to Rego v1 (`--rego-version v0` restores the old syntax), which requires `contains` and `if`:
```rego
package main

deny contains msg if {
  not input.meta.owner
  msg := sprintf("%s: missing meta.owner", [input.name])
}

deny contains msg if {
  some c in input.columns
  c.meta.pii == true
  not c.meta.masking_policy
  msg := sprintf("%s.%s is PII but has no masking_policy", [input.name, c.name])
}
```
Run end to end here (dbt-duckdb 1.12.6 project with `meta: {pii: true}` on a column; jq `map` over the `.nodes` object works; conftest 0.71.1): output was `FAIL - models.json - main - orders.email is PII but has no masking_policy` and `FAIL ... orders: missing meta.owner`, `2 tests, 0 passed, 2 failures`. Model- and column-level `meta` appear in the manifest as `.meta` and `.columns.<name>.meta`.
Alternatives: dbt-checkpoint pre-commit hooks (`check-model-has-meta-keys` exists in its hook list), dbt-project-evaluator (its current README is for a version that requires dbt 2.0+; the 1.x branch is for dbt 1).

## Warehouse access as code
Resource and argument names below match the terraform-provider-snowflake docs (`snowflake_masking_policy`, `snowflake_grant_privileges_to_account_role` with `on_schema_object { all { ... } }`); not applied here (no Snowflake account or Terraform).
```hcl
resource "snowflake_masking_policy" "email" {
  name     = "MASK_EMAIL"
  database = "GOVERNANCE"
  schema   = "POLICIES"
  argument {
    name = "VAL"
    type = "VARCHAR"
  }
  body             = "CASE WHEN IS_ROLE_IN_SESSION('PII_READER') THEN VAL ELSE '***' END"
  return_data_type = "VARCHAR"
}
resource "snowflake_grant_privileges_to_account_role" "analyst_read" {
  account_role_name = "ANALYST"
  privileges        = ["SELECT"]
  on_schema_object {
    all {
      object_type_plural = "TABLES"
      in_schema = "\"ANALYTICS\".\"MARTS\""
    }
  }
}
```
Same idea for BigQuery IAM and policy tags, Databricks Unity Catalog grants (Terraform provider), Lake Formation permissions.

## Policy checks on infrastructure plans
Conftest/OPA or Sentinel over `terraform show -json`: block storage without encryption, public ACLs, data stores in non-approved regions (residency).

## Runtime enforcement
- Query-time: masking/row access policies, Unity Catalog ABAC, Immuta/Privacera-style policy engines evaluating user attributes.
- Detect drift: nightly job comparing actual grants to code (Terraform plan with no changes expected), alerting on manual grants.

## Auditability
Policies in Git give history, review and approval; CI logs prove the checks ran; exceptions are explicit (allowlist file with owner and expiry) rather than silent.

## Verify
- [ ] A PR adding a PII column without masking fails CI with a clear message.
- [ ] Nightly drift check shows zero grants outside Terraform.
