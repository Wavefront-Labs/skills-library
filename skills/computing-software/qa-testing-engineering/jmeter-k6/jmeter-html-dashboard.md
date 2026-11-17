---
id: computing-software.qa-testing-engineering.jmeter-k6.jmeter-html-dashboard
name: jmeter-html-dashboard
category: computing-software
field: qa-testing-engineering
product: jmeter-k6
tags: [jmeter-dashboard, html-report, apdex, jmeter-reportgenerator, statistics-json]
level: practitioner
status: docs-checked
description: "Generate and customise the JMeter HTML dashboard: required JTL fields, Apdex thresholds, granularity, transaction filters, statistics.json for CI checks and common errors."
sources:
  - https://jmeter.apache.org/usermanual/generating-dashboard.html
  - https://github.com/apache/jmeter/blob/master/bin/reportgenerator.properties
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Generating and customizing the HTML dashboard

## Generate
```bash
jmeter -n -t plan.jmx -l run.jtl -e -o report/      # at end of a run
jmeter -g run.jtl -o report/                         # from an existing JTL
```
Required JTL settings (the manual lists them; keep them enabled): CSV output with `bytes`, `label`, `latency`, `response_code`, `response_message`, `successful`, `thread_counts`, `thread_name`, `time`, `connect_time` and `assertion_results_failure_message` set to true, and a `jmeter.save.saveservice.timestamp_format` that includes the time (`ms` is the default).

## Customise (user.properties)
```properties
# APDEX thresholds in ms (defaults 500 and 1500)
jmeter.reportgenerator.apdex_satisfied_threshold=500
jmeter.reportgenerator.apdex_tolerated_threshold=1500
# per-transaction APDEX: name or regex, colon, satisfied|tolerated, ending with a semicolon
jmeter.reportgenerator.apdex_per_transaction=Login:300|900;Search.*:800|2000;
# granularity in ms of the over-time graphs (default 60000, must be above 1000)
jmeter.reportgenerator.overall_granularity=10000
# keep only these series; the pattern must end with (-success|-failure)?$
jmeter.reportgenerator.exporter.html.series_filter=^(Login|Checkout|Search)(-success|-failure)?$
jmeter.reportgenerator.report_title=Checkout load test
# sliding window for percentile evaluation (default 20000; larger is more accurate and uses more memory)
jmeter.reportgenerator.statistic_window=20000
# regex of samples to keep (note the doubled backslash in a properties file)
jmeter.reportgenerator.sample_filter=^(?!.*\\.(css|js|png)).*$
```

## Reading it
- Statistics table: per label samples, error %, average and percentiles (`aggregate_rpt_pct1..3`, defaults 90, 95 and 99), throughput; an APDEX table.
- Over-time graphs: response times, active threads, bytes throughput, latencies, connect time, hits per second.
- Time VS Threads and Response Time Vs Request: where latency bends as load rises.
- Errors and Top 5 Errors by Sampler.

## CI use
The JSON exporter (`jmeter.reportgenerator.exporter.json.*` in `reportgenerator.properties`) generates `statistics.json` with the per-label statistics; check its field names in a sample run, then parse it in a pipeline step to enforce thresholds.

## Gotchas
- An incorrect filter configuration can produce an empty report; if a timestamp format has no year, the report uses 1970 as the year.
- To report only Transaction Controller samples for a page that triggers Ajax calls, use "Generate parent sample" on the controller and apply the naming policy; filter series with `series_filter` so children are not double counted.
- Slice warm-up out with `jmeter.reportgenerator.start_date`/`end_date` (default date format `yyyyMMddHHmmss`, set by `date_format`).

## Verify
Dashboard sample counts equal JTL row count (minus filtered labels); Apdex values reflect configured thresholds.

## Checked
Checked against the Apache JMeter user manual sources (apache/jmeter, xdocs/usermanual and bin/, master as of 2026-10-01; latest release 5.6.3). Confirmed: `-e -o` and `-g`, required save-service properties, APDEX defaults and per-transaction format, granularity default and minimum, series_filter suffix rule, statistic_window default, sample_filter, percentile properties and defaults, graph names, JSON exporter creating statistics.json, start_date/end_date. Field names inside statistics.json were not found in the docs and are no longer stated.

Method: documentation only; no commands were run.
