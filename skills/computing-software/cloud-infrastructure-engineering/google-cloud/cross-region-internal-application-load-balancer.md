---
id: computing-software.cloud-infrastructure-engineering.google-cloud.cross-region-internal-application-load-balancer
name: cross-region-internal-application-load-balancer
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, cloud-load-balancing, cross-region-internal-alb, internal-load-balancer, multi-region, failover]
level: advanced
status: docs-checked
description: "Build a cross-region internal Application Load Balancer: proxy-only subnets per region, global backend service, regional forwarding rules, DNS geo routing and failover."
sources: ["https://cloud.google.com/load-balancing/docs/l7-internal/setting-up-l7-cross-reg-internal", "https://cloud.google.com/load-balancing/docs/l7-internal", "https://cloud.google.com/dns/docs/zones/manage-routing-policies"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cross-region internal Application Load Balancer

Internal L7 load balancer whose backends span regions, with a frontend IP in each region.
Clients use their local VIP; if local backends fail, traffic goes to healthy backends elsewhere.

## 1. Network prerequisites
```bash
for R in us-east1 us-west1; do
  gcloud compute networks subnets create proxy-only-$R --network=<VPC> --region=$R \
    --range=10.129.$([ $R = us-east1 ] && echo 0 || echo 1).0/23 \
    --purpose=GLOBAL_MANAGED_PROXY --role=ACTIVE
done
```
Purpose `GLOBAL_MANAGED_PROXY` (not `REGIONAL_MANAGED_PROXY`). Firewall: allow from proxy-only ranges and health-check ranges to backends.

## 2. Global resources
```bash
gcloud compute health-checks create http hc-app --global --port=8080 --request-path=/healthz
gcloud compute backend-services create be-app --global --load-balancing-scheme=INTERNAL_MANAGED \
  --protocol=HTTP --health-checks=hc-app --global-health-checks
gcloud compute backend-services add-backend be-app --global --instance-group=app-east --instance-group-region=us-east1
gcloud compute backend-services add-backend be-app --global --instance-group=app-west --instance-group-region=us-west1
gcloud compute url-maps create um-app --default-service=be-app --global
gcloud compute target-http-proxies create tp-app --url-map=um-app --global
```

## 3. Regional frontends
```bash
gcloud compute forwarding-rules create fr-app-east --global --load-balancing-scheme=INTERNAL_MANAGED \
  --network=<VPC> --subnet=app-subnet-east --subnet-region=us-east1 --address=10.1.0.50 \
  --ports=80 --target-http-proxy=tp-app
# same for us-west1
```

## 4. DNS
Cloud DNS geolocation routing policy with health checks so clients get the nearest healthy VIP:
`gcloud dns record-sets create app.internal. --zone=<Z> --type=A --ttl=30 --routing-policy-type=GEO --routing-policy-data="us-east1=fr-app-east@global;us-west1=fr-app-west@global" --enable-health-checking`
(each global forwarding rule is referenced as `NAME@global`; the Google example uses a 30 second TTL).

## Gotchas
- HTTPS needs Certificate Manager certificates (the Google example creates them with `--scope=all-regions`), not classic SSL certificates.
- The forwarding rule IP comes from the regional subnet, not the proxy-only subnet (creation fails otherwise). There can be only one active proxy-only subnet per purpose, per region, per network.
- In a standard Shared VPC deployment the load balancer uses IP addresses and subnets from the host project.

## Verify
- [ ] Draining the east instance group sends east-client requests to west (check backend logs); DNS answers switch when a VIP's backends are unhealthy.

## Checked
Date: 2026-10-28. Confirmed against the cross-region internal Application Load Balancer setup page and the internal Application Load Balancer overview: `GLOBAL_MANAGED_PROXY` purpose and one proxy-only subnet per region, `--global-health-checks`, forwarding rule address must not come from the proxy-only subnet, `--scope=all-regions` Certificate Manager certificate, GEO routing policy with `--enable-health-checking`, `@global` forwarding rule references, 30 second TTL; gcloud flags (including `--instance-group-region`, `--max-rate-per-instance`) verified against the CLI reference. Removed: the "global access is inherent" and nearest-region spillover claims (not found on the pages). Addresses and names are examples.
Method: documentation only; no commands were run.
