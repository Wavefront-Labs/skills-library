---
id: computing-software.data-engineering.data-warehouse-architecture.reverse-etl
name: reverse-etl
category: computing-software
field: data-engineering
product: data-warehouse-architecture
tags: [data-warehouse-architecture, data-serving, reverse-etl, hightouch, census, operational-analytics, crm-sync, api-rate-limits, diff-based-sync]
level: practitioner
status: docs-checked
description: "Sync warehouse models back into operational tools (CRM, ads, support): sync models, record matching, diff-based upserts, rate limits, failures, ownership."
sources:
  - https://docs.hightouch.com/getting-started/concepts
  - https://docs.hightouch.com/syncs/overview
  - https://developer.salesforce.com/docs/platform/api-asynch/guide/asynch-api-intro.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Reverse ETL

**Goal:** push trusted warehouse data (scores, segments, account health) into tools people work in, reliably, without hammering their APIs or overwriting what humans entered.

## 1. Build a dedicated sync model
- One model per destination object: `rev_etl.salesforce_account_updates` with exactly the destination fields, already typed and formatted to what the destination accepts (picklist values, date and phone formats: check the destination's docs).
- Every model needs a unique primary key so each row can be identified and changes tracked between syncs (Hightouch requires one).
- Include the **matching key** the destination uses to find the right record (for a CRM, its record ID or an external ID field; for ad platforms, whatever identifier and hashing the platform documents).
- Keep it narrow: only fields the warehouse owns. Never sync a field that users also edit in the tool unless you agree who wins.

## 2. Diff-based syncing
Tools (Hightouch uses change data capture, comparing the current result with the previous run; or a home-grown job) send only added, changed and removed rows. The first run usually adds every row. Hightouch compares against the immediately previous run only, so it cannot delete records that left your source before the run.
Home-grown equivalent:
```sql
-- rows that changed since the last successful sync
SELECT c.* FROM rev_etl.account_updates c
LEFT JOIN rev_etl._last_synced l USING (account_id)
WHERE l.account_id IS NULL OR l.row_hash <> c.row_hash;
```
Update `_last_synced` only for rows the destination accepted.

## 3. Sync modes
Hightouch sync modes are insert, update, upsert and archive; available modes depend on the destination.
| Mode | Effect |
|---|---|
| Upsert | create or update by key — most common |
| Update | never create records (e.g. only enrich existing CRM accounts) |
| Insert | events (e.g. conversions to ad platforms); a full resync can create duplicates on insert-mode, event and webhook syncs |
Separately, a **delete behavior** setting decides what happens when a record leaves the model: do nothing, clear the mapped fields, or delete the destination record. Deleting mirrors the source and is dangerous on a CRM: use it for audiences, not systems of record.

## 4. Destination limits and failures
- Respect each destination's API quotas and batch sizes (see its docs). Salesforce suggests Bulk API 2.0 for operations over 2,000 records and synchronous bulkified REST or SOAP calls below that; Bulk API is asynchronous with no SLA. Schedule big syncs off-peak.
- Expect per-row rejections (validation rules, invalid picklist, locked record). Hightouch marks a run "completed with errors" and lists rejected rows with the destination's error message; capture row ID and error in any tool, alert on rejection rate, and retry only transient errors.
- First run of a new sync = full load; test a single row, and dry-run on a sandbox org first (Hightouch can send a single test row where the destination supports it).
- Field-level ownership: document in the destination (field help text "Managed by data team sync — edits are overwritten").

## 5. Operate it like a pipeline
- Trigger the sync after the dbt model builds (orchestrator or tool's dbt integration), not on an unrelated clock.
- Test the model (unique key, not null, accepted values) before it syncs — bad data reaches salespeople within minutes.
- Track: rows sent, rejected, duration, last success; owner per sync.

## Verify
- [ ] Sync model key is unique and not null (dbt tests).
- [ ] Rejected-row rate is visible and below threshold.
- [ ] No sync uses mirror/delete mode on a system of record without sign-off.
- [ ] API usage stays below the destination quota with headroom.

## Checked
2026-11-08: Read in full the Hightouch concepts page, the Hightouch syncs overview and the Salesforce Bulk API 2.0 introduction. Confirmed: models need a unique primary key, CDC diffing against the previous run, modes insert/update/upsert/archive, delete-behavior options, rejected-row handling, test-row feature, triggering by dbt Cloud/Airflow/cron, Bulk API threshold of 2,000 records and asynchronous no-SLA behavior. Removed: the Census source (redirects to a Fivetran page with no relevant content), the ">~10k rows" threshold, HubSpot rate-limit figure, SHA-256 hashing recipe, E.164 phone format and the "Mirror / all" mode name (not on the pages). The home-grown diff SQL and operating advice are method, not vendor claims.
Method: documentation only; no commands were run.
