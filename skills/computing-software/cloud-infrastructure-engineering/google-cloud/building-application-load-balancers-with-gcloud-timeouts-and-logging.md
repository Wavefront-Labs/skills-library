---
id: computing-software.cloud-infrastructure-engineering.google-cloud.building-application-load-balancers-with-gcloud-timeouts-and-logging
name: building-application-load-balancers-with-gcloud-timeouts-and-logging
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, cloud-load-balancing, gcloud-compute-backend-services, lb-gcloud-setup, backend-timeouts, lb-timeouts, lb-logging, lb-monitoring, health-checks]
level: practitioner
status: docs-checked
description: "Assemble a global external Application Load Balancer from gcloud pieces, set backend, keepalive and draining timeouts correctly, and use LB logs and metrics to debug 5xx and latency."
sources: ["https://cloud.google.com/load-balancing/docs/https/ext-https-lb-simple", "https://cloud.google.com/load-balancing/docs/backend-service", "https://cloud.google.com/load-balancing/docs/https/https-logging-monitoring", "https://cloud.google.com/load-balancing/docs/https/troubleshooting-ext-https-lbs", "https://cloud.google.com/load-balancing/docs/health-check-concepts", "https://cloud.google.com/sdk/gcloud/reference/compute/backend-services/create", "https://cloud.google.com/sdk/gcloud/reference/compute/target-https-proxies/create"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Building Application Load Balancers with gcloud: timeouts and logging

## 1. The chain
```bash
gcloud compute health-checks create http web-hc --port=8080 --request-path=/healthz --check-interval=5s --unhealthy-threshold=3
gcloud compute backend-services create web-bes --global --load-balancing-scheme=EXTERNAL_MANAGED \
  --protocol=HTTP --port-name=http --health-checks=web-hc --global-health-checks \
  --timeout=30s --connection-draining-timeout=60s --enable-logging --logging-sample-rate=0.2
gcloud compute backend-services add-backend web-bes --global --instance-group=web-mig --instance-group-region=europe-west2 \
  --balancing-mode=UTILIZATION --max-utilization=0.8
gcloud compute url-maps create web-um --default-service=web-bes
gcloud compute target-https-proxies create web-px --url-map=web-um --certificate-map=web-map --http-keep-alive-timeout-sec=610
gcloud compute addresses create web-ip --global
gcloud compute forwarding-rules create web-fr --global --load-balancing-scheme=EXTERNAL_MANAGED \
  --address=web-ip --target-https-proxy=web-px --ports=443
```
Firewall: allow the health check probe range `35.191.0.0/16` (IPv6 `2600:2d00:1:b029::/64`) to the backend port; see the health check concepts page for the current ranges.

## 2. Timeouts
| Setting | Where | Guidance |
|---|---|---|
| Backend service timeout (`--timeout`) | backend service | default 30 s; for Application Load Balancers it is the request and response timeout |
| Client HTTP keepalive | target proxy `--http-keep-alive-timeout-sec` | default 610 s; 5 to 1200 s on global external ALB |
| Backend keepalive | your server | set the web server's keepalive longer than the load balancer's 600 s; 620 s is recommended, or you get intermittent 502s |
| Connection draining | backend service | time for in-flight requests when a backend is removed |
Long uploads/streams: raise `--timeout` on that backend service only (separate path in the URL map).

## 3. Logs and metrics
```
resource.type="http_load_balancer"
httpRequest.status>=500
```
`jsonPayload.statusDetails` explains why the load balancer returned the status: `backend_timeout` (backend timed out generating a response), `failed_to_connect_to_backend` (including connection-phase timeouts), `backend_connection_closed_before_data_sent_to_client` (backend closed the connection early; see keepalive above), `response_sent_by_backend` (your app returned the status). Metrics: `loadbalancing.googleapis.com/https/request_count` by
`response_code_class`, and `https/total_latencies` vs `https/backend_latencies`.

## Gotchas
- The logging sample rate is 0.0 to 1.0 and defaults to 1.0; lower it on high-traffic load balancers and raise it during incidents.
- `gcloud compute backend-services create` defaults to `--load-balancing-scheme=EXTERNAL` (classic); `EXTERNAL_MANAGED` is the scheme used here.
- A health-check path that touches the database turns a database blip into all backends unhealthy.

## Verify
- [ ] `gcloud compute backend-services get-health web-bes --global` all HEALTHY.
- [ ] A 5xx breakdown by `statusDetails` is available from the load balancer logs.

## Checked

- Date: 2026-10-27; documentation release: Google Cloud documentation pages as published on that date.
- Found wrong: the 130.211.0.0/22 health check range is no longer listed (only 35.191.0.0/16 and the IPv6 range); a backend service that uses a global health check needs `--global-health-checks` (create synopsis lists `--global-health-checks | --health-checks-region`); the backend keepalive guidance is 'longer than 600 s, 620 s recommended' per the troubleshooting page.
- Confirmed (gcloud reference): `target-https-proxies create --certificate-map --http-keep-alive-timeout-sec` (default 610 s, 5 to 1200 s for global external ALB), `backend-services create --logging-sample-rate --connection-draining-timeout --enable-logging`, `health-checks create http --check-interval --unhealthy-threshold --request-path --port`, `add-backend --balancing-mode --max-utilization --instance-group-region`, load-balancing-scheme default EXTERNAL.
- Confirmed (backend service page): default backend service timeout 30 s, request and response timeout for Application Load Balancers. Confirmed (logging page): statusDetails values, logging sample rate 0.0 to 1.0 default 1.0, metric names request_count, total_latencies, backend_latencies, response_code_class.
- Removed: the WebSocket-lifetime and 'don't mix EXTERNAL and EXTERNAL_MANAGED' statements (not found in the pages read).

Method: documentation only; no commands were run.
