---
id: computing-software.cybersecurity-defensive.splunk.spl-timechart-and-outlier-detection
name: spl-timechart-and-outlier-detection
category: computing-software
field: cybersecurity-defensive
product: splunk
tags: [splunk, spl, timechart, outlier-detection, anomaly-detection, baselining, standard-deviation, predict, investigation]
level: practitioner
status: draft
description: "Spot spikes and drops with SPL: timechart spans, moving baselines with streamstats, z-score and IQR outliers, and the predict command."
sources: ["https://docs.splunk.com/Documentation/Splunk/latest/SearchReference/Timechart", "https://docs.splunk.com/Documentation/Splunk/latest/SearchReference/Predict", "https://docs.splunk.com/Documentation/Splunk/latest/SearchReference/Anomalydetection"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# timechart and statistical outlier detection

**Goal:** turn raw counts into a trend and flag points that break the baseline, for both
investigation (when did this start?) and detection (alert on unusual volume).

## timechart essentials
```
index=auth action=failure | timechart span=1h count by user limit=10 useother=t
index=proxy | timechart span=15m sum(bytes_out) as out by src_ip limit=5
```
- `limit=` caps series (default 10) and folds the rest into OTHER; `limit=0` for all.
- Use `span` explicitly; automatic spans change with the time range and break comparisons.
- `tstats ... by _time span=1h` then `timechart` is much faster on accelerated data.

## Z-score over a moving baseline
```
| tstats count where index=auth action=failure by _time span=1h
| streamstats window=168 current=f avg(count) as mean stdev(count) as sd
| eval z=round((count-mean)/sd,2) | where z>3
```
A 168-hour window gives a week of baseline excluding the current point (`current=f`).

## Seasonal (hour-of-week) baseline
```
| tstats count where index=vpn earliest=-30d@h latest=@h by _time span=1h
| eval how=strftime(_time,"%a-%H")
| eventstats median(count) as med perc25(count) as q1 perc75(count) as q3 by how
| eval upper=q3+1.5*(q3-q1), lower=q1-1.5*(q3-q1)
| where _time>=relative_time(now(),"-1h@h") AND (count>upper OR count<lower)
```
IQR with medians resists the very outliers you are hunting; mean/stdev do not.

## predict
```
| timechart span=1d count | predict count algorithm=LLP5 future_timespan=7
```
Gives `upper95`/`lower95` bands; good for capacity and dashboards, weaker for alerting on
short spans.

## Gotchas
- Gaps: `timechart` fills empty buckets with 0 (or `cont=false` leaves them out); zero
  buckets drag the baseline down.
- By-entity baselines (per user) need enough history per entity; new entities always look
  anomalous. Require a minimum count before alerting.
- Holidays and month-end shift volumes; review alerts against the business calendar.

## Verify
Backtest over the past 30 days and count how often the condition would have fired; tune
thresholds until the rate is one an analyst will actually review.
