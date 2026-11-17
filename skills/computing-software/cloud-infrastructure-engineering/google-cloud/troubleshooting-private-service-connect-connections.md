---
id: computing-software.cloud-infrastructure-engineering.google-cloud.troubleshooting-private-service-connect-connections
name: troubleshooting-private-service-connect-connections
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, private-service-connect, psc-troubleshooting, psc-endpoint-status, nat-subnet, connectivity-tests]
level: practitioner
status: docs-checked
description: "Debug PSC endpoints and service attachments: endpoint pscConnectionStatus, accept lists and NAT subnets, producer metrics, and connectivity tests."
sources: ["https://cloud.google.com/vpc/docs/monitor-private-service-connect-connections", "https://cloud.google.com/network-intelligence-center/docs/connectivity-tests/concepts/overview", "https://www.googleapis.com/discovery/v1/apis/compute/v1/rest"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Troubleshooting Private Service Connect connections

## Consumer side
```bash
gcloud compute forwarding-rules describe <EP> --region=<R> \
  --format="yaml(pscConnectionStatus,pscConnectionId,target,IPAddress,allowPscGlobalAccess)"
```
`pscConnectionStatus` values (Compute API ForwardingRule):

| Value | Meaning |
|---|---|
| `ACCEPTED` | accepted by the producer; look at DNS, firewall, routes, producer backends |
| `PENDING` | pending acceptance by the producer (check the producer's connection preference and accept list) |
| `REJECTED` | rejected by the producer |
| `NEEDS_ATTENTION` | accepted, but the producer must take further action before the forwarding rule can serve traffic |
| `CLOSED` | closed by the producer; will not serve traffic |

## Producer side
```bash
gcloud compute service-attachments describe <SA> --region=<R> \
  --format="yaml(connectionPreference,consumerAcceptLists,natSubnets,connectedEndpoints)"
```
- `connectionPreference` is `ACCEPT_AUTOMATIC` or `ACCEPT_MANUAL`; `consumerAcceptLists` says which consumer projects or networks may connect; `natSubnets` lists the NAT subnets.
- A NAT subnet has purpose `PRIVATE_SERVICE_CONNECT`.
- Watch NAT usage with the producer metrics `private_service_connect/producer/used_nat_ip_addresses` and `nat_ip_address_capacity` (prefix `compute.googleapis.com/`), plus `connected_consumer_forwarding_rules`, `open_connections` and `dropped_received_packets_count`.

## Path test
```bash
gcloud network-management connectivity-tests create psc-test \
  --source-instance=projects/<P>/zones/<Z>/instances/client-1 \
  --destination-forwarding-rule=projects/<P>/regions/<R>/forwardingRules/<EP> \
  --destination-port=443 --protocol=TCP
gcloud network-management connectivity-tests describe psc-test --format="yaml(reachabilityDetails)"
```

## Verify
- [ ] Endpoint `ACCEPTED` and the connectivity test reports the path reachable.

## Checked
2026-10-28. Confirmed via the Compute API discovery document (ForwardingRule `pscConnectionStatus` enum and meanings, `pscConnectionId`, `allowPscGlobalAccess`; ServiceAttachment `connectionPreference`, `consumerAcceptLists`, `natSubnets`, `connectedEndpoints`; Subnetwork purpose `PRIVATE_SERVICE_CONNECT`), the PSC monitoring page (metric names) and check_commands.py (gcloud commands and flags). Removed: the PSC troubleshooting page citation (returned 404), claims that NEEDS_ATTENTION means NAT exhaustion, REJECTED meaning connection limit, producer source-IP/firewall and health advice, global-access and routing gotchas, DNS advice.
Method: documentation only; no commands were run.
