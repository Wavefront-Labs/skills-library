---
id: computing-software.it-support-helpdesk.servicenow.import-sets-and-transform-maps
name: import-sets-and-transform-maps
category: computing-software
field: it-support-helpdesk
product: servicenow
tags: [it-support-helpdesk, servicenow, import-sets, transform-maps, coalesce, data-load, bulk-update, data-source]
level: advanced
status: gated
description: "Load bulk data into ServiceNow safely with import sets: data sources, transform maps, coalesce fields, transform scripts, testing on sub-prod, and cleaning up a bad load."
sources:
  - "https://www.servicenow.com/docs/bundle/zurich-integrate-applications/page/script/server-scripting/concept/c_ImportSets.html"
  - "https://www.servicenow.com/docs/bundle/zurich-integrate-applications/page/script/server-scripting/concept/c_CreatingATransformMap.html"
  - "https://www.servicenow.com/docs/bundle/zurich-integrate-applications/page/script/server-scripting/concept/c_Coalesce.html"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# import-sets-and-transform-maps

Support admins use import sets to bulk-load users' devices, assignment group members,
locations, KB articles or a vendor's asset list. The data lands in a staging table first,
then a transform map writes it to the target table.

Claims in this skill were not verified against primary documentation (gated: unconfirmed, source is paywalled or blocked).

## Steps
1. **Load data**: System Import Sets > Load Data. Upload CSV/Excel (or define a Data
   Source for scheduled JDBC/LDAP/REST/file loads). Creates staging table `u_imp_...`
   with columns from the headers.
2. **Transform map**: source = staging table, target = e.g. `cmdb_ci_computer`. Use
   **Auto map matching fields**, then fix field maps manually.
3. **Coalesce**: tick coalesce on the unique key(s) (serial number, email, asset tag).
   Match found -> update; none -> insert. No coalesce = every run inserts duplicates.
4. Reference fields: map the display value (e.g. user email) and set **Referenced value
   field name** (e.g. `email`) so it resolves to the right sys_id; choose "Choice action"
   reject/ignore for unknown choice values.
5. **Run transform**; review the import set row states (Inserted, Updated, Ignored,
   Error) and the import log.

## Transform scripts (when field maps aren't enough)
- `onBefore`: `if (!source.u_serial) { ignore = true; }` to skip bad rows.
- `onAfter`: create relationships, set related records.
- Field map script for formatting (trim, case, date parsing with a set date format).

## Safety
- Always load to sub-production first and compare counts.
- Back up: export the target rows (XML) before a bulk update.
- **Run business rules** checkbox on the transform map: off for pure data loads to avoid
  notifications and workflows firing; on if you rely on them (e.g. user creation flows).
- Date formats in the CSV must match the field map's date format, or values import blank.

## Cleaning up a bad load
- Import Set > related list of target records; or filter target table by `sys_import_set`
  / `sys_created_on` window and created by your user.
- Rollback: newer releases support Import Set **rollback** for inserted/updated records
  if the transform had rollback enabled (Rollback contexts); otherwise restore from the
  XML export.
- Staging tables are cleaned by the Import Set Deleter scheduled job (default 7 days).

## Verify
Row counts: CSV rows = inserted + updated + ignored + errors; spot-check 10 records on
the target including references; a second run of the same file shows only Updated/Ignored.

## Checked

- Date: 2026-11-01. Reason: every cited source is paywalled, login-gated or blocked to automated readers (servicenow.com); no readable alternative was found.

Method: documentation only; no commands were run.
