---
id: computing-software.cloud-infrastructure-engineering.google-cloud.estimating-and-controlling-data-access-log-volume
name: estimating-and-controlling-data-access-log-volume
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, cloud-audit-logs, data-access-log-volume, audit-log-cost, data-access-logs, log-ingestion-cost, exclusion-filters]
level: practitioner
status: docs-checked
description: "Enable Data Access audit logs deliberately: log types, hierarchy rules, exempted principals and _Default sink exclusions to control volume and cost."
sources: ["https://docs.cloud.google.com/logging/docs/audit/configure-data-access", "https://cloud.google.com/products/observability/pricing", "https://docs.cloud.google.com/logging/docs/routing/overview"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Estimating and controlling Data Access log volume

Data Access audit logs are disabled by default for all services except some BigQuery services. Google warns the
volume can be large and may increase your logging charges (see the Cloud Logging section of the Google Cloud
Observability pricing page for the current ingestion rate and monthly free allotment per project).

## Estimate first
1. Enable the types you want in one representative project for a day or two.
2. Measure the volume of `log_id("cloudaudit.googleapis.com/data_access")` entries in Logs Explorer or with
   Cloud Logging usage metrics, by service.
3. Multiply by the number of projects the setting will apply to and price using the pricing page.

## Types and scope
- ADMIN_READ (read metadata or configuration), DATA_READ (read user-provided data), DATA_WRITE (write
  user-provided data). ADMIN_WRITE (Admin Activity) logs are always on and cannot be disabled.
- Configure at organization, folder, project, or (via gcloud) billing account. The result is the union across the
  hierarchy: a child cannot disable a log type enabled by a parent, nor remove a parent's exempted principals.
  A service-specific config is unioned with the `allServices` config.
- Enable per service and per type rather than `allServices` where you can. Enabling everything at organization
  level forces it on in every project beneath.
- Exempted principals do not generate Data Access logs for the log types you disable for them. Caution from the
  page: adding an exempted principal for a service and log type enables that log type even if it was disabled.
- Data Access logs are stored in the `_Default` bucket unless you route them elsewhere. Viewing them needs the
  Private Logs Viewer role (`roles/logging.privateLogViewer`); the Editor role does not include it.
- Google notes that if Data Access logs track Storage objects, authenticated browser downloads from
  `storage.cloud.google.com` can return 403.

## Cut volume with sink exclusions
Each sink has one inclusion filter and optional exclusion filters; an entry that matches an exclusion filter is not
routed by that sink. The `_Default` sink can be modified, including adding exclusion filters.
```bash
gcloud logging sinks update _Default --project=<PROJECT_ID> \
  --add-exclusion=name=noisy-reads,filter='log_id("cloudaudit.googleapis.com/data_access") AND protoPayload.serviceName="storage.googleapis.com"'
```
- Exclusion filters apply after entries reach the Logging API, so they do not reduce `entries.write` quota use.
- Every sink evaluates each entry independently, so another sink (for example an aggregated sink) can still route
  an entry you excluded in `_Default`.
- Do not exempt or exclude human users' access if you need the audit trail.

## Verify
- [ ] Data Access ingestion is within the budgeted amount a few days after enablement.

## Checked
2026-11-09. Confirmed against Enable Data Access audit logs (read to the exemptions section), Log routing overview
(searched for sink, exclusion and _Default behaviour, not read in full) and the Observability pricing page
(searched for the logging allotment). The `gcloud logging sinks update` flags passed the reference check. Removed:
the Log Analytics SQL, the `byte_count` metric filter, specific service examples (Secret Manager, KMS, GKE),
the claim that excluded logs are not billed, and numeric prices.
Method: documentation only; no commands were run.
