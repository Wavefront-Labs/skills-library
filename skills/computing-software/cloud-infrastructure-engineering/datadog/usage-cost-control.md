---
id: computing-software.cloud-infrastructure-engineering.datadog.usage-cost-control
name: usage-cost-control
category: computing-software
field: cloud-infrastructure-engineering
product: datadog
tags: [datadog, usage-attribution, plan-and-usage, estimated-usage, cost-management]
level: practitioner
status: docs-checked
description: "Monitor Datadog usage with estimated usage metrics, usage attribution and monitors to avoid surprise bills."
sources: ["https://docs.datadoghq.com/account_management/billing/usage_metrics/", "https://docs.datadoghq.com/account_management/billing/usage_attribution/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Usage, attribution and cost control
Goal: keep spend predictable.

```
sum:datadog.estimated_usage.logs.ingested_events{*}.as_count()
sum:datadog.estimated_usage.apm.indexed_spans{*}
sum:datadog.estimated_usage.hosts{*}
sum:datadog.estimated_usage.metrics.custom{*}
```

- Datadog computes estimated usage in near real time. You can graph it, create monitors on thresholds you choose, alert on spikes or drops, and assess the effect of code changes.
- Query estimated usage metrics with `sum` as the space aggregator: many are split by tag or child organisation and only `sum` adds them up.
- Metrics include hosts, containers, indexed and ingested custom metrics (`metrics.custom`, `metrics.custom.ingested`, with `.by_metric` and `.by_tag` variants), logs ingested bytes and events, APM indexed and ingested spans, RUM sessions, Synthetic API and browser runs, and DBM hosts.
- Usage Attribution (Plan & Usage section; administrators or users with the Usage Read permission) breaks usage down by up to three tag keys. The first report takes 24 hours after tags are set; monthly reports update daily; CSV downloads include usage and percentages for chargeback. Hourly and monthly data are also available through the API.
- Usage that cannot be tagged during instrumentation (for example Incident Management users, Parallel Testing slots, Audit Trail) is not supported by attribution.
- In attribution data, `<empty>` means tagged with no value, no value means untagged, and `a | b` means the tag was applied multiple times.

Gotcha: estimated usage is not the invoice. The docs say it differs from billable usage by 10 to 20 percent on average, with larger error at small volumes, so reconcile with the billing figures.

## Verify
- A monitor on an estimated usage metric exists and a Usage Attribution report appears 24 hours after tag keys are chosen.

## Checked
2026-11-09. Confirmed against the Estimated Usage Metrics and Usage Attribution pages (near-real-time purpose, `sum` aggregator rule, metric names and families, 10 to 20 percent difference, three tag keys, permission, 24-hour first report, CSV and API, unsupported usage types, empty-value meanings). Removed: the `avg(last_1d)` monitor with a 150000 threshold and `avg:` aggregators, the claim that Usage Attribution is an enterprise-tier feature, the list of typical cost drivers, the statement that Plan & Usage shows billable usage by product (not read), and the monthly-review, budget, pull-request-check and tagging-from-day-one advice.
Method: documentation only; no commands were run.
