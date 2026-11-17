---
id: computing-software.cloud-infrastructure-engineering.aws.site-to-site-vpn-customer-gateway-static-vs-dynamic
name: site-to-site-vpn-customer-gateway-static-vs-dynamic
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, site-to-site-vpn, static-routing-vpn, customer-gateway, bgp, vpn-configuration]
level: practitioner
status: docs-checked
description: "Configure the customer gateway device for Site-to-Site VPN and choose static or BGP routing: device config download, static routes, tunnel failover behaviour."
sources: ["https://docs.aws.amazon.com/vpn/latest/s2svpn/your-cgw.html", "https://docs.aws.amazon.com/vpn/latest/s2svpn/VPNRoutingTypes.html", "https://docs.aws.amazon.com/vpn/latest/s2svpn/cgw-options.html", "https://docs.aws.amazon.com/vpn/latest/s2svpn/vpn-limits.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Customer gateway configuration: static vs dynamic routing

## 1. Customer gateway resource
```bash
aws ec2 create-customer-gateway --type ipsec.1 --ip-address 198.51.100.10 --bgp-asn 65010 \
  --tag-specifications 'ResourceType=customer-gateway,Tags=[{Key=Name,Value=dc1-fw}]'
```
- The device IP must be static (IPv4, or IPv6 only for connections on a transit gateway or Cloud WAN). Behind NAT, use the NAT device's IP and allow UDP 500 (and 4500 if NAT traversal is used).
- BGP ASN (dynamic routing only): 1-4,294,967,295; not 7224 (reserved everywhere), 9059 (eu-west-1), 10124 (ap-northeast-1) or 17943 (ap-southeast-1). Private ranges 64,512-65,534 and 4,200,000,000-4,294,967,294; default 64512.
- Certificate-based authentication uses an ACM private certificate from a subordinate AWS Private CA; the IP address is then optional.

## 2. Static vs dynamic
| | Static | Dynamic (BGP) |
|---|---|---|
| Create | `--options StaticRoutesOnly=true` | default |
| Routes | `create-vpn-connection-route --destination-cidr-block 10.50.0.0/16` per prefix (virtual private gateway) | advertised by BGP |
| Precedence on a VGW | static routes are preferred over identical BGP routes | |
| Limits | 100 static routes from the CGW per VGW connection | 100 dynamic routes from the CGW per VGW connection; 1,000 on a transit gateway |
| ECMP on a transit gateway | not supported | supported |
| Device needs | IPsec; AWS is route-based only | BGP support |
If you choose BGP advertisement you cannot specify static routes. Prefer advertising specific BGP routes to influence routing on the VGW.
```bash
aws ec2 create-vpn-connection --type ipsec.1 --customer-gateway-id cgw-0abc --vpn-gateway-id vgw-0abc --options StaticRoutesOnly=true
aws ec2 create-vpn-connection-route --vpn-connection-id vpn-0abc --destination-cidr-block 10.50.0.0/16
```
You must also update the route table of your subnets (or enable route propagation on a VGW).

## 3. Download the device config
```bash
aws ec2 get-vpn-connection-device-types --query 'VpnConnectionDeviceTypes[?Vendor==`<VENDOR>`]'
aws ec2 get-vpn-connection-device-sample-configuration --vpn-connection-id vpn-0abc \
  --vpn-connection-device-type-id <TYPE_ID> --internet-key-exchange-version ikev2 --output text > fw.cfg
```

## 4. Device essentials
- Configure **both** tunnels: when one is unavailable (for example for maintenance) traffic uses the other.
- Traffic from AWS prefers one tunnel but fails over; traffic from on-premises can use both.
- Policy-based VPNs are not supported; use a route-based configuration. See the tunnel options skill for IKE, DPD and startup settings.
- MTU 1446 / MSS 1406 at most.

## Verify
- [ ] `describe-vpn-connections --query 'VpnConnections[].VgwTelemetry'` shows both tunnels `UP`.
- [ ] Shutting tunnel 1 moves traffic to tunnel 2.

## Checked
2026-10-28. Confirmed on cgw-options, VPNRoutingTypes, VPNTunnels and vpn-limits pages: ASN rules and reserved ASNs, NAT and UDP ports, certificate option, static-over-BGP precedence, static/BGP exclusivity, route and ECMP limits, two-tunnel failover, MTU/MSS. Fixed: `create-customer-gateway` now documents `--ip-address` (also IPv6) instead of `--public-ip`, and `create-vpn-connection-route` applies to virtual private gateway connections, not the transit-gateway example. Removed as unconfirmed: DPD-based static failover, AS-path prepend/MED advice, MSS 1379, "AWS maintains one tunnel at a time", transit gateway static route claim, vendor query value, policy-based SA-pair advice (the docs say policy-based is unsupported).
Method: documentation only; no commands were run.
