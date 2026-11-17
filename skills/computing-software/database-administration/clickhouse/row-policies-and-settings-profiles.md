---
id: computing-software.database-administration.clickhouse.row-policies-and-settings-profiles
name: row-policies-and-settings-profiles
category: computing-software
field: database-administration
product: clickhouse
tags: [database-administration, clickhouse, row-policy, settings-profile, constraints, quota, precedence]
level: practitioner
status: docs-checked
description: "Restrict rows per user with row policies and cap resource use with settings profiles and constraints in ClickHouse."
sources:
  - https://github.com/ClickHouse/clickhouse-docs/blob/main/docs/guides/sre/user-management/index.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# row policies and settings profiles
Row policies filter which rows a user can read; settings profiles bundle settings and limits.
```sql
CREATE ROW POLICY region_eu ON db.sales FOR SELECT USING region = 'EU' TO ana;

CREATE SETTINGS PROFILE limited SETTINGS max_memory_usage = 10000000000 TO analyst;
```
A settings profile holds settings and constraints plus the roles and/or users it applies to.

Precedence at login, highest first: the user account's own settings, the settings of the user's default roles, the settings profiles assigned to the user or its default roles, then server-wide defaults or the default profile. If a setting is configured in several roles, or in several profiles, the order of application is undefined.

Gotcha from the guide: row policies are only meaningful when the user has read-only access. A user who can modify a table or copy partitions can bypass them, so combine the policy with strictly read-only grants.

Inspect with `SHOW POLICIES` and `SHOW CREATE ROW POLICY`.

## Checked
2026-11-03. Confirmed against the ClickHouse docs guide "Users and roles" (user-management): row policy definition and the read-only caveat, settings profile definition, the settings priority order, and the SHOW POLICIES statement. Removed: the MIN/MAX/READONLY constraint syntax and the claim that constraints cap a user, which that page does not show.
Method: documentation only; no commands were run.
