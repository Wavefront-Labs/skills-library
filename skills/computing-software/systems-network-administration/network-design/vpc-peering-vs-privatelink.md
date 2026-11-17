---
id: computing-software.systems-network-administration.network-design.vpc-peering-vs-privatelink
name: vpc-peering-vs-privatelink
category: computing-software
field: systems-network-administration
product: network-design
tags: [network-design, cloud-networking, privatelink, transitive-peering, vpc-peering, transit-gateway, private-endpoint]
level: practitioner
status: docs-checked
description: "Choose between VPC/VNet peering, transit hubs and PrivateLink/Private Endpoints: non-transitive peering, overlapping CIDRs, service exposure and DNS for private endpoints."
sources:
  - https://docs.aws.amazon.com/vpc/latest/peering/vpc-peering-basics.html
  - https://docs.aws.amazon.com/vpc/latest/privatelink/what-is-privatelink.html
  - https://learn.microsoft.com/en-us/azure/private-link/private-endpoint-overview
  - https://cloud.google.com/vpc/docs/private-service-connect
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# VPC peering vs PrivateLink

## Peering
- Connects two VPCs/VNets at L3: full routing between CIDRs (subject to SGs/NSGs).
- **Not transitive** (AWS): A-B and B-C peered does not let A reach C, and there is no
  edge-to-edge routing through a peer's internet gateway or NAT device.
- CIDRs **must not overlap**.
- Many VPCs -> a full peering mesh grows quickly; use each cloud's transit hub service instead.

## PrivateLink / Private Endpoint / Private Service Connect
- Exposes a **service** as an endpoint with a private IP inside the consumer network (AWS
  interface VPC endpoints, Azure private endpoints, Google Private Service Connect endpoints).
- Azure: a private endpoint is a network interface using a private IP address from your virtual
  network, connecting privately to a service powered by Private Link.
- Also used to reach cloud PaaS services over private addresses.

## DNS is the usual failure
Private endpoints only work if clients resolve the service name to the private IP:
- Azure: the private endpoint overview has a DNS configuration section; the DNS settings you use
  to connect to a private-link resource are important, and a name that still resolves to the
  public address bypasses the endpoint.
- AWS and Google: see each service's DNS documentation for private DNS names.

## Choose
Broad app-to-app connectivity inside one org -> hub transit. Expose a single service, cross-account
consumers -> PrivateLink. Overlapping CIDRs rule out peering. Small fixed pair of VPCs -> peering.

## Verify
- [ ] `nslookup <service>` from consumer subnets and on-prem returns private IPs; traffic flows only via intended paths (flow logs).

## Checked

- Date: 2026-10-28
- Confirmed: AWS peering is not transitive, forbids overlapping CIDRs and gives no edge-to-edge routing through a peer's gateway; Azure private endpoint is a network interface with a private IP from your VNet; Azure DNS settings matter for private-link resources; PSC endpoints and AWS interface endpoints exist.
- Removed: GCP and Azure transitivity claims, hub product names, NLB requirement, one-directional and NAT remarks, 'overlapping CIDRs are fine' for PrivateLink, gateway-endpoint and Route 53 Resolver details, privatelink DNS zone names.

Method: documentation only; no commands were run.
