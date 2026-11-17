---
id: computing-software.data-engineering.metabase.row-and-column-security
name: row-and-column-security
category: computing-software
field: data-engineering
product: metabase
tags: [row-level-security, column-security, sandboxing, user-attributes, custom-policy]
level: sme
status: docs-checked
description: "Apply Metabase row and column security policies: row-level versus custom policies, exact-match user attributes, required SQL variables, and the bypass paths that leak data."
sources:
  - https://www.metabase.com/docs/latest/permissions/row-and-column-security
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Availability: Pro and Enterprise. Formerly called data sandboxing.

Mechanics: a policy is a filtered version of a table that replaces the original table everywhere it is used in Metabase, plus the group that sees it. You can define up to one policy per table and group combination. Row-level policies filter one column against a user attribute. Custom policies use a saved SQL question and can filter on multiple columns, restrict columns and edit columns.

Setup (row-level): Admin > Permissions, pick the database and table, set the group's View data to "Row and column security", then choose the column and the user attribute key. Custom: choose "Use a saved question to create a custom view for this table"; keep the SQL question in an admin-only collection (No access for all groups except Administrators). Prefer a SQL question over a query-builder question, which can pull in data from other questions or models.

Requirements:
- User attributes are required for row security and optional for column security. The attribute value must exactly match the filter value, case sensitive, or the person gets an empty result.
- SQL variables used for row restriction must be required (an optional `[[...]]` clause does not work) and be text, number or date. Map the variable to a user attribute key, not a value.
- Edited columns must return the same number of columns and matching types as the original table; you cannot add columns.

Gotchas and limits:
- A person in two groups with policies on the same table gets an error. Fix by leaving one group, or setting all but one group's View data access to Blocked.
- Policies are limited to the query builder: you cannot set native query permissions for groups with row and column security. To enforce row-level rules in the native editor, the page points to impersonation.
- SQL questions always use the original tables. The docs say "You cannot secure the rows or columns of SQL results", so put them in collections with No access for the secured groups.
- Public links and public dashboards bypass policies; the page says to disable public sharing to prevent that. Alerts and dashboard subscriptions created by unsecured people can also expose data.
- People under a policy cannot create Slack alerts or subscriptions (email still works) or run actions on that database; public action forms do not check row and column security.
- MongoDB and Druid support row-level security only.
- Advanced types (enums, arrays) need casting in a SQL question, a database view, or a transform; the original table must also be blocked for the view and transform options.

## Checked
Method: 2026-11-08 read the cited Metabase row-and-column-security page in full (raw docs source). Corrected the native-query claim (permissions cannot be set, rather than "bypass"), and added the setup, conflict-resolution and action/public-form points; remaining claims confirmed unchanged.
