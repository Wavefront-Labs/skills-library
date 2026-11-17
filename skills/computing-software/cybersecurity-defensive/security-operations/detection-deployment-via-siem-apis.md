---
id: computing-software.cybersecurity-defensive.security-operations.detection-deployment-via-siem-apis
name: detection-deployment-via-siem-apis
category: computing-software
field: cybersecurity-defensive
product: security-operations
tags: [detection-as-code, detection-deployment-api, splunk-rest-api, kibana-detection-engine-api, sentinel-arm, ci-cd, idempotent-deployment]
level: advanced
status: draft
description: "Push detections from a repo to Splunk, Elastic and Sentinel through their APIs idempotently: auth, create-or-update by stable ID, disabling removed rules, and rollback."
sources: ["https://docs.splunk.com/Documentation/Splunk/latest/RESTREF/RESTsearch#saved.2Fsearches", "https://www.elastic.co/guide/en/security/current/rules-api-create.html", "https://learn.microsoft.com/en-us/rest/api/securityinsights/alert-rules/create-or-update"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Deploying detections through SIEM APIs

The deploy step of detection-as-code: the repo is the source of truth, a pipeline makes the SIEM
match it. Requirements: idempotent (re-running changes nothing), keyed on a stable ID, and
reversible.

## Splunk (REST)
```
# create (fails if exists)
curl -k -H "Authorization: Bearer $TOKEN" https://sh:8089/servicesNS/nobody/detections/saved/searches \
  -d name="DET-0042 Brute force" --data-urlencode search="index=auth ..." \
  -d cron_schedule="*/15 * * * *" -d is_scheduled=1 -d dispatch.earliest_time=-20m
# update
curl -k -H "Authorization: Bearer $TOKEN" \
  "https://sh:8089/servicesNS/nobody/detections/saved/searches/DET-0042%20Brute%20force" -d ...
```
- Use an app namespace you own (`nobody` owner = app-level sharing).
- On a search head cluster, call any member; changes replicate. ES correlation searches need the
  `action.correlationsearch.*` and `action.notable.*` parameters, or ship them as an app via the deployer.
- Alternatively package detections as a Splunk app and deploy with the deployer/ACS (Cloud).

## Elastic (Kibana detection engine API)
```
curl -X POST "$KIBANA/api/detection_engine/rules/_import?overwrite=true" \
  -H "kbn-xsrf: true" -H "Authorization: ApiKey $KEY" --form file=@rules.ndjson
```
- `rule_id` is the stable key (keep it in the repo file). `overwrite=true` makes import idempotent.
- Bulk enable/disable: `POST /api/detection_engine/rules/_bulk_action` with `action: enable|disable`.
- Spaces: prefix the path with `/s/<space-id>`.
- Elastic's `detection-rules` CLI (`kibana import-rules`) wraps this.

## Microsoft Sentinel
`PUT https://management.azure.com/subscriptions/{sub}/resourceGroups/{rg}/providers/Microsoft.OperationalInsights/workspaces/{ws}/providers/Microsoft.SecurityInsights/alertRules/{ruleId}?api-version=2024-09-01`
- `{ruleId}` is a GUID you keep in the repo: PUT is create-or-update.
- Or deploy ARM/Bicep templates, or use Sentinel Repositories.
- Auth with a workload identity (OIDC federated credential from the CI runner), role Sentinel Contributor.

## Pipeline shape
1. Validate (schema, query syntax, unit tests on sample data).
2. Plan: diff repo vs SIEM (GET all rules by tag/prefix), print creates/updates/disables.
3. Apply to staging, run smoke tests, then prod with approval.
4. Rules removed from the repo: disable, do not delete (keeps history), then delete after N days.

## Gotchas
- Portal edits are overwritten by the next deploy; communicate that and restrict write access.
- Secrets (tokens, API keys) belong in the CI secret store, scoped to deploy jobs only.
- Rate limits on bulk operations; batch and retry with backoff.

## Verify
Run the pipeline twice: the second run must report zero changes. Then change one rule and
confirm only that rule updates.
