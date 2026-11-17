---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.federation-pitfalls
name: federation-pitfalls
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [prometheus, federation, federation-staleness, federation-timestamp-skew, series-explosion, troubleshooting]
level: advanced
status: docs-checked
description: "Why federating large swathes of series fails: single-machine limits and heavy /federate requests, extra failure points, delayed or missed data, and the aggregated-series fix."
sources: ["https://prometheus.io/docs/prometheus/latest/federation/", "https://www.robustperception.io/federation-what-is-it-good-for/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Federation pitfalls

The Prometheus federation docs describe federation as one server scraping selected series from another, for hierarchies of aggregates or for cross-service series. Brian Brazil's "Federation, what is it good for?" explains where it does not fit: pulling large swathes of series, or all series, from another Prometheus and doing alerting and graphing only from there.

| Problem | Cause (per the article) | What to do |
|---|---|---|
| Global server hits one machine's limits | Routing all data to one global Prometheus limits monitoring to what one machine can handle; the federation request itself can be heavy for the receiver to serve | Pull only aggregated series (for example `{__name__=~"^job:.*"}`) so you are limited by what one datacenter Prometheus can handle |
| Alerts break when a WAN link or the global server is down | Moving data used for alerting to another Prometheus adds a point of failure, risky across WANs | Push alerting as deep down the hierarchy as possible: a target-down alert belongs on the Prometheus scraping the target |
| Odd artefacts, gaps or late data in global graphs | Federation pulls data some time after it was scraped and may miss some due to races | Tolerate it for aggregates; avoid federating everything, and do not use a Prometheus as a proxy by federating all data out of it (alert and graph on the scraping Prometheus, or use a real proxy via `proxy_url`) |
| Series from different servers collide or cannot be told apart | Every Prometheus in an organization should have unique external labels | Set distinct `external_labels` per server |
| Config churn with each new aggregate | Matching individual names needs a config change per rule | Name aggregating rules with a level prefix (`job:...`) and match `{__name__=~"^job:.*"}` |

## Cross-service federation
The article says to ask the owning team first when reaching into another team's Prometheus: it can be like using the undocumented internals of a library in terms of maintenance and stability. It is usually used only for alerting, since Grafana can use multiple data sources in one graph.

## Native histograms
Per the federation page: set `scrape_native_histograms: true` on the scraping server (protobuf scraping); float samples are always federated as untyped while histograms keep full type information.

## Verify
- [ ] The `match[]` selectors request aggregated series only, not `{job=~".+"}`-style wide matches.
- [ ] Each server has unique `external_labels`.
- [ ] Alerts that matter for a target live on the Prometheus that scrapes it.

## Checked
Date: 2026-11-07. Read in full: the Prometheus Federation page and the Robust Perception article "Federation, what is it good for?". Thin skill: the draft's symptom table (the 5-minute lookback and vanishing series, missing staleness markers across federation, `out of order sample` / `duplicate sample` errors, honoured source timestamps causing odd `rate()`, a scrape-timeout threshold, 2-3 interval alert delay, the "timestamp skew" section, NTP advice and the diagnosis queries using `prometheus_target_scrapes_sample_out_of_order_total` and `scrape_samples_scraped`) is not stated on either page and was removed. What remains is the article's three reasons (performance, reliability, correctness), the external-labels and ask-first advice, and the native histogram note. The robustperception article is a 2017 blog post, not official docs.
Method: documentation only; no commands were run.
