---
id: computing-software.cloud-infrastructure-engineering.google-cloud.cloud-load-balancing-selection-and-backends
name: cloud-load-balancing-selection-and-backends
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, cloud-load-balancing, load-balancer, global-external-alb, regional-external-alb, internal-load-balancer, internal-alb, passthrough-nlb, proxy-nlb, backend-service, url-map, health-checks, serverless-neg, hybrid-neg, internet-neg, balancing-mode, session-affinity, connection-draining, proxy-only-subnet, anycast, envoy]
level: practitioner
status: docs-checked
description: "Pick the right Cloud Load Balancer and build it in order: backend service, NEG types, health checks and firewall, balancing modes, URL maps, proxy-only subnet."
sources: ["https://cloud.google.com/load-balancing/docs/choosing-load-balancer", "https://cloud.google.com/load-balancing/docs/https", "https://cloud.google.com/load-balancing/docs/backend-service", "https://cloud.google.com/load-balancing/docs/health-check-concepts", "https://cloud.google.com/load-balancing/docs/negs", "https://cloud.google.com/load-balancing/docs/l7-internal/proxy-only-subnets"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cloud Load Balancing selection and backends

**Goal:** one decision table to choose the balancer, one command sequence to build it, and
the five things that make a backend show UNHEALTHY when the app is fine.

## 1. Choose
| Need | Balancer | Notes |
|---|---|---|
| HTTP(S) from the internet, one anycast IP worldwide, CDN/Armor/IAP | **Global external Application LB** | Envoy-based; Premium Tier only |
| HTTP(S) from the internet, must stay in one region (residency, Standard Tier) | Regional external Application LB | needs proxy-only subnet |
| HTTP(S) inside the VPC (microservices, internal apps) | **Internal Application LB** (regional or cross-region) | needs proxy-only subnet |
| TCP/SSL proxying from the internet (non-HTTP, TLS offload) | Global/regional external Proxy Network LB | terminates the client connection at a proxy |
| TCP/UDP/any protocol, preserve client IP, no proxy | **External passthrough Network LB** (regional) | no proxy; backend sees the client IP |
| Same but internal | Internal passthrough Network LB | for internal TCP/UDP traffic |
Classic (pre-Envoy) variants still exist; choose the "(new)" Envoy ones for new work.

## 2. Build order (global external ALB example)
```bash
gcloud compute addresses create web-ip --global --ip-version=IPV4
gcloud compute health-checks create http web-hc --port=8080 --request-path=/healthz \
  --check-interval=10s --timeout=5s --healthy-threshold=2 --unhealthy-threshold=3 --global
gcloud compute backend-services create web-bs --global --load-balancing-scheme=EXTERNAL_MANAGED \
  --protocol=HTTP --port-name=http --health-checks=web-hc --timeout=30s \
  --connection-draining-timeout=60 --enable-logging --logging-sample-rate=1.0
gcloud compute backend-services add-backend web-bs --global --instance-group=web-mig --instance-group-region=europe-west1 \
  --balancing-mode=UTILIZATION --max-utilization=0.8 --capacity-scaler=1
gcloud compute url-maps create web-map --default-service=web-bs
gcloud compute target-https-proxies create web-proxy --url-map=web-map --certificate-map=web-certs   # or --ssl-certificates
gcloud compute forwarding-rules create web-fr --global --address=web-ip --target-https-proxy=web-proxy --ports=443 --load-balancing-scheme=EXTERNAL_MANAGED
```
Firewall for health checks and (for ALBs) proxy traffic: allow the probe ranges listed on the health check concepts page (for example `35.191.0.0/16`) to the backend port, plus the **proxy-only subnet range** for regional/internal ALBs. Without this the backend is UNHEALTHY forever.

## 3. Backends and NEGs
| Backend | Use |
|---|---|
| Instance group (MIG, `--port-name` → named port on the group) | VMs |
| **Zonal NEG** (`GCE_VM_IP_PORT`) | GKE pods (container-native), hand-registered VM IP:ports |
| **Serverless NEG** | Cloud Run / Functions / App Engine behind an ALB (`--network-endpoint-type=serverless --cloud-run-service=`) |
| **Internet NEG** | external origin (FQDN/IP) behind the LB for CDN/Armor on third-party backends |
| **Hybrid NEG** (`NON_GCP_PRIVATE_IP_PORT`) | on-prem endpoints via VPN/Interconnect |
| **PSC NEG** | published services via Private Service Connect |
| Backend bucket | GCS static content (`backend-buckets create --gcs-bucket-name`) |
- **Balancing mode**: `UTILIZATION` (approximate CPU utilisation of VMs in an instance-group zone), `RATE` (new HTTP requests per second; `--max-rate-per-instance`/`--max-rate-per-endpoint`), `IN_FLIGHT` (in-flight requests; use instead of RATE when requests take over a second), `CONNECTION` (new TCP connections), `CUSTOM_METRICS`. Regional passthrough Network LB backends use `CONNECTION` but have no target capacity or capacity scaler; internet, serverless and PSC NEGs support none of these parameters.
- `--capacity-scaler=0` drains a backend without removing it (canary off); 0 is not allowed when the service has only one backend, otherwise values run 0.1 to 1.0.
- Session affinity (`--session-affinity=GENERATED_COOKIE|CLIENT_IP|HEADER_FIELD`) + `--affinity-cookie-ttl`; locality LB policy (`--locality-lb-policy=MAGLEV|RING_HASH|LEAST_REQUEST`) on Envoy LBs.
- Outlier detection and circuit breaking (`--outlier-detection-*`, `--max-connections`) for Envoy-based backends.

## 4. URL maps and routing
`gcloud compute url-maps add-path-matcher web-map --path-matcher-name=api --default-service=api-bs --path-rules='/api/*=api-bs,/static/*=static-bucket'` plus host rules; advanced **route rules** (YAML import via `url-maps import`) give header/query matching, weighted splits (canary), rewrites, redirects, retries, timeouts, CORS, fault injection. `url-maps validate` tests a map before use.

## 5. Health checks (why it is UNHEALTHY)
1. Firewall lacks the probe ranges / proxy-only subnet.
2. Named port on the MIG does not exist or points at a port the app does not listen on (`instance-groups set-named-ports`).
3. HC path returns a redirect (301 ≠ 200) or needs a Host header (`--host`).
4. The app binds `127.0.0.1` instead of `0.0.0.0`.
5. Protocol mismatch: HTTPS backend with HTTP health check.
`gcloud compute backend-services get-health web-bs --global` shows per-endpoint state; LB logs (`resource.type="http_load_balancer"`) carry a `statusDetails` field explaining why a request failed.

## Gotchas
- One **proxy-only subnet** (`--purpose=REGIONAL_MANAGED_PROXY`, /26 or shorter, /23 recommended) per region per VPC for regional/internal ALBs; forgetting it is the most common ILB failure (creation succeeds, nothing routes).
- Global external ALB needs **Premium Tier**; the regional external ALB supports Premium or Standard Tier.
- Forwarding rule `--load-balancing-scheme` must match the backend service's (`EXTERNAL_MANAGED` vs `EXTERNAL`); mixing them fails.
- The backend service timeout kills long polls and uploads; raise it for WebSockets.
- Deleting in the wrong order fails: forwarding rule → proxy → url-map → backend service → health check.

## Verify
- [ ] `get-health` shows HEALTHY for every endpoint; curl to the LB IP with the Host header returns 200 within a minute of creation.
- [ ] LB logs show no failure `statusDetails` for normal traffic and the backend sees `X-Forwarded-For` with the client IP.
- [ ] Setting `--capacity-scaler=0` on one backend drains it with no 5xx (connection draining respected).
- [ ] A weighted route rule 90/10 is observed in backend request counts.

## Checked
2026-10-28. Confirmed against the backend service, proxy-only subnet, choosing-a-load-balancer and health check concepts pages: balancing modes and capacity scaler rules, which backends support them, proxy-only subnet purpose, size (/26 or shorter, /23 recommended) and one active per VPC and region, Premium/Standard Tier support, REGIONAL_MANAGED_PROXY. All gcloud commands and flags passed check_commands. Removed: the 130.211.0.0/22 literal range, the 30 s default, the MIG-only and mixed-mode claims, statusDetails values, cross-region and loopback notes.
Method: documentation only; no commands were run.
