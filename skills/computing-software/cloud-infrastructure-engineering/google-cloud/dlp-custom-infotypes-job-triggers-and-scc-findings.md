---
id: computing-software.cloud-infrastructure-engineering.google-cloud.dlp-custom-infotypes-job-triggers-and-scc-findings
name: dlp-custom-infotypes-job-triggers-and-scc-findings
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, sensitive-data-protection, custom-infotypes, regex-infotypes, dictionary-infotypes, job-triggers, dlp-inspection-triggers, dlp-scc-integration, dlp-findings-scc, discovery]
level: advanced
status: docs-checked
description: "Find organisation-specific sensitive data with Sensitive Data Protection: custom infoTypes with hotwords, scheduled inspection job triggers, and findings sent to SCC."
sources: ["https://cloud.google.com/sensitive-data-protection/docs/creating-custom-infotypes", "https://cloud.google.com/sensitive-data-protection/docs/creating-job-triggers", "https://cloud.google.com/sensitive-data-protection/docs/concepts-actions", "https://cloud.google.com/sensitive-data-protection/docs/data-profiles"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# DLP: custom infoTypes, job triggers and SCC findings

## 1. Inspect template with custom infoTypes
```json
{
  "inspectTemplate": {
    "displayName": "corp-sensitive",
    "inspectConfig": {
      "infoTypes": [{"name": "EMAIL_ADDRESS"}],
      "customInfoTypes": [
        {"infoType": {"name": "CUSTOMER_ID"}, "regex": {"pattern": "CUST-[0-9]{8}"},
         "likelihood": "POSSIBLE",
         "detectionRules": [{"hotwordRule": {"hotwordRegex": {"pattern": "(?i)customer|account"},
            "proximity": {"windowBefore": 30}, "likelihoodAdjustment": {"fixedLikelihood": "VERY_LIKELY"}}}]},
        {"infoType": {"name": "PROJECT_CODENAME"},
         "dictionary": {"wordList": {"words": ["bluefin", "kestrel", "atlas-x"]}}}
      ],
      "minLikelihood": "LIKELY"
    }
  }
}
```
```bash
curl -X POST -H "Authorization: Bearer $(gcloud auth print-access-token)" -H 'Content-Type: application/json' \
  "https://dlp.googleapis.com/v2/projects/<P>/locations/europe-west2/inspectTemplates" -d @template.json
```
For large dictionaries, look up stored infoTypes in the custom infoType docs.
Test patterns with `content:inspect` on sample text before scanning data.

## 2. Job trigger (scheduled inspection)
```json
{"jobTrigger": {
  "displayName": "weekly-landing-bucket",
  "triggers": [{"schedule": {"recurrencePeriodDuration": "604800s"}}],
  "inspectJob": {
    "storageConfig": {"cloudStorageOptions": {"fileSet": {"url": "gs://<B>/landing/**"}},
                      "timespanConfig": {"enableAutoPopulationOfTimespanConfig": true}},
    "inspectTemplateName": "projects/<P>/locations/europe-west2/inspectTemplates/<ID>",
    "actions": [{"publishSummaryToCscc": {}},
                {"saveFindings": {"outputConfig": {"table": {"projectId": "<P>", "datasetId": "dlp", "tableId": "findings"}}}},
                {"pubSub": {"topic": "projects/<P>/topics/dlp-done"}}]}}}
```
POST to `.../locations/europe-west2/jobTriggers`. `enableAutoPopulationOfTimespanConfig` scans only
new/changed data each run. Limit how much is scanned per run to control cost (see the job trigger docs for sampling options).

## 3. SCC
`publishSummaryToCscc` sends a job summary finding to Security Command Center; **discovery**
(data profiling) for BigQuery/Cloud SQL/GCS at org level publishes sensitivity and risk profiles to SCC,
which then raise findings such as high-risk data being public. Prefer discovery for breadth, triggers
for targeted deep scans.

## Gotchas
- Unbounded triggers on big buckets can be costly; see the vendor's pricing page.
- Regex without hotwords produces false positives on IDs that look similar; use exclusion rules too.
- The DLP service agent needs read on sources and write on result datasets.

## Verify
- [ ] A sample file with a known CUST- ID shows a finding with the expected likelihood in the results table.
- [ ] SCC shows the DLP source and findings for the scanned resources.

## Checked
2026-10-28. Confirmed: job trigger page (`publishSummaryToCscc`, `enableAutoPopulationOfTimespanConfig`, `recurrencePeriodDuration`); DLP v2 discovery document (`hotwordRule` with `hotwordRegex`, `proximity`, `likelihoodAdjustment`; `minLikelihood` on InspectConfig).
Removed: `UK_NATIONAL_INSURANCE_NUMBER` (built-in infoType list not fetched), the 10k-term threshold, `bytesLimitPerFile` and `rowsLimitPercent` values, and the per-GB billing statement.
Method: documentation only; no commands were run.
