---
id: computing-software.cybersecurity-defensive.security-operations.detection-health-monitoring
name: detection-health-monitoring
category: computing-software
field: cybersecurity-defensive
product: security-operations
tags: [detection-engineering, detection-health-monitoring, silent-failure, sentinel-health, rule-failures, coverage-metrics, elastic-rule-monitoring]
level: advanced
status: docs-checked
description: "Monitor that detections are actually working: Sentinel analytics rule health queries, Elastic rule monitoring, data dependencies, zero-alert drift and synthetic tests."
sources: ["https://learn.microsoft.com/en-us/azure/sentinel/monitor-analytics-rule-integrity", "https://www.elastic.co/docs/solutions/security/detect-and-alert/monitor-rule-executions"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Detection health and silent-failure monitoring

**Goal:** catch detections that stopped working (rule errors, delayed or skipped runs, missing
data, renamed fields) before an incident proves it.

## Failure modes
1. Rule fails to run (query error, timeout, permissions, missing table or function).
2. Rule run is delayed or a window is skipped.
3. Rule runs but data is missing (log source down, table renamed, parser change).
4. Rule runs on data but a field changed, so it can never match again.

## Microsoft Sentinel
Turn on the Sentinel health feature for the workspace first; the `SentinelHealth` table is created
at the first success or failure event of an analytics rule, and `SentinelAudit` records changes
such as a rule being deleted. Microsoft recommends building queries on the functions
`_SentinelHealth()` and `_SentinelAudit()` rather than the tables, for schema compatibility.
```
_SentinelHealth()
| where SentinelResourceType == "Analytics Rule"
| summarize Occurrence=count(), Unique_rule=dcount(SentinelResourceId) by Status, Reason
```
- Scheduled rules: a failed run is retried five more times on the same window, so a window is
  only skipped if all six attempts fail (a failure of any one means the alert is delayed). The
  docs give a query that counts `startTime` groups with `failuresByStartTime == 6`.
- NRT rules: a failed window is added to the next run (one minute later) for up to 60 failures
  (one hour); watch the delay per rule instead of single failures.
- Reasons you may see include a missing table (verify the data source is connected), query
  timeouts, syntax or semantic errors (try resetting the rule by editing and saving without
  changes), queries using too many resources, rule runs delayed by long ingestion times, and
  entity or alert-size limits (32 KB alert size limit).
- Install the Analytics Health & Audit workbook from the content hub to visualise this data.

## Elastic Security
Rules table > **Last response** column shows the status of the latest run (success, failure or
warning). The **Rule Monitoring** tab summarises recent failures, execution times and gaps; the
Rule Monitoring Overview panel shows outcomes and unfilled gap time; a rule's **Execution
results** tab logs each run with status, run type (scheduled or manual), timestamp, execution
duration, alerts created and message. Gaps from missed runs can be filled (see the page's Fill
rule execution gaps section, which this skill did not read).

## Data dependency checks
For each detection record its required sources and fields. A scheduled job verifies that the source
sent data recently and that required fields are populated. Choose the freshness window per
source from its normal volume.

## Zero-alert drift
Compare each rule's alert count with its backtested baseline. A rule that used to fire regularly
and has been silent for a long time is suspect; investigate rather than celebrate.

## Synthetic tests
Schedule harmless trigger tests for key detections and assert the alert appears within the expected
time. Track the pass rate. Tag test alerts clearly and auto-close them, but still count them.

## Gotchas
- A temporarily disabled rule is easy to forget: Sentinel logs a health Reason when the rule is disabled and was not executed, so alert on it.

## Verify
Break a test rule in dev (rename a field in its query) and confirm the health check or rule status
flags it; stop a test log source and confirm the dependency check fires.

## Checked
Date: 2026-11-07. Read: Microsoft Learn "Monitor the health and audit the integrity of your analytics rules" (health-feature, SentinelHealth/SentinelAudit and function guidance, query examples, retry behaviour for scheduled and NRT rules, status and failure table; the workbook setup steps only skimmed) and Elastic "Monitor rule executions" (status, Rule Monitoring tab and Execution results table sections; read by targeted search of the page text, not top to bottom). The Splunk Monitoring Console source was dropped because docs.splunk.com returns 403 to fetchers; all Splunk SPL (`index=_internal sourcetype=scheduler`, `tstats`) was removed with it, as were the `.kibana-event-log-*` query with `event.outcome: failure`, the "30 days" drift window, "Atomic Red Team", "Splunk Attack Range" and "commercial BAS" tool names, and the old summarize-by-`SentinelResourceName` query. The linked Fill rule execution gaps and Sentinel health-feature enablement pages were not read.
Method: documentation only; no commands were run.
