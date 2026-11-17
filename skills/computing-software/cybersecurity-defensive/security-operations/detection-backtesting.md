---
id: computing-software.cybersecurity-defensive.security-operations.detection-backtesting
name: detection-backtesting
category: computing-software
field: cybersecurity-defensive
product: security-operations
tags: [detection-engineering, detection-backtesting, historical-search, alert-volume, true-positive-rate, tuning, splunk, kql]
level: advanced
status: draft
description: "Backtest a new detection against historical data before enabling it: expected alert volume, precision sampling, known-incident recall and setting thresholds from the data."
sources: ["https://www.splunk.com/en_us/blog/security/detection-engineering-lifecycle.html", "https://github.com/palantir/alerting-detection-strategy-framework", "https://learn.microsoft.com/en-us/azure/sentinel/create-analytics-rules"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Backtesting detections against history

**Goal:** know before go-live how often a detection will fire, what fraction of hits are
real, and whether it would have caught past incidents.

## 1. Run over history
Run the exact production query over 30-90 days (as far as hot retention allows),
bucketed by day:
```
<detection search> earliest=-30d@d latest=@d | bin _time span=1d | stats count by _time
```
KQL: wrap the rule query and `summarize count() by bin(TimeGenerated, 1d)` over `ago(30d)`.
Scheduled-rule semantics matter: if the rule groups by entity per run, emulate that
(`stats ... by user, _time span=<frequency>`) to count alerts, not raw events.

## 2. Volume budget
Translate to alerts per day and analyst time (alerts x minutes per triage). If it exceeds
the queue's capacity, it will be ignored; tune or lower to a risk/hunting signal instead.

## 3. Precision sample
Randomly sample 20-50 historical hits and label them TP / benign TP / FP. Precision =
TP / labelled. Record the common FP causes; they become filters.
```
<detection search> earliest=-30d | sample 50   ```or | eval r=random() | sort r | head 50```
```

## 4. Recall check
Re-run over the time windows of past incidents, red-team or purple-team runs, and replayed
attack datasets. Every one the detection is meant to catch should hit. Misses reveal data
gaps or logic too narrow.

## 5. Threshold from data
For count-based rules, look at the distribution per entity:
```
... | stats count by user | stats perc95(count) perc99(count) max(count)
```
Set thresholds above normal tails, then confirm known-bad cases are still above them.

## 6. Record
Put volume per day, precision, recall evidence and chosen thresholds in the ADS / pull
request. They become the baseline for detection health monitoring later.

## Gotchas
- Retention shorter than the lookback hides seasonal behaviour (month-end jobs, quarterly
  patching); note the limit.
- Backtest results with tuning filters added afterwards must be re-run; filters can remove TPs.
- Data that only exists going forward (new log source) cannot be backtested; ship as
  test/experimental status with monitoring.

## Verify
After two weeks live, actual alert volume and precision fall within the backtested range;
large differences mean the backtest did not match the production query semantics.
