---
id: computing-software.data-engineering.data-warehouse-architecture.access-control-and-governance
name: access-control-and-governance
category: computing-software
field: data-engineering
product: data-warehouse-architecture
tags: [data-warehouse-architecture, rbac, row-level-security, column-level-security, dynamic-data-masking, least-privilege, data-governance, pii, gdpr, functional-roles, role-hierarchy, access-review, tag-based-masking]
level: practitioner
status: docs-checked
description: "Design role-based access control, row/column-level security and masking policies across a warehouse so least-privilege survives growth."
sources:
  - https://docs.snowflake.com/en/user-guide/security-access-control-overview
  - https://docs.databricks.com/en/data-governance/unity-catalog/index.html
  - https://docs.snowflake.com/en/user-guide/security-row-intro
  - https://docs.databricks.com/aws/en/tables/row-and-column-filters
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Warehouse access control that survives growth, not just launch

**Goal:** a permission model where adding the 500th user doesn't mean auditing 499 ad hoc grants, and where PII access is enforced by policy, not by trusting everyone to remember not to `SELECT *`.

## 1. Functional roles, not per-person grants
Grant privileges to **roles that represent a job function** (`analyst_finance`, `engineer_pipeline`, `bi_reader_marketing`), then assign people to roles. Snowflake describes the same model: privileges go to roles, roles are assigned to users or other roles, and granting a role to another role creates a hierarchy in which privileges are inherited by the roles above. The test: can you answer "who can read this PII column" by listing roles, in seconds? If not, the model has drifted to per-person grants.
- Snowflake recommends a hierarchy that ultimately assigns custom roles to SYSADMIN; a custom role outside that hierarchy cannot be managed by system administrators, only by roles with MANAGE GRANTS.
- Route urgent access through a role grant you can revoke on a deadline, not a permanent direct grant. How to automate expiry is platform-specific and was not checked here.
- Databricks Unity Catalog grants permissions on securable objects to users, service principals or groups, in a catalog.schema.object namespace; grant to groups.

## 2. Row-level security
Define a row access policy (Snowflake) or row filter (Databricks Unity Catalog) once on the table, mapping a role or attribute to the rows visible. This avoids per-region views or tables that drift from the source logic. Snowflake policies may use CURRENT_ROLE or a mapping table, but mapping tables can reduce performance; Databricks recommends ABAC policies for consistent filtering across many tables and simple UDFs for performance.
- **Gotcha:** an aggregate (for example `COUNT(*)`) run by a row-restricted role is correct for the rows that role sees, which can look wrong to someone expecting the company-wide total. Document policies where analysts will see them.
- Databricks row filters and column masks cannot be applied to a view.

## 3. Column-level security and masking
Column masks (Databricks: a SQL UDF returning the original or a masked value, one mask per column) and Snowflake masking policies let the column exist while returning redacted values to roles without privilege. Prefer a masking policy to separate masked and unmasked table copies, which drift. Databricks ABAC policies apply by governed tags at catalog or schema level, so new tagged tables are covered automatically; Unity Catalog also offers automatic data classification. Set up tag-driven policy before PII is scattered over hundreds of tables.

## 4. Governance process, not just technical controls
- **Periodic access review**: scheduled review of who has access to PII-bearing roles, with explicit sign-off, catches stale grants that no technical control prevents (someone changed teams). Choose a cadence that matches your risk.
- **PII inventory**: a maintained list of which columns hold regulated data is the prerequisite for tag-based masking and for answering "where is this data" quickly.
- Unity Catalog audit log system table and lineage help evidence who accessed what.

## Verify
- [ ] No table/schema privilege is granted directly to an individual user; every grant traces to a functional role or group.
- [ ] An emergency access grant was revoked on time; the revoke was tested.
- [ ] A row-level policy was checked against an aggregate query, not only `SELECT *`.
- [ ] Every PII-inventory column has an active masking or column-level policy.
- [ ] The last access review happened within the defined cadence and removed at least one stale grant.

## Checked
Date: 2026-11-09. Confirmed from the Snowflake access-control overview (roles, hierarchy, SYSADMIN and MANAGE GRANTS), the Snowflake row access policy page, the Databricks Unity Catalog overview (securables, access control, lineage, audit, classification) and the Databricks row-filter page (UDF filters and masks, ABAC, view limitation). Removed as unconfirmed: Snowflake temporary roles, BigQuery row and column policies, quarterly review cadence, tag-based masking details for Snowflake. Role-naming, access-review and PII-inventory points are practice guidance, not page claims.
Method: documentation only; no commands were run.
