---
id: computing-software.cloud-infrastructure-engineering.google-cloud.network-hub-and-spoke-projects
name: network-hub-and-spoke-projects
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, landing-zone, hub-and-spoke, network-hub-project, network-connectivity-center, vpc-peering, shared-vpc, nva]
level: advanced
status: docs-checked
description: "Design hub-and-spoke networking across projects: hub project with hybrid links, spoke Shared VPC hosts, and the choice between NCC VPC spokes, VPC peering, VPN and NVAs."
sources: ["https://cloud.google.com/network-connectivity/docs/network-connectivity-center/concepts/vpc-spokes-overview", "https://cloud.google.com/vpc/docs/vpc-peering"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Network hub and spoke projects

## 1. Project layout
| Project | Holds |
|---|---|
| `net-hub` | hub VPC, Interconnect/HA VPN to on-prem, optional NVAs/Cloud NGFW, egress NAT |
| `net-spoke-prod`, `net-spoke-nonprod`, `net-spoke-dev` | one Shared VPC host each; service projects attach here |
Keep spokes per environment so prod/non-prod firewall and VPC-SC boundaries stay separate. (Project names are examples.)

## 2. Pick the spoke connectivity
| Method | Transitive | Notes |
|---|---|---|
| **NCC VPC spokes** | per hub topology: mesh connects all spokes; star has a center group and an edge group | managed; NCC does not connect spokes in the edge group to each other |
| VPC Network Peering | no | non-transitive: if A-B and A-C are peered, B and C are not connected; custom (static and dynamic) routes move only with `--export-custom-routes` on one side and `--import-custom-routes` on the other |
| HA VPN hub to spoke | via Cloud Router BGP | useful when NVAs must not be bypassed |
| NVA in hub | via routing to the appliance | route spoke traffic to an internal load balancer fronting the appliances; most operational load |

NCC star example:
```bash
gcloud network-connectivity hubs create corp-hub --project=net-hub --preset-topology=star
gcloud network-connectivity spokes linked-vpc-network create hub-vpc --project=net-hub --hub=corp-hub \
  --global --vpc-network=projects/net-hub/global/networks/hub --group=center
gcloud network-connectivity spokes linked-vpc-network create prod --project=net-spoke-prod \
  --hub=projects/net-hub/locations/global/hubs/corp-hub --global \
  --vpc-network=projects/net-spoke-prod/global/networks/prod --group=edge
```
Peering example:
```bash
gcloud compute networks peerings create hub-to-prod --project=net-hub --network=hub \
  --peer-project=net-spoke-prod --peer-network=prod --export-custom-routes
gcloud compute networks peerings create prod-to-hub --project=net-spoke-prod --network=prod \
  --peer-project=net-hub --peer-network=hub --import-custom-routes
```
NCC limits: you cannot use VPC Network Peering between two VPC spokes that are also connected through the same NCC hub, except between two spokes of the edge group in a star hub.

## Gotchas
- IP plan first: peered VPC networks cannot have overlapping subnet ranges (no range may match, contain or fit within another); peering fails if they do.
- Peering has per-peering-group quotas for subnet ranges and routes; check the quota pages before sizing.
- Changing topology later means re-attaching every service project; decide before onboarding workloads.

## Verify
- [ ] From a spoke VM: on-prem host reachable, other spoke unreachable (star edge) or reachable (mesh) as designed.
- [ ] `gcloud compute routers get-status <router> --region=<R> --project=net-hub` shows the BGP state and the routes learned and advertised.

## Checked
2026-10-31. Confirmed against the NCC VPC spokes overview (mesh and star presets, edge group not connected, peering limitation) and the VPC Network Peering page (non-transitive example, no overlapping subnets, `--export-custom-routes`/`--import-custom-routes`, per-peering-group quotas). gcloud commands and flags checked against the gcloud reference. Removed: the DNS peering/forwarding section, the "NCC is preferred / raises limits" opinions, the claim that spoke custom routes are not advertised to on-prem automatically, and the HA VPN per-tunnel bandwidth remark (not on the pages read); the architecture-blueprint URLs were not fetched and are no longer cited.
Method: documentation only; no commands were run.
