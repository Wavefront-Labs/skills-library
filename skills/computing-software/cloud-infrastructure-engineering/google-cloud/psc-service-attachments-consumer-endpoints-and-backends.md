---
id: computing-software.cloud-infrastructure-engineering.google-cloud.psc-service-attachments-consumer-endpoints-and-backends
name: psc-service-attachments-consumer-endpoints-and-backends
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, private-service-connect, psc-service-attachment, published-services, psc-consumer-endpoint, psc-forwarding-rule, psc-backends, psc-neg]
level: advanced
status: docs-checked
description: "Publish an internal service with a Private Service Connect service attachment, consume it via endpoint forwarding rules or PSC backends (NEGs) behind your own load balancer."
sources: ["https://docs.cloud.google.com/vpc/docs/configure-private-service-connect-producer", "https://docs.cloud.google.com/vpc/docs/configure-private-service-connect-services", "https://docs.cloud.google.com/vpc/docs/private-service-connect-backends"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# PSC: service attachments, consumer endpoints and backends

PSC connects consumer and producer VPCs **without peering or shared IP space**: the consumer gets a
private IP in its own VPC; the producer sees connections NATed from a PSC subnet.

## 1. Producer: publish
```bash
gcloud compute networks subnets create psc-nat --network=svc-vpc --region=europe-west2 \
  --range=10.250.0.0/24 --purpose=PRIVATE_SERVICE_CONNECT
gcloud compute service-attachments create orders-sa --region=europe-west2 \
  --producer-forwarding-rule=orders-ilb-fr --nat-subnets=psc-nat \
  --connection-preference=ACCEPT_MANUAL --consumer-accept-list=<CONSUMER_PROJECT>=10 \
  --enable-proxy-protocol=false
gcloud compute service-attachments describe orders-sa --region=europe-west2 --format='yaml(connectedEndpoints)'
```
The producer forwarding rule belongs to the producer's load balancer (see "Features and compatibility" in the PSC docs for
supported types). Size the NAT subnet for expected consumer connections: an exhausted NAT subnet makes connections
`NEEDS_ATTENTION`. Allow traffic from the sources the producer docs list (and health-check probes) in producer firewall rules.

## 2. Consumer: endpoint
```bash
gcloud compute addresses create orders-ep-ip --region=europe-west2 --subnet=app-subnet --addresses=10.10.5.20
gcloud compute forwarding-rules create orders-ep --region=europe-west2 --network=prod \
  --address=orders-ep-ip \
  --target-service-attachment=projects/<PRODUCER_P>/regions/europe-west2/serviceAttachments/orders-sa
gcloud compute forwarding-rules describe orders-ep --region=europe-west2 --format='value(pscConnectionStatus)'   # ACCEPTED
```
Add a private DNS record (`orders.internal.example.com → 10.10.5.20`). Global access for clients in
other regions: `--allow-psc-global-access`.

## 3. Consumer: PSC backends (NEG)
When the consumer wants its own LB features (TLS cert, Cloud Armor, URL routing, failover, logging):
```bash
gcloud compute network-endpoint-groups create orders-psc-neg --region=europe-west2 \
  --network-endpoint-type=private-service-connect \
  --psc-target-service=projects/<PRODUCER_P>/regions/europe-west2/serviceAttachments/orders-sa \
  --network=prod --subnet=app-subnet
# then use it as a backend of an internal or external Application LB backend service
```
Backend services with PSC NEGs do not support health checks.

## Gotchas
- `ACCEPT_AUTOMATIC` skips manual approval; prefer `ACCEPT_MANUAL` with an accept list (`PROJECT=LIMIT`).
- Producer sees NAT IPs; enable PROXY protocol (only where the target service supports it) if it needs consumer connection details.
- `pscConnectionStatus` values: `PENDING` (waiting for the producer), `ACCEPTED`, `REJECTED`, `NEEDS_ATTENTION`, `CLOSED`.

## Verify
- [ ] Consumer VM reaches the service via the endpoint IP/DNS name; producer logs show the PSC NAT source.
- [ ] Service attachment lists only expected consumer projects.

## Checked
2026-10-28. Confirmed against the PSC producer, consumer-services and backends pages and the Compute API v1 discovery document
(`pscConnectionStatus`, `allowPscGlobalAccess`, `connectionPreference`, `enableProxyProtocol`, `consumerAcceptLists`). Commands verified against
the gcloud reference. Removed: supported-producer-LB list, PSC NEG target list, and the REJECTED=not-on-list explanation.
Method: documentation only; no commands were run.
