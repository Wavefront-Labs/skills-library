---
id: computing-software.cloud-infrastructure-engineering.google-cloud.building-ha-vpn-with-gcloud
name: building-ha-vpn-with-gcloud
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, hybrid-connectivity, ha-vpn-gcloud, vpn-tunnel-setup, cloud-router, bgp]
level: advanced
status: docs-checked
description: "Build HA VPN to an on-prem peer with gcloud: VPN gateway, external peer gateway, Cloud Router with ASN, two tunnels, BGP sessions on link-local /30s, and the 99.99% SLA conditions."
sources: ["https://cloud.google.com/network-connectivity/docs/vpn/how-to/creating-ha-vpn", "https://cloud.google.com/network-connectivity/docs/vpn/concepts/topologies", "https://cloud.google.com/network-connectivity/docs/vpn/concepts/mtu-considerations", "https://cloud.google.com/sdk/gcloud/reference/compute/vpn-tunnels/create", "https://cloud.google.com/sdk/gcloud/reference/compute/routers/add-bgp-peer"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Building HA VPN with gcloud

## 1. Gateways and router
```bash
gcloud compute vpn-gateways create havpn-gw --network=VPC --region=REGION --stack-type=IPV4_ONLY
gcloud compute external-vpn-gateways create onprem-gw --interfaces=0=198.51.100.1,1=198.51.100.2
gcloud compute routers create havpn-router --network=VPC --region=REGION --asn=65010
```
The HA VPN gateway gets two public IPs (interface 0 and 1). For the 99.99% SLA there must be a tunnel from each gateway interface to the peer, with one peer gateway having one IP (`SINGLE_IP_INTERNALLY_REDUNDANT`), one peer with two IPs, or two peers with one IP each (`TWO_IPS_REDUNDANCY`). A single active interface or tunnel gives no availability SLA.

## 2. Tunnels
```bash
SECRET=$(openssl rand -base64 24)
for i in 0 1; do
gcloud compute vpn-tunnels create tun-$i --region=REGION --vpn-gateway=havpn-gw --interface=$i \
  --peer-external-gateway=onprem-gw --peer-external-gateway-interface=$i \
  --ike-version=2 --shared-secret="$SECRET" --router=havpn-router
done
```

## 3. BGP
```bash
gcloud compute routers add-interface havpn-router --region=REGION --interface-name=if-tun-0 \
  --ip-address=169.254.10.1 --mask-length=30 --vpn-tunnel=tun-0
gcloud compute routers add-bgp-peer havpn-router --region=REGION --peer-name=onprem-0 \
  --interface=if-tun-0 --peer-ip-address=169.254.10.2 --peer-asn=65001 --advertised-route-priority=100
# repeat with 169.254.11.0/30 and tun-1
```
Give on-prem the GCP public IPs, shared secret, link-local IPs and ASNs, and configure the device with ciphers from the Cloud VPN supported IKE ciphers page. BGP link-local addresses must be a /30 inside 169.254.0.0/16, each the first or second host, unique among the VPC's Cloud Routers.

## 4. Routing choices
- Active/active: identical advertised route priorities on both tunnels (omit `--advertised-route-priority`). Active/passive: unequal priorities, for example 10 and 20.
- Advertise custom ranges with `--advertisement-mode=CUSTOM` and `--set-advertisement-ranges`.
- With VPC global dynamic routing mode, every Cloud Router applies learned on-premises routes to all subnets of the VPC network.

## Gotchas
- SLA requires both tunnels up with BGP on both, and the topology matching a supported layout.
- MTU: the Cloud VPN gateway MTU is 1460 bytes and the payload MTU is lower after IPsec overhead; Cloud VPN clamps TCP MSS but does not fragment packets after encapsulation.
- BGP session up but no routes: check the peer's advertisements and the router's `--set-advertisement-*` settings.

## Verify
- [ ] `gcloud compute vpn-tunnels describe tun-0 --region=REGION --format='value(status,detailedStatus)'` is ESTABLISHED; `gcloud compute routers get-status havpn-router --region=REGION` shows both BGP peers UP and learned routes.

## Checked

- Date: 2026-10-27; documentation release: Google Cloud documentation pages as published on that date.
- Found wrong: the skill said one peer IP gives at most 99.9%. The topologies page gives 99.99% for one peer gateway with one IP (SINGLE_IP_INTERNALLY_REDUNDANT) as long as both gateway interfaces have a tunnel. The 1360 MSS value was not in documentation.
- Confirmed (gcloud reference): vpn-gateways create --network --stack-type (IPV4_ONLY default), external-vpn-gateways create --interfaces ID=IP, vpn-tunnels create --peer-external-gateway --peer-external-gateway-interface --ike-version --shared-secret --router, routers add-interface --ip-address --mask-length --vpn-tunnel, add-bgp-peer --advertised-route-priority --advertisement-mode.
- Confirmed (creating HA VPN page): link-local /30 in 169.254.0.0/16 rules, active-active versus active-passive priorities, custom advertisement flags, global dynamic routing behaviour, get-status command. Confirmed (MTU page): gateway MTU 1460, MSS clamping, no fragmentation after encapsulation.

Method: documentation only; no commands were run.
