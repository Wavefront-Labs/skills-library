---
id: computing-software.cloud-infrastructure-engineering.cortex.per-tenant-ingestion-rate-limiting
name: per-tenant-ingestion-rate-limiting
category: computing-software
field: cloud-infrastructure-engineering
product: cortex
tags: [rate-limiting, ingestion-rate, burst, token-bucket, 429]
level: practitioner
status: docs-checked
description: "Tune Cortex write-path rate limits: the per-tenant token bucket, local versus global strategy, burst sizing and per-instance limits."
sources:
  - https://github.com/cortexproject/cortex/blob/master/docs/guides/rate-limiting.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
There are two write-path layers. The per-tenant limit in each distributor is a token bucket. The per-instance limit is a safety valve on the total rate a single distributor or ingester accepts. Per-tenant rejection returns HTTP 429; per-instance rejection returns 503. Prometheus remote_write retries 5xx, and 429 when `retry_on_http_429` is set.

Per-tenant settings:

- `ingestion_rate` (`-distributor.ingestion-rate-limit`, default 25000 samples/s): refill rate.
- `ingestion_burst_size` (`-distributor.ingestion-burst-size`, default 50000): bucket capacity.
- `ingestion_rate_strategy` (`-distributor.ingestion-rate-limit-strategy`, default `local`).

Each push consumes tokens equal to float samples plus native histogram samples plus exemplars plus metadata entries. If tokens are short, the whole request is rejected and counted in `cortex_discarded_samples_total{reason="rate_limited"}`. Limits are re-read every 10 seconds, so overrides apply without restart.

Strategies: `local` means each distributor enforces the full rate, so N distributors allow N times the rate; `global` divides the rate by the number of healthy distributors from the distributor ring (`distributor.ring` config required), but burst is not divided. Global assumes evenly spread requests, which a load balancer provides.

Sizing: set the burst at least as large as your biggest single push request, or you get spurious 429s; `2 * ingestion_rate` is a reasonable start. Native histograms have their own separate limiter applied after the main one, and a failure drops only histogram samples.

## Checked

2026-11-04. Claims were read against the Cortex docs page: Rate Limiting guide (see sources). Removed filler and unconfirmed wording.

Method: documentation only; no commands were run.
