---
id: computing-software.data-science-and-analytics.apache-superset.row-level-security
name: row-level-security
category: computing-software
field: data-science-and-analytics
product: apache-superset
tags: [row-level-security, rls, base-filter, group-key, rls-in-sqllab]
level: advanced
status: docs-checked
description: "Restrict Superset rows with RLS filters: Regular versus Base types, group keys combining OR and AND, virtual datasets, RLS_IN_SQLLAB and the audit API."
sources:
  - https://github.com/apache/superset/blob/master/docs/admin_docs/security/security.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: show each audience only its rows.

Row Level Security filters (Security menu) are assigned to a dataset and a set of subjects (roles, and users or groups). The clause is arbitrary text added to the generated SQL WHERE clause, for example `department = "finance"` assigned to the Finance role, `date_field > DATE_SUB(NOW(), INTERVAL 30 DAY)` or `client_id = 6 AND advertiser="foo"`. Clauses support Jinja when `ENABLE_TEMPLATE_PROCESSING` is on, for example `user_id = '{{ current_username() }}'`.

Filter types:
- **Regular**: applied when the querying user matches one of the filter's subjects.
- **Base**: applied to everyone except the matching subjects; a default restriction that privileged subjects are exempt from. Example: clause `1 = 0` with the Admin role subject hides all rows from everyone but Admin (deny by default).

Group keys: filters sharing a group key are combined with OR; different keys are combined with AND; a filter with no key is its own group and is always AND'd. Example: F1 `department = 'Finance'` and F2 `department = 'Marketing'` (key `department`) with F3 `region = 'Europe'` (key `region`) give `(department = 'Finance' OR department = 'Marketing') AND (region = 'Europe')`. Alternatives without a shared key, such as `client_id = 4` and `client_id = 5`, AND into an empty result.

Virtual datasets: filters are assigned to datasets, not tables. A filter on a virtual dataset is applied to the outer query and must reference the virtual dataset's output columns; filters on the physical datasets referenced in its SQL are injected into the inner subquery, so you generally need not duplicate them.

SQL Lab: RLS is enforced only when the `RLS_IN_SQLLAB` feature flag is enabled; predicates are then injected for tables with datasets that have RLS filters.

Auditing: a lock badge appears next to datasets in the list and in Explore, but it is a visibility aid only. For exact answers use the API (needs `can_read` on the Row Level Security resource): `GET /api/v1/rowlevelsecurity/`, `GET /api/v1/rowlevelsecurity/<id>`, or filter the list with Rison queries on `tables` or `subjects` (`opr:rel_m_m`). The response includes name, `filter_type`, `clause`, `group_key`, tables and subjects.

## Checked

2026-11-08: read the Row Level Security section of security.mdx (lines 303-374) in full; the rest of the 50k-character page (authentication, roles, other sections) was not read. Removed claims not in that section: "test by impersonating a user", least-privilege database accounts, and guest-token RLS.
Method: documentation only; no commands were run.
