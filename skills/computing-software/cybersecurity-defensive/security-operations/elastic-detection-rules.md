---
id: computing-software.cybersecurity-defensive.security-operations.elastic-detection-rules
name: elastic-detection-rules
category: computing-software
field: cybersecurity-defensive
product: security-operations
tags: [elastic-security, elastic-detection-rules, eql, esql, kql, threshold-rules, prebuilt-rules, detection-rules-repo]
level: advanced
status: docs-checked
description: "Build and tune Elastic Security detection rules: query, EQL sequence, threshold, ES|QL and ML types, prebuilt rule updates, exceptions and rule health."
sources: ["https://www.elastic.co/guide/en/security/current/rules-ui-create.html", "https://github.com/elastic/detection-rules", "https://www.elastic.co/guide/en/elasticsearch/reference/current/eql-syntax.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Elastic detection rules

**Goal:** detections in Elastic Security that use the right rule type, run reliably, and
survive prebuilt rule updates.

## Rule types
- **Custom query** (KQL or Lucene): single-event matches.
- **EQL**: sequences and joins across events in order:
  ```
  sequence by host.id with maxspan=1m
    [process where event.type == "start" and process.name == "winword.exe"]
    [process where event.type == "start" and process.parent.name == "winword.exe" and process.name in ("powershell.exe","cmd.exe")]
  ```
- **Threshold**: counts per field (`source.ip` with > 50 failed logons in 5 min) with
  cardinality conditions.
- **ES|QL**: aggregations and computed fields in one query.
- **Indicator match**: events against threat intel indices.
- **New terms**: first time a value (or combination) is seen in a history window.
- **Machine learning**: anomaly jobs (rare process, unusual login times).

## Scheduling
`interval` (how often) and `from` (lookback) leave
overlap for ingest delay; alerts are deduplicated.

## Prebuilt rules
Security > Rules > Add Elastic rules installs from the `detection-rules` package. Updates
are listed for review in the Rules page. Do not edit a prebuilt rule's query to tune it: use
**exceptions** (rule or shared exception lists) and actions; edits are overwritten when
you accept updates.

## Exceptions
Rule exceptions with conditions (`process.executable is %ProgramFiles%\Backup\agent.exe AND
user.name is svc_backup`). Shared exception lists for org-wide allowlists. Value lists
(uploaded IP/keyword lists) for large sets. Endpoint exceptions also stop Elastic Defend
prevention, use carefully.

## As code
The elastic/detection-rules repo provides a CLI (`python -m detection_rules`) to validate
TOML rules, unit test, and import/export via the Kibana API; keep custom rules there.

## Gotchas
- Rules need the right index patterns or data view; missing indices give silent zero matches.
- Rule failures (`Failed`, `Partial failure`) appear in Rule monitoring; gaps happen when
  execution exceeds the interval.
- ECS field mismatches (custom sources not normalised) make rules never fire.

## Checked
2026-10-28. Confirmed in the Elastic Security Timeline, detection rule and EQL pages fetched: EQL sequence syntax with `maxspan`, rule types. Removed: the `now-6m` example, `max_signals`, the "Update available" label and the field-level merge claim (not found).
Method: documentation only; no commands were run.

## Verify
Rules > Rule monitoring: zero failures, execution time well under interval. Trigger the
detection with an Atomic Red Team test and confirm an alert with expected fields.
