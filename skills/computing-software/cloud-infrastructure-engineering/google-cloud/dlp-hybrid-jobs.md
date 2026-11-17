---
id: computing-software.cloud-infrastructure-engineering.google-cloud.dlp-hybrid-jobs
name: dlp-hybrid-jobs
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, sensitive-data-protection, dlp-hybrid-jobs, hybrid-inspection, on-prem-data, findings]
level: advanced
status: docs-checked
description: "Inspect data from anywhere (on-prem, other clouds, apps) with DLP hybrid jobs: create a hybrid job trigger, send hybridInspect requests with labels, and save findings to BigQuery."
sources: ["https://cloud.google.com/sensitive-data-protection/docs/hybrid-inspection", "https://cloud.google.com/sensitive-data-protection/docs/how-to-hybrid-jobs", "https://cloud.google.com/sensitive-data-protection/docs/reference/rest/v2/projects.locations.jobTriggers/hybridInspect"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# DLP hybrid jobs

Normal inspection jobs read Google storage. **Hybrid** jobs receive content you push, from any source,
and aggregate findings like a job (stats, actions), unlike stateless `content:inspect`.

## 1. Create a hybrid job trigger
```json
{
  "triggerId": "onprem-db-scan",
  "jobTrigger": {
    "triggers": [{"manual": {}}],
    "inspectJob": {
      "storageConfig": {"hybridOptions": {
        "description": "On-prem Postgres row samples",
        "requiredFindingLabelKeys": ["source"],
        "labels": {"env": "prod"},
        "tableOptions": {"identifyingFields": [{"name": "customer_id"}]}}},
      "inspectTemplateName": "projects/<P>/locations/global/inspectTemplates/pii",
      "actions": [{"saveFindings": {"outputConfig": {"table": {"projectId": "<P>", "datasetId": "dlp", "tableId": "hybrid_findings"}}}}]}}
}
```
POST to `https://dlp.googleapis.com/v2/projects/<P>/locations/global/jobTriggers`, then activate it
(`jobTriggers/onprem-db-scan:activate`) to get a running job.

## 2. Send content
```bash
curl -X POST -H "Authorization: Bearer $(gcloud auth print-access-token)" -H "Content-Type: application/json" \
  https://dlp.googleapis.com/v2/projects/<P>/locations/global/jobTriggers/onprem-db-scan:hybridInspect \
  -d '{"hybridItem": {"item": {"value": "Contact jane@example.com"},
       "findingDetails": {"containerDetails": {"fullPath": "pg://crm/customers", "type": "postgres"},
                           "labels": {"source": "crm-db"}}}}'
```
Use `item.table` for structured rows so findings reference columns. Batch with client libraries and backoff.

## 3. Finish
A hybrid job trigger can keep receiving data: you can stop the active job, change the configuration and start new jobs within the trigger without reconfiguring your hybridInspect requests. Findings accumulate in the BigQuery table during the run.

## Gotchas
- Supply the labels named in `requiredFindingLabelKeys` with each hybridInspect request.
- Check the Sensitive Data Protection quotas page and sample data rather than streaming everything.
- The `publishSummaryToCscc` and `publishFindingsToCloudDataCatalog` actions are not supported for hybrid inspection.
- Sending data to DLP moves it into Google Cloud: check data-transfer approvals for on-prem regulated data.

## Verify
- [ ] Job shows processed bytes and findings counts in the console; BigQuery table has rows with your container path and labels.

## Checked

2026-10-28. Confirmed against: Sensitive Data Protection how-to-hybrid-jobs page (hybridInspect requests, requiredFindingLabelKeys, identifyingFields, manual trigger, activate, stop-and-reconfigure behaviour) and the note that publishSummaryToCscc is not supported for this operation.

Removed or rewritten: the publishSummaryToCscc action from the example (the docs say it is unsupported), the dlpJobs finish call, and the per-minute quota claim.

Method: documentation only; no commands were run.
