---
id: computing-software.cloud-infrastructure-engineering.google-cloud.searching-resources-with-search-all-resources
name: searching-resources-with-search-all-resources
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, cloud-asset-inventory, search-all-resources, asset-search-query, resource-search, gcloud-asset-search]
level: practitioner
status: docs-checked
description: "Find resources across an organization with gcloud asset search-all-resources: query syntax for labels, locations, states and KMS keys, asset type filters, and read-time masks."
sources: ["https://cloud.google.com/asset-inventory/docs/search-resources", "https://cloud.google.com/asset-inventory/docs/search-query-syntax", "https://cloud.google.com/sdk/gcloud/reference/asset/search-all-resources"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Searching resources with searchAllResources

Search across a project, folder or organization scope with the Cloud Asset API
`searchAllResources` method. Check the Permissions section of the search page for the role the
caller needs at the scope.

## Queries
```bash
S=organizations/<ORG>
# resources missing an owner label (existence check works on labels only)
gcloud asset search-all-resources --scope=$S --query="NOT labels.owner:*" --asset-types='compute.googleapis.com/.*'
# resources whose location starts with us-central
gcloud asset search-all-resources --scope=$S --query="location:us-central*"
# resources encrypted with a specific key
gcloud asset search-all-resources --scope=$S --query="kmsKeys:projects/<P>/locations/<R>/keyRings/<KR>/cryptoKeys/<KEY>"
# VMs that are not running
gcloud asset search-all-resources --scope=$S --asset-types=compute.googleapis.com/Instance --query="NOT state:running"
# created after a date (YYYY-MM-DD, UTC)
gcloud asset search-all-resources --scope=$S --query="createTime>2026-01-01"
```
Syntax:
- `field:value` is a partial, case-insensitive token match; it can use phrases, combinations
  (`field:(a b)`, uppercase `AND`/`OR`, parentheses) and a trailing `*` prefix wildcard.
- `field=value` is an exact, case-sensitive match and cannot contain wildcards.
- `NOT` negates (resource searches only). `labels.key:*` checks that a label key exists.
- `=`, `>`, `>=`, `<`, `<=` compare numbers and timestamps (`createTime`, `updateTime`) given as epoch
  seconds, `YYYY-MM-DD` or `"YYYY-MM-DDThh:mm:ss"`.
- A query holds at most 10 comparisons and 2048 characters. Escape double quotes in `--query`.

## Output control
`--order-by="createTime DESC"`, `--read-mask="name,assetType,location,labels,additionalAttributes"`,
`--format` / `--flatten` for scripting. `additionalAttributes` holds type-specific searchable attributes.
Page size is capped at 500.

## Gotchas
- Searchable fields are those of the `ResourceSearchResult` reference; use the asset types list for
  what each type exposes.
- For full resource configuration or relationships use export or other Asset Inventory methods instead.

## Verify
- [ ] Query results match `gcloud compute instances list` for a sample project.

## Checked
2026-10-31. Confirmed against the Asset Inventory "Search resources" and "Search query syntax" pages and the
Cloud Asset v1 discovery document (`searchAllResources` parameters, `ResourceSearchResult` fields).
Removed: the public-IP `natIP:*` query (existence checks work on labels only), `roles/cloudasset.viewer`
and `cloudasset.assets.searchAllResources` claims, the "index lags by minutes" and free-text-search claims.
Method: documentation only; no commands were run.
