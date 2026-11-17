---
id: computing-software.cloud-infrastructure-engineering.google-cloud.recommendation-state-transitions-and-tracking
name: recommendation-state-transitions-and-tracking
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, recommender, recommendation-state, mark-recommendation-claimed, mark-succeeded, dismiss-recommendation, etag]
level: practitioner
status: docs-checked
description: "Track Active Assist recommendations through ACTIVE, CLAIMED, SUCCEEDED, FAILED and DISMISSED with gcloud and etags, plus state metadata for ticket links."
sources: ["https://docs.cloud.google.com/recommender/docs/using-api", "https://docs.cloud.google.com/sdk/gcloud/reference/recommender/recommendations", "https://recommender.googleapis.com/$discovery/rest?version=v1"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Recommendation state transitions and tracking

## States
`ACTIVE` -> `CLAIMED` (someone is working on it) -> `SUCCEEDED` / `FAILED`; or `DISMISSED` (won't do). Google can update the content of `ACTIVE` and `DISMISSED` recommendations; `CLAIMED`, `SUCCEEDED` and `FAILED` content is immutable. Every state change takes the current **etag** (optimistic locking): it ensures the operation only happens if the recommendation has not changed since you read it.

## Commands
```bash
REC=google.compute.instance.MachineTypeRecommender
gcloud recommender recommendations describe <ID> --project=<P> --location=<ZONE> --recommender=$REC --format="value(etag,stateInfo.state)"
gcloud recommender recommendations mark-claimed <ID> --project=<P> --location=<ZONE> --recommender=$REC \
  --etag=<ETAG> --state-metadata=ticket=OPS-1234,owner=team-web
gcloud recommender recommendations mark-succeeded <ID> ... --etag=<NEW_ETAG> --state-metadata=ticket=OPS-1234
gcloud recommender recommendations mark-failed <ID> ... --etag=<ETAG> --state-metadata=reason=app-regression
gcloud recommender recommendations mark-dismissed <ID> ... --etag=<ETAG>
```
`--state-metadata` (`stateMetadata` in the API) is a string map set by users or automation. Each call overwrites any existing state metadata and returns a new etag, so re-read the etag before the next transition.

## Automation
Pipelines that auto-apply (for example, delete idle disks after a snapshot) should mark CLAIMED before acting and SUCCEEDED or FAILED after, so humans do not double-handle.

## Gotchas
- An etag mismatch means someone else updated the recommendation; re-describe and retry.
- Record the reason when dismissing, in state metadata.
- Updating state needs the update permission for that recommender type; check the permissions listed for the recommender in the Recommender docs.
- Reporting on outcomes by BigQuery export: take table and column names from the export's own documentation rather than guessing them.

## Verify
- [ ] A claimed recommendation shows `stateInfo.state` CLAIMED with your metadata; no ACTIVE high-impact recommendations sit without an owner.

## Checked
2026-10-31. Confirmed in the Recommender API v1 discovery document (RecommendationStateInfo states and immutability wording, `stateMetadata` map, `etag` as optimistic locking on the mark-claimed request), the "using the API" state-update page (etag use and `--etag` flag), and by check_commands against the gcloud reference (`describe` and the four `mark-*` commands with their flags). Removed: the BigQuery reporting query and `state_metadata` export column, the cost-unit sign convention, the example permission string and the claim that dismissed recommendations reappear (the BigQuery-export source page returned 404 and the others do not state these).
Method: documentation only; no commands were run.
