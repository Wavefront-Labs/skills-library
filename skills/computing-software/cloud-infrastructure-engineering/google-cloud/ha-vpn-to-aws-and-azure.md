---
id: computing-software.cloud-infrastructure-engineering.google-cloud.ha-vpn-to-aws-and-azure
name: ha-vpn-to-aws-and-azure
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, hybrid-connectivity, vpn-to-aws, multi-cloud-vpn, azure-vpn-gateway, bgp]
level: advanced
status: docs-checked
description: "Connect GCP to AWS and Azure with HA VPN and BGP: four-tunnel AWS layout with two VGW/TGW connections, Azure active-active APIPA addressing, and matching IKE settings."
sources: ["https://cloud.google.com/network-connectivity/docs/vpn/tutorials/create-ha-vpn-connections-google-cloud-aws", "https://cloud.google.com/network-connectivity/docs/vpn/tutorials/create-ha-vpn-connections-google-cloud-azure", "https://cloud.google.com/network-connectivity/docs/vpn/concepts/supported-ike-ciphers", "https://cloud.google.com/network-connectivity/docs/vpn/concepts/overview"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# HA VPN to AWS and Azure

## 1. AWS (4 tunnels)
1. GCP: HA VPN gateway (2 interfaces) + Cloud Router (ASN e.g. 65534).
2. AWS: two **customer gateways** (one per GCP interface IP, BGP ASN = Cloud Router's), a VGW or Transit Gateway, and two **Site-to-Site VPN connections** (each gives 2 tunnels) with dynamic routing.
3. GCP: external VPN gateway with **four** interfaces = the 4 AWS tunnel outside IPs:
```bash
gcloud compute external-vpn-gateways create aws-gw --interfaces=0=<AWS_T1>,1=<AWS_T2>,2=<AWS_T3>,3=<AWS_T4>
```
4. Four tunnels: GCP interface 0 → AWS ext interfaces 0 and 1; GCP interface 1 → 2 and 3. Use each AWS tunnel's pre-shared key and its inside CIDR (a link-local /30) for the Cloud Router interface and BGP peer addresses. Use IKEv2 and select only one IKE cipher set (one Phase 1 and one Phase 2 encryption, integrity and DH group): the default AWS transform sets create large SA payloads that cause IKE packet fragmentation, which Cloud VPN does not support.

## 2. Azure (active-active)
1. Azure: route-based VPN virtual network gateway, **active-active**, BGP enabled with two custom APIPA BGP addresses from the `169.254.21.*` and `169.254.22.*` ranges (the valid Azure APIPA ranges), e.g. 169.254.21.1 and 169.254.22.1.
2. Azure local network gateways for each GCP interface IP, with BGP peer = GCP's link-local IP and ASN.
3. GCP: external VPN gateway with Azure's two public IPs; tunnels from interface 0/1; Cloud Router BGP peers to the two Azure APIPA addresses, each pair in a /30 inside the 169.254.21.* or 169.254.22.* range.
4. Azure connections: IKEv2 with BGP enabled and the same shared key.

## 3. Common
- Use non-overlapping CIDRs across clouds; advertise only needed ranges.
- Each Cloud VPN tunnel supports up to 250,000 packets per second (ingress plus egress), about 1 to 3 Gbps depending on packet size; add tunnels for more. On AWS, a virtual private gateway uses only one tunnel across its connections, so use a transit gateway if you need ECMP across tunnels.

## Gotchas
- Cloud VPN uses Dead Peer Detection (RFC 3706); an unhealthy tunnel's routes are withdrawn so traffic fails over. The DPD interval is not configurable.
- Use a distinct ASN on each side; on Azure set the ASN of the active-active gateway when enabling BGP, and use it in the Cloud Router BGP peer.
- Check Cloud VPN logs (`resource.type="vpn_gateway"`) for IKE negotiation errors when a tunnel will not establish.

## Verify
- [ ] All tunnels ESTABLISHED and all BGP sessions UP (`gcloud compute routers get-status`); a VM-to-VM ping across clouds works on both paths when one tunnel is disabled.

## Checked

- Date: 2026-10-27; documentation release: Google Cloud documentation pages as published on that date.
- Confirmed (AWS tutorial): two AWS Site-to-Site VPN connections of two tunnels each, customer gateways using the Google ASN and one per HA VPN interface, virtual private gateway or transit gateway, four tunnels minimum for 99.99%, IKEv2 with a single cipher set, fragmented IKE packets unsupported, VGW selects one tunnel while transit gateway enables ECMP, tunnel inside CIDRs.
- Confirmed (Azure tutorial): active-active route-based VPN gateway with BGP, APIPA ranges 169.254.21.* and 169.254.22.*, ASN set on the gateway and reused in Cloud Router BGP peers. Confirmed (Cloud VPN overview): 250,000 packets per second per tunnel equal to 1 to 3 Gbps, DPD behaviour.
- Removed: AWS link-local .1/.2 side assignment, the 1.25 Gbps AWS tunnel figure, the idle-tunnel and 65515 reserved-ASN statements, the VpnGw1+ SKU and UseBgp wording (not found in the pages read).

Method: documentation only; no commands were run.
