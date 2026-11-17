---
id: computing-software.cloud-infrastructure-engineering.google-cloud.cloud-asset-inventory
name: cloud-asset-inventory
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, cloud-asset-inventory, asset-inventory, asset-search, asset-export, asset-feeds, iam-policy-search, policy-analyzer, resource-search, bigquery-asset-export, drift-detection, cmdb, gcloud-asset, org-wide-inventory]
level: practitioner
status: docs-checked
description: "Use Cloud Asset Inventory for org-wide questions: search resources and IAM policies, export snapshots to BigQuery, and stream change feeds to Pub/Sub."
sources: ["https://cloud.google.com/asset-inventory/docs/overview", "https://cloud.google.com/asset-inventory/docs/searching-resources", "https://cloud.google.com/asset-inventory/docs/exporting-to-bigquery", "https://cloud.google.com/asset-inventory/docs/monitoring-asset-changes", "https://cloud.google.com/policy-intelligence/docs/policy-analyzer-overview"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cloud Asset Inventory

**Goal:** one query answers "every VM with an external IP in the org", "who can read bucket X",
or "what changed in the last hour", without iterating projects.

## 1. Enable and permissions
- `gcloud services enable cloudasset.googleapis.com` in the *calling* project (the one whose quota is used).
- `roles/cloudasset.viewer` (Cloud Asset Viewer) on the organization, folder or project you query.
- Scope any call with `--organization=<ORG_ID>`, `--folder=<ID>` or `--project=<ID>`.

## 2. Resource search (interactive, seconds)
```bash
# Compute Engine instances in US locations
gcloud asset search-all-resources --scope=organizations/<ORG_ID> \
  --asset-types=compute.googleapis.com/Instance \
  --query='location:us-*' --format='table(name,location,project)'

# anything that has an env label
gcloud asset search-all-resources --scope=organizations/<ORG_ID> --query='labels.env:*'

# created after a date
gcloud asset search-all-resources --scope=organizations/<ORG_ID> --query='createTime>2026-10-08'
```
Per-type attributes such as external IPs appear in the returned `additionalAttributes`; use `--format=json` and filter.
Searchable fields differ per asset type; see the searching-resources page and `gcloud asset search-all-resources --help`.

## 3. IAM policy search
```bash
# who has the Owner role anywhere
gcloud asset search-all-iam-policies --scope=organizations/<ORG_ID> --query='roles:roles/owner'
# every policy that binds one principal
gcloud asset search-all-iam-policies --scope=organizations/<ORG_ID> \
  --query='policy:"user:alex@example.com"'
```
For *effective* access including inheritance and group expansion use **Policy Analyzer**:
`gcloud asset analyze-iam-policy --organization=<ORG_ID> --identity=user:alice@example.com --expand-groups --expand-resources`.

## 4. Snapshot export to BigQuery (reporting, CMDB)
```bash
gcloud asset export --organization=<ORG_ID> --content-type=resource \
  --bigquery-table=projects/<PROJ>/datasets/assets/tables/resource --output-bigquery-force \
  --per-asset-type   # one table per asset type (RELATIONSHIP content type can't use it)
```
Content types: `resource`, `iam-policy`, `org-policy`, `access-policy`, `os-inventory`, `relationship`.
Schedule exports with Cloud Scheduler. For history, `gcloud asset get-history` needs a `--start-time` no older than 35 days.

## 5. Feeds (real-time change events)
```bash
gcloud asset feeds create firewall-changes --organization=<ORG_ID> \
  --asset-types=compute.googleapis.com/Firewall --content-type=resource \
  --pubsub-topic=projects/<PROJ>/topics/asset-changes \
  --condition-expression='!temporal_asset.deleted'
```
Messages contain `priorAsset` and `asset` so you can diff. Feed conditions can test `temporal_asset.prior_asset_state` (for example `DOES_NOT_EXIST` for newly created assets). Consumers: a function that reverts a `0.0.0.0/0` ingress rule and pages security; drift detection against Terraform state.

## Gotchas
- Not every API is covered: check the supported asset types list before promising an inventory of a niche service.
- A search page holds at most 500 results (`pageSize`); page through with the next-page token.
- Deleted resources vanish from search; for history use `gcloud asset get-history --content-type=resource --asset-names=... --start-time=...`.

## Verify
- [ ] An org-wide label query returns the known test VM and nothing from projects you cannot see is leaked (scope works).
- [ ] BigQuery export table row count equals the console Asset Inventory count for the same type.
- [ ] Creating a test firewall rule publishes a feed message with `priorAssetState: DOES_NOT_EXIST`.

## Checked

2026-10-28. Confirmed against: Cloud Asset API v1 discovery document (ContentType values RESOURCE, IAM_POLICY, ORG_POLICY, ACCESS_POLICY, OS_INVENTORY, RELATIONSHIP for exports and feeds; Feed fields), gcloud reference pages for the `gcloud asset` commands used (checked with the command checker), the searching-resources page (page size maximum 500), the get-history reference (35 day limit), the monitoring-asset-changes page (`temporal_asset.prior_asset_state`), and the export page (Cloud Asset Viewer role).

Also confirmed: the `--per-asset-type` flag (separate tables per asset type; not usable with RELATIONSHIP) and the search query forms `location:us-*`, `labels.env:*`, `createTime>`, `roles:roles/owner` and `policy:"user:..."`.

Removed: `roles/iam.securityReviewer`, the external-IP and uniform-bucket-access queries (field names not in the docs read), the query-syntax field list, the eventual-consistency and org-scope gotchas, and the one-minute timing.

Method: documentation only; no commands were run.
