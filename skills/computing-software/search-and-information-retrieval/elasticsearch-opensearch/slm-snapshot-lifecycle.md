---
id: computing-software.search-and-information-retrieval.elasticsearch-opensearch.slm-snapshot-lifecycle
name: slm-snapshot-lifecycle
category: computing-software
field: search-and-information-retrieval
product: elasticsearch-opensearch
tags: [search-and-information-retrieval, elasticsearch-opensearch, elasticsearch, opensearch, slm-snapshot-lifecycle]
level: advanced
status: docs-checked
description: "Schedule snapshots and retention with an Elasticsearch SLM policy, or with OpenSearch snapshot management policies."
sources:
  - https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-slm-put-lifecycle
  - https://www.elastic.co/docs/deploy-manage/tools/snapshot-and-restore/create-snapshots
  - https://www.elastic.co/docs/reference/elasticsearch/configuration-reference/snapshot-restore-settings
  - https://docs.opensearch.org/latest/tuning-your-cluster/availability-and-recovery/snapshots/snapshot-management/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Snapshot lifecycle management

**Goal:** automatic backups.
- Elasticsearch: `PUT _slm/policy/nightly-snapshots {"schedule":"0 30 1 * * ?","name":"<nightly-snap-{now/d}>","repository":"my_repository","config":{"indices":["data-*"],"include_global_state":false},"retention":{"expire_after":"30d","min_count":5,"max_count":50}}`. Needs `manage` index and `manage_slm` cluster privileges.
- The repository must exist before the policy is created. A UUID is appended to each snapshot name; the name supports date math. Updating a policy increments its version, and schedule changes apply immediately. `schedule` may also be an interval such as `"1h"`; the first snapshot comes one hour after the policy is modified.
- Retention: `expire_after`, `min_count` (kept even if expired) and `max_count` (kept at most, even if not expired). Retention is a cluster-level task separate from the snapshot schedule, controlled by `slm.retention_schedule` (default `0 30 1 * * ?`, daily 1:30am UTC); `slm.retention_duration` (default 1h) limits how long it spends deleting. Run it now with `POST _slm/_execute_retention`. A policy's retention applies only to snapshots it created.
- Keep node clocks synchronized: SLM uses the system clock for schedules and retention ages.
- Run now: `POST _slm/policy/nightly-snapshots/_execute` (does not affect the schedule). Status and next scheduled run: `GET _slm/policy/nightly-snapshots`; history: `GET _slm/stats`.
- Several policies can share a repository on different schedules (hourly, daily, monthly) since retention is per policy.
- OpenSearch: Snapshot Management, which needs the Index Management plugin. Policies via `POST _plugins/_sm/policies/{policy_name}` (update with `PUT ...?if_seq_no=...&if_primary_term=...`), with a creation cron schedule and an optional separate deletion schedule. Policy names must be unique and cannot be renamed. Failed operations retry up to three times; check `GET _plugins/_sm/policies/{policy_names}/_explain`. Start and stop with `_start` and `_stop`. No concurrent operations within one policy. The request body fields were not shown on the page.
- Failure mode: retention runs on its own schedule, not after every snapshot.

## Verify
- [ ] After `_execute`, `GET _slm/policy/nightly-snapshots` shows the run; OpenSearch: `_explain` shows `metadata.latest_execution`.

## Checked
Checked 2026-11-08 against the Elasticsearch "Create or update a policy" API page, "Create snapshots" guide, "Snapshot and restore settings" page, and the OpenSearch "Snapshot management" page. Removed: `GET _snapshot/my_repo/_all` as a verify step (not on the pages read) and the `*` indices default.
Method: documentation only; no commands were run.
