---
id: computing-software.cloud-infrastructure-engineering.contour.contour-health-endpoints
name: contour-health-endpoints
category: computing-software
field: cloud-infrastructure-engineering
product: contour
tags: [health, healthz, health-port, health-address, port-8000, kubernetes-probes]
level: intro
status: docs-checked
description: "Contour's /health and /healthz endpoints on 0.0.0.0:8000, changing them with --health-address and --health-port, and keeping the Service manifest in step."
sources: ["https://github.com/projectcontour/contour/blob/main/site/content/docs/main/guides/health-checking.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Contour health endpoints

Contour exposes two health endpoints, `/health` and `/healthz`. By default both are served on `0.0.0.0:8000`.

Change the listener with `contour serve` flags:
- `--health-address` sets the bind address.
- `--health-port` sets the port. For example `--health-port 9999` creates a health listener on `0.0.0.0:9999`.

The Service manifest used to install Contour must be updated to the same port, otherwise probes and any Service-based checks look at the wrong port.

What it checks: the health endpoints perform a connection to the Kubernetes cluster's API.

Note the distinction from metrics: `--http-address`/`--http-port` configure the Prometheus `/metrics` listener, which also defaults to port 8000, so if you move one of the two to avoid a clash, update the Service port to match.

## Checked

2026-11-04. Confirmed against the Contour health checking guide (guides/health-checking.md) and the configuration reference: the fields, defaults, flags and behaviours stated above. Removed: the probe-wiring advice and the paragraph on what readiness/liveness imply (the page only says the endpoints connect to the Kubernetes API).

Method: documentation only; no commands were run.
