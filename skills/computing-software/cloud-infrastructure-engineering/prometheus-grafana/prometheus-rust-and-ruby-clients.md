---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.prometheus-rust-and-ruby-clients
name: prometheus-rust-and-ruby-clients
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [prometheus-rust-client, prometheus-ruby-client, client-libraries, instrumentation, rack-middleware, openmetrics]
level: practitioner
status: docs-checked
description: "Instrument Ruby apps with the prometheus-client gem (Rack middleware, labels, data stores for pre-fork servers) and know what the Rust OpenMetrics client promises."
sources:
  - https://github.com/prometheus/client_rust
  - https://github.com/prometheus/client_ruby
  - https://prometheus.io/docs/instrumenting/clientlibs/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Rust and Ruby client libraries

Both are on the Prometheus client-libraries list (Go, Java/Scala, Node.js, Python, Ruby and Rust are the officially listed languages).

## Rust: `prometheus-client` (client_rust)
- A Rust implementation of the OpenMetrics specification. API docs are at https://docs.rs/prometheus-client/ (the README links there rather than showing code, so take type and function names from docs.rs, not from memory).
- Stated goals: no `unsafe` inside the library, type safety (the type system should catch common instrumentation mistakes at compile time), and speed so that you can instrument often.
- Known gaps against the OpenMetrics spec (the README calls these bugs to be fixed): state set metric, gauge histogram metric, summary metric, and no enforcement of rules such as unique MetricFamily names, snake_case names, UNIT metadata and at least one histogram bucket. Do not rely on the library to reject a bad name.
- The README points to `rust-prometheus` (tikv) as a related library; see tikv/rust-prometheus issue 392 for a comparison.

## Ruby: `prometheus-client` gem
Install with `gem install prometheus-client` or add `gem "prometheus-client"` to the Gemfile.
```ruby
require 'prometheus/client'
prometheus = Prometheus::Client.registry
http_requests = prometheus.counter(:http_requests, docstring: 'A counter of HTTP requests made')
http_requests.increment

counter = Prometheus::Client::Counter.new(:service_requests_total, docstring: '...', labels: [:service])
counter.increment(by: 5, labels: { service: 'bar' })
```
Metric types: Counter, Gauge (`set`, `increment`, `decrement`), Histogram (`observe`; default buckets 0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1, 2.5, 5, 10; `Histogram.linear_buckets` and `Histogram.exponential_buckets`) and Summary (only sum and count, no quantiles).

### Rack middleware
Two middlewares: `Prometheus::Middleware::Exporter` exposes the metrics endpoint, and `Prometheus::Middleware::Collector` traces all HTTP requests. The README recommends gzip for the endpoint, for example `Rack::Deflater`:
```ruby
use Rack::Deflater
use Prometheus::Middleware::Collector
use Prometheus::Middleware::Exporter
```

### Labels
- Declare label names when creating the metric; every declared label must be present on each update. Avoid high-cardinality labels (an HTTP status code is fine, a user ID is not).
- `preset_labels:` fixes some label values in the definition; `with_labels(...)` returns a view with labels set, and if all labels are preset, validation happens once instead of on every observation, which helps in fast loops.
- Time series do not exist until first touched; `init_label_set` initialises a label set (a counter at 0).
- Reserved labels `:job`, `:instance` and `:pid` raise `ReservedLabelError`.

### Data stores
Metric values live in a global data store set through `Prometheus::Client.config.data_store = <instance>`, which must be set before any metrics are initialised.
- `Synchronized` (default): thread safe, single process only.
- `SingleThreaded`: fastest, not thread safe.
- `DirectFileStore`: one file per process and metric; the recommended store for pre-fork servers (Unicorn, Puma with multiple processes). It takes a `dir:` parameter.
- DirectFileStore caveats from the README: empty the directory at app start (before the server forks) or each run keeps exporting the previous run's values; declare metrics before forking; expect many files and noticeable memory use when scraped; counters, histograms and summaries are summed across processes while gauges are exported per process with a `pid` label unless you set `store_settings: { aggregation: :max }` (SUM, MAX, MIN or MOST_RECENT; MOST_RECENT allows only `set`).

### Pushgateway
For batch jobs: `Prometheus::Client::Push.new(job: 'my-batch-job').add(registry)`, plus `replace` and `delete`. Credentials must go through `push.basic_auth("user", "password")`, not the gateway URL, which raises an error.

## Verify
- [ ] Under a pre-fork server, repeated scrapes show consistent counters rather than one worker's numbers (needs DirectFileStore).
- [ ] The metrics endpoint responds at the path your Rack app serves.

## Checked
Checked 2026-11-08 against the client_rust README, client_ruby README and the client libraries list. Removed because the pages do not state them: the Rust code sample, the `_total` auto-suffix claim, the content type to serve, "do not mix both crates in one binary", the Ruby default metric names created by Collector, the `/tmp` store path, and the Rust memory/cardinality gotchas.

Method: docs-only read of cited pages, 2026-11-08
