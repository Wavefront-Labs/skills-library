---
id: computing-software.email-administration.mailcow.mailcow-prometheus-exporter
name: mailcow-prometheus-exporter
category: computing-software
field: email-administration
product: mailcow
tags: [prometheus-exporter, metrics-endpoint, readonly-api-key, mailcow-exporter, scrape-config]
level: practitioner
status: docs-checked
description: "Expose mailcow metrics to Prometheus with the bundled exporter override, a read-only API key and a scrape job that passes host and key as parameters."
sources: ["https://docs.mailcow.email/third_party/prometheus_exporter/third_party-prometheus_exporter/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Prometheus exporter for mailcow

Enable by copying `helper-scripts/docker-compose.override.yml.d/PROMETHEUS_EXPORTER/docker-compose.override.yml` into the mailcow directory and running `docker compose up -d` again. To serve it through mailcow's Nginx instead of publishing port 9099, remove the `ports: - "9099:9099"` section from the override and create `data/conf/nginx/site.metrics.custom` with a `location /metrics/` that does `proxy_pass http://prometheus-exporter:9099/metrics;`, then `docker compose restart nginx-mailcow`.

The `/metrics` endpoint takes `host` (your mailcow hostname) and `apiKey` URL parameters; the key should be a read-only API key from the mailcow UI under Access > API. An optional `scheme` parameter defaults to `https`; use `http` for an API without TLS. Restrict access to the exporter and protect the key.

Prometheus scrape job: `job_name: 'mailcow'`, target `mailcow_exporter:9099`, with `params` `MAILCOW_EXPORTER_HOST: ['mail.example.com']` and `MAILCOW_EXPORTER_API_KEY: ['YOUR-APIKEY-HERE']`, plus `token` when the exporter token is not disabled (`MAILCOW_EXPORTER_TOKEN_DISABLE=false`).

For a single mailcow host, set the host and key at start-up instead of on every request: flag `host` or environment variable `MAILCOW_EXPORTER_HOST`, and flag `apikey` or `MAILCOW_EXPORTER_API_KEY`; if both flag and variable are set, the flag wins.

## Checked

2026-11-04. Confirmed on the Prometheus exporter page: the override file copy and compose run, the Nginx proxy variant with restart, host and apiKey parameters with a read-only key from Access > API, the optional scheme parameter defaulting to https, the scrape config with params and the token line, and the host/apikey flags and MAILCOW_EXPORTER_* variables with flag precedence. Added the nginx-mailcow restart step.

Method: documentation only; no commands were run.
