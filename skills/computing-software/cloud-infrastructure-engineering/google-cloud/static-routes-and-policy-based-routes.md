---
id: computing-software.cloud-infrastructure-engineering.google-cloud.static-routes-and-policy-based-routes
name: static-routes-and-policy-based-routes
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, vpc, static-routes, policy-based-routes, nva, routing]
level: advanced
status: docs-checked
description: "Steer VPC traffic with static routes (next hops, tags, priority) and policy-based routes to an internal passthrough LB, e.g. forcing traffic through firewall appliances."
sources: ["https://docs.cloud.google.com/vpc/docs/routes", "https://docs.cloud.google.com/vpc/docs/static-routes", "https://docs.cloud.google.com/vpc/docs/use-policy-based-routes"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Static routes and policy-based routes

## 1. Route selection order
1. Policy-based routes: evaluated before any other type of route; they match on source range, destination range and protocol.
2. Subnet routes: evaluated after policy-based routes and before custom routes.
3. Custom routes (static and dynamic): lower priority number wins (0 is highest, 65,535 lowest). Routes with the same
   destination and priority can share traffic (ECMP) for next-hop types that support it.

## 2. Static routes
```bash
gcloud compute routes create egress-via-nva --network=<VPC> \
  --destination-range=0.0.0.0/0 --next-hop-ilb=fw-ilb-fr --next-hop-ilb-region=<R> \
  --priority=800 --tags=inspect
gcloud compute routes create onprem-backup --network=<VPC> --destination-range=10.50.0.0/16 \
  --next-hop-vpn-tunnel=tun-a --next-hop-vpn-tunnel-region=<R> --priority=2000
```
- Next hops: default internet gateway (`--next-hop-gateway`), instance by name/zone or by address, internal passthrough
  Network Load Balancer (`--next-hop-ilb`), and Classic VPN tunnel (`--next-hop-vpn-tunnel`).
- A static route without a network tag applies to the whole VPC network; with `--tags` it applies only to VMs with that tag
  (and tagged routes are never exchanged over VPC Network Peering).
- Deleting the default `0.0.0.0/0 → default-internet-gateway` route also breaks Private Google Access unless you add routes for `199.36.153.8/30` / `199.36.153.4/30`.

## 3. Policy-based routes
```bash
gcloud network-connectivity policy-based-routes create inspect-east-west \
  --network=projects/<P>/global/networks/<VPC> \
  --source-range=10.10.0.0/16 --destination-range=10.20.0.0/16 --ip-protocol=ALL \
  --protocol-version=IPV4 --next-hop-ilb-ip=10.0.0.10 --priority=100 --tags=app
```
Use them to force traffic between subnets through an NVA (subnet routes would otherwise win). Add a
higher-priority PBR with `--next-hop-other-routes=DEFAULT_ROUTING` to exempt the NVAs' own traffic and health checks.

## Gotchas
- A PBR next hop is an internal passthrough Network Load Balancer, or a next hop that skips other policy-based routes.
  Enable global access on that load balancer so it does not drop packets from other regions.
- A PBR with no tags applies to all egress packets matching it, including traffic from the load balancer's own backends: be careful.

## Verify
- [ ] `gcloud compute routes list` and `gcloud network-connectivity policy-based-routes list` show the routes.

## Checked
2026-10-28. Confirmed against the VPC pages "Routes", "Static routes" and "Use policy-based routes": evaluation order, priority
range, network-tag scoping, next-hop types, PBR next hops, tags and global access advice. Commands verified against the gcloud reference.
Removed: tie-break wording, `--can-ip-forward`, symmetric-return and VM-recreation claims, list `--filter` example.
Method: documentation only; no commands were run.
