---
id: computing-software.data-engineering.databricks.system-access-audit-queries
name: system-access-audit-queries
category: computing-software
field: data-engineering
product: databricks
tags: [databricks, system-access-audit, audit-logs, system-tables, security-monitoring]
level: advanced
status: docs-checked
description: "Investigate Databricks activity with system.access.audit: schema, discovering action names, table access and failure queries, masking."
sources:
  - https://docs.databricks.com/aws/en/admin/system-tables/audit-logs
  - https://docs.databricks.com/aws/en/admin/account-settings/audit-log-delivery
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# system.access.audit queries

**Goal:** answer security and compliance questions with SQL over the audit log system table.

## Shape
Key columns: `event_time`, `event_date`, `workspace_id`, `service_name`, `action_name`, `user_identity.email`, `request_params` (map), `response` (struct with `statusCode` and `errorMessage` in the documented example), `source_ip_address`, `user_agent`, `session_id`, `audit_level`, `identity_metadata` (`run_by`, `run_as`). The table is in Public Preview; account-level events record `workspace_id` as 0.

## Queries
```sql
-- discover which actions a service emits (do this before writing filters)
SELECT action_name, count(*) FROM system.access.audit
WHERE service_name = 'unityCatalog' AND event_date >= current_date() - 7
GROUP BY 1 ORDER BY 2 DESC;

-- failed requests by source IP
SELECT source_ip_address, service_name, action_name, count(*) FROM system.access.audit
WHERE response.statusCode <> 200 AND event_date >= current_date() - 7
GROUP BY ALL ORDER BY 4 DESC;

-- who read a sensitive table (UC access events)
SELECT event_time, user_identity.email, action_name
FROM system.access.audit
WHERE service_name = 'unityCatalog'
  AND request_params.full_name_arg = 'main.hr.salaries'
  AND event_date >= current_date() - 30;
```

## Practice
- Filter on `event_date` (partition column) for speed.
- Build Databricks SQL alerts on queries over the actions you care about, once you have confirmed their `action_name` values from sample rows.
- Audit log delivery writes JSON files per workspace, plus one for account-level events, to an S3 bucket if you need the logs outside the system table.
- Deleting a workspace removes that workspace's audit events older than 14 days from the system table.

## Gotchas
- `request_params` keys differ by action; inspect sample rows before writing filters.
- Keys holding SQL definitions (`function_info`, `view_definition`, `definition_json`, `managed_definition`) are omitted unless you are an account admin or in the `databricks_pii_access` group.
- Querying from dedicated access mode compute needs Databricks Runtime 15.4 LTS or above and a serverless-enabled workspace.
- Most audit logs are only available in the region of the workspace.

## Verify
Perform a test action (for example read the sensitive table); it appears in the table-access query.

## Checked

2026-11-09. Confirmed on the Databricks audit log system table reference and audit log delivery pages: table path, columns and types, event_date filter advice, workspace_id 0 for account-level events, 14-day removal on workspace deletion, request_params masking keys and databricks_pii_access, dedicated compute requirements, full_name_arg key and unityCatalog service name in the schema example, delivery of JSON files to S3. Removed: updatePermissions, login action names, securable_* parameter keys, lineage tables, enabling system schemas and alert examples (none on the pages read).

Method: documentation only; no commands were run.

