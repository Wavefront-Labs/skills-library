---
id: computing-software.rpa-and-low-code.n8n.endpoints-and-metrics-env
name: endpoints-and-metrics-env
category: computing-software
field: rpa-and-low-code
product: n8n
tags: [n8n, endpoints, metrics, prometheus, webhook-url, payload-size]
level: practitioner
status: docs-checked
description: "Configure n8n endpoint paths, payload limits, N8N_WEBHOOK_URL behind a proxy and the /metrics endpoint with its label and queue metric switches."
sources:
  - https://docs.n8n.io/deploy/host-n8n/configure-n8n/basic-configuration/use-environment-variables/endpoints
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: control URL paths, request limits and Prometheus metrics.

## Paths and URLs
`N8N_ENDPOINT_REST` (`rest`), `N8N_ENDPOINT_WEBHOOK` (`webhook`), `N8N_ENDPOINT_WEBHOOK_TEST` (`webhook-test`), `N8N_ENDPOINT_WEBHOOK_WAIT` (`webhook-waiting`), `N8N_ENDPOINT_HEALTH` (`healthz`). These set only paths. Behind a reverse proxy set the base URL with `N8N_WEBHOOK_URL`; `WEBHOOK_URL` is a deprecated alias from n8n 2.35.0 (logs a warning). `N8N_DISABLE_PRODUCTION_MAIN_PROCESS=true` stops production webhooks on the main process so webhook processes take the load.

## Limits
`N8N_PAYLOAD_SIZE_MAX` (16 MiB; restart required; larger payloads need more memory and CPU), `N8N_FORMDATA_FILE_SIZE_MAX` (200 MiB for files in form-data webhooks).

## Metrics
`N8N_METRICS=true` (default false) enables `/metrics`. `N8N_METRICS_PREFIX` (`n8n_`), `N8N_METRICS_INCLUDE_DEFAULT_METRICS` (true). Opt-in groups, all default false: cache, message event bus, API endpoints, queue (`N8N_METRICS_INCLUDE_QUEUE_METRICS`, refreshed every `N8N_METRICS_QUEUE_METRICS_INTERVAL` = 20 s), durable scheduler, poll trigger, system task (these three main instances only), SSRF and DNS cache. Optional labels: `..._INCLUDE_WORKFLOW_ID_LABEL`, `..._NODE_TYPE_LABEL`, `..._CREDENTIAL_TYPE_LABEL`, `..._API_PATH_LABEL`, `..._API_METHOD_LABEL`, `..._API_STATUS_CODE_LABEL`. Labels multiply metric cardinality; enable only what dashboards need.

## Checked

2026-11-03. Read against the official n8n documentation pages:
- https://docs.n8n.io/deploy/host-n8n/configure-n8n/basic-configuration/use-environment-variables/endpoints

Confirmed: parameter names, defaults, limits, commands and behaviour in this skill match those pages. Nothing removed; every concrete claim matched the page.

Method: documentation only; no commands were run.
