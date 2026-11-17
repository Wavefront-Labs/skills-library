---
id: sales-marketing.sales-management.crm-systems.pipeline-config-dashboards-and-data-hygiene
name: pipeline-config-dashboards-and-data-hygiene
category: sales-marketing
field: sales-management
product: crm-systems
tags: [crm-systems, crm, salesforce, hubspot, pipedrive, zoho-crm, dynamics-365, microsoft-dynamics, sales-pipeline, deal-stages, opportunity-stages, validation-rules, required-properties, dashboards, reports, data-hygiene, duplicates, deduplication, crm-adoption, field-governance, sales-ops, revops, sales-management]
level: practitioner
status: draft
description: "Run sales in a CRM (Salesforce, HubSpot, Pipedrive): configure pipeline stages and required fields, build the 5 dashboards managers need, keep data clean, and drive rep adoption."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Pipeline configuration, dashboards and data hygiene

**Goal:** a CRM that reflects reality — so forecasts, coaching and comp can run off it —
with the least data entry reps can get away with.

Menu paths below are approximate and change with releases/editions; confirm in your
vendor's current docs. Some features (validation rules, multiple pipelines) need paid tiers.

## 1. Configure the pipeline
- One pipeline per genuinely different sales motion (new business, renewals, partner) —
  not per rep or region.
- Stages and probabilities from your sales process (see
  sales-marketing.sales-management.sales-process-design.stage-exit-criteria-and-handoffs).
  - **Salesforce:** Setup › Object Manager › Opportunity › Fields › Stage (picklist values
    with default probability); *Sales Processes* tie stages to record types; *Path*
    shows guidance per stage.
  - **HubSpot:** Settings › Objects › Deals › Pipelines — edit stages, win probability and
    *conditional stage properties* (required properties when moving into a stage).
  - **Pipedrive:** Pipeline view › edit pipeline; stage probabilities; required fields
    via *Data fields* settings (plan-dependent).
- **Required at stage change:** 2–4 fields max (amount, close date, next step, decision-maker).
  Salesforce validation rule example:
  ```
  AND( ISPICKVAL(StageName, "Proposal"), ISBLANK(Next_Step_Date__c) )
  ```
  with an error message telling the rep what to fill in (custom field name is illustrative).

## 2. Field governance
- Keep a field dictionary: name, purpose, who owns it, picklist values.
- Prefer **picklists** over free text for anything you'll report on (loss reason, source).
- Archive unused fields quarterly; every field you add is data entry tax.

## 3. The five dashboards that matter
1. **Pipeline by stage and close period** (amount and count), by rep.
2. **Forecast:** commit / best case / pipeline vs target this period.
3. **Hygiene:** open deals with past close dates, no activity in 14+ days, missing amount.
4. **Conversion & velocity:** stage-to-stage conversion, win rate, average cycle length.
5. **Activity / leading indicators:** meetings and new opportunities created per rep per week.
Schedule them by email to managers weekly (both Salesforce and HubSpot support
dashboard subscriptions on most tiers).

## 4. Data hygiene routines
- **Duplicates:** turn on duplicate rules/matching (Salesforce: Duplicate Rules; HubSpot:
  Manage duplicates tool) and merge weekly. Standardise company names and domains.
- **Imports:** map fields in a test import of 10 rows first; set the dedupe key (email for
  contacts, domain for companies).
- **Monthly sweep:** close or update stale deals; fill missing owners; fix invalid stages.

## 5. Adoption
- "If it's not in the CRM, it didn't happen": forecasts, 1:1s and commissions run from CRM
  data only.
- Reduce friction: email/calendar sync, mobile app, auto-logging calls.
- Look at login and update reports per rep; low usage is a coaching conversation.

## Gotchas
- Changing stage picklist values renames history; plan carefully and snapshot reports first.
- Integrations (marketing automation, billing) can overwrite fields — set field-level sync rules.
- Over-engineered automation (dozens of workflows) becomes unmaintainable; document each one.
- Permissions: least privilege for exports; CRM data is personal data under privacy law.

## Verify
- [ ] Stages and probabilities match the written sales process.
- [ ] Required fields enforced at stage change; error messages are clear.
- [ ] The five dashboards exist and are emailed weekly.
- [ ] Duplicate rules on; hygiene dashboard trends toward zero.
- [ ] Forecast and comp are calculated from CRM data only.
