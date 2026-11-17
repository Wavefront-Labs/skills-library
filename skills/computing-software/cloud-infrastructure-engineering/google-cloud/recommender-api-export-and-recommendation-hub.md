---
id: computing-software.cloud-infrastructure-engineering.google-cloud.recommender-api-export-and-recommendation-hub
name: recommender-api-export-and-recommendation-hub
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, active-assist, recommender-api, gcloud-recommender, recommender-bigquery-export, recommendation-hub, active-assist-automation, finops]
level: practitioner
status: docs-checked
description: "Work Active Assist at scale: list recommendations with gcloud recommender, track state with etags, and export daily snapshots to BigQuery."
sources: ["https://docs.cloud.google.com/recommender/docs/whatis-activeassist", "https://docs.cloud.google.com/recommender/docs/use-api", "https://docs.cloud.google.com/recommender/docs/bq-export/export-recommendations-to-bq"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Recommender API, export and Recommendation Hub

Recommenders generate recommendations in six value categories. Have a reviewer who understands your
infrastructure assess impact before applying any recommendation; if you apply without human review, set up
rollback first.

## 1. List and act with gcloud
Each recommender has a fully-qualified ID (for example `google.compute.instance.MachineTypeRecommender`) and a
location (zone, region or `global`). With gcloud you must use the project ID.
```bash
gcloud recommender recommendations list --project=<PROJECT_ID> --location=<LOCATION> \
  --recommender=<RECOMMENDER_ID> --format=json
gcloud recommender recommendations mark-claimed <RECOMMENDATION_ID> --etag=<ETAG> \
  --project=<PROJECT_ID> --location=<LOCATION> --recommender=<RECOMMENDER_ID> \
  --state-metadata=ticket=OPS-123
```
- `gcloud beta recommender recommendations list --project=...` lists all recommendations in a project without
  location and recommender (Preview).
- State changes: `mark-claimed` (you intend to apply; Recommender stops updating its content), `mark-dismissed`
  (no longer ACTIVE; content may still update), then `mark-succeeded` or `mark-failed` after applying.
  `--state-metadata` (KEY=VALUE pairs) is available on claimed, succeeded and failed.
- Reference a recommendation by ID plus `etag`; the operation applies only if it has not changed since you
  retrieved it, so list again before marking.
- Apply the change with the resource's own commands, targeting the `resource` field of the `OperationsGroup`
  in `content.operationGroups`.
- Only recommendations retrieved through the API can be interacted with using the API or BigQuery export.
- Insights: `gcloud recommender insights list --project=... --location=... --insight-type=<INSIGHT_TYPE>`.
- Permissions are recommender-specific (see the Recommenders table); with a billing project in the request you
  also need `serviceusage.services.use` (Service Usage Consumer role).

## 2. Export to BigQuery
The export uses BigQuery Data Transfer Service to give daily snapshots for the organization (all projects,
folders and billing accounts, plus organization-level items). Projects without an organization are not exported.
- The dataset holds two date-partitioned tables, `recommendations_export` and `insights_export`.
- The identity setting it up needs `roles/recommender.exporter` at the organization, granted with
  `gcloud organizations add-iam-policy-binding`.
- The daily job waits until data is ready, so use the latest available snapshot rather than depending on a
  dated table. Backfill is possible for dates after the organization opted in.
- Recommendation columns include `cloud_entity_id`, `recommender`, `recommender_subtype`, `state` (ACTIVE,
  CLAIMED, SUCCEEDED, FAILED, DISMISSED) and `primary_impact.cost_projection.cost` (`units`, `nanos`).

## Verify
- [ ] Export tables refresh daily.
- [ ] Every applied recommendation is marked succeeded with a ticket reference in `--state-metadata`.

## Checked
2026-11-09. Confirmed against Recommender overview, Use the API - Recommendations (read in full) and Export
recommendations to BigQuery (searched for tables, roles, state and column names, not read in full). The four
gcloud commands passed the reference check. Removed: the savings SQL and negative-cost claim, the fortnightly
review cadence, automation advice, the Recommendation Hub category ranking and viewer role names.
Method: documentation only; no commands were run.
