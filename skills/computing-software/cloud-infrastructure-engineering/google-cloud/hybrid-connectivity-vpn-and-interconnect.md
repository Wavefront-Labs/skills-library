---
id: computing-software.cloud-infrastructure-engineering.google-cloud.hybrid-connectivity-vpn-and-interconnect
name: hybrid-connectivity-vpn-and-interconnect
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, cloud-vpn, ha-vpn, cloud-interconnect, dedicated-interconnect, partner-interconnect, cross-cloud-interconnect, vlan-attachments, cloud-router, bgp, dynamic-routing-mode, global-routing, custom-route-advertisements, macsec, interconnect-redundancy, 99-99-sla, hybrid-connectivity, network-connectivity-center, router-appliance]
level: advanced
status: docs-checked
description: "Connect on-prem and other clouds to GCP: HA VPN with BGP on Cloud Router, Dedicated/Partner/Cross-Cloud Interconnect, route advertisement, MACsec, NCC hub-and-spoke."
sources: ["https://docs.cloud.google.com/network-connectivity/docs/vpn/concepts/overview", "https://docs.cloud.google.com/network-connectivity/docs/vpn/how-to/creating-ha-vpn", "https://docs.cloud.google.com/network-connectivity/docs/interconnect/concepts/overview", "https://docs.cloud.google.com/network-connectivity/docs/interconnect/concepts/dedicated-overview", "https://docs.cloud.google.com/network-connectivity/docs/interconnect/tutorials/dedicated-creating-9999-availability", "https://docs.cloud.google.com/network-connectivity/docs/router/concepts/overview", "https://docs.cloud.google.com/network-connectivity/docs/network-connectivity-center/concepts/overview"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Hybrid connectivity: Cloud VPN and Cloud Interconnect

**Goal:** a private path between your datacentre/other cloud and every GCP VPC that
survives any single device or edge-availability-domain failure, learns routes dynamically, and has a measured bandwidth ceiling.

## 1. Choose
| Option | Bandwidth | SLA | Use |
|---|---|---|---|
| **HA VPN** (IPsec over internet) | 3 Gbps per tunnel (multiple tunnels) | 99.99% or 99.9% depending on topology (see HA VPN topologies) | quick start, DR path, branch |
| **Dedicated Interconnect** | 10 Gbps or 100 Gbps links | 99.99% (critical production) or 99.9% (non-critical production) by configuration | you are in a colo with a Google PoP |
| **Partner Interconnect** | 50 Mbps to 50 Gbps per VLAN attachment (sizes depend on the partner) | same reliability options | no colo presence; a partner provides the connection |
| **Cross-Cloud Interconnect** | see the Cross-Cloud Interconnect pages | see the Interconnect overview | direct to other cloud providers |
| Classic VPN | static routing only | 99.9% | legacy; HA VPN is the replacement |
Interconnect does not encrypt traffic by default: use **MACsec** on supported circuits or deploy HA VPN over Cloud Interconnect for IPsec.

## 2. HA VPN with BGP
```bash
gcloud compute routers create cr-prod --network=prod-vpc --region=europe-west1 --asn=65001 \
  --advertisement-mode=CUSTOM --set-advertisement-groups=ALL_SUBNETS --set-advertisement-ranges=199.36.153.4/30=restricted-googleapis
gcloud compute vpn-gateways create ha-gw --network=prod-vpc --region=europe-west1          # 2 interfaces, 2 public IPs
gcloud compute external-vpn-gateways create onprem --interfaces=0=203.0.113.1,1=203.0.113.2  # 2 peer devices
for i in 0 1; do for j in 0 1; do
  gcloud compute vpn-tunnels create t-$i-$j --region=europe-west1 --vpn-gateway=ha-gw --interface=$i \
    --peer-external-gateway=onprem --peer-external-gateway-interface=$j --router=cr-prod \
    --ike-version=2 --shared-secret=<FROM_SECRET_MANAGER>
  gcloud compute routers add-interface cr-prod --interface-name=if-$i-$j --vpn-tunnel=t-$i-$j --ip-address=169.254.$i$j.1 --mask-length=30 --region=europe-west1
  gcloud compute routers add-bgp-peer cr-prod --peer-name=p-$i-$j --interface=if-$i-$j --peer-ip-address=169.254.$i$j.2 --peer-asn=65000 --region=europe-west1
done; done
```
- An HA VPN gateway with only one active interface gets no availability SLA; see the HA VPN topologies page for which layouts reach 99.99% or 99.9%. Google-to-Google HA VPN (two VPCs) uses `--peer-gcp-gateway`.
- BGP sessions use link-local addresses from `169.254.0.0/16`; set `--advertised-route-priority` on the peer to prefer one tunnel.
- BFD can be enabled on BGP peers (`--bfd-session-initialization-mode=ACTIVE`); cipher suites must match the peer (see the supported IKE ciphers page).

## 3. Dedicated Interconnect, 99.99 % pattern
- For 99.99% follow the Google tutorial "Dedicated Interconnect 99.99% availability" (circuits in two metros, four VLAN attachments); after the cross-connects are live, create attachments, for example `gcloud compute interconnects attachments dedicated create att-a1 --interconnect=ic-a1 --router=cr-ew1 --region=europe-west1 --vlan=100 --bandwidth=10g --encryption=NONE|IPSEC`.
- Cloud Router provides the BGP sessions for the attachments (the 99.99% tutorial pairs attachments across regions and metros); `--mtu` on the attachment must match the VPC network MTU.
- **Partner**: `attachments partner create --edge-availability-domain=availability-domain-1` → pairing key → partner portal → `attachments partner update --admin-enabled`; L3 partners run BGP for you, L2 partners pass BGP to your router.
- Cloud Router advertisement: `DEFAULT` (all subnets of the region, or all regions if **global dynamic routing**) vs `CUSTOM` (subnets + extra prefixes like the `private.googleapis.com` VIP, PSA ranges for Cloud SQL, GKE pod ranges — these are *not* advertised unless you add them). Learned routes get priority from `--advertised-route-priority` on the peer; `--enable-ipv6` for dual stack.
- **Dynamic routing mode** on the VPC: `REGIONAL` vs `GLOBAL` (global dynamic routing lets one Interconnect serve all regions of the VPC).

## 4. Many VPCs: NCC
**Network Connectivity Center** hub with **VLAN attachment / VPN tunnel / router-appliance spokes** turns one Interconnect into site-to-site data transfer and shares it with multiple VPC spokes (`gcloud network-connectivity hubs create`, `spokes linked-vpc-network create`). Alternatives: Shared VPC (one host network, simplest), or VPC peering with `--export-custom-routes`/`--import-custom-routes` so on-prem routes propagate one hop.

## 5. Operate
- Alert on BGP session and tunnel state changes and on attachment utilisation (pick the metrics from the Cloud Monitoring VPN, Interconnect and Cloud Router metric lists).
- `gcloud compute routers get-status cr-prod --region=…` shows BGP state and learned prefixes; **Connectivity Tests** (Network Intelligence Center) validate a path end-to-end including firewall.
- Throughput ceiling for VPN: 3 Gbps per tunnel, so use multiple tunnels.
- The on-prem and VPC IP address ranges must not overlap, or traffic is not routed properly — plan IP space.

## Gotchas
- Forgetting custom advertisement of the restricted/private Google APIs VIP means on-prem cannot use Private Google Access over Interconnect.
- HA VPN supports a peer behind NAT using NAT-T; see the Cloud VPN overview for the requirements.
- With `REGIONAL` dynamic routing, only subnets in the attachment's region are reachable over it.

## Checked
2026-10-31. Confirmed against the Cloud VPN overview (HA VPN 99.99% or 99.9% by topology, single active interface has no SLA, Classic VPN 99.9% and static routing, 3 Gbps per tunnel, NAT-T), the Cloud Interconnect overview (50 Mbps to 50 Gbps Partner attachments, 100 Gbps connections, 99.99% and 99.9% reliability options, no encryption by default, MACsec and HA VPN over Interconnect, custom advertisements for Private Google Access, non-overlapping ranges) and the Dedicated Interconnect pages. gcloud flags were verified by check_commands. Removed unconfirmed: Cross-Cloud bandwidth and SLA, partner names, 5 Gbps step, MTU values, metric names, 70 percent threshold, dataplane remark, BFD timing, circuit-count SLA mapping.
Method: documentation only; no commands were run.

## Verify
- [ ] All four VPN tunnels `ESTABLISHED`, four BGP sessions `UP`; failing one on-prem device or interface leaves traffic flowing on the other.
- [ ] `routers get-status` lists on-prem prefixes as learned; on-prem router sees GCP subnets + the custom VIP ranges.
- [ ] Interconnect: a throughput test across an attachment approaches the attachment bandwidth.
- [ ] Connectivity Test from an on-prem IP to a GCP VM port passes end-to-end.
