---
id: computing-software.database-administration.influxdb.scrape-prometheus-metrics-with-scrapers
name: scrape-prometheus-metrics-with-scrapers
category: computing-software
field: database-administration
product: influxdb
tags: [scrapers, prometheus, metrics, scrape, monitoring]
level: practitioner
status: docs-checked
description: "Create an InfluxDB scraper for Prometheus-format endpoints, with the default target, the start delay and the scrape interval."
sources:
  - https://docs.influxdata.com/influxdb/v2/write-data/no-code/scrape-data/manage-scrapers/create-a-scraper/
  - https://docs.influxdata.com/influxdb/v2/write-data/developer-tools/scrape-prometheus-metrics/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

A scraper collects data at regular intervals from any HTTP(S)-accessible endpoint that serves the Prometheus data format and writes it to a bucket. In the UI, go to Data (Load Data), Scrapers, Create Scraper, then enter a name, select the destination bucket and enter the target URL.

Defaults and timing from the page: the default target URL is `http://localhost:8086/metrics`, which serves InfluxDB-specific metrics in Prometheus format; a new scraper begins scraping after approximately 10 seconds and then scrapes at 10 second intervals.

Alternatives for Prometheus-format endpoints, per the developer-tools page: Telegraf, or the Flux function `prometheus.scrape()` (for example `prometheus.scrape(url: "http://example.com/metrics")`, optionally in a task to run at regular intervals).

## Checked

Method: docs-checked 2026-11-09 against the InfluxDB v2 pages "Create an InfluxDB scraper" and "Scrape Prometheus metrics", article bodies (lines 574-625) read from the downloaded text.

Removed: the claims about `storage_*` and `task_*` metric families replacing the 1.x `_internal` database, the `hardening-enabled` private-address note and the TLS certificate note, none of which these pages state.
