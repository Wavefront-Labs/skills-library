---
id: computing-software.systems-network-administration.network-design.cloud-private-dns-and-resolver-endpoints
name: cloud-private-dns-and-resolver-endpoints
category: computing-software
field: systems-network-administration
product: network-design
tags: [cloud-networking, private-dns-zone, route-53-resolver, azure-dns-private-resolver, hybrid-dns, conditional-forwarding, private-endpoint-dns]
level: practitioner
status: docs-checked
description: "Make hybrid DNS work between on-prem and cloud: private hosted zones, Route 53 Resolver and Azure DNS Private Resolver endpoints, forwarding rules, and PrivateLink names."
sources:
  - https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/resolver.html
  - https://learn.microsoft.com/en-us/azure/dns/dns-private-resolver-overview
  - https://learn.microsoft.com/en-us/azure/private-link/private-endpoint-dns
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cloud private DNS and resolver endpoints

## The pieces
- Private zones: AWS Route 53 private hosted zones associated with VPCs; Azure Private DNS zones
  linked to VNets.
- AWS: the Route 53 VPC Resolver (previously named Route 53 Resolver) is available by default in
  every VPC and is reached at the VPC+2 address; it answers VPC names, private hosted zones and
  public names recursively.
- Resolver endpoints bridge to on-prem:
  - Inbound endpoint: lets on-prem DNS servers send queries into the VPC/VNet.
  - Outbound endpoint + forwarding rules: cloud resolver forwards `corp.example.net` to on-prem DNS.

## Typical hybrid setup
On-prem (BIND/AD DNS):
```
zone "aws.example.net" { type forward; forward only; forwarders { 10.64.1.10; 10.64.2.10; }; };  # inbound endpoint IPs
```
For AD DNS: conditional forwarder for `aws.example.net` and the PrivateLink zones to the same IPs.

AWS: outbound endpoint + rule `corp.example.net -> 10.0.0.53, 10.0.1.53`; rules are applied to VPCs
and can be shared across accounts. Azure: DNS Private Resolver with an outbound endpoint and a forwarding ruleset linked to VNets.

## PrivateLink / private endpoints
Private endpoints rely on DNS: `mystorage.blob.core.windows.net` must resolve to the private IP via
the `privatelink.blob.core.windows.net` zone. On-prem clients need to resolve the public name
through the cloud resolver (forward `blob.core.windows.net`, or at least the privatelink zone, to
the inbound endpoint). Otherwise they get the public IP and traffic leaves via the internet or is
denied.

## Verify
```
dig @10.64.1.10 app.aws.example.net           # from on-prem to inbound endpoint
dig mystorage.blob.core.windows.net            # from on-prem: should return 10.x private IP
nslookup corp-dc01.corp.example.net            # from a cloud VM: via outbound rule
```

## Gotchas
- Endpoints sit behind security groups/NSGs: allow DNS from the forwarding servers.
- Forwarding loops: on-prem forwards a zone to the cloud, cloud rule forwards it back.
- Multiple accounts/subscriptions: associate private zones centrally or names resolve only in one
  VPC.
- Endpoints have several IPs; point forwarders at all of them.

## Verify
- [ ] Resolution works in both directions and PrivateLink names return private IPs from on-prem.

## Checked
2026-10-28. Confirmed against the Route 53 VPC Resolver overview (VPC+2 address, inbound and outbound endpoints, conditional forwarding rules shareable across accounts, rename from Route 53 Resolver), the Azure DNS Private Resolver overview (inbound and outbound endpoints, forwarding rulesets) and the Azure private endpoint DNS page (`privatelink.blob.core.windows.net` zone, public zone forwarders). Removed: the 169.254.169.253 and 168.63.129.16 addresses, GCP zones, the RAM name, UDP+TCP 53 and two-per-AZ endpoint claims (not in the fetched pages).
Method: documentation only; no commands were run.
