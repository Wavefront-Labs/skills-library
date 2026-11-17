---
id: computing-software.cloud-infrastructure-engineering.garage.prometheus-api-request-metrics
name: prometheus-api-request-metrics
category: computing-software
field: cloud-infrastructure-engineering
product: garage
tags: [api-s3-request-counter, api-s3-error-counter, api-request-duration, histogram]
level: practitioner
status: docs-checked
description: "Use the per-endpoint S3 and admin API request, error and duration metrics."
sources:
  - https://garagehq.deuxfleurs.fr/documentation/reference-manual/monitoring/
  - https://garagehq.deuxfleurs.fr/documentation/reference-manual/configuration/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Besides cluster health, Garage exposes metrics per API endpoint:

- `api_admin_request_counter` counts calls per admin API endpoint, labelled `api_endpoint`, for example `Metrics`.
- `api_admin_request_duration` is a histogram (with `_bucket`, `_sum` and `_count` series) of admin call durations.
- `api_s3_request_counter` counts calls per S3 endpoint, for example `CreateMultipartUpload`.
- `api_s3_error_counter` counts calls that returned an error, labelled with `api_endpoint` and `status_code`, such as GetObject with 404.
- `api_s3_request_duration` is the histogram for S3 call durations.

The `[s3_web]` option `add_host_to_metrics` adds the Host header to the web endpoint metrics, but is off by default because the number of distinct hosts is unbounded and can explode label cardinality.

The configuration page's `block_max_concurrent_reads` entry adds that the `block_read_semaphore_timeouts` Prometheus metric counts read-slot timeouts, and a non-zero number indicates an I/O bottleneck on HDD read speed.

The same page lists the equivalent K2V metrics (`api_k2v_request_counter`, `api_k2v_error_counter`, `api_k2v_error_duration`) and the web endpoint metrics (`web_request_counter`, `web_request_duration`, `web_error_counter`).

## Checked

2026-11-07. Read in full (stripped page text, including the inline code blocks; no linked include files were opened): Configuration file format, Monitoring. Confirmed on the monitoring page: the admin and S3 request, error and duration metrics, their labels and histogram series, and the K2V and web metric names. Confirmed on the configuration page: `add_host_to_metrics` and `block_read_semaphore_timeouts`. Removed: the claim that every metric carries HELP and TYPE lines and the curl command (not on the page), and the `api_admin_error_counter` sample claim (not on the page).

Method: documentation only; no commands were run.
