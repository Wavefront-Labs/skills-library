---
id: computing-software.cloud-infrastructure-engineering.google-cloud.troubleshooting-load-balancer-502-and-503-errors
name: troubleshooting-load-balancer-502-and-503-errors
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, cloud-load-balancing, lb-502-errors, load-balancer-5xx, statusdetails, backend-connection-closed, failed-to-pick-backend]
level: practitioner
status: docs-checked
description: "Fix 502/503 responses from Google Cloud Application Load Balancers using statusDetails in LB logs: no healthy backends, keepalive mismatches, timeouts, and serverless NEG errors."
sources: ["https://cloud.google.com/load-balancing/docs/https/https-logging-monitoring#statusdetail_http_failure_messages", "https://cloud.google.com/load-balancing/docs/https/troubleshooting-ext-https-lbs", "https://cloud.google.com/load-balancing/docs/https#timeouts_and_retries"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Troubleshooting load balancer 502 and 503 errors

## Get statusDetails
Enable logging on the backend service (`--enable-logging --logging-sample-rate=1.0` while
debugging), then:
```
resource.type="http_load_balancer" httpRequest.status>=500
```
```bash
gcloud logging read 'resource.type="http_load_balancer" AND httpRequest.status>=500' --freshness=1h \
  --format="table(timestamp,httpRequest.status,jsonPayload.statusDetails,httpRequest.requestUrl)" --limit=50
```

## statusDetails cheat sheet
| statusDetails | Cause | Fix |
|---|---|---|
| `failed_to_pick_backend` / `failed_to_pick_backend_by_hash` (502, 503) | no healthy backend: all regions at capacity, no backend for the computed hash, or none matching the config; also seen when no firewall rule allows health checks | verify backend health, health check port/path/protocol, firewall for prober range 35.191.0.0/16; drain unhealthy instance groups by setting capacity to zero (failover is limited to a few alternate groups) |
| `backend_connection_closed_before_data_sent_to_client` (502, 503) | backend or an intermediate device closed the connection before the response; on GKE with NEG backends, pods scaling down or terminating | set the backend web server HTTP keepalive timeout above the load balancer's 600-second timeout (Google recommends 620 seconds); on GKE raise `terminationGracePeriodSeconds` |
| `backend_timeout` | backend connected but did not respond within the backend service timeout | increase the backend service timeout, or fix backend slowness |
| `backend_connection_closed_after_partial_response_sent` | backend connection closed after a partial response; status 0 means incomplete headers | app logs, memory limits |
| `failed_to_connect_to_backend` (502, 503) | no SYN-ACK from the backend, or an internal or network disruption | check firewall allows 35.191.0.0/16, the app listens on the configured port, backend CPU/memory/connections |
| `backend_early_response_with_non_error_status` (502, 503) | backend sent a 1XX/2XX before reading the full request body | fix the backend to read the body before responding |
| `response_sent_by_backend` | the backend itself returned the 5xx | app problem |
| `client_disconnected_before_any_response` (status 0) | client connection broke before any response | slowness or client timeout |
| `retriable_error` (503) | IaC tools replacing URL map rules, or transient config propagation | update URL maps in place; wait a few minutes after changes |

The classic Application Load Balancer reports every load-balancer-generated error as 502; the global and regional external ALBs return meaningful codes such as 503 and 504.

## Backend health
```bash
gcloud compute backend-services get-health web-be --global
```

## Gotchas
- The default backend service timeout is 30 seconds (except serverless NEGs); on internal Application Load Balancers idle websocket connections close at that timeout. Websocket timeouts differ by load balancer type.
- Configuration changes to the global external ALB (adding or removing a backend service) can cause a brief burst of 502 with `failed_to_pick_backend` while changes propagate.

## Verify
- [ ] After the fix, 5xx rate by statusDetails drops to baseline over a full traffic cycle.

## Checked
Date: 2026-10-28. Confirmed against the Application Load Balancer troubleshooting page, the statusDetail HTTP failure messages table and the timeouts/backend-service pages: statusDetails names, causes and status codes, the 600-second load balancer timeout with the 620-second keepalive recommendation, 35.191.0.0/16 prober range, 30-second default timeout, websocket idle behaviour, classic ALB 502 behaviour. gcloud flags checked against the CLI reference. Removed: `no_healthy_backend`, the 610-second classic keepalive, the 130.211.0.0/22 range, the serverless NEG and ingress row, the connection-draining 502 burst claim and the `proxyStatus` remark (not on the pages); the nginx and Node keepalive snippets.
Method: documentation only; no commands were run.
